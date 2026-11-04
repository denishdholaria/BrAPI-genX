# BrAPI-GenX — Phase 1B Implementation Roadmap

**Status:** Phase 1B.0 planning. Authorized for execution after maintainer review.
**Baseline:** commit `55f970d92dc3e64d34ea36fd184b3a48ec670f13`.
**Architecture:** `docs/architecture/BRAPI-GENX-CLUSTER-1-IMPLEMENTATION-ARCHITECTURE.md`.

---

## 1. Ordered development slices

Each slice is independently verifiable, has bounded scope, and can be executed by
a smaller AI coding model without loading the entire architecture.

| Slice | Name | Depends on | Blocks |
|---|---|---|---|
| 0 | Implementation boundaries & interfaces | — | 1, 4 |
| 1 | JCS canonicalization primitive | 0 | 2, 3, 5 |
| 2 | Digest primitives (raw + canonical) | 1 | 3 |
| 3 | Cross-language digest agreement | 2 | 11 |
| 4 | Operation identity & namespace resolution | 0 | 5, 6, 7 |
| 5 | Request fingerprint construction | 1, 4 | 6, 7 |
| 6 | Idempotency state machine (in-memory) | 4, 5 | 7 |
| 7 | Durable persistence & transaction coordination | 6 | 8, 9, 10 |
| 8 | Replay authentication & authorization | 7 | 11 |
| 9 | Retention & tombstone management | 7 | 11 |
| 10 | External effect coordination (outbox) | 7 | 11 |
| 11 | Integrated conformance validation | 3, 8, 9, 10 | — |

---

## 2. Slice specifications

### Slice 0 — Implementation boundaries & interfaces

**Objective:** Define exact module boundaries, public interfaces, and ownership
for the Cluster 1 implementation.

**Scope:**
- Create `src/digest/` module with public interface.
- Create `src/idempotency/` module with public interface.
- Define abstract `IdentityResolver` interface.
- Define `DigestResult`, `RequestFingerprintInput`, `IdempotencyRecord` types.
- No implementation logic — only interfaces and types.

**Dependencies:** None.

**Exclusions:** No JCS implementation, no database code, no HTTP handlers.

**Acceptance criteria:**
- Interfaces compile in target language(s).
- No circular dependencies.
- All types documented with purpose and constraints.

**Verification:** `cargo check` / `mypy --strict` / `tsc --noEmit`.

---

### Slice 1 — JCS canonicalization primitive

**Objective:** Implement the generic JCS-RFC8785 canonicalization component as a
reusable, independently testable library function.

**Scope:**
- `jcs_canonicalize(json_bytes: bytes) -> bytes` (returns canonical UTF-8 bytes).
- Duplicate-property detection (before standard parse).
- JCS input validation: reject NaN/Infinity, lone surrogates, unsafe integers.
- No cryptographic hashing — this slice produces canonical bytes only.
- Deterministic output for valid input.

**Dependencies:** Slice 0 (interfaces).

**Exclusions:** No SHA-256, no digest envelope, no domain-specific logic.

**Acceptance criteria:**
- Passes all 13 structured JCS vectors from `digest-vectors.json`.
- Passes 5 rejection vectors (correctly rejects).
- Passes 2 exact-byte vectors (passthrough for raw-byte path).
- Cross-language: Python and TypeScript/Bun produce identical canonical bytes.
- No external dependencies beyond standard library + `rfc8785` (Python) /
  `canonicalize` (TypeScript).

**Verification:** `python -m pytest test_jcs.py -v` / `bun test jcs.test.ts`.

---

### Slice 2 — Digest primitives

**Objective:** Implement raw-byte and canonical JSON digest functions using the
approved SHA-256 algorithm.

**Scope:**
- `raw_byte_digest(data: bytes) -> DigestResult`
- `canonical_json_digest(json_bytes: bytes) -> DigestResult`
- `DigestResult` includes: algorithm, purpose, value, canonicalization_profile.
- SHA-256 via standard library (`hashlib` / `node:crypto` / `crypto` crate).

**Dependencies:** Slice 1 (JCS canonicalization).

**Exclusions:** No semantic fingerprints, no domain logic.

**Acceptance criteria:**
- Raw-byte digest matches 2 exact-byte vectors.
- Canonical JSON digest matches 13 structured JCS vectors.
- DigestResult encoding consistent across languages.
- Algorithm identifier present and correct.

**Verification:** Unit tests + cross-language digest vector agreement.

---

### Slice 3 — Cross-language digest agreement

**Objective:** Validate that Python, TypeScript/Bun, and (optionally) Rust
produce identical digests for the full candidate corpus.

