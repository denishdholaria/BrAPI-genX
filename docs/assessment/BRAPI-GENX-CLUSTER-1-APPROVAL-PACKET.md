# BrAPI-GenX — Cluster 1 Approval Packet (D-02 / D-24 / D-25)

**Status:** DRAFT — NOT APPROVED. For maintainer review only.

## 1. Executive summary

This packet presents the evidence, options, and recommendations for the first
critical decision cluster: digest canonicalization (D-02), idempotency
equivalence (D-24), and idempotency scope/retention/durability (D-25).

**No decision is accepted by this document.** All proposed decision text is
draft and requires explicit maintainer authorization.

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

## 4. Recommended options (draft)

- D-02: Versioned GenX canonicalization profile referencing JCS for generic
  JSON, with domain-specific rules for decimals/quantities; separate digest
  purposes.
- D-24: Composite idempotency identity (tenant + principal + operation +
  endpoint + canonical payload); header precedence with documented conflict
  handling; 409 on payload mismatch.
- D-25: Composite key namespace; durable DB-backed state for production claims;
  configurable retention with documented minimum; tombstone retention; at-least-once
  delivery, not exactly-once execution.

## 5. Evidence supporting recommendations

- Prototype: Python `canonical()` (sort_keys, compact) + TS agreement on ASCII.
- JCS candidate corpus: 12 structured + 2 exact-byte + 5 rejection + 2 legacy
  + 10 mutation vectors (exploratory).
- Idempotency: L-01…L-05, L-24 (8-thread concurrency) on in-memory reference.
- No durability, multi-instance, or tenant-isolation evidence exists.

## 6. Outstanding uncertainty

- Scientific decimal handling in JCS (IEEE 754 vs decimal strings).
- Unicode normalization policy.
- In-flight and post-failure replay behaviour.
- Retention duration justification.
- Multi-instance coordination mechanism.
- Authorization on replay.

## 7. Accountable authority

- D-02: technical architecture + interoperability review; community if normative.
- D-24: maintainer + implementers + community (normative API contract).
- D-25: maintainer + security + operational.

## 8. Required reviewers

- Implementers (Python and TypeScript/Bun).
- Security specialist (D-22 adjacent).
- Operational reviewers (durability/retention).
- BrAPI community (if normative compatibility claimed).

## 9. Approval criteria

- Cross-language digest agreement on a normative vector set.
- Documented equivalence rules with edge cases.
- Tenant-isolation and authorization-on-replay specified.
- Durability guarantees honestly scoped (at-least-once, not exactly-once).
- Maintainer explicit approval recorded in `DECISIONS.md`.

## 10. Implementation consequences after approval

- Update RFC-001 idempotency section.
- Update digest scope inventory.
- Add conformance probes for the normative rules.
- Migrate reference server from prototype canonical form if changed.
- Update test vectors to normative status.

## 11. Decisions that must remain open

- D-02, D-24, D-25 themselves (this packet does not resolve them).
- D-22 (security) — separate cluster.
- D-20 (BrAPI overlap) — separate cluster.
- D-01, D-03…D-19 — per ownership matrix.

## 11.5 Maintainer Review — Critical Architectural Questions

### Question 1 — Digest purpose
Should GenX distinguish raw-byte digests, canonical JSON digests, and
domain-specific semantic fingerprints? Recommendation (draft): yes. Trade-off:
clarity vs. complexity. Consequence: each purpose gets its own contract.

### Question 2 — JCS
Should JCS (RFC 8785) be the candidate for generic JSON canonicalization, with
scientific decimals/units handled separately? Recommendation (draft): yes, as a
candidate, with explicit limitations documented (IEEE 754 numbers, no Unicode
normalization). Consequence: JCS compliance tests required.

### Question 3 — Idempotency identity
Should the system separate idempotency record lookup identity from request
fingerprint? Recommendation (draft): yes. Proposed: namespace+key for lookup;
operation identity + canonical payload for fingerprint.

### Question 4 — Operation identity and scope
What should define the idempotency namespace? Evaluate tenant, authenticated
client, principal, stable operation identity. Recommendation (draft): composite
(tenant + principal + operation + endpoint), not global.

### Question 5 — Header/body conflict and replay authorization
Should header/body conflict be rejected (400) rather than silently ignored?
Should authorization be re-checked on replay? Recommendation (draft): reject on
conflict; re-verify authorization on replay.

### Question 6 — Durability and side effects
What guarantees should the contract require for production-conforming
idempotency? Recommendation (draft): at-least-once delivery + idempotent retry;
not exactly-once execution; durable DB-backed state; separate external
side-effect strategy.

## 12. Cross-references

- Baseline: `docs/assessment/BRAPI-GENX-CLUSTER-1-IMPLEMENTATION-BASELINE.md`
- Options: `docs/assessment/BRAPI-GENX-CLUSTER-1-DECISION-OPTIONS.md`
- Matrix: `docs/assessment/BRAPI-GENX-CLUSTER-1-INTEROPERABILITY-MATRIX.md`
- Original decisions: `Specification/BrAPI-GenX/DECISIONS.md` (D-02, D-24, D-25)
- Governance: `docs/governance/BRAPI-GENX-DECISION-GOVERNANCE.md`
- Ownership: `docs/governance/BRAPI-GENX-DECISION-OWNERSHIP-MATRIX.md`