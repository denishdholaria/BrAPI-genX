# BrAPI-GenX — Phase 1 Backlog

**Status:** planned, not started. Phase 0 must pass acceptance criteria first.
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
3. **Resolve D-02** (digest canonicalisation) via review of JCS vs custom;
   do not migrate helpers until decided.

## Priority 2 — Governance and security (P1)

4. **D-22 security review**: define scopes, auth profiles, tenant enforcement;
   document that prototype is not secure.
5. **D-21/D-23 capability negotiation**: decide requiredness and job-type
   advertisement policy.
6. **D-24/D-25 idempotency**: define equivalence, header/body precedence,
   namespace, retention, durability.

Dependency note: digest canonicalization (D-02), idempotency request equivalence
(D-24), and idempotency scope/retention/durability (D-25) are **not**
independent. D-24's equivalence definition depends on whether D-02's canonical
form is adopted; D-25's retention/expiry behavior interacts with D-24's
conflict detection. These must be resolved as a coordinated cluster, not as
separate implementation tasks.

## Priority 3 — Validation and evidence (P2)

7. **Domain-specific validators** for at least 2 modules beyond generic
   structural checks.
8. **Independent implementation evidence**: second implementation for at
   least one module.
9. **Refresh Conformance/RESULTS.md** with commit-pinned current run; keep
   historical runs labelled.
10. **Resolve S-22**: either register the guardrail as a probe or remove
    references.

## Priority 4 — Documentation and identity (P2/P3)

11. **Versioning policy**: adopt `0.x.y` proposal series formally (maintainer
    decision) and document BrAPI compatibility target separately.
12. **Update root README/identity docs** as needed after Phase 0 corrections.
13. **No bulk RFC generation** until quality gate is enforced in CI.

## Dependencies

- Phase 0 acceptance criteria must be met.
- Scientific decisions require maintainer/community authorization.
- No promotion of draft RFCs to accepted status in Phase 1 without governance.