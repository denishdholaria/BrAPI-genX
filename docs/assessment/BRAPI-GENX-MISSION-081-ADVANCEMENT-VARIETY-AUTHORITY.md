# Mission 081 — Population advancement and candidate-variety authority boundaries

**Parent:** `2c1a4d48ab1accfed3d54619012f3fc9f3e4c321` (Mission 080), 2026-11-24.  
**Scope:** source-backed scientific authority qualification, existing decision preservation, and regression checks. No official Breeding Application Programming Interface (BrAPI) version 2.1 wire contract, GenX schema, operation identifier, registry, conformance maturity or decision ratification changed.

## Source-verified findings

1. **PopulationAdvancement** (Request for Comments (RFC) 035) has an **accepted D-BP-10 boundary**: it records actual population progression and is not a scheme transition rule. The registration request requires `populationAdvancementDbId`, authority-qualified `programReference` and `populationReference` and `advancedAt`; response additionally requires status. `pipelineContext` and `schemeContext` are optional, with stage identity restricted to an exact scheme version. A successful record is not independent evidence of physically executed material movement, owner authorization or an actual `SelectionDecision` verdict. D-102–D-104 remain deferred.
2. **CandidateVariety** (RFC-039, D-115–D-117) requires `candidateVarietyDbId`, `programDbId`, and `varietyName` on registration. The status defaults to `candidate`; its enum includes `registered` and `released`, but **no regulatory authority, certificate, official approval evidence, jurisdiction or validated `germplasmDbId` join** exists. The optional `registeredAt` is not required even in registered status. A local label cannot confer statutory release or seed-market permissions. D-116 previously described a BreedingPipeline link as optional although no `breedingPipelineDbId` field is modelled.
3. **CrossingSchedule** (RFC-037) remains explicitly **DEFERRED by D-BP-11**. No GroupDescription review coverage or implementation is added for it. Official BrAPI PlannedCross and CrossingProject remain authoritative for mating intent.

## Implementation and scope

- Add source-linked `STRUCTURAL_DRAFT` GroupDescriptions for PopulationAdvancement and CandidateVarietyLifecycle.
- Qualify README and RFC text to avoid treating recorded events, local statuses and versioned intent as executed or legally authoritative decisions.
- Add guarded source-derived test checks for required fields, optional scheme/pipeline context, distinct SelectionDecision verdict, candidate status semantics, and CrossingSchedule deferral.
- Evidence-reviewed group descriptions become **132 of 156**, leaving **24 deferred**, only on the unmerged stacked branch.

## Verification boundary

Authoritative source file cross-checks and link resolution are necessary but not a substitute for running the Python tests and full registry/conformance gates. These changes do not independently establish external authorization, statutory compliance, operational inventory transfer, distributed identity verification or production runtime replay.
