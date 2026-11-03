# BrAPI-GenX — Cluster 1 Approved Decisions

**Decision-status authority:** [`Specification/BrAPI-GenX/DECISIONS.md`](../../Specification/BrAPI-GenX/DECISIONS.md) is the authoritative decision register.

**Approval authority:** BrAPI-GenX project maintainer
**Approval date:** 2026-11-03
**Scope:** D-02, D-24, and D-25 architectural direction

## 1. Approval summary and boundary

The maintainer accepted the Cluster 1 architectural direction: D-02 separates digest purposes and adopts JCS/RFC 8785 for generic canonical JSON; D-24 separates idempotency lookup identity from request fingerprint and requires fresh authorization on replay; and D-25 requires durable shared production idempotency state, recovery discipline, and separate response/tombstone retention.

This is an internal BrAPI-GenX approval. It is not an official BrAPI community decision, a claim of deployment, an implementation completion statement, or independent conformance evidence. Implementation, security review, operational policy, and verification remain required.

## 2. D-02 — Digest architecture

Three purposes are distinct:

- **Raw-byte digest:** identifies an exact sequence of bytes for file integrity, artifact verification, exact-payload verification, and byte-level provenance.
- **Canonical JSON digest:** identifies generic JSON after the agreed deterministic serialization method. The approved method is JCS from RFC 8785, identified as `JCS-RFC8785`.
- **Scientific semantic fingerprint:** an optional, domain-specific fingerprint of scientifically meaningful content under explicit domain rules. It is not a universal GenX digest requirement.

JCS must be implemented as published: reject duplicate object properties and non-finite values, do not normalize Unicode automatically, and obey JCS number representation constraints. High-precision scientific decimal values must be represented as strings where their scientific data contract requires it. Unit conversion, rounding, temporal interpretation, identifier equivalence, uncertainty treatment, and other scientific semantics belong to explicit domain rules, not generic JCS.

```text
Input data
    |
    +-- Exact bytes
    |       |
    |       +-- Raw-byte digest
    |
    +-- Generic JSON
    |       |
    |       +-- JCS-RFC8785 canonicalization
    |               |
    |               +-- Canonical JSON digest
    |
    +-- Scientific domain data
            |
            +-- Explicit domain-specific rules
                    |
                    +-- Optional scientific semantic fingerprint

Cryptographic hash algorithm: separate selected/profiled element; not selected by D-02.
```

No universal semantic digest, automatic unit conversion, decimal rounding, Unicode normalization, or universal cryptographic hash algorithm is approved. Existing SHA-256 implementation evidence does not select SHA-256 as the universal GenX algorithm.

## 3. D-24 — Idempotency identity, equivalence, and replay

The idempotency lookup identity is separate from the request fingerprint:

```text
lookup identity     = idempotency_namespace + idempotency_key
request fingerprint = stable_genx_operation_id
                      + relevant_request_context
                      + canonical_request_payload
idempotency namespace = tenant_id
                        + authenticated_client_id
                        + effective_principal_id
                        + stable_genx_operation_id
```

`tenant_id` is the data-isolation boundary; `authenticated_client_id` identifies the calling application/service; `effective_principal_id` identifies whose authority is exercised; and the stable operation ID identifies the logical GenX operation. A service identity is the effective principal for service-to-service use. Delegation preserves both client and effective user. Route aliases for the same operation use the same stable operation ID; IDs are not derived from mutable route strings.

| Namespace/key | Fingerprint | Result |
|---|---|---|
| Same | Same | Retry or replay candidate |
| Same | Different | Conflicting key reuse |
| Different | Same | Potentially a distinct logical operation |
| Different tenant | Same key/payload | Separate tenant namespace |

Only query values, headers, and other context that materially affect operation semantics belong in the fingerprint. The exact field set remains operation-specific.

If both an `Idempotency-Key` header and a body key are supplied, equal values are permitted and different values are rejected with HTTP 400. The header is the authoritative transport mechanism. Any retained body-only compatibility must be documented; changing it is a separate compatibility decision.

Every replay performs fresh authentication and authorization before disclosure. The server establishes current tenant/client/effective-principal context, verifies authority to perform/access the operation and stored result, and returns only authorized information. Possession of a key grants no retrieval right. Unauthorized handling must not reveal another tenant's or user's record.

## 4. D-25 — Durability, recovery, and retention

Production-conforming implementations require durable, shared idempotency state across application instances; atomic claim/create; namespace-scoped unique-key enforcement; restart persistence; recovery of accepted operations; and duplicate recognition during the documented retention window. Database-backed storage is appropriate but not mandated. Process-local dictionaries and locks are development/reference-only.

Where an idempotency record and business mutation share a transactional store, they must be coordinated atomically. A success record without its committed mutation, or a committed mutation without safe retry recognition, is not acceptable. When a common transaction boundary is unavailable, the coordination and recovery mechanism must be documented.

External effects need an operation-appropriate recovery strategy, such as a transactional outbox, downstream idempotency propagation, durable workflow state, event deduplication, reconciliation, or compensation. This is an at-least-once architecture with idempotent effects/deduplication/recovery where required; it does not promise universal exactly-once execution.

Full-response retention and idempotency-tombstone retention are independent. A tombstone retains identity/outcome information after a full response is discarded, preventing accidental re-execution. When a response has expired, an implementation should return an appropriate operation reference, status, or documented result-expired response.

The implementation must document supported retry window, full-response retention, tombstone retention, expiry behaviour, key-reuse behaviour, recovery implications, and necessary retention extensions. Retention may be configurable, but a justified documented minimum is required. No numeric duration is approved here.