**Scope:**
- Run full `digest-vectors.json` corpus through all implementations.
- Include legacy diagnostics (document divergence, don't fail).
- Generate cross-language agreement report.

**Dependencies:** Slice 2.

**Exclusions:** No new implementation — validation only.

**Acceptance criteria:**
- All 13 structured JCS vectors: identical SHA-256 across all runtimes.
- Both exact-byte vectors: identical across runtimes.
- All 5 rejection vectors: rejected in all runtimes.
- Legacy diagnostics documented (Python/TypeScript divergence acknowledged).

**Verification:** `python test_digest_vectors.py && bun test-digest-vectors.ts`.

---

### Slice 4 — Operation identity & namespace resolution

**Objective:** Implement stable operation identity lookup and composite namespace
construction from authenticated request context.

**Scope:**
- Load `ENDPOINT-REGISTRY.json` or generated operation map at startup.
- `get_operation_id(request) -> str` using stable `recommendedOperationId`.
- `IdentityResolver` implementation for current auth scheme (bearer token →
  tenant/client/principal).
- Composite namespace construction: `(tenant, client, principal, operation_id)`.
- Namespace encoding for serialized form (if needed).

**Dependencies:** Slice 0.

**Exclusions:** No idempotency logic, no fingerprint, no persistence.

**Acceptance criteria:**
- All 462 GenX operations resolve to correct `recommendedOperationId`.
- Identity resolver returns correct components for test requests.
- Composite key construction deterministic.

**Verification:** Unit tests with mocked requests covering all operation types.

---

### Slice 5 — Request fingerprint construction

**Objective:** Build operation-specific request fingerprints using the canonical
payload and relevant context.

**Scope:**
- Operation-specific context registry (which query params/headers per operation).
- `RequestFingerprintInput` construction from HTTP request.
- `compute_fingerprint(input: RequestFingerprintInput) -> str` (SHA-256 of
  JCS-canonicalized envelope).
- Default: no query params, no extra headers, only `Content-Type` for POST.
- Extensible for operations that need additional context.

**Dependencies:** Slices 1, 4.

**Exclusions:** No idempotency state machine, no persistence.

**Acceptance criteria:**
- Fingerprint stable for semantically equivalent requests (key order, whitespace).
- Fingerprint differs for materially different requests (array order, values).
- Operation-specific context correctly included/excluded.
- Cross-language agreement on fingerprint values.

**Verification:** Fingerprint test vectors with expected outputs.

---

### Slice 6 — Idempotency state machine (in-memory)

**Objective:** Implement the complete state machine with atomic claim, fingerprint
comparison, and conflict detection — initially in-memory for development and
testing.

**Scope:**
- `IdempotencyRecord` with all fields (status, timestamps, fingerprint, etc.).
- Atomic claim: check-and-insert under lock.
- Fingerprint comparison: same → replay, different → conflict.
- State transitions per architecture diagram.
- In-memory storage with `threading.Lock` / `asyncio.Lock` / `Mutex`.
- **No durability** — explicitly in-memory for this slice.

**Dependencies:** Slices 4, 5.

**Exclusions:** No database, no transaction coordination, no retention cleanup.

**Acceptance criteria:**
- All existing `test_job_idempotency.py` tests pass.
- Concurrent same-key/same-body → exactly one job created (48 threads).
- Concurrent same-key/different-body → one winner, rest conflict.
- Different keys → independent jobs.
- State transitions follow diagram.
- Replay returns existing job with 200.

**Verification:** `python -m pytest test_idempotency_state.py -v`.

---

### Slice 7 — Durable persistence & transaction coordination

**Objective:** Replace in-memory storage with durable, shared, database-backed
idempotency state with atomic transaction coordination.

**Scope:**
- Database schema (see architecture document).
- Atomic claim via `INSERT ... ON CONFLICT` / `UPSERT` with composite PK.
- Transactional coordination: idempotency record + business mutation in same
  transaction where they share a store.
- Multi-instance safety: SERIALIZABLE isolation or explicit row locking.
- Recovery: `INDETERMINATE` state detection and reconciliation procedure.

**Dependencies:** Slice 6.

**Exclusions:** No replay authorization (Slice 8), no retention (Slice 9),
no external effects (Slice 10).

**Acceptance criteria:**
- Process restart: previously claimed operations recover correctly.
- Two concurrent processes: only one claims the key (DB unique constraint).
- Crash during mutation: transaction rollback removes claim.
- Crash after commit: retry finds COMPLETED record → replay.
- `INDETERMINATE` state detected and reconciled.

**Verification:**
- Database integration tests (testcontainers / tmp Postgres).
- Multi-process concurrency test.
- Crash-recovery simulation (kill process mid-transaction).

---

### Slice 8 — Replay authentication & authorization

**Objective:** Integrate fresh authentication and authorization checks before
returning stored replay results.

**Scope:**
- Authorization check on replay: `authorize_replay(principal, record) -> bool`.
- Distinguish operation authorization vs. result authorization.
- Information leakage prevention: 404 for both "unauthorized" and "not found".
- Integration with existing auth middleware.

**Dependencies:** Slice 7.

**Exclusions:** No new auth scheme — uses existing identity resolution.

**Acceptance criteria:**
- Same principal replaying own job → 200 with result.
- Different principal (same tenant) replaying → 404 (no leak).
- Different tenant replaying → 404.
- Expired token on replay → 401.
- Authorization change after original operation respected.

**Verification:** Auth integration tests with multiple principals/tenants.

---

### Slice 9 — Retention & tombstone management

**Objective:** Implement separate response retention and identity tombstone
retention with configurable TTLs and background cleanup.

**Scope:**
- `response_ttl` and `tombstone_ttl` configuration.
- Background job: delete expired responses, delete expired tombstones.
- `expires_at` field management on state transitions.
- Safe key reuse after tombstone expiry.
- Metrics: retention queue size, cleanup latency.

**Dependencies:** Slice 7.

**Exclusions:** No new state machine states.

**Acceptance criteria:**
- Response discarded after `response_ttl`; tombstone remains.
- Tombstone prevents re-execution during `tombstone_ttl`.
- Key reusable after tombstone expiry.
- Background cleanup runs without blocking operations.
- Configurable TTLs (not hardcoded).

**Verification:** Time-accelerated tests (mock clock), retention metric checks.

---

### Slice 10 — External effect coordination (outbox)

**Objective:** Implement transactional outbox pattern for async job completion
events and other external side effects.

**Scope:**
- `outbox` table in same database as idempotency records.
- On transaction commit: write event to outbox atomically with business state.
- Background publisher: reads outbox, delivers to message broker, marks
  published.
- Idempotent downstream delivery (include correlation ID).
- Only for operations that actually have external effects (async jobs).

**Dependencies:** Slice 7.

**Exclusions:** No complex workflow engine, no compensation logic (unless needed).

**Acceptance criteria:**
- Job completion event published exactly once (at-least-once + idempotent consumer).
- Crash after commit, before publish → publisher recovers on restart.
- Outbox does not block primary transaction latency.

**Verification:** Outbox delivery test with mock broker, crash-recovery test.

---

### Slice 11 — Integrated conformance validation

**Objective:** End-to-end validation of the complete Cluster 1 implementation
against the conformance test plan.

**Scope:**
- Run full conformance test suite (see test plan document).
- Cross-language digest agreement (Slice 3).
- Idempotency: replay, conflict, concurrency, crash recovery.
- Replay authorization.
- Retention and expiry.
- Multi-instance coordination.
- External effect delivery.
- Generate conformance report.

**Dependencies:** Slices 3, 8, 9, 10.

**Acceptance criteria:**
- All conformance tests PASS.
- Cross-language digest vectors agree.
- No flaky tests.
- Report generated with evidence.

**Verification:** `python -m pytest conformance/ -v --tb=short`.

---

## 3. Migration considerations

- **Existing reference server** (`genx_test_server.py`) uses Python `canonical()`
  (sort_keys) and in-memory idempotency. It will be migrated slice by slice.
- **Digest vectors** currently exercise JCS as candidate. After Slice 3, they
  become normative for canonical JSON digest.
- **Idempotency tests** currently test prototype behaviour. After Slice 7, they
  test durable implementation.
- **No breaking changes to API contracts** — only internal implementation.

---

## 4. Priorities and risks

### Priority order
1. Slices 0–3 (digest foundation) — unlocks everything else.
2. Slices 4–6 (idempotency logic) — core Cluster 1 value.
3. Slice 7 (durability) — production requirement.
4. Slices 8–10 (security, retention, external effects) — production hardening.
5. Slice 11 (validation) — release gate.

### Key risks
| Risk | Mitigation |
|---|---|
| JCS library differences across runtimes | Slice 3 validates early; pin versions |
| Database transaction coordination complexity | Start with single DB; test multi-instance early |
| Authorization integration with unknown auth scheme | Abstract `IdentityResolver`; test with mock |
| Retention cleanup performance | Batch deletes; index `expires_at` |
| External effect delivery reliability | Transactional outbox; idempotent consumers |

---

## 5. Recommended first implementation slice

**Slice 0 → Slice 1** (Implementation boundaries + JCS canonicalization).

**Why:**
- No external dependencies beyond `rfc8785` / `canonicalize`.
- Independently testable with existing `digest-vectors.json`.
- Unblocks all subsequent slices.
- Small enough for a smaller AI model to execute in one session.
- Immediate validation: existing test vectors become pass/fail gate.

**Prerequisites for Slice 1:**
- Maintainer confirms SHA-256 as algorithm (recommended).
- Target language(s) selected (Python + TypeScript/Bun minimum; Rust optional).

---

## 6. Exit criteria for Phase 1B

Phase 1B is complete when:
- All 12 slices implemented and verified.
- Conformance test plan (Slice 11) passes 100%.
- Cross-language digest agreement established.
- Durable idempotency demonstrated under multi-instance concurrency.
- Replay authorization enforced.
- Retention and cleanup operational.
- No unresolved blocking technical decisions.

---

*This roadmap translates ratified architecture into executable engineering work.
It does not authorize implementation — that requires maintainer approval of this
roadmap.*