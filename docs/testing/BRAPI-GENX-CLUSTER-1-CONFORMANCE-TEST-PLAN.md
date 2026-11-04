# BrAPI-GenX — Cluster 1 Conformance Test Plan

**Status:** Phase 1B.0 planning. Executable after implementation slices complete.
**Architecture:** `docs/architecture/BRAPI-GENX-CLUSTER-1-IMPLEMENTATION-ARCHITECTURE.md`.
**Roadmap:** `docs/assessment/BRAPI-GENX-PHASE-1B-IMPLEMENTATION-ROADMAP.md`.

---

## 1. Test categories and execution status

| Category | Current status | Phase 1B target |
|---|---|---|
| Raw-byte digest | Not implemented | Executable (Slice 2) |
| JCS conformance vectors | Exploratory candidate | Normative (Slice 3) |
| Duplicate-property rejection | Exploratory | Normative (Slice 1) |
| Unicode & numeric edge cases | Exploratory | Normative (Slice 1) |
| Scientific decimal representation | Exploratory | Normative (Slice 1) |
| Cross-language digest agreement | Exploratory (ASCII only) | Full agreement (Slice 3) |
| Idempotency identity (namespace) | Prototype (in-memory) | Normative (Slice 4, 7) |
| Request fingerprint equivalence | Prototype (Python canonical) | Normative (Slice 5, 7) |
| Tenant/principal isolation | Not implemented | Normative (Slice 8) |
| Header/body key conflict | Prototype (header wins silently) | Normative reject 400 (Slice 6) |
| Replay authorization | Not implemented | Normative (Slice 8) |
| Concurrency (in-process) | Verified (48 threads) | Normative + multi-instance (Slice 6, 7) |
| Multi-instance coordination | Not implemented | Normative (Slice 7) |
| Restart & crash recovery | Not implemented | Normative (Slice 7) |
| Transaction rollback | Not implemented | Normative (Slice 7) |
| External effect failures | Not implemented | Normative (Slice 10) |
| Retention & expiry | Not implemented | Normative (Slice 9) |
| Independent implementation testing | Python + TS/Bun reference | Required for release |

---

## 2. Raw-byte digest tests

**Target slice:** 2 | **Status:** Not implemented

| Test ID | Description | Input | Expected |
|---|---|---|---|
| RAW-01 | Exact file bytes | `b"{\"a\": 1}\n"` | SHA-256 matches `e8c628edc996...` |
| RAW-02 | Key order preserved | `b"{\"b\":2,\"a\":1}"` | SHA-256 matches `3fb75453225c...` |
| RAW-03 | Binary artifact | Random 1KB bytes | Deterministic, reproducible |
| RAW-04 | Empty bytes | `b""` | SHA-256 of empty string |
| RAW-05 | Large file streaming | 10MB generated | Matches streaming hash |

**Cross-language:** All implementations must produce identical hex digest.

---

## 3. JCS canonical JSON digest tests (normative)

**Target slice:** 1, 3 | **Status:** Exploratory candidate → Normative

### 3.1 Structured JSON vectors (from `digest-vectors.json`)

| Vector ID | Key property tested |
|---|---|
| `object-key-order-and-whitespace` | Key sorting, whitespace removal |
| `unicode-escaped-input-canonical-unescaped-output` | Unicode escape → literal |
| `nested-objects-arrays-null-booleans` | Recursive canonicalization |
| `string-escaping` | Control chars, quotes, slashes |
| `utf16-property-order` | Supplementary plane key ordering |
| `number-serialization-and-negative-zero` | IEEE 754 shortest form, `-0 → 0` |
| `exact-scientific-decimal-represented-as-string` | Decimal strings preserved |
| `unicode-composed-form-preserved` | NFC preserved (no normalization) |
| `unicode-decomposed-form-preserved-without-normalization` | NFD preserved |
| `empty-object` | `{}` |
| `empty-array` | `[]` |
| `safe-integer-interoperability-boundary` | `9007199254740991` (2^53-1) |

**Each vector validates:**
1. Canonical UTF-8 bytes match `expectedCanonicalUtf8`.
2. SHA-256 of canonical bytes matches `expectedSha256`.
3. Cross-language agreement (Python, TypeScript/Bun, Rust).

### 3.2 Exact-byte vectors (raw-byte path)

| Vector ID | Description |
|---|---|
| `http-body-whitespace-preserved` | Raw bytes including whitespace |
| `http-body-key-order-preserved` | Raw bytes preserving key order |

