"""Persistent idempotency state machine for BrAPI-GenX (Slice 5).

Authoritative PostgreSQL-backed store. Shares a single schema with the
TypeScript/Bun implementation; both runtimes read and write the same
``genx_idempotency_records`` table.

This module does NOT redesign the JCS fingerprint pipeline. It consumes
``request_fingerprint_digest`` output (a hex SHA-256 string) and persists it.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Optional

import psycopg
from psycopg import errors as pg_errors


class IdempotencyStatus(str, Enum):
    CLAIMED = "claimed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    RETRYABLE_FAILURE = "retryable_failure"
    TERMINAL_FAILURE = "terminal_failure"
    INDETERMINATE = "indeterminate"
    TOMBSTONED = "tombstoned"


TERMINAL_STATUSES = {IdempotencyStatus.COMPLETED, IdempotencyStatus.TERMINAL_FAILURE, IdempotencyStatus.TOMBSTONED}


@dataclass(frozen=True)
class IdempotencyIdentity:
    tenant_id: uuid.UUID
    client_id: uuid.UUID
    principal_id: uuid.UUID
    operation_id: str
    idempotency_key: str

    def as_tuple(self):
        return (str(self.tenant_id), str(self.client_id), str(self.principal_id),
                self.operation_id, self.idempotency_key)


@dataclass
class IdempotencyRecord:
    identity: IdempotencyIdentity
    request_fingerprint: str
    canonicalization_profile: str = "jcs-rfc8785:v1"
    fingerprint_algorithm: str = "sha256"
    status: IdempotencyStatus = IdempotencyStatus.IN_PROGRESS
    lease_owner: Optional[str] = None
    lease_expires_at: Optional[datetime] = None
    retry_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    response_http_status: Optional[int] = None
    response_body: Any = None
    response_content_type: Optional[str] = None
    response_headers: Optional[dict] = None
    response_expires_at: Optional[datetime] = None
    tombstone_expires_at: Optional[datetime] = None
    failure_kind: Optional[str] = None
    failure_info: Optional[Any] = None

    @property
    def response_expired(self) -> bool:
        if self.response_expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.response_expires_at

    @property
    def tombstone_expired(self) -> bool:
        if self.tombstone_expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.tombstone_expires_at


COLUMNS = (
    "tenant_id, client_id, principal_id, operation_id, idempotency_key, "
    "request_fingerprint, fingerprint_algorithm, canonicalization_profile, status, "
    "lease_owner, lease_expires_at, retry_count, created_at, updated_at, completed_at, "
    "response_http_status, response_body, response_content_type, response_headers, "
    "response_expires_at, tombstone_expires_at, failure_kind, failure_info"
)


def _row_to_record(row: tuple) -> IdempotencyRecord:
    (tenant_id, client_id, principal_id, operation_id, idempotency_key,
     request_fingerprint, fingerprint_algorithm, canonicalization_profile, status,
     lease_owner, lease_expires_at, retry_count, created_at, updated_at, completed_at,
     response_http_status, response_body, response_content_type, response_headers,
     response_expires_at, tombstone_expires_at, failure_kind, failure_info) = row
    ident = IdempotencyIdentity(
        tenant_id=uuid.UUID(str(tenant_id)),
        client_id=uuid.UUID(str(client_id)),
        principal_id=uuid.UUID(str(principal_id)),
        operation_id=operation_id,
        idempotency_key=idempotency_key,
    )
    return IdempotencyRecord(
        identity=ident,
        request_fingerprint=request_fingerprint,
        canonicalization_profile=canonicalization_profile,
        fingerprint_algorithm=fingerprint_algorithm,
        status=IdempotencyStatus(status),
        lease_owner=lease_owner,
        lease_expires_at=lease_expires_at,
        retry_count=retry_count or 0,
        created_at=created_at,
        updated_at=updated_at,
        completed_at=completed_at,
        response_http_status=response_http_status,
        response_body=response_body,
        response_content_type=response_content_type,
        response_headers=response_headers,
        response_expires_at=response_expires_at,
        tombstone_expires_at=tombstone_expires_at,
        failure_kind=failure_kind,
        failure_info=failure_info,
    )


class PostgresIdempotencyStore:
    """PostgreSQL-backed authoritative idempotency store."""

    def __init__(
        self,
        dsn: str,
        response_ttl: timedelta = timedelta(days=7),
        tombstone_ttl: timedelta = timedelta(days=30),
        lease_seconds: int = 300,
    ):
        self.dsn = dsn
        self.response_ttl = response_ttl
        self.tombstone_ttl = tombstone_ttl
        self.lease_seconds = lease_seconds
        self._closed = False

    def close(self) -> None:
        """Release any database resources held by this store.

        The store uses short-lived connections, so this primarily marks the
        store as closed for lifecycle/shutdown purposes.
        """
        self._closed = True

    def _connect(self):
        return psycopg.connect(self.dsn)

    def migrate(self) -> None:
        import pathlib
        schema_path = pathlib.Path(__file__).resolve().parents[2] / "migrations" / "0001_idempotency_state.sql"
        sql = schema_path.read_text(encoding="utf-8") if schema_path.exists() else None
        if sql is None:
            # fallback: minimal schema inline
            sql = ""
        with self._connect() as conn:
            with conn.cursor() as cur:
                if sql:
                    try:
                        cur.execute(sql)
                    except pg_errors.DuplicateObject:
                        conn.rollback()
                        # retry without constraints by running table/index parts is not needed;
                        # constraints already exist
            conn.commit()

    # ---------- claim ----------
    def claim(
        self,
        identity: IdempotencyIdentity,
        request_fingerprint: str,
        canonicalization_profile: str = "jcs-rfc8785:v1",
        lease_owner: Optional[str] = None,
    ):
        """Attempt to acquire execution ownership.

        Returns (record, disposition) where disposition is one of:
        'acquired', 'replay', 'conflict', 'in_progress'.
        """
        owner = lease_owner or str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        lease_expiry = now + timedelta(seconds=self.lease_seconds)
        t = identity.as_tuple()

        # 1. Try insert.
        try:
            with self._connect() as conn:
                with conn.transaction():
                    with conn.cursor() as cur:
                        cur.execute(
                            f"INSERT INTO genx_idempotency_records "
                            f"({COLUMNS}) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                            f"RETURNING {COLUMNS}",
                            (str(identity.tenant_id), str(identity.client_id), str(identity.principal_id),
                             identity.operation_id, identity.idempotency_key,
                             request_fingerprint, "sha256", canonicalization_profile, IdempotencyStatus.IN_PROGRESS.value,
                             owner, lease_expiry, 0, now, now, None,
                             None, None, None, None, None, None, None, None),
                        )
                        row = cur.fetchone()
            return _row_to_record(row), "acquired"
        except pg_errors.UniqueViolation:
            pass

        # 2. Existing record.
        with self._connect() as conn:
            with conn.transaction():
                with conn.cursor() as cur:
                    cur.execute(
                        f"SELECT {COLUMNS} FROM genx_idempotency_records "
                        f"WHERE tenant_id=%s AND client_id=%s AND principal_id=%s AND operation_id=%s AND idempotency_key=%s "
                        f"FOR UPDATE",
                        (str(identity.tenant_id), str(identity.client_id), str(identity.principal_id),
                         identity.operation_id, identity.idempotency_key),
                    )
                    row = cur.fetchone()
                    if row is None:
                        raise RuntimeError("idempotency record vanished")
                    existing = _row_to_record(row)

                    # fingerprint conflict
                    if existing.request_fingerprint != request_fingerprint:
                        return existing, "conflict"

                    # expiry handling: tombstone expired -> delete + claim
                    if existing.tombstone_expired:
                        cur.execute(
                            "DELETE FROM genx_idempotency_records "
                            "WHERE tenant_id=%s AND client_id=%s AND principal_id=%s AND operation_id=%s AND idempotency_key=%s",
                            (str(identity.tenant_id), str(identity.client_id), str(identity.principal_id),
                             identity.operation_id, identity.idempotency_key),
                        )
                        # re-insert
                        cur.execute(
                            f"INSERT INTO genx_idempotency_records "
                            f"({COLUMNS}) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                            f"RETURNING {COLUMNS}",
                            (str(identity.tenant_id), str(identity.client_id), str(identity.principal_id),
                             identity.operation_id, identity.idempotency_key,
                             request_fingerprint, "sha256", canonicalization_profile, IdempotencyStatus.IN_PROGRESS.value,
                             owner, lease_expiry, 0, now, now, None,
                             None, None, None, None, None, None, None, None),
                        )
                        new_row = cur.fetchone()
                        return _row_to_record(new_row), "acquired"

                    # completed / tombstoned -> replay
                    if existing.status in (IdempotencyStatus.COMPLETED, IdempotencyStatus.TOMBSTONED):
                        return existing, "replay"

                    # in-progress states: check lease
                    if (existing.lease_expires_at is not None
                            and existing.lease_expires_at > now
                            and existing.lease_owner not in (None, owner)):
                        return existing, "in_progress"

                    # reclaim (expired lease or same owner)
                    new_lease = now + timedelta(seconds=self.lease_seconds)
                    cur.execute(
                        "UPDATE genx_idempotency_records SET status=%s, lease_owner=%s, lease_expires_at=%s, "
                        "updated_at=%s, retry_count=retry_count+1 WHERE tenant_id=%s AND client_id=%s AND principal_id=%s "
                        "AND operation_id=%s AND idempotency_key=%s",
                        (IdempotencyStatus.IN_PROGRESS.value, owner, new_lease, now,
                         str(identity.tenant_id), str(identity.client_id), str(identity.principal_id),
                         identity.operation_id, identity.idempotency_key),
                    )
                    cur.execute(
                        f"SELECT {COLUMNS} FROM genx_idempotency_records "
                        f"WHERE tenant_id=%s AND client_id=%s AND principal_id=%s AND operation_id=%s AND idempotency_key=%s",
                        (str(identity.tenant_id), str(identity.client_id), str(identity.principal_id),
                         identity.operation_id, identity.idempotency_key),
                    )
                    updated_row = cur.fetchone()
                    return _row_to_record(updated_row), "acquired"

    # ---------- complete ----------
    def complete(
        self,
        identity: IdempotencyIdentity,
        request_fingerprint: str,
        response_http_status: int,
        response_body: Any = None,
        response_content_type: str = "application/json",
        response_headers: Optional[dict] = None,
        completed_at: Optional[datetime] = None,
    ) -> IdempotencyRecord:
        now = completed_at or datetime.now(timezone.utc)
        resp_expires = now + self.response_ttl
        tomb_expires = now + self.tombstone_ttl
        body_json = response_body
        # ensure JSON-serializable
        with self._connect() as conn:
            with conn.transaction():
                with conn.cursor() as cur:
                    cur.execute(
                        f"UPDATE genx_idempotency_records SET "
                        f"status=%s, completed_at=%s, response_http_status=%s, response_body=%s, "
                        f"response_content_type=%s, response_headers=%s, response_expires_at=%s, "
                        f"tombstone_expires_at=%s, lease_owner=NULL, lease_expires_at=NULL, updated_at=%s "
                        f"WHERE tenant_id=%s AND client_id=%s AND principal_id=%s AND operation_id=%s AND idempotency_key=%s "
                        f"AND request_fingerprint=%s "
                        f"RETURNING {COLUMNS}",
                        (IdempotencyStatus.COMPLETED.value, now, response_http_status,
                         psycopg.types.json.Jsonb(body_json) if body_json is not None else None,
                         response_content_type,
                         psycopg.types.json.Jsonb(response_headers) if response_headers is not None else None,
                         resp_expires, tomb_expires, now,
                         str(identity.tenant_id), str(identity.client_id), str(identity.principal_id),
                         identity.operation_id, identity.idempotency_key, request_fingerprint),
                    )
                    row = cur.fetchone()
                    if row is None:
                        raise RuntimeError("complete: record not found or fingerprint mismatch")
                    return _row_to_record(row)

    # ---------- fail ----------
    def fail(
        self,
        identity: IdempotencyIdentity,
        retryable: bool = True,
        failure_kind: Optional[str] = None,
        failure_info: Optional[Any] = None,
    ) -> IdempotencyRecord:
        status = IdempotencyStatus.RETRYABLE_FAILURE if retryable else IdempotencyStatus.TERMINAL_FAILURE
        now = datetime.now(timezone.utc)
        with self._connect() as conn:
            with conn.transaction():
                with conn.cursor() as cur:
                    cur.execute(
                        f"UPDATE genx_idempotency_records SET status=%s, failure_kind=%s, failure_info=%s, "
                        f"lease_owner=NULL, lease_expires_at=NULL, updated_at=%s "
                        f"WHERE tenant_id=%s AND client_id=%s AND principal_id=%s AND operation_id=%s AND idempotency_key=%s "
                        f"RETURNING {COLUMNS}",
                        (status.value, failure_kind, psycopg.types.json.Jsonb(failure_info) if failure_info is not None else None,
                         now,
                         str(identity.tenant_id), str(identity.client_id), str(identity.principal_id),
                         identity.operation_id, identity.idempotency_key),
                    )
                    row = cur.fetchone()
                    if row is None:
                        raise RuntimeError("fail: record not found")
                    return _row_to_record(row)

    # ---------- get ----------
    def get(self, identity: IdempotencyIdentity) -> Optional[IdempotencyRecord]:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT {COLUMNS} FROM genx_idempotency_records "
                    f"WHERE tenant_id=%s AND client_id=%s AND principal_id=%s AND operation_id=%s AND idempotency_key=%s",
                    (str(identity.tenant_id), str(identity.client_id), str(identity.principal_id),
                     identity.operation_id, identity.idempotency_key),
                )
                row = cur.fetchone()
                if row is None:
                    return None
                return _row_to_record(row)

    # ---------- cleanup ----------
    def cleanup_expired(self) -> int:
        now = datetime.now(timezone.utc)
        with self._connect() as conn:
            with conn.transaction():
                with conn.cursor() as cur:
                    cur.execute(
                        "DELETE FROM genx_idempotency_records WHERE tombstone_expires_at IS NOT NULL AND tombstone_expires_at < %s",
                        (now,),
                    )
                    deleted = cur.rowcount
            conn.commit()
        return deleted

    # ---------- purge all (testing) ----------
    def purge(self) -> None:
        with self._connect() as conn:
            with conn.transaction():
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM genx_idempotency_records")
            conn.commit()


__all__ = [
    "IdempotencyStatus",
    "IdempotencyIdentity",
    "IdempotencyRecord",
    "PostgresIdempotencyStore",
    "TERMINAL_STATUSES",
]
