# BrAPI-GenX — Scientific Pilot Selection

**Status:** Phase 1A planning. No implementation authorized.
**Companion:** `docs/assessment/BRAPI-GENX-PHASE-1A-DECISION-DEPENDENCY-REVIEW.md`,
`docs/governance/BRAPI-GENX-SPECIFICATION-QUALITY-STANDARD.md`.

## 1. Methodology

Candidates are scored 1–5 on seven dimensions (weights sum to 100%):

| Dimension | Weight |
|---|---:|
| Scientific importance to agricultural research/breeding | 20% |
| Current specification gap / improvement opportunity | 20% |
| Availability of domain evidence and expertise | 15% |
| Feasibility of precise, testable contracts | 15% |
| Interoperability and alignment potential | 10% |
| Ability to demonstrate independent implementation | 10% |
| Manageable scope and decision dependencies | 10% |

A high score is not proof of scientific validity. Scores reflect planning
feasibility and are explicitly uncertain where evidence is thin.

## 2. Candidate inventory

| Candidate | RFC | Maturity | Notes |
|---|---|---|---|
| BreedingPipeline | RFC-154 | STRUCTURAL_DRAFT | Templated; single `pipelineStage` string; no ordered stages/gates |
| RemoteSensingMetadata | RFC-145 | STRUCTURAL_DRAFT | Templated; untyped strings for CRS/resolution/date |
| ExperimentalDesign | RFC-018 | STRUCTURAL_DRAFT | Trial layout, replication, randomization, treatment assignment |
| RepeatedMeasurement | (RepeatedMeasurement/) | STRUCTURAL_DRAFT | Time-ordered values, quality flags |
| SelectionDecisions | RFC-008 | STRUCTURAL_DRAFT | Breeding verdicts; no BrAPI v2.1 equivalent |
| Seed-Lot Ledger | RFC-003 | CONTRACT_VALIDATED | Quality benchmark; already deeper |

## 3. Detailed assessment — RFC-154 BreedingPipeline

Scientific purpose: represent a breeding pipeline (program, stages, advancement)
as an interoperable record. Current schema has `pipelineStage` (string) only —
no ordered stage collection, gate criteria, transitions, or stage-specific
evidence. The index description claims "ordered stage gates" that the schema
does not model.

Deficiencies: required fields only id + status; breedingProgram/targetTrait/
pipelineType optional; unbounded strings; no lifecycle beyond enum; no provenance
beyond embedded envelope; no relationship to experiments/studies/germplasm.

Required expertise: plant breeding, breeding-program management, experimental
design. External standards: none established for breeding pipelines; would need
domain research (no inventing stage-gate semantics).

BrAPI overlap: BrAPI v2.1 has Program/Trial/Study but no pipeline concept. Low
direct overlap, but relationship to Program/Trial must be defined.

Decision dependencies: D-454 (targetTrait required?), D-455 (pipelineType vocab?),
D-456 (ResearchAsset link). These are RFC-local and manageable. Does not depend
on digest/BrAPI-overlap clusters.

Scope: moderate (1 resource, 3 operations). Feasible as a bounded pilot IF
stage-gate semantics are researched first.

## 4. Detailed assessment — RFC-145 RemoteSensingMetadata

Scientific purpose: record remote-sensing acquisition metadata. Current schema
has platform, sensor, acquisition date, CRS, resolution as untyped strings — no
structured spatial footprint, no typed bands, no processing level, no product
identity, no calibration.

Deficiencies: date and CRS are free-form strings; resolution is a string like
"10m"; no spatial geometry; no spectral band model; no processing-level enum;
no asset reference typing.

Required expertise: remote sensing, geospatial standards (CRS, GeoJSON/OGC),
spectral bands, calibration. External standards to investigate: OGC, STAC,
GeoJSON, EPSG CRS registry — but appropriateness must be established, not
assumed.

BrAPI overlap: none directly (BrAPI has no remote-sensing resource). Risk of
overreach: a metadata record is not an observation or raster.

Decision dependencies: D-433 (resolution required?), D-434 (platform vocab?),
D-435 (ResearchAsset link). Plus unresolved geospatial standard choices (not
yet even captured as decisions).

Scope: potentially large due to geospatial standard investigation. Higher risk
of scope creep.

## 5. Additional candidate — ExperimentalDesign (RFC-018)

Scientifically valuable (trials/studies are core to BrAPI). BrAPI v2.1 already
covers Study/Trial/ObservationUnit; GenX extension must justify what it adds
(block/replication/randomization/treatment assignment). Overlap risk is high —
could duplicate BrAPI. Also depends on D-20-style overlap analysis. Deferred
as reserve/alternative rather than primary.

## 6. RFC-003 as quality benchmark

RFC-003 (Seed-Lot Ledger) demonstrates: explicit domain entities, meaningful
lifecycle, precise quantity semantics (fixed-scale decimal strings), provenance,
conflict/replay, explicit unresolved questions (D-07, D-08, D-20), and honest
treatment of BrAPI overlap. The quality bar: problem statement with BrAPI
comparison, typed properties with units, identifier policy, lifecycle, operations
justified by lifecycle, security, acceptance criteria, fixtures. Do not copy
RFC-003's structure into unrelated domains; use it as a bar.

## 7. Weighted scoring matrix

| Candidate | Sci importance 20% | Gap 20% | Evidence 15% | Testability 15% | Interop 10% | Independent impl 10% | Scope/deps 10% | Weighted total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BreedingPipeline (RFC-154) | 4 | 4 | 3 | 3 | 3 | 3 | 4 | 3.55 |
| RemoteSensingMetadata (RFC-145) | 4 | 4 | 2 | 2 | 3 | 2 | 2 | 2.95 |
| ExperimentalDesign (RFC-018) | 5 | 3 | 3 | 3 | 2 | 3 | 3 | 3.35 |
| SelectionDecisions (RFC-008) | 4 | 4 | 3 | 3 | 3 | 3 | 4 | 3.55 |
| RepeatedMeasurement | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3.00 |

Weights sum to 100%. Scores are 1–5. Weighted total = sum(score × weight).

BreedingPipeline and SelectionDecisions tie at 3.55. BreedingPipeline is chosen
as primary because its decision dependencies are RFC-local and manageable, and
it demonstrates the "ordered process" modelling challenge central to the quality
standard. SelectionDecisions is the reserve because it has no BrAPI v2.1
equivalent (cleaner scope) but slightly less domain-evidence availability.

## 8. Primary recommendation

**Primary pilot: RFC-154 BreedingPipeline.**

Rationale: scientifically meaningful (breeding program advancement), bounded
(1 resource, 3 operations), decision dependencies are RFC-local and do not
force premature resolution of digest/BrAPI-overlap clusters, and it directly
exercises the quality standard's hardest requirement — modelling an ordered
process rather than a descriptive record.

## 9. Reserve recommendation

**Reserve pilot: RFC-008 SelectionDecisions.**

Rationale: no BrAPI v2.1 equivalent (clean interoperability story), bounded
scope, but slightly less domain evidence available today.

## 10. Deferred candidates

- RFC-145 RemoteSensingMetadata: deferred because geospatial standard
  investigation is a prerequisite not yet captured as a decision; high scope-creep
  risk.
- RFC-018 ExperimentalDesign: deferred because BrAPI overlap is high and
  requires D-20-style overlap analysis first.
- RepeatedMeasurement: lower scientific importance score; defer.

## 11. Suggested Phase 1B boundaries (for primary pilot only)

- In scope: domain investigation, terminology, entity model, lifecycle, units,
  provenance, API contract, schema, fixtures, conformance, independent
  implementability review.
- Out of scope: implementation code, new endpoints beyond the 3 already declared,
  changes to other RFCs, resolution of digest/idempotency/security clusters.
- Acceptance: RFC upgraded from STRUCTURAL_DRAFT to SEMANTICALLY_REVIEWED with
  all quality-standard sections populated and falsifiable tests defined.