### 3.3 Rejection vectors (must reject)

| Vector ID | Reason class | Why |
|---|---|---|
| `duplicate-property-name` | `jcs-input-constraint` | JCS forbids duplicate keys |
| `duplicate-property-name-after-unescaping` | `jcs-input-constraint` | After escape decoding |
| `non-json-nan-token` | `invalid-json-syntax` | NaN not valid JSON |
| `lone-unicode-surrogate` | `jcs-input-constraint` | Unpaired surrogate |
| `integer-outside-safe-interoperability-range` | `candidate-profile-hardening` | > 2^53-1 |

### 3.4 Legacy diagnostics (documented divergence)

| Vector ID | Purpose |
|---|---|
| `non-ascii-escaping` | Python `ensure_ascii=True` vs JCS literal Unicode |
| `unicode-property-order` | Python/TS legacy canonicalization difference |

**Note:** Legacy diagnostics are not normative; they document known prototype
divergence from JCS. They must not fail the conformance suite.

---

## 4. Scientific decimal representation

**Target slice:** 1, 3 | **Status:** Exploratory

| Test ID | Description | Input | Expected |
|---|---|---|---|
| DEC-01 | Decimal as string preserved | `{"v": "0.0000000000000001"}` | String unchanged in canonical |
| DEC-02 | High precision decimal | `{"v": "1.234567890123456789"}` | Exact string in canonical |
| DEC-03 | Scientific notation as string | `{"v": "1.23e-20"}` | String preserved (not normalized) |
| DEC-04 | Decimal number normalized | `{"v": 0.0000000000000001}` | JCS normalizes to `1e-16` |

**Rule:** Scientific decimals requiring exact representation **must** be encoded as
JSON strings in domain contracts. Generic JCS does not preserve numeric
precision beyond IEEE 754 binary64.

---

## 5. Idempotency identity tests

**Target slice:** 4, 6, 7 | **Status:** Prototype → Normative

### 5.1 Namespace construction

| Test ID | Scenario | Expected |
|---|---|---|
| IDN-01 | Tenant + client + principal + op_id + key | Composite key unique |
| IDN-02 | Same tenant, different client | Separate namespace |
| IDN-03 | Same client, different principal | Separate namespace |
| IDN-04 | Different operation, same key | Separate namespace |
| IDN-05 | Service-to-service (no user) | Service = principal |
| IDN-06 | Delegated request | Both client + principal recorded |

### 5.2 Request fingerprint equivalence

| Test ID | Scenario | Equivalent? |
|---|---|---|
| RFP-01 | Same key, identical request | **Yes** (replay) |
| RFP-02 | Same key, different property order | **Yes** |
| RFP-03 | Same key, different whitespace | **Yes** |
| RFP-04 | Same key, omitted vs explicit `null` | **No** (conflict) |
| RFP-05 | Same key, different numeric repr (1 vs 1.0) | **Yes** (JCS normalizes) |
| RFP-06 | Same key, different array order | **No** (conflict) |
| RFP-07 | Same key, different query param | **No** |
| RFP-08 | Same key, different HTTP method | **No** |
| RFP-09 | Different tenant, same key+payload | N/A (separate namespace) |

### 5.3 Header/body key conflict

| Test ID | Scenario | Expected |
|---|---|---|
| HBK-01 | Header only | Accept |
| HBK-02 | Body only | Accept (compatibility) |
| HBK-03 | Header + body identical | Accept |
| HBK-04 | Header + body conflicting | **Reject HTTP 400** |
| HBK-05 | Empty header + body key | Accept (body) |
| HBK-06 | Malformed header | Reject 400 |

---

## 6. Replay authorization tests

**Target slice:** 8 | **Status:** Not implemented

| Test ID | Scenario | Expected |
|---|---|---|
| RAZ-01 | Same principal, own completed job | 200 replay |
| RAZ-02 | Different principal, same tenant | 404 (no leak) |
| RAZ-03 | Different tenant | 404 |
| RAZ-04 | Expired token on replay | 401 |
| RAZ-05 | Authorization revoked after original | 403/404 |
| RAZ-06 | Operation authorized, result not authorized | 404 |
| RAZ-07 | In-progress job replay | 202/200 with progress |

---

## 7. Concurrency tests

**Target slice:** 6, 7 | **Status:** In-process verified → Multi-instance required

### 7.1 In-process (Slice 6)

