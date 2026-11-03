# BrAPI-GenX — Cluster 1 Interoperability Matrix

**Historical status:** Phase 1A.1 decision engineering.

> **Ratification update (2026-11-03):** D-02, D-24, and D-25 are accepted BrAPI-GenX architectural directions. This matrix preserves pre-approval evidence and test gaps. The authoritative status is in `Specification/BrAPI-GenX/DECISIONS.md`; implementation and verification remain pending.

## 1. Canonicalization test matrix (D-02)

| Case | Approved JCS rule | Python prototype | Current requirement / follow-up |
|---|---|---|---|
| Object property ordering | Normalized (sorted) | Normalized (sorted) | JCS-RFC8785 |
| Array ordering | Preserved | Preserved | JCS-RFC8785 |
| Whitespace | Ignored | Ignored | JCS-RFC8785 |
| Duplicate property names | Reject | Reject (hook) | Reject |
| `null` vs missing | Differ | Differ | JCS semantics; operation contracts define fingerprint fields |
| Negative zero | Normalized to 0 | Python keeps -0.0 | JCS-RFC8785 |
| Large integers | JCS uses shortest repr | Python arbitrary precision | JCS constraints; use domain strings where required |
| Exponential notation | Normalized | Python preserves | JCS-RFC8785 |
| Unicode normalization | None (preserved) | None (preserved) | No automatic normalization |
| Lone surrogates | Reject | Reject (custom) | JCS-RFC8785 |
| Non-JSON constants (NaN/Infinity) | Reject | Reject (parse_constant) | Reject |
| Decimal as string | Treated as string | Treated as string | Use strings where domain contract requires |

## 2. Request-equivalence matrix (D-24)

| # | Variation | Equivalent? (approved model / implementation follow-up) |
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
| 12 | Same key, different tenant | Separate namespace; do not disclose another record |
| 13 | Same key, different client | Separate namespace |
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
- Same key, different payload, simultaneous → one accepted, one conflict; D-01 still governs any general conflict status while header/body key disagreement is HTTP 400 under D-24.
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
| Serialization determinism | Python/TS prototype | Implement approved JCS-RFC8785 |
| Cross-language digest | 12 structured + 2 exact-byte + 5 rejection vectors | Scientific decimal/domain contracts and normative implementation evidence |
| Request equivalence | Prototype canonical comparison | Implement approved identity/fingerprint and HTTP 400 header/body rule |
| Concurrency | L-24 (8-thread) | Multi-instance not tested |
| Durability | None (in-memory) | No durable implementation |
| Failure recovery | None | No fault-injection tests |
| Tenant isolation | None | No tests |
| Authorization on replay | None | No tests |
