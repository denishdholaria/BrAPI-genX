-- BrAPI-GenX persistent idempotency state machine (Slice 5)
-- PostgreSQL schema. Apply with: psql -f migrations/0001_idempotency_state.sql

CREATE TABLE IF NOT EXISTS genx_idempotency_records (
    tenant_id               UUID        NOT NULL,
    client_id               UUID        NOT NULL,
    principal_id            UUID        NOT NULL,
    operation_id            TEXT        NOT NULL,
    idempotency_key         TEXT        NOT NULL,

    request_fingerprint     TEXT        NOT NULL,
    fingerprint_algorithm   TEXT        NOT NULL DEFAULT 'sha256',
    canonicalization_profile TEXT       NOT NULL DEFAULT 'jcs-rfc8785:v1',

    status                  TEXT        NOT NULL,

    lease_owner             TEXT,
    lease_expires_at        TIMESTAMPTZ,
    retry_count             INTEGER     NOT NULL DEFAULT 0,

    created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at            TIMESTAMPTZ,

    response_http_status     INTEGER,
    response_body           JSONB,
    response_content_type   TEXT,
    response_headers        JSONB,
    response_expires_at     TIMESTAMPTZ,

    tombstone_expires_at    TIMESTAMPTZ,

    failure_kind            TEXT,
    failure_info            JSONB,

    PRIMARY KEY (tenant_id, client_id, principal_id, operation_id, idempotency_key)
);

CREATE INDEX IF NOT EXISTS idx_genx_idemp_lease
    ON genx_idempotency_records (lease_expires_at)
    WHERE status IN ('claimed','in_progress','indeterminate');

CREATE INDEX IF NOT EXISTS idx_genx_idemp_tombstone
    ON genx_idempotency_records (tombstone_expires_at);

CREATE INDEX IF NOT EXISTS idx_genx_idemp_status
    ON genx_idempotency_records (status);

-- Idempotency key format constraint (1..255 ASCII printable)
ALTER TABLE genx_idempotency_records
    ADD CONSTRAINT genx_idempotency_key_len
    CHECK (char_length(idempotency_key) BETWEEN 1 AND 255);

ALTER TABLE genx_idempotency_records
    ADD CONSTRAINT genx_idempotency_status_check
    CHECK (status IN ('claimed','in_progress','completed','retryable_failure','terminal_failure','indeterminate','tombstoned'));
