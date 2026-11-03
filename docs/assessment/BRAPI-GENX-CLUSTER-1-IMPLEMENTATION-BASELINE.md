# BrAPI-GenX — Cluster 1 Implementation Baseline (D-02 / D-24 / D-25)

**Status:** Phase 1A.1 decision engineering. No normative decision is made.
**Baseline branch:** `planning/cluster-1-decision-package` (from `e0146c98`).

## 1. Current implementation inventory

### Digest usage (three distinct purposes)

1. **Canonical request-body fingerprint (Python `canonical()`)** —
   `Scripts/genx_test_server.py::canonical(doc)`:
   `json.dumps(doc, sort_keys=True, separators=(",", ":"))`. Used for idempotency
   equivalence comparison. Verified implementation fact.
2. **SHA-256 digest of canonicalized inputs** —
   `hashlib.sha256(canonical(inputs).encode("utf-8")).hexdigest()` in model
   registration (`inputsDigest`). Used for provenance/mutation binding.
   Verified implementation fact.
3. **Digest test vectors** — `Scripts/test_digest_vectors.py` and
   `Scripts/digest-conformance/test-digest-vectors.ts` exercise RFC 8785 (JCS)
   canonicalization as an *unselected candidate* (script docstring states this).
   Exploratory evidence only.

These are different purposes (request equivalence vs. provenance binding vs.
candidate standard evaluation) and are not currently unified. Verified fact.

### Idempotency implementation

- In-memory dict `Store.idempotency`: key → `{"body": canonical, "jobDbId": str}`.
- Header `Idempotency-Key` takes precedence over body `idempotencyKey`
  (`key = self.headers.get("Idempotency-Key") or body.get("idempotencyKey")`).
- Equivalence: `seen["body"] == body_canonical` where both are the Python
  canonical string. Different canonical body → 409.
- Replay returns 200 with the existing job; first submit returns 202.
- Process-local, not durable, not multi-instance. Verified limitation.

### Concurrency

- `Store.lock` (threading.Lock) guards `submit_idempotent`. In-process
  concurrency serialized. Verified fact.
- No multi-process or multi-instance coordination. Verified limitation.

### Retention/expiry

- `ttl_days=7` default; `self.ttl = timedelta(days=ttl_days)`. Job expiry
  checked via `L-05`. Idempotency dict has no explicit expiry/cleanup.
  Verified implementation fact + limitation.

## 2. Lifecycle walkthrough

1. Client submits `POST /genx/v1/jobs` with body (+ optional `Idempotency-Key`).
2. Server parses JSON; validates `jobType`.
3. Extracts key (header precedence).
4. Computes `canon = canonical(body)` (sort_keys, compact separators).
5. `submit_idempotent` checks `self.idempotency.get(key)`:
   - If present and `body` equal → replay (200, existing job).
   - If present and different → conflict (409).
   - If absent → create job, store key→{body, jobDbId}, return accepted (202).
6. Worker thread runs asynchronously.
7. Client retry: same path → replay or conflict.

## 3. Language implementation comparison

- Python: `json.dumps(doc, sort_keys=True, separators=(",", ":"))`.
- TypeScript/Bun: sorted-keys + compact separators + UTF-8 (per conformance
  README). Digest agreement with Python holds for ASCII payloads.
- Note: JCS (RFC 8785) is the candidate in digest test vectors; the reference
  server uses Python's canonical form, not JCS. Verified fact.

## 4. Existing test coverage

- `test_job_idempotency.py`: idempotency replay/conflict/tenant tests.
- `test_digest_vectors.py` + `test_digest_vector_mutations.py`: JCS candidate
  corpus (12 structured + 2 exact-byte + 5 rejection + 2 legacy + 10 mutations).
- Conformance L-01…L-05, L-24: live replay/conflict/cancel/expired/concurrency.
- Evidence: prototype behaviour only, not normative.

## 5. Verified limitations

- No durability across restart (in-memory).
- No multi-instance coordination.
- No tenant-scoped key namespace (key is global in the dict).
- No explicit retention/expiry for idempotency records.
- No response storage (only job reference).
- No authorization on replay (replayed response not re-checked).
- Canonical form is Python-specific, not a documented standard.

## 6. Refinement — Digest-purpose inventory

Three distinct digest purposes are present and must not be conflated:

1. **Raw-byte digest** — identifies an exact byte sequence (file/artifact
   integrity). Not currently implemented as a separate mechanism; the
   `inputsDigest` hashes canonicalized inputs, not raw bytes.
2. **Canonical JSON digest** — identifies a JSON representation under a
   defined serialization rule. Implemented as `canonical()` + SHA-256 for
   provenance binding in model registration.
3. **Scientific semantic fingerprint** — not implemented. Would require
   domain-specific normalization (units, decimals, identifiers) that must not
   be performed silently during JSON canonicalization.

## 7. Refinement — JCS compatibility findings

Python `json.dumps(sort_keys=True, separators=(",",":"))` differs from JCS
(RFC 8785) in at least: ASCII escaping (Python escapes non-ASCII by default
unless `ensure_ascii=False`), handling of non-finite numbers (Python emits
`NaN`/`Infinity` by default), and numeric serialization. The prototype is
**not** JCS-compliant. The digest test vectors exercise JCS as an unselected
candidate. Verified fact: `test_digest_vectors.py` docstring states
"RFC 8785 remains an unselected candidate."

## 8. Refinement — Transaction boundary and replay authorization

- The idempotency record and business mutation are both in-memory; no
  transactional boundary exists. No crash-recovery guarantee.
- Replay returns the stored job object without re-checking the current caller's
  authorization. This is a verified security limitation (D-22 adjacent).
- No external side-effect coordination exists (no outbox, no downstream
  idempotency propagation).