## 5. Integrated idempotency architecture

```text
Incoming request
    |
    +-- Authentication
    |
    +-- Establish tenant/client/effective-principal context
    |
    +-- Stable GenX operation identity
    |
    +-- Idempotency namespace + idempotency key
    |
    +-- Atomic lookup/claim in durable shared state
            |
            +-- Request fingerprint comparison
                    |
                    +-- Same fingerprint
                    |       |
                    |       +-- Fresh authorization
                    |               |
                    |               +-- Replay eligible result/status
                    |
                    +-- Different fingerprint
                            |
                            +-- Conflict

New accepted operation --> atomic business mutation + idempotency outcome
                         --> external-effect coordination/recovery
                         --> response retention and longer/independent tombstone retention
```

## 6. Dependencies and security boundary

- D-02 supplies the canonical JSON method for D-24 when a canonical payload is used.
- D-24 supplies identity and equivalence semantics for D-25's durable record lifecycle.
- D-25 supplies durability, transaction, recovery, and retention requirements for D-24.
- D-22 remains **open**. The narrow D-24 requirement for fresh authentication and authorization on replay is approved, but it does not define D-22's provider, scopes, policy model, denial model, or operational guarantees.

## 7. Normative requirements vs implementation choices

| Normative architectural requirement | Implementation-specific choice left open |
|---|---|
| JCS-RFC8785 for generic canonical JSON | JCS library/runtime integration |
| Three distinct digest purposes | Cryptographic hash algorithm/profile |
| Composite namespace and separate fingerprint | Storage schema and concurrency primitive |
| Fresh authorization on replay | Authentication provider and authorization policy |
| Durable shared production state | Database technology |
| Atomicity/recovery and at-least-once honesty | Outbox/workflow/reconciliation technique per operation |
| Separate response/tombstone retention | Numeric durations and storage tiering |

## 8. Explicit exclusions and deferred matters

| Matter | Status |
|---|---|
| Full D-22 security architecture | Open |
| Cryptographic hash algorithm selection | Not approved by this cluster |
| Numeric tombstone retention duration | Not selected |
| Exact fingerprint fields per operation | Operation-specific specification required |
| Scientific semantic fingerprints | Optional future domain decisions |
| Database technology | Implementation choice |
| External BrAPI community endorsement | Not implied |
| Independent evidence and production conformance | Pending |

An accepted decision may be reconsidered only for a documented standards conflict, material interoperability defect, security/safety defect, scientific evidence changing the contract, or formally authorized governance change.

## 9. Implementation acceptance criteria

### D-02

- [ ] Distinguish raw-byte, canonical JSON, and optional scientific semantic purposes.
- [ ] Use unmodified JCS-RFC8785 for generic canonical JSON; reject duplicates and non-finite numbers.
- [ ] Do not automatically normalize Unicode, units, or scientific decimals.
- [ ] Use contract-appropriate string representations for high-precision scientific decimals.
- [ ] Identify digest purpose and canonicalization method; handle hash selection separately.
- [ ] Provide cross-language vectors for supported inputs.

### D-24

- [ ] Keep lookup identity distinct from the request fingerprint.
- [ ] Use tenant, authenticated client, effective principal, and stable operation ID in the namespace.
- [ ] Define service and delegated identity; keep operation ID independent of route aliases.
- [ ] Treat same scoped key/fingerprint as replay candidate and a changed fingerprint as conflict.
- [ ] Reject conflicting header/body keys with HTTP 400 and document retained body-only compatibility.
- [ ] Freshly authenticate and authorize replays without record-existence disclosure; make concurrency deterministic.

### D-25

- [ ] Provide shared durable production state, atomic claim/create, multi-instance coordination, and restart-safe recognition.
- [ ] Coordinate mutation and idempotency outcome atomically where possible; document other recovery paths.
- [ ] Coordinate external effects and do not claim universal exactly-once execution.
- [ ] Retain response and tombstone separately; prevent re-execution during tombstone retention.
- [ ] Document retry window, minimum retention, expiry, and key-reuse behaviour without inventing an unapproved duration.

## 10. Required conformance evidence

- Cross-language JCS vectors, including rejection and scientific-string cases.
- Operation-specific fingerprint vectors and header/body conflict tests.
- Authentication/authorization replay tests proving non-disclosure.
- Same-instance and multi-instance concurrency tests.
- Restart, crash-window, transactional rollback, and recovery/fault-injection tests.
- Retention/expiry/tombstone tests, including expired-response handling.
- Independent implementation interoperability evidence before any production-conformance claim.

## 11. References

- Authoritative register: `Specification/BrAPI-GenX/DECISIONS.md` (D-02, D-22, D-24, D-25).
- Phase 1A.1 baseline: `docs/assessment/BRAPI-GENX-CLUSTER-1-IMPLEMENTATION-BASELINE.md`.
- Phase 1A.2 approval materials: `docs/assessment/BRAPI-GENX-CLUSTER-1-APPROVAL-PACKET.md`, `BRAPI-GENX-CLUSTER-1-DECISION-OPTIONS.md`, `BRAPI-GENX-CLUSTER-1-INTEROPERABILITY-MATRIX.md`, and `BRAPI-GENX-CLUSTER-1-MAINTAINER-REVIEW-GUIDE.md`.
- Governance: `docs/governance/BRAPI-GENX-DECISION-GOVERNANCE.md` and `BRAPI-GENX-DECISION-OWNERSHIP-MATRIX.md`.
