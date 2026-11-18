# BrAPI-GenX — Cluster 1 Maintainer Review Guide

**Status:** REVIEW COMPLETE — six maintainer approval components recorded on 2026-11-03.

The BrAPI-GenX project maintainer approved the D-02, D-24, and D-25 architectural direction. `Specification/BrAPI-GenX/DECISIONS.md` remains the decision-status authority. This guide preserves the review framing and now directs follow-up implementation and verification; it does not claim implementation, production conformance, or official BrAPI endorsement.

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

## 4. Six questions resolved by maintainer approval

See approval packet §11.5 (Questions 1–6).

## 5. Approved answers and remaining trade-offs

The approved digest purposes, JCS adoption, identity/fingerprint separation,
composite namespace, header/body HTTP 400 rule, fresh replay authorization, and
durability/recovery requirements are summarized in the approved decision record.
Operation-specific fingerprints, retention duration, security architecture, and
implementation mechanisms remain follow-up work.

## 6. Implementation choices delegable to technical implementers

- Choice of hash algorithm/profile (not selected by this approval).
- Storage engine selection.
- Concurrency control mechanism.

## 7. Work requiring security/operational review

- Broader tenant isolation and authorization policy (D-22 remains open); fresh
  authentication and authorization on replay is already required by D-24.
- Retention periods and expiry policy.
- Durability guarantees and production claims.

## 8. Matters possibly requiring external standards consultation

- Independent interoperability evidence for JCS implementation; no official
  BrAPI/community endorsement is implied by internal approval.
- BrAPI overlap for LotLedger (D-20, community).

## 9. Evidence still missing

- Cross-language scientific-decimal digest vectors.
- Durability/multi-instance/tenant-isolation tests.
- Authorization-on-replay tests.
- Fault-injection recovery tests.

## 10. What the recorded approval authorizes

The approval authorizes future implementation planning for the approved
architecture, including RFC-001 updates, digest scope work, conformance probes,
and replacement of prototype-only behavior through separately authorized work.
It does not itself implement or validate those changes.

## Compact decision table

| Decision | Proposed direction | Authority | Status |
|---|---|---|---|
| D-02 | Three digest purposes; JCS-RFC8785 for generic JSON; domain rules separate | BrAPI-GenX maintainer | Approved — implementation pending |
| D-24 | Separate lookup/fingerprint; approved namespace; HTTP 400 key conflict; fresh replay authorization | BrAPI-GenX maintainer | Approved — implementation pending |
| D-25 | Durable shared state; atomic/recovery discipline; at-least-once; separate tombstones | BrAPI-GenX maintainer | Approved — implementation pending |

## Links

- Approval packet: `docs/assessment/BRAPI-GENX-CLUSTER-1-APPROVAL-PACKET.md`
- Implementation baseline: `docs/assessment/BRAPI-GENX-CLUSTER-1-IMPLEMENTATION-BASELINE.md`
- Decision options: `docs/assessment/BRAPI-GENX-CLUSTER-1-DECISION-OPTIONS.md`
- Interoperability matrix: `docs/assessment/BRAPI-GENX-CLUSTER-1-INTEROPERABILITY-MATRIX.md`
