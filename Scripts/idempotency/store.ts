// Persistent idempotency state machine for BrAPI-GenX — TypeScript/Bun (Slice 5).
// Shares genx_idempotency_records schema with the Python implementation.

import { Client } from "pg";

export type IdempotencyStatus =
  | "claimed"
  | "in_progress"
  | "completed"
  | "retryable_failure"
  | "terminal_failure"
  | "indeterminate"
  | "tombstoned";

export interface IdempotencyIdentity {
  tenantId: string;
  clientId: string;
  principalId: string;
  operationId: string;
  idempotencyKey: string;
}

export interface IdempotencyRecord {
  identity: IdempotencyIdentity;
  requestFingerprint: string;
  fingerprintAlgorithm: string;
  canonicalizationProfile: string;
  status: IdempotencyStatus;
  leaseOwner: string | null;
  leaseExpiresAt: Date | null;
  retryCount: number;
  createdAt: Date | null;
  updatedAt: Date | null;
  completedAt: Date | null;
  responseHttpStatus: number | null;
  responseBody: unknown;
  responseContentType: string | null;
  responseHeaders: Record<string, string> | null;
  responseExpiresAt: Date | null;
  tombstoneExpiresAt: Date | null;
  failureKind: string | null;
  failureInfo: unknown;
}

export type ClaimDisposition = "acquired" | "replay" | "conflict" | "in_progress";

const COLUMNS =
  "tenant_id, client_id, principal_id, operation_id, idempotency_key, " +
  "request_fingerprint, fingerprint_algorithm, canonicalization_profile, status, " +
  "lease_owner, lease_expires_at, retry_count, created_at, updated_at, completed_at, " +
  "response_http_status, response_body, response_content_type, response_headers, " +
  "response_expires_at, tombstone_expires_at, failure_kind, failure_info";

function rowToRecord(row: any): IdempotencyRecord {
  return {
    identity: {
      tenantId: row.tenant_id,
      clientId: row.client_id,
      principalId: row.principal_id,
      operationId: row.operation_id,
      idempotencyKey: row.idempotency_key,
    },
    requestFingerprint: row.request_fingerprint,
    fingerprintAlgorithm: row.fingerprint_algorithm,
    canonicalizationProfile: row.canonicalization_profile,
    status: row.status as IdempotencyStatus,
    leaseOwner: row.lease_owner,
    leaseExpiresAt: row.lease_expires_at ? new Date(row.lease_expires_at) : null,
    retryCount: row.retry_count ?? 0,
    createdAt: row.created_at ? new Date(row.created_at) : null,
    updatedAt: row.updated_at ? new Date(row.updated_at) : null,
    completedAt: row.completed_at ? new Date(row.completed_at) : null,
    responseHttpStatus: row.response_http_status,
    responseBody: row.response_body ?? null,
    responseContentType: row.response_content_type,
    responseHeaders: row.response_headers ?? null,
    responseExpiresAt: row.response_expires_at ? new Date(row.response_expires_at) : null,
    tombstoneExpiresAt: row.tombstone_expires_at ? new Date(row.tombstone_expires_at) : null,
    failureKind: row.failure_kind,
    failureInfo: row.failure_info ?? null,
  };
}

function now(): Date {
  return new Date();
}

export class PostgresIdempotencyStore {
  constructor(
    private dsn: string,
    private responseTtlMs: number = 7 * 86400000,
    private tombstoneTtlMs: number = 30 * 86400000,
    private leaseSeconds: number = 300,
  ) {}

  private async withClient<T>(fn: (c: Client) => Promise<T>): Promise<T> {
    const c = new Client({ connectionString: this.dsn });
    await c.connect();
    try {
      return await fn(c);
    } finally {
      await c.end();
    }
  }

  async migrate(): Promise<void> {
    const fs = await import("node:fs");
    const path = new URL("../../migrations/0001_idempotency_state.sql", import.meta.url);
    // migrations is at repo root; resolve relative to this file's package location
    let sql = "";
    try {
      sql = fs.readFileSync(new URL("../../../migrations/0001_idempotency_state.sql", import.meta.url), "utf8");
    } catch {
      try {
        sql = fs.readFileSync("/home/dennis/src/reevuLabs/Bijmantra-Project/brapi-genx/migrations/0001_idempotency_state.sql", "utf8");
      } catch {
        sql = "";
      }
    }
    await this.withClient(async (c) => {
      try {
        await c.query(sql);
      } catch (e: any) {
        // ignore duplicate object errors
        if (!/already exists|duplicate/i.test(String(e?.message))) throw e;
      }
    });
  }

  async purge(): Promise<void> {
    await this.withClient(async (c) => {
      await c.query("DELETE FROM genx_idempotency_records");
    });
  }

  async cleanupExpired(): Promise<number> {
    const n = now();
    return this.withClient(async (c) => {
      const r = await c.query("DELETE FROM genx_idempotency_records WHERE tombstone_expires_at IS NOT NULL AND tombstone_expires_at < $1", [n]);
      return r.rowCount ?? 0;
    });
  }

  async claim(
    identity: IdempotencyIdentity,
    requestFingerprint: string,
    canonicalizationProfile: string = "jcs-rfc8785:v1",
    leaseOwner?: string,
  ): Promise<{ record: IdempotencyRecord; disposition: ClaimDisposition }> {
    const owner = leaseOwner ?? crypto.randomUUID();
    const n = now();
    const leaseExpiry = new Date(n.getTime() + this.leaseSeconds * 1000);

    // 1. try insert
    try {
      const rec = await this.withClient(async (c) => {
        const r = await c.query(
          `INSERT INTO genx_idempotency_records (${COLUMNS}) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23) RETURNING ${COLUMNS}`,
          [
            identity.tenantId, identity.clientId, identity.principalId, identity.operationId, identity.idempotencyKey,
            requestFingerprint, "sha256", canonicalizationProfile, "in_progress",
            owner, leaseExpiry, 0, n, n, null,
            null, null, null, null, null, null, null, null,
          ],
        );
        return rowToRecord(r.rows[0]);
      });
      return { record: rec, disposition: "acquired" };
    } catch (e: any) {
      if (!/duplicate|unique/i.test(String(e?.message))) throw e;
    }

    // 2. existing
    return this.withClient(async (c) => {
      await c.query("BEGIN");
      try {
        const sel = await c.query(
          `SELECT ${COLUMNS} FROM genx_idempotency_records WHERE tenant_id=$1 AND client_id=$2 AND principal_id=$3 AND operation_id=$4 AND idempotency_key=$5 FOR UPDATE`,
          [identity.tenantId, identity.clientId, identity.principalId, identity.operationId, identity.idempotencyKey],
        );
        if (sel.rowCount === 0) throw new Error("idempotency record vanished");
        const existing = rowToRecord(sel.rows[0]);

        if (existing.requestFingerprint !== requestFingerprint) {
          await c.query("COMMIT");
          return { record: existing, disposition: "conflict" as ClaimDisposition };
        }

        // tombstone expired -> delete + claim
        if (existing.tombstoneExpiresAt && existing.tombstoneExpiresAt < n) {
          await c.query(
            "DELETE FROM genx_idempotency_records WHERE tenant_id=$1 AND client_id=$2 AND principal_id=$3 AND operation_id=$4 AND idempotency_key=$5",
            [identity.tenantId, identity.clientId, identity.principalId, identity.operationId, identity.idempotencyKey],
          );
          const ins = await c.query(
            `INSERT INTO genx_idempotency_records (${COLUMNS}) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23) RETURNING ${COLUMNS}`,
            [
              identity.tenantId, identity.clientId, identity.principalId, identity.operationId, identity.idempotencyKey,
              requestFingerprint, "sha256", canonicalizationProfile, "in_progress",
              owner, leaseExpiry, 0, n, n, null,
              null, null, null, null, null, null, null, null,
            ],
          );
          await c.query("COMMIT");
          return { record: rowToRecord(ins.rows[0]), disposition: "acquired" as ClaimDisposition };
        }

        // completed/tombstoned -> replay
        if (existing.status === "completed" || existing.status === "tombstoned") {
          await c.query("COMMIT");
          return { record: existing, disposition: "replay" as ClaimDisposition };
        }

        // in-progress states: check lease
        if (existing.leaseExpiresAt && existing.leaseExpiresAt > n && existing.leaseOwner && existing.leaseOwner !== owner) {
          await c.query("COMMIT");
          return { record: existing, disposition: "in_progress" as ClaimDisposition };
        }

        // reclaim
        const newLease = new Date(n.getTime() + this.leaseSeconds * 1000);
        await c.query(
          "UPDATE genx_idempotency_records SET status=$1, lease_owner=$2, lease_expires_at=$3, updated_at=$4, retry_count=retry_count+1 WHERE tenant_id=$5 AND client_id=$6 AND principal_id=$7 AND operation_id=$8 AND idempotency_key=$9",
          ["in_progress", owner, newLease, n, identity.tenantId, identity.clientId, identity.principalId, identity.operationId, identity.idempotencyKey],
        );
        const upd = await c.query(
          `SELECT ${COLUMNS} FROM genx_idempotency_records WHERE tenant_id=$1 AND client_id=$2 AND principal_id=$3 AND operation_id=$4 AND idempotency_key=$5`,
          [identity.tenantId, identity.clientId, identity.principalId, identity.operationId, identity.idempotencyKey],
        );
        await c.query("COMMIT");
        return { record: rowToRecord(upd.rows[0]), disposition: "acquired" as ClaimDisposition };
      } catch (e) {
        await c.query("ROLLBACK");
        throw e;
      }
    });
  }

