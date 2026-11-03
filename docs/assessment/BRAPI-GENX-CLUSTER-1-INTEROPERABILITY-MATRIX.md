# BrAPI-GenX — Cluster 1 Interoperability Matrix

**Status:** Phase 1A.1 decision engineering.

## 1. Canonicalization test matrix (D-02)

| Case | JCS candidate | Python prototype | Required rule |
|---|---|---|---|
| Object property ordering | Normalized (sorted) | Normalized (sorted) | Define |
| Array ordering | Preserved | Preserved | Define (likely preserved) |
| Whitespace | Ignored | Ignored | Define |
| Duplicate property names | Reject | Reject (hook) | Define |
| `null` vs missing | Differ | Differ | Define |
| Negative zero | Normalized to 0 | Python keeps -0.0 | Define |
| Large integers | JCS uses shortest repr | Python arbitrary precision | Define safe range |
| Exponential notation | Normalized | Python preserves | Define |
| Unicode normalization | None (preserved) | None (preserved) | Define (no normalization) |
| Lone surrogates | Reject | Reject (custom) | Define |
| Non-JSON constants (NaN/Infinity) | Reject | Reject (parse_constant) | Define |
| Decimal as string | Treated as string | Treated as string | Define (string) |

## 2. Request-equivalence matrix (D-24)

| # | Variation | Equivalent? (candidate composite model) |
|---|---|---|
| 1 | Same key, identical request | Yes (replay) |
| 2 | Same key, different property order | Yes |
| 3 | Same key, different whitespace | Yes |
| 4 | Same key, omitted vs explicit null | TBD (define) |
| 5 | Same key, different numeric representation | TBD (define) |
| 6 | Same key, different array order | No (array order significant) |
| 7 | Same key, different query params | No (query is part of identity) |
| 8 | Same key, different HTTP method | No |
| 9 | Same key, different route | No |
| 10 | Same key, different API version | No |
| 11 | Same key, different content type | No |
| 12 | Same key, different tenant | No (conflict/unauthorized) |
| 13 | Same key, different client | Depends on scope (D-25) |
| 14 | Same body, different keys | No (different identity) |
| 15 | Same key after success | Replay |
| 16 | Same key while pending | TBD (define in-flight behaviour) |
| 17 | Same key after failure | TBD (define failure retention) |
| 18 | Same key after partial side effect | TBD |
| 19 | Same key after client timeout | Replay if recorded |
| 20 | Same key after process restart | Depends on durability (D-25) |

## 3. Concurrency scenarios

- Two identical requests simultaneously → one accepted (202), one replay (200)
  requires atomic check-and-create under lock.
- Same key, different payload, simultaneous → one accepted, one conflict (409).
- Cross-instance same key → requires distributed coordination (not in prototype).
- Crash after accept before store → no idempotency record; retry creates duplicate
  unless durable pre-write.

## 4. Replay scenarios

- Replay must not re-execute side effects.
- Replay response authorization must be re-checked (current prototype does not).
- Replay of a still-running request: define representation (e.g., 202 with
  current status) — TBD.
- Replay after expiry: TBD (new operation or conflict).

## 5. Expiry scenarios

- Key expires after TTL → reuse allowed as new operation (candidate).
- Tombstone retained after response discarded → conflict detection without full
  response storage (candidate).
- Clock skew across instances → complicates expiry; define clock source.

## 6. Failure-recovery scenarios

- Process crash mid-operation: at-least-once delivery; client retries; server
  deduplicates if durable record exists.
- DB transaction rollback: idempotency record must roll back with business state
  (atomicity requirement).
- Network partition: client may retry; server must not double-apply.

## 7. Cross-language interoperability requirements

- Canonical form must be specified independently of any language's default
  serialization.
- Digest vectors must include expected canonical bytes and expected digest.
- Two independent implementations must agree on all vectors.
- Current evidence: Python/TS agreement on ASCII payloads only (not sufficient).

## 7.5 Refinement — Raw-byte vs canonical vs semantic identity cases

- Raw-byte: two byte sequences differing in whitespace → different digest.
- Canonical JSON: two JSON docs differing only in key order/whitespace → same
  digest (under canonical rule).
- Scientific semantic: `100 cm` vs `1 m` may be equivalent only under an
  explicit domain rule; must not be normalized silently in JSON canonicalization.

## 7.6 Refinement — Crash windows and external side effects

- Failure A (before record): no durable state; retry creates new operation.
- Failure B (after record, before mutation): claimed but unexecuted; retry
  replays or conflicts.
- Failure C (during mutation): transaction rollback must roll back idempotency
  record too.
- Failure D (after mutation, before result persist): uncertain outcome;
  reconciliation required.
- Failure E (after commit, before response): operation succeeded; client retry
  must be deduplicated via durable record.
- Failure F (async worker): durable workflow state required.
- Failure G (external side effect before local record): downstream idempotency
  propagation required.

## 7.7 Refinement — Retention and expiry cases

- Full response retained vs discarded with tombstone.
- Key reuse after expiry (new operation vs conflict).
- Clock skew across instances.
- Multi-instance concurrency (unique constraint, atomic claim).

## 8. Evidence status

| Requirement | Existing evidence | Gap |
|---|---|---|
| Serialization determinism | Python/TS prototype | No normative spec |
| Cross-language digest | 12 structured + 2 exact-byte + 5 rejection vectors | Scientific decimals, units, Unicode normalization |
| Request equivalence | Prototype canonical comparison | No spec; header/body precedence undecided |
| Concurrency | L-24 (8-thread) | Multi-instance not tested |
| Durability | None (in-memory) | No durable implementation |
| Failure recovery | None | No fault-injection tests |
| Tenant isolation | None | No tests |
| Authorization on replay | None | No tests |