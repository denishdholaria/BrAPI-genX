"""PostgreSQL-backed idempotency state machine tests."""

import os
import sys
import uuid
import threading
from datetime import timedelta, timezone, datetime
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from brapi_genx.idempotency import (
    PostgresIdempotencyStore,
    IdempotencyIdentity,
    IdempotencyStatus,
)

DSN = os.environ.get("GENX_IDEMPOTENCY_DSN", "postgresql://postgres:postgres@localhost/brapi_genx_idempotency")


@pytest.fixture(scope="module")
def store():
    s = PostgresIdempotencyStore(DSN, response_ttl=timedelta(days=7), tombstone_ttl=timedelta(days=30), lease_seconds=2)
    s.migrate()
    s.purge()
    yield s
    s.purge()


def make_identity():
    return IdempotencyIdentity(
        tenant_id=uuid.uuid4(),
        client_id=uuid.uuid4(),
        principal_id=uuid.uuid4(),
        operation_id="genxSubmitAsyncJob",
        idempotency_key=f"key-{uuid.uuid4()}",
    )


def test_new_claim_and_complete(store):
    ident = make_identity()
    rec, disp = store.claim(ident, "fp1")
    assert disp == "acquired"
    assert rec.status == IdempotencyStatus.IN_PROGRESS
    store.complete(ident, "fp1", 202, {"jobDbId": "JOB_0001"}, "application/json")
    rec2 = store.get(ident)
    assert rec2.status == IdempotencyStatus.COMPLETED
    assert rec2.response_http_status == 202
    assert rec2.response_body == {"jobDbId": "JOB_0001"}
    assert rec2.canonicalization_profile == "jcs-rfc8785:v1"


def test_replay_same_fingerprint(store):
    ident = make_identity()
    store.claim(ident, "fp1")
    store.complete(ident, "fp1", 200, {"ok": True})
    rec, disp = store.claim(ident, "fp1")
    assert disp == "replay"
    assert rec.status == IdempotencyStatus.COMPLETED


def test_conflict_different_fingerprint(store):
    ident = make_identity()
    store.claim(ident, "fp1")
    store.complete(ident, "fp1", 200, {"ok": True})
    rec, disp = store.claim(ident, "fp2")
    assert disp == "conflict"


def test_concurrent_reservation_only_one_acquired(store):
    ident = make_identity()
    results = []
    barrier = threading.Barrier(2)

    def worker():
        barrier.wait()
        r, d = store.claim(ident, "fp1")
        results.append(d)

    t1 = threading.Thread(target=worker)
    t2 = threading.Thread(target=worker)
    t1.start(); t2.start()
    t1.join(); t2.join()
    assert sorted(results) == ["acquired", "in_progress"]


def test_concurrent_conflicting_fingerprints(store):
    ident = make_identity()
    results = []
    barrier = threading.Barrier(2)

    def worker(fp):
        barrier.wait()
        r, d = store.claim(ident, fp)
        results.append((fp, d))

    t1 = threading.Thread(target=worker, args=("fpA",))
    t2 = threading.Thread(target=worker, args=("fpB",))
    t1.start(); t2.start()
    t1.join(); t2.join()
    # one acquired, the other conflict (or in_progress after fp mismatch? conflict expected)
    disps = [d for _, d in results]
    assert "conflict" in disps or "in_progress" in disps
    # at least one acquired
    assert "acquired" in disps


def test_lease_expiry_recovery(store):
    ident = make_identity()
    rec, disp = store.claim(ident, "fp1", lease_owner="procA")
    assert disp == "acquired"
    # wait for lease to expire
    import time
    time.sleep(2.5)
    rec2, disp2 = store.claim(ident, "fp1", lease_owner="procB")
    assert disp2 == "acquired"
    assert rec2.lease_owner == "procB"


def test_tenant_isolation(store):
    ident_a = make_identity()
    ident_b = IdempotencyIdentity(
        tenant_id=uuid.uuid4(),  # different tenant
        client_id=ident_a.client_id,
        principal_id=ident_a.principal_id,
        operation_id=ident_a.operation_id,
        idempotency_key=ident_a.idempotency_key,
    )
    store.claim(ident_a, "fp1")
    store.complete(ident_a, "fp1", 200, {"secret": "A"})
    # different tenant same key -> new record, no replay of A's response
    rec, disp = store.claim(ident_b, "fp1")
    assert disp == "acquired"


def test_cleanup_expired(store):
    ident = make_identity()
    store.claim(ident, "fp1")
    store.complete(ident, "fp1", 200, {"ok": True})
    # force tombstone expiry by direct update
    import psycopg
    with psycopg.connect(DSN) as conn:
        with conn.transaction():
            with conn.cursor() as cur:
                cur.execute("UPDATE genx_idempotency_records SET tombstone_expires_at=now()-interval '1 day', response_expires_at=now()-interval '1 day' WHERE idempotency_key=%s", (ident.idempotency_key,))
    deleted = store.cleanup_expired()
    assert deleted >= 1
    assert store.get(ident) is None


def test_failure_semantics(store):
    ident = make_identity()
    store.claim(ident, "fp1")
    r = store.fail(ident, retryable=True, failure_kind="business", failure_info={"msg": "boom"})
    assert r.status == IdempotencyStatus.RETRYABLE_FAILURE
    # retryable -> reclaim allowed
    rec, disp = store.claim(ident, "fp1")
    assert disp == "acquired"


def test_fingerprint_profile_persisted(store):
    ident = make_identity()
    store.claim(ident, "fp1", canonicalization_profile="jcs-rfc8785:v1")
    store.complete(ident, "fp1", 200, {"ok": True})
    rec = store.get(ident)
    assert rec.canonicalization_profile == "jcs-rfc8785:v1"
    assert rec.fingerprint_algorithm == "sha256"
