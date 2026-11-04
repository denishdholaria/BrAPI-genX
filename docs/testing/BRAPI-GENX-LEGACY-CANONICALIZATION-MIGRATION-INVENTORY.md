# BrAPI-GenX — Legacy Canonicalization Migration Inventory

Migration has NOT occurred. Reference servers and conformance tooling still
use legacy canonicalizers. This inventory documents the consumers for a
future bounded migration task.

## Consumers

### 1. Python reference server

- File: `Scripts/genx_test_server.py`
- Function: `canonical(doc)` → `json.dumps(doc, sort_keys=True, separators=(",", ":"))`
- Purpose: request/response body canonicalization for idempotency and digest
  diagnostics in the in-memory reference server.
- Current serialization: Python `json.dumps` with sorted keys, compact
  separators, `ensure_ascii=True` default (escapes non-ASCII).
- Expected future canonicalizer: `brapi_genx.canonicalization.jcs_canonicalize`.
- Compatibility impact: non-ASCII escaping changes (legacy escapes; JCS
  emits literal UTF-8). Key ordering already matches for BMP; supplementary
  plane ordering changes from code-point to UTF-16 code-unit order.
- Dependencies: reference server in-memory state, conformance fixtures.
- Required migration test: byte-for-byte comparison of JCS output vs legacy
  for all conformance fixtures; idempotency replay/conflict behaviour.

### 2. TypeScript/Bun reference server

- File: `Scripts/genx_test_server_ts.ts`
- Function: `canonical(value)` → recursive sorted keys, compact separators,
  `JSON.stringify` (literal UTF-8).
- Purpose: second independent reference server for cross-runtime evidence.
- Current serialization: TS recursive with `Object.keys(...).sort()` (UTF-16
  code-unit sort) and `JSON.stringify`.
- Expected future canonicalizer: `Scripts/jcs-canonicalization/jcs.ts`
  (`jcsCanonicalize`).
- Compatibility impact: number serialization already aligned; lone-surrogate
  and safe-integer validation added.
- Dependencies: server in-memory state.
- Required migration test: cross-server digest agreement after migration.

### 3. Conformance checker

- File: `Scripts/checkGenXConformance.py`
- Function: `canonical(doc)` → `json.dumps(doc, sort_keys=True, separators=(",", ":"))`
- Purpose: comparing request bodies in idempotency conformance probes.
- Expected future canonicalizer: `brapi_genx.canonicalization.jcs_canonicalize`.
- Compatibility impact: low (comparison only; both sides migrated together).
- Dependencies: conformance fixtures.
- Required migration test: existing idempotency relation probes still pass.

### 4. Digest vector tooling

- File: `Scripts/test_digest_vectors.py`
- Function: `legacy_python_canonical(value)` → `json.dumps(value, sort_keys=True, separators=(",", ":"))`
- Purpose: documents legacy divergence; not normative.
- Expected future canonicalizer: retained as diagnostic only (legacy path
  documented, not migrated).
- Compatibility impact: none (diagnostic).
- Required migration test: none (kept for historical comparison).

### 5. Digest module (internal)

- File: `src/brapi_genx/digest.py` (`request_fingerprint_digest`)
- Current: builds envelope and serializes with `json.dumps(..., sort_keys=True)` then hashes (does NOT call `jcs_canonicalize`).
- Expected future canonicalizer: `jcs_canonicalize` on the envelope bytes.
- Compatibility impact: fingerprint values change once migrated; idempotency
  namespace unaffected but stored fingerprints invalidated.
- Dependencies: idempotency state machine (not yet implemented).
- Required migration test: fingerprint equivalence vectors (RFP-*).

## Migration policy

Migration is deferred to a separate bounded task per Phase 1B.2 scope.
No observable request/response behaviour changes in this phase.
EOF
