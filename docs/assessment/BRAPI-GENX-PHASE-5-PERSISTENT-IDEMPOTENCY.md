# BrAPI-GenX — Slice 5: Persistent Idempotency State Machine

**Status:** Implemented (Slice 5).  
**Date:** 2026-11-04  
**Governs:** D-24, D-25.

## Summary

Authoritative PostgreSQL-backed idempotency state shared across independent
processes and both reference runtimes (Python and TypeScript/Bun). Schema and
state machine are identical in both runtimes; cross-runtime replay and conflict
behaviour verified.

## State machine

States: `claimed`, `in_progress`, `completed`, `retryable_failure`,
`terminal_failure`, `indeterminate`, `tombstoned`.

Transitions:
- new claim -> `in_progress` (atomic INSERT on composite PK)
- `in_progress` -> `completed` (on success, with stored response)
- `in_progress` -> `retryable_failure` / `terminal_failure`
- expired lease on `in_progress`/`claimed`/`indeterminate` -> reclaim (new owner)
- `completed` -> tombstone after `response_ttl`; record deleted after `tombstone_ttl`

## Identity boundary

Composite primary key: `(tenant_id, client_id, principal_id, operation_id,
idempotency_key)`. Tenant/client/principal isolation enforced by DB.

## Fingerprint

Uses existing `request_fingerprint_digest` (SHA-256, JCS_RFC8785_V1). Stored
with `fingerprint_algorithm` and `canonicalization_profile` columns for future
profile migration. No second canonicalizer.

## Concurrency

- Atomic reservation via INSERT ... ON CONFLICT (unique PK).
- Conflicting fingerprint on same key -> `conflict`.
- Lease-based ownership with expiry; expired leases reclaimable; prevents
  duplicate execution while lease valid.

## Response persistence

Stores HTTP status, body (JSONB), content type, headers, completion timestamp,
response expiry, tombstone expiry. Hop-by-hop headers excluded by caller
convention.

## Schema / migration

`migrations/0001_idempotency_state.sql` — reproducible initialization, unique
PK, indexes on lease and tombstone expiry.

## Implementations

- Python: `src/brapi_genx/idempotency.py` (`PostgresIdempotencyStore`)
- TypeScript/Bun: `Scripts/idempotency/store.ts` (`PostgresIdempotencyStore`)

## Tests

- `tests/test_idempotency_postgres.py` (10 tests)
- `Scripts/idempotency/store.test.ts` (8 tests)

## Guarantees and limitations

- Duplicate execution prevented within lease window and across restarts.
- No universal exactly-once for external side effects; at-least-once with
  idempotent effects.
- Recovery of abandoned in-progress records via lease expiry; no blanket
  deletion at startup.

## Outstanding decisions

- Retention durations (response_ttl=7d, tombstone_ttl=30d) subject to
  maintainer operational policy.
- Expired-response behaviour returns stored record with expired flag; server
  layer maps to status message.