| Test ID | Description | Threads | Expected |
|---|---|---|---|
| CON-01 | Same key, same body | 48 | 1 created, 47 replay |
| CON-02 | Same key, different bodies | 24 | 1 created, 23 conflict |
| CON-03 | Different keys | 24 | 24 created |
| CON-04 | Mixed same/different | 24 | 1 winner per body |

### 7.2 Multi-instance (Slice 7)

| Test ID | Description | Instances | Expected |
|---|---|---|---|
| CON-10 | Same key, simultaneous | 2 processes | 1 claim succeeds |
| CON-11 | Crash during claim | 1 process kill | Rollback, key free |
| CON-12 | Crash after commit | 1 process kill | Retry → replay |
| CON-13 | DB failover | Primary → replica | No duplicate claims |

---

## 8. Crash recovery & transaction tests

**Target slice:** 7 | **Status:** Not implemented

| Test ID | Failure window | Expected recovery |
|---|---|---|
| CRV-01 | Before claim | Retry = new operation |
| CRV-02 | Claimed, before mutation | Record = CLAIMED; reconcile → retry or mark failed |
| CRV-03 | During mutation | Transaction rollback; claim removed |
| CRV-04 | After mutation, before commit | Rollback; claim removed |
| CRV-05 | After commit, before response | Retry → replay (COMPLETED) |
| CRV-06 | Async worker crash | Outbox delivers on restart |

---

## 9. External side-effect failure tests

**Target slice:** 10 | **Status:** Not implemented

| Test ID | Scenario | Expected |
|---|---|---|
| EXT-01 | Broker down at publish | Outbox retains; retry on recovery |
| EXT-02 | Duplicate delivery | Downstream deduplicates via correlation ID |
| EXT-03 | Partial external success | Reconciliation detects; compensation if needed |
| EXT-04 | Worker crash mid-external-call | Durable workflow state enables retry |

---

## 10. Retention & expiry tests

**Target slice:** 9 | **Status:** Not implemented

| Test ID | Scenario | Expected |
|---|---|---|
| RET-01 | Response TTL expires | Response discarded; tombstone remains |
| RET-02 | Tombstone TTL expires | Record deleted; key reusable |
| RET-03 | Key reuse after tombstone | New operation (no conflict) |
| RET-04 | Key reuse during tombstone | Conflict (prevented) |
| RET-05 | Clock skew across instances | Expiry based on DB clock |

---

## 11. Independent implementation testing

**Target slice:** 11 | **Status:** Required for release

| Requirement | Description |
|---|---|
| IMP-01 | Second implementation (different language/runtime) passes all conformance tests |
| IMP-02 | Cross-language digest agreement on full vector corpus |
| IMP-03 | Cross-language idempotency: same keys produce same replay/conflict |
| IMP-04 | No implementation-specific behaviour in normative tests |

**Minimum:** Python + TypeScript/Bun. Rust recommended for production backend.

---

## 12. Test execution matrix

| Slice | Test suites to pass | Command |
|---|---|---|
| 1 | JCS canonicalization | `pytest test_jcs.py -v` |
| 2 | Digest primitives | `pytest test_digest_primitives.py -v` |
| 3 | Cross-language digest | `test_digest_vectors.py && bun test-digest-vectors.ts` |
| 4 | Operation identity | `pytest test_operation_identity.py -v` |
| 5 | Request fingerprint | `pytest test_fingerprint.py -v` |
| 6 | Idempotency state machine (in-mem) | `pytest test_idempotency_state.py -v` |
| 7 | Durable persistence | `pytest test_durable_idempotency.py -v` |
| 8 | Replay authorization | `pytest test_replay_auth.py -v` |
| 9 | Retention & expiry | `pytest test_retention.py -v` |
| 10 | External effects | `pytest test_outbox.py -v` |
| 11 | Full conformance | `pytest conformance/ -v --tb=short` |

---

## 13. Acceptance criteria for Phase 1B release

- [ ] All test suites in §12 PASS.
- [ ] Cross-language digest agreement: 100% vector match.
- [ ] Multi-instance concurrency: 0 duplicate claims under load.
- [ ] Crash recovery: 0 data loss in 100 simulated crashes.
- [ ] Replay authorization: 0 unauthorized access in 1000 attempts.
- [ ] Retention: 0 premature deletions, 0 leaked responses.
- [ ] Independent implementation: Python + TypeScript/Bun both pass.
- [ ] No flaky tests (3 consecutive clean runs).

---

*This test plan defines the verification requirements for the Cluster 1
implementation. Tests marked "Not implemented" are future requirements to be
built during the corresponding implementation slice.*