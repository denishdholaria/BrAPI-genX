# BrAPI-GenX — Cluster 1 Approval Packet (D-02 / D-24 / D-25)

**Historical status:** DRAFT — NOT APPROVED. Prepared for maintainer review.

> **Ratification update (2026-11-03):** The BrAPI-GenX project maintainer approved the D-02, D-24, and D-25 architectural direction. This packet preserves the assessment that informed that decision; it is not the status authority. See `Specification/BrAPI-GenX/DECISIONS.md` and `docs/governance/BRAPI-GENX-CLUSTER-1-APPROVED-DECISIONS.md`. Implementation, conformance, security review, and external endorsement remain pending.

## 1. Executive summary

This packet presents the historical evidence, options, and recommendations for the first
critical decision cluster: digest canonicalization (D-02), idempotency
equivalence (D-24), and idempotency scope/retention/durability (D-25).

**No decision is accepted by this document.** The required maintainer
authorization was subsequently recorded in the authoritative decision register.

## 2. Exact questions requiring decisions

**D-02:**
1. What is being hashed (request body? inputs? artifact?)?
2. What canonicalization rule applies?
3. Is JCS (RFC 8785) adopted, adapted, or rejected?
4. How are scientific decimals/units handled?
5. Is canonicalization versioned?
6. Is algorithm agility required?

**D-24:**
1. What makes two requests equivalent?
2. Is equivalence exact-byte, canonical-JSON, or composite?
3. How is header/body key precedence resolved?
4. What is in-flight replay behaviour?
5. What is post-failure replay behaviour?
6. Is authorization re-checked on replay?

**D-25:**
1. What is the key namespace (tenant/principal/operation/endpoint)?
2. What is the minimum retention period?
3. What must survive restart?
4. What is the multi-instance model?
5. What is the expiry-reuse rule?
6. What guarantees can be honestly claimed?

## 3. Recommended resolution sequence

D-02 → D-24 → D-25, with feedback: D-25 scope/retention constrains D-24's
identity model. Partially parallel: D-02 and D-25-scope analysis can run
concurrently; D-24's equivalence depends on D-02.

## 4. Historical recommended options (draft at time of assessment)

- D-02: Versioned GenX canonicalization profile referencing JCS for generic
  JSON, with domain-specific rules for decimals/quantities; separate digest
  purposes.
- D-24: The historical recommendation was a composite identity. The accepted
  direction now uses tenant + authenticated client + effective principal +
  stable GenX operation ID as the namespace, a separate request fingerprint,
  and HTTP 400 for conflicting header/body keys.
- D-25: Composite key namespace; durable DB-backed state for production claims;
  configurable retention with documented minimum; tombstone retention; at-least-once
  delivery, not exactly-once execution.

## 5. Evidence supporting recommendations

- Prototype: Python `canonical()` (sort_keys, compact) + TS agreement on ASCII.
- JCS candidate corpus: 12 structured + 2 exact-byte + 5 rejection + 2 legacy
  + 10 mutation vectors (exploratory).
- Idempotency: L-01…L-05, L-24 (8-thread concurrency) on in-memory reference.
- No durability, multi-instance, or tenant-isolation evidence exists.

## 6. Outstanding implementation and policy work

- Operation/domain contracts for scientific decimal strings and fingerprint
  preimages.
- In-flight and post-failure replay representation.
- Retention-duration justification and documented minimum.
- Multi-instance coordination mechanism and recovery evidence.
- Implementation and verification of the approved replay-authorization rule.

## 7. Approval authority and remaining review

- D-02/D-24/D-25: approved by the BrAPI-GenX project maintainer on 2026-11-03.
- Implementers remain accountable for implementation and cross-language evidence.
- Security and operational reviewers remain responsible for D-22, replay
  enforcement evidence, durability, recovery, and retention validation.
- External BrAPI/community consultation remains separate and is not implied.

## 8. Required reviewers

- Implementers (Python and TypeScript/Bun).
- Security specialist (D-22 adjacent).
- Operational reviewers (durability/retention).
- BrAPI community (if normative compatibility claimed).

## 9. Post-approval implementation and evidence criteria

- Cross-language digest agreement on a normative vector set.
- Documented equivalence rules with edge cases.
- Tenant-isolation and authorization-on-replay specified.
- Durability guarantees honestly scoped (at-least-once, not exactly-once).
- Maintainer approval is recorded in `DECISIONS.md`; retain evidence showing
  the approved architecture is implemented correctly.

## 10. Implementation consequences after approval

- Update RFC-001 idempotency section.
- Update digest scope inventory.
- Add conformance probes for the normative rules.
- Migrate reference server from prototype canonical form if changed.
- Update test vectors to normative status.

## 11. Decisions and matters that remain open

- D-22 (security) — separate cluster.
- D-20 (BrAPI overlap) — separate cluster.
- D-01, D-03…D-19 — per ownership matrix.
- Cryptographic hash-algorithm selection, numeric retention minimum, exact
  operation fingerprint fields, and domain semantic fingerprints.

## 11.5 Maintainer Review — Critical Architectural Questions

### Question 1 — Digest purpose (approved)
Should GenX distinguish raw-byte digests, canonical JSON digests, and
domain-specific semantic fingerprints? **Approved:** yes. Each purpose has its
own contract; scientific semantic fingerprints remain optional and domain-specific.

### Question 2 — JCS (approved)
Should JCS (RFC 8785) be used for generic JSON canonicalization, with scientific
decimals/units handled separately? **Approved:** yes, as unmodified
`JCS-RFC8785`, with its IEEE 754 constraints and no Unicode normalization. JCS
implementation and conformance tests remain required.

### Question 3 — Idempotency identity (approved)
Should the system separate idempotency record lookup identity from request
fingerprint? **Approved:** yes: namespace+key for lookup; stable operation ID +
relevant context + canonical payload for the fingerprint.

### Question 4 — Operation identity and scope (approved)
What should define the idempotency namespace? Evaluate tenant, authenticated
client, principal, stable operation identity. **Approved:** tenant +
authenticated client + effective principal + stable GenX operation ID; no
route-derived endpoint component.

### Question 5 — Header/body conflict and replay authorization (approved)
Should header/body conflict be rejected (400) rather than silently ignored?
Should authorization be re-checked on replay? **Approved:** reject differing
key values with HTTP 400 and freshly authenticate/authorize before disclosure.

### Question 6 — Durability and side effects (approved)
What guarantees should the contract require for production-conforming
idempotency? **Approved:** durable shared state, coordinated mutation/recovery,
at-least-once delivery with idempotent effects, no universal exactly-once claim,
and separate response/tombstone retention. Technology and durations remain open.

## 12. Cross-references

- Baseline: `docs/assessment/BRAPI-GENX-CLUSTER-1-IMPLEMENTATION-BASELINE.md`
- Options: `docs/assessment/BRAPI-GENX-CLUSTER-1-DECISION-OPTIONS.md`
- Matrix: `docs/assessment/BRAPI-GENX-CLUSTER-1-INTEROPERABILITY-MATRIX.md`
- Original decisions: `Specification/BrAPI-GenX/DECISIONS.md` (D-02, D-24, D-25)
- Governance: `docs/governance/BRAPI-GENX-DECISION-GOVERNANCE.md`
- Ownership: `docs/governance/BRAPI-GENX-DECISION-OWNERSHIP-MATRIX.md`
