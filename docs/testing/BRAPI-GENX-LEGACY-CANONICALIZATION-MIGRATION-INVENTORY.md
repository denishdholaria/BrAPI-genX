# BrAPI-GenX — Legacy Canonicalization Migration Inventory

Migration status (Phase 1C, 2026-11-04): production-facing consumers migrated
to the verified JCS implementation (`brapi_genx.canonicalization.jcs_canonicalize`
and `Scripts/jcs-canonicalization/jcs.ts`). Legacy diagnostic helper retained.
This inventory records previous/new implementations and compatibility impact.

## Consumers

### 1. Python reference server

- File: `Scripts/genx_test_server.py`
- Function: `canonical(doc)` → `jcs_canonicalize(json.dumps(doc).encode("utf-8")).decode("utf-8")`
- Purpose: request/response body canonicalization for idempotency and digest
  diagnostics in the in-memory reference server.
- Previous serialization: Python `json.dumps` with sorted keys, compact
  separators, `ensure_ascii=True` default (escapes non-ASCII).
- New serialization: authoritative Python JCS (`brapi_genx.canonicalization`).
  `_read_json` now parses via `parse_strict_json`, enforcing JCS input
  constraints (duplicate properties, non-finite numbers, lone surrogates,
  unsafe integers).
- Compatibility impact: non-ASCII now emitted as literal UTF-8; property
  ordering follows UTF-16 code-unit order; numeric serialization follows
  IEEE 754 shortest form. Idempotency replay/conflict behaviour preserved
  for valid JSON; malformed/non-JCS input now rejected at read time.
- Dependencies: reference server in-memory state, conformance fixtures.
- Migration status: MIGRATED (Phase 1C).
- Verification: `Scripts/test_job_idempotency.py` (6 tests), live conformance
  `L-01..L-28` against Python server (0 failures).

### 2. TypeScript/Bun reference server

- File: `Scripts/genx_test_server_ts.ts`
- Function: `canonical(value)` → `new TextDecoder().decode(jcsCanonicalize(new TextEncoder().encode(JSON.stringify(value))))`
- Purpose: second independent reference server for cross-runtime evidence.
- Previous serialization: TS recursive with `Object.keys(...).sort()` (UTF-16
  code-unit sort) and `JSON.stringify`.
- New serialization: authoritative TS/Bun JCS (`Scripts/jcs-canonicalization/jcs.ts`).
  `readBody` now parses via `parseStrictJson`, enforcing JCS input
  constraints. `canonical()` delegates to `jcsCanonicalize`.
- Compatibility impact: numeric serialization and validation aligned with
  Python; cross-server digest agreement for ASCII and non-ASCII payloads.
- Dependencies: server in-memory state.
- Migration status: MIGRATED (Phase 1C).
- Verification: live conformance subset (jobs/models/inference) passes;
  cross-language harness `Scripts/test_cross_language_jcs.py` (12 structured,
  2 exact-byte, 5 rejection vectors).

### 3. Conformance checker

- File: `Scripts/checkGenXConformance.py`
- Function: `canonical(doc)` → `jcs_canonicalize(json.dumps(doc).encode("utf-8")).decode("utf-8")`
- Purpose: comparing request bodies in idempotency conformance probes.
- New serialization: authoritative Python JCS (`brapi_genx.canonicalization`).
- Compatibility impact: low (comparison only; both sides migrated together).
  `check_idempotency_relations` continues to pass for fixtures.
- Dependencies: conformance fixtures.
- Migration status: MIGRATED (Phase 1C).
- Verification: `Scripts/checkGenXConformance.py` (0 failures, 28 skipped static;
  0 failures live against Python server).

### 4. Digest vector tooling

- File: `Scripts/test_digest_vectors.py`
- Function: `legacy_python_canonical(value)` → `json.dumps(value, sort_keys=True, separators=(",", ":"))`
- Purpose: documents legacy divergence; not normative.
- Status: RETAINED AS DIAGNOSTIC (not migrated). Used to document the
  legacy/TypeScript divergence captured by `legacyDiagnostics` vectors.
- Compatibility impact: none (diagnostic).
- Verification: `Scripts/test_digest_vectors.py` (legacy diagnostic vectors
  still pass).

### 5. Digest module (internal)

- File: `src/brapi_genx/digest.py` (`request_fingerprint_digest`)
- Previous: builds envelope and serializes with `json.dumps(..., sort_keys=True)` then hashes (did NOT call `jcs_canonicalize`).
- New: validates raw payload bytes via `jcs_canonicalize`, builds the
  approved envelope `{"v":1,"op":...,"method":...,"payload":...,"query":...,
  "headers":...,"cv":...}`, then JCS-canonicalizes the envelope bytes before
  SHA-256. `DigestResult.canonicalization_profile` set to `JCS_RFC8785_V1`.
- Compatibility impact: fingerprint values change versus legacy (non-ASCII
  escaping, numeric shortest form, lone-surrogate/unsafe-integer rejection).
  No persisted idempotency state machine exists yet, so no stored
  fingerprints are invalidated in production; the public function output is
  now JCS-based. Envelope version remains `v=1`; canonicalization version is
  tracked separately via `CanonicalizationProfile`.
- Dependencies: idempotency state machine (not yet implemented).
- Migration status: MIGRATED (Phase 1C).
- Verification: `tests/test_digest_migration.py` (property-order independence,
  shared-vector SHA-256 equality, numeric/Unicode cases, duplicate rejection,
  determinism).

## Migration policy

Phase 1C migration completed for production-facing consumers (Python digest
API, both reference servers, conformance checker). Legacy diagnostic helper
retained. Digest encoding/envelope decisions remain as recorded in
`BRAPI-GENX-PHASE-1B-OPEN-TECHNICAL-DECISIONS.md`.
