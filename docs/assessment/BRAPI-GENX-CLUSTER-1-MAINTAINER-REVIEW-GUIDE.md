# BrAPI-GenX — Cluster 1 Maintainer Review Guide

**Status:** DRAFT — NOT APPROVED. Reading guide for the repository maintainer.

## 1. What the three decisions are about

- **D-02** — Digest canonicalization: what byte sequence is hashed, under what
  rule, for what purpose.
- **D-24** — Idempotency equivalence: what makes two requests equivalent.
- **D-25** — Idempotency scope, retention, durability: namespace, retention,
  expiry, multi-instance, failure recovery.

## 2. Why they are interdependent

D-02 defines canonicalization used by D-24's request fingerprint. D-25's scope
and retention constrain D-24's identity model. D-24's replay requirements
constrain D-25's retention. Dependency: D-02 → D-24 → D-25, with feedback
from D-25 to D-24.

## 3. Three most important architectural corrections

1. Digest purposes must be separated: raw-byte, canonical JSON, and (possibly)
   scientific semantic fingerprint are distinct.
2. Idempotency record lookup identity must be separated from request fingerprint.
3. Database transactions are not distributed transactions; exactly-once
   execution cannot be claimed from duplicate-request detection.

## 4. Six questions requiring review

See approval packet §11.5 (Questions 1–6).

## 5. Recommended answers and trade-offs

Summarized in the approval packet. All recommendations are draft.

## 6. Decisions delegable to technical implementers

- Choice of hash algorithm (within approved profile).
- Storage engine selection.
- Concurrency control mechanism.

## 7. Decisions requiring security/operational authority

- Tenant isolation and authorization on replay (D-22 adjacent).
- Retention periods and expiry policy.
- Durability guarantees and production claims.

## 8. Decisions possibly requiring external standards consultation

- JCS adoption as normative canonicalization (community).
- BrAPI overlap for LotLedger (D-20, community).

## 9. Evidence still missing

- Cross-language scientific-decimal digest vectors.
- Durability/multi-instance/tenant-isolation tests.
- Authorization-on-replay tests.
- Fault-injection recovery tests.

## 10. What approval would authorize

Approval of D-02/D-24/D-25 would authorize updating RFC-001, the digest scope
inventory, conformance probes, and migrating the reference server from prototype
canonical form — not Phase 1B implementation.

## Compact decision table

| Decision | Proposed direction | Authority | Status |
|---|---|---|---|
| D-02 | Versioned GenX canonicalization profile (JCS candidate, domain rules separate) | Technical architecture + interoperability | Open |
| D-24 | Composite idempotency identity + separate request fingerprint | Maintainer + implementers + community | Open |
| D-25 | Composite namespace; durable DB-backed; at-least-once; tombstone retention | Maintainer + security + operational | Open |

## Links

- Approval packet: `docs/assessment/BRAPI-GENX-CLUSTER-1-APPROVAL-PACKET.md`
- Implementation baseline: `docs/assessment/BRAPI-GENX-CLUSTER-1-IMPLEMENTATION-BASELINE.md`
- Decision options: `docs/assessment/BRAPI-GENX-CLUSTER-1-DECISION-OPTIONS.md`
- Interoperability matrix: `docs/assessment/BRAPI-GENX-CLUSTER-1-INTEROPERABILITY-MATRIX.md`