  async complete(
    identity: IdempotencyIdentity,
    requestFingerprint: string,
    responseHttpStatus: number,
    responseBody: unknown = null,
    responseContentType: string = "application/json",
    responseHeaders: Record<string, string> | null = null,
  ): Promise<IdempotencyRecord> {
    const n = now();
    const respExpires = new Date(n.getTime() + this.responseTtlMs);
    const tombExpires = new Date(n.getTime() + this.tombstoneTtlMs);
    return this.withClient(async (c) => {
      const r = await c.query(
        `UPDATE genx_idempotency_records SET status=$1, completed_at=$2, response_http_status=$3, response_body=$4, response_content_type=$5, response_headers=$6, response_expires_at=$7, tombstone_expires_at=$8, lease_owner=NULL, lease_expires_at=NULL, updated_at=$9 WHERE tenant_id=$10 AND client_id=$11 AND principal_id=$12 AND operation_id=$13 AND idempotency_key=$14 AND request_fingerprint=$15 RETURNING ${COLUMNS}`,
        [
          "completed", n, responseHttpStatus, responseBody, responseContentType, responseHeaders,
          respExpires, tombExpires, n,
          identity.tenantId, identity.clientId, identity.principalId, identity.operationId, identity.idempotencyKey,
          requestFingerprint,
        ],
      );
      if (r.rowCount === 0) throw new Error("complete: record not found or fingerprint mismatch");
      return rowToRecord(r.rows[0]);
    });
  }

  async fail(
    identity: IdempotencyIdentity,
    retryable: boolean = true,
    failureKind: string | null = null,
    failureInfo: unknown = null,
  ): Promise<IdempotencyRecord> {
    const n = now();
    const status = retryable ? "retryable_failure" : "terminal_failure";
    return this.withClient(async (c) => {
      const r = await c.query(
        `UPDATE genx_idempotency_records SET status=$1, failure_kind=$2, failure_info=$3, lease_owner=NULL, lease_expires_at=NULL, updated_at=$4 WHERE tenant_id=$5 AND client_id=$6 AND principal_id=$7 AND operation_id=$8 AND idempotency_key=$9 RETURNING ${COLUMNS}`,
        [status, failureKind, failureInfo, n, identity.tenantId, identity.clientId, identity.principalId, identity.operationId, identity.idempotencyKey],
      );
      if (r.rowCount === 0) throw new Error("fail: record not found");
      return rowToRecord(r.rows[0]);
    });
  }

  async get(identity: IdempotencyIdentity): Promise<IdempotencyRecord | null> {
    return this.withClient(async (c) => {
      const r = await c.query(
        `SELECT ${COLUMNS} FROM genx_idempotency_records WHERE tenant_id=$1 AND client_id=$2 AND principal_id=$3 AND operation_id=$4 AND idempotency_key=$5`,
        [identity.tenantId, identity.clientId, identity.principalId, identity.operationId, identity.idempotencyKey],
      );
      if (r.rowCount === 0) return null;
      return rowToRecord(r.rows[0]);
    });
  }
}
