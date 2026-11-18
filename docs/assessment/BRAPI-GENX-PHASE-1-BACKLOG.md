# BrAPI-GenX — Phase 1 Backlog

**Status:** planned; Cluster 1 architectural direction approved, implementation not started.
**Baseline commit:** `6c09dff4c8f68fc89df541fc1fdcb09abc95e30c`

## Priority 1 — Deepen scientifically important modules (P1)

1. **RFC-003-style depth for 3–5 modules.** Select modules with real
   interoperability value (e.g. LotLedger, SelectionDecisions, VariantMatrix
   references, FAIRPackage). For each: problem statement, domain model,
   typed properties with units/precision, identifier policy, lifecycle,
   operations justified by lifecycle, security, acceptance criteria, fixtures.
   Acceptance: RFC upgraded from STRUCTURAL_DRAFT to SEMANTICALLY_REVIEWED.
2. **Resolve D-20** (SeedLotTransaction vs LotLedgerEntry relationship) with
   community/implementer input before any dual-write guidance is published.
3. **Implement approved D-02 architecture:** introduce JCS-RFC8785 where
   canonical JSON is required; keep raw-byte and scientific semantic purposes
   separate; define preimages and cross-language vectors. Cryptographic hash
   selection remains separate.

## Priority 2 — Governance and security (P1)

4. **D-22 security review**: define scopes, auth profiles, tenant enforcement;
   document that prototype is not secure.
5. **D-21/D-23 capability negotiation**: decide requiredness and job-type
   advertisement policy.
6. **Implement approved D-24/D-25 idempotency architecture:** define
   operation-specific fingerprint fields; implement the composite namespace,
   HTTP 400 key-conflict rule, fresh replay authorization, durable shared state,
   atomic/recovery coordination, and explicit response/tombstone retention.

Dependency note: D-02, D-24, and D-25 are approved as a coordinated
architecture. D-24 implementation uses D-02's JCS rule where canonical JSON is
appropriate, and D-25 provides the lifecycle/durability constraints for D-24.
Do not reopen their approved direction for implementation convenience. The exact
fingerprint fields, numeric retention minimum, hash algorithm, and D-22 security
architecture remain separately governed.

## Priority 3 — Validation and evidence (P2)

7. **Domain-specific validators** for at least 2 modules beyond generic
   structural checks.
8. **Independent implementation evidence**: second implementation for at
   least one module.
9. **Refresh Conformance/RESULTS.md** with commit-pinned current run; keep
   historical runs labelled.
10. **Resolve S-22**: either register the guardrail as a probe or remove
    references.
11. **Cluster 1 conformance evidence:** cross-language JCS vectors,
    replay-authorization/non-disclosure probes, multi-instance concurrency,
    restart/fault recovery, external-effect recovery, and retention/tombstone
    tests. Obtain independent interoperability evidence before any production
    conformance claim.

## Priority 4 — Documentation and identity (P2/P3)

11. **Versioning policy**: adopt `0.x.y` proposal series formally (maintainer
    decision) and document BrAPI compatibility target separately.
12. **Update root README/identity docs** as needed after Phase 0 corrections.
13. **No bulk RFC generation** until quality gate is enforced in CI.

## Dependencies

- Phase 0 acceptance criteria must be met.
- D-02, D-24, and D-25 have maintainer authorization; their implementation and
  verification remain pending. Other scientific decisions retain their stated
  authorization requirements.
- No promotion of draft RFCs to accepted status in Phase 1 without governance.
