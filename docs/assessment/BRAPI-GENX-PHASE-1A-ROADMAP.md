# BrAPI-GenX — Phase 1A Roadmap

**Status:** Phase 1A planning. Cluster 1 direction is approved; no implementation is authorized by this roadmap.
**Companions:** decision dependency review, ownership matrix, pilot selection.

## 1. Dependency-aware work sequence

### Workstream 0 — Governance hygiene (can start immediately, no authorization needed)
1. Migrate ~415 RFC-local `D-NNN` identifiers to `RFC-NNN-QN` (governance only).
2. Adopt decision governance policy (already documented).
3. Update Phase 1 backlog decision cluster dependency note (done).

### Workstream 1 — Prerequisite decision clusters
1. Cluster 1: D-02 → D-24 → D-25 (digest + idempotency) — approved by the BrAPI-GenX project maintainer on 2026-11-03; implementation and evidence remain pending.
2. Cluster 2: D-22 (security).
3. Cluster 3: D-20 (BrAPI overlap).
4. Cluster 4: D-21, D-23 (capability advertisement).
5. Remaining D-01, D-03…D-19 per ownership matrix.

### Workstream 2 — Scientific pilot (Phase 1B, after Workstream 1 prerequisites)
1. Domain investigation for BreedingPipeline (RFC-154).
2. Terminology and standards investigation.
3. Domain model (entities, identity, lifecycle, provenance).
4. API contract design.
5. Schema and fixtures.
6. Conformance design.
7. Independent implementability review.
8. Governance review and maturity upgrade.

## 2. Prerequisite decisions

Minimum set before Phase 1B implementation:
- D-02 (digest canonicalization) — approved architecture; implementation and
  conformance evidence are required if a pilot touches provenance/mutation.
- D-22 (security meaning) — if pilot declares authorization.
- D-20 (BrAPI overlap) — if pilot overlaps BrAPI resources.

For BreedingPipeline specifically: D-454/D-455/D-456 (RFC-local) plus domain
research on stage-gate semantics. No digest/BrAPI-overlap dependency.

## 3. Parallel workstreams

- Governance hygiene (Workstream 0) can run in parallel with Cluster 1 implementation planning.
- D-22 and D-20 can run in parallel with Cluster 1 implementation (different authorities).
- Pilot domain investigation can begin in parallel with decision clusters,
  provided no normative claims are made.

## 4. Required reviewers

| Workstream | Reviewers |
|---|---|
| Cluster 1 | Implementers (Python/TS), security, maintainer |
| Cluster 2 | Security specialist, maintainer |
| Cluster 3 | BrAPI community, implementers, maintainer |
| Cluster 4 | Implementers, maintainer |
| Pilot | Domain experts (breeding), standards reviewers, maintainer |

## 5. Evidence milestones

- M1: D-02 approved decision record (complete); cross-language implementation evidence remains required.
- M2: D-24/D-25 approved decision records (complete); implementation, durability, and security evidence remains required.
- M3: Security contract definition (D-22).
- M4: BrAPI overlap analysis for LotLedger (D-20).
- M5: Capability advertisement model (D-21, D-23).
- M6: Pilot RFC upgraded to SEMANTICALLY_REVIEWED with full quality-standard
  sections and falsifiable tests.

## 6. Phase 1B readiness criteria

Phase 1B implementation may begin only when:
- The pilot's RFC-local decisions are resolved or explicitly deferred with
  documented consequences.
- Domain evidence and terminology are documented.
- At least one prerequisite decision cluster relevant to the pilot is resolved.
- The maintainer explicitly authorizes implementation.

## 7. Explicitly deferred work

- Implementation of digest/idempotency/security behaviour.
- New RFCs or endpoints.
- Modification of official BrAPI v2.1 contracts.
- Ambika catalogue changes.
- Promotion of any RFC to accepted status.
- Generation of additional bulk RFCs.

## 8. Cross-references

- Decision dependency review: `docs/assessment/BRAPI-GENX-PHASE-1A-DECISION-DEPENDENCY-REVIEW.md`
- Decision ownership matrix: `docs/governance/BRAPI-GENX-DECISION-OWNERSHIP-MATRIX.md`
- Scientific pilot selection: `docs/assessment/BRAPI-GENX-SCIENTIFIC-PILOT-SELECTION.md`
- Phase 0 quality standard: `docs/governance/BRAPI-GENX-SPECIFICATION-QUALITY-STANDARD.md`
- Phase 0 maturity register: `docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md`
- Phase 1 backlog: `docs/assessment/BRAPI-GENX-PHASE-1-BACKLOG.md`
