# BrAPI-GenX — Scientific evidence review roadmap, Missions 078–085

**Prepared 2026-11-24.** This is a bounded development plan and not scientific standard ratification. Its starting context is the latest verified `main` of 2026-11-24 (`32de809d52147a1c204da781abae5eea427cc43b`). Missions 074–077 are separately committed to draft, stacked pull requests #24–#27; do not mistake their branch heads for merged `main`.

## Immutable development constraints

- Official Breeding Application Programming Interface (BrAPI) v2.1 schemas and operations remain byte-unchanged.
- Draft GenX operations, paths, operation identifiers, registry records and source semantic neighbors are not altered by evidence-review missions.
- `STRUCTURAL_DRAFT` remains a candidate status; source-linked documentation does not imply scientific or service conformance.
- No deferred scientific decision may be marked accepted by an AI (Artificial Intelligence) agent.
- All changes should have a bounded regression assertion. Source links must be verified. The full applicable test suite must actually execute before merging.
- Hosted Continuous Integration (CI) remains infrastructure-limited by billing; don't bypass branch security requirements or report non-executed tests as passed.
- Don't accumulate unlimited stacked pull requests. Each group of slices must end in a verification/integration checkpoint.

## Mission plan

- [x] **Mission 078 — Kinship, GenomicRelationship, PedigreeAnalysis evidence.** Three matrix/pedigree-related draft modules; preserve the distinction between relatedness estimands, matrix storage metadata, and authoritative germplasm ancestry. Documentation and regression assertions committed to a dedicated branch; **not executed or merged**.
- [ ] **Mission 079 — Population/genomics assumptions.** Inspect `Genotyping/HaplotypeAnalysis`, `Genotyping/ExpressionQtl`, and `Genotyping/MethylationAnalysis` against actual schemas and authoritative official genomics resources. Prioritize phasing, sample context, units and reproducibility; do not infer scientific validity.
- [ ] **Mission 080 — Field phenotyping and environmental context.** Review `Phenotyping/ImageMetadata`, `Phenotyping/PhenologyObservation`, and `Geospatial/VegetationIndex`. Distinguish metadata capture from field-proven observations; examine units, sensor calibration, temporal alignment, and observation identity.
- [ ] **Mission 081 — Breeding decision provenance.** Assess `Breeding/PopulationAdvancement`, `Breeding/SelectionDecisions`, and crossing/lifecycle proposals for distinctions between candidate scores, approved verdicts and actual material movement. Avoid retrofitting verified pipeline decisions into draft resources.
- [ ] **Mission 082 — Environmental and spatial reasoning.** Review `Environment/ExtremeWeather`, `Environment/SoilChemistry`, and `Geospatial/RemoteSensingMetadata` for reference coordinate systems, thresholds, standards, measurement method and data quality.
- [ ] **Mission 083 — Stronger science tests.** Consolidate repeated schema-derived assertions into reusable helpers where this reduces maintenance burden **without weakening mutation sensitivity**. Verify decision references against the governed decision register; preserve existing scientific boundary checks.
- [ ] **Mission 084 — Local integration assurance.** Execute the full modified Python test suite, group-description checker, registry/source consistency, generated catalogue reproducibility, source standards overlap, reference-server conformance, and any affected cross-language digest tests on the final stacked branch. Record exact commands and failure evidence.
- [ ] **Mission 085 — Merge and baseline closure.** Only after actual verification, merge the stacked PR sequence through normal repository policy, retargeting each dependent PR to `main`. Record resulting merge hashes, module counts and irreversible decisions. Do not bypass branch protection or change billing.

## Evidence categories and acceptance standard

For each reviewed module, record (1) **what the current schema requires**, (2) what is optional or unmodelled, (3) authoritative official BrAPI overlap where applicable, (4) scientific interpretation limits, (5) source-local evidence and open decision references, and (6) a regression assertion tied to actual source properties.

A retained numerical field, matrix URI (Uniform Resource Identifier), object map or identifier string is **not** evidence of population validity, calibrated statistics, referential integrity, security enforcement or deployed persistence.

## Current review coverage

At the starting `main` baseline, 113 of 156 registered groups had protected evidence-reviewed descriptions. Draft Missions 074–077 add eight groups (121/156). Draft Mission 078 adds three more (124/156), with **32 groups still deferred**, subject to successful verification and integration. These figures are documentation evidence coverage, *not* completed scientific specification maturity.
