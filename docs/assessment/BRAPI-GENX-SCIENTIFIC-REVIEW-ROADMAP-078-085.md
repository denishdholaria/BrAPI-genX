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
- [x] **Mission 079 — Population/genomics assumptions.** Reviewed `Genotyping/HaplotypeAnalysis`, `Genotyping/ExpressionQtl`, and `Genotyping/MethylationAnalysis` against actual response/request schemas. Source-linked draft evidence and regression assertions written. **Tests not executed; not merged; scientific validity not inferred.**
- [x] **Mission 080 — Field phenotyping and environmental context.** Source-reviewed `Phenotyping/ImageMetadata`, `Phenotyping/PhenologyObservation`, and `Geospatial/VegetationIndex`. Corrected official BrAPI image-metadata overlap claim and singular-vs-plural VegetationIndex README route; added guarded source-backed descriptions and test assertions. **Tests not yet executed; draft only.**
- [x] **Mission 081 — Breeding decision provenance.** Reviewed `Breeding/PopulationAdvancement` and `Breeding/CandidateVarietyLifecycle` against exact source contracts and existing SelectionDecision. Preserved the accepted D-BP-10 actual-event distinction and **did not revive CrossingSchedule (DEFERRED D-BP-11)**. Added review documents and regression assertions. **Tests not executed; no maturity promotion.**
- [x] **Mission 082 — Environmental and spatial reasoning.** Reviewed ExtremeWeather, SoilChemistry and RemoteSensingMetadata against authoritative schemas, corrected claims of required links/measurements in their RFCs, and added guarded source evidence plus tests. **Not executed or merged; no scientific maturity promotion.**
- [x] **Mission 083 — README endpoint identity assurance.** Found that comprehensive contract checks did not verify human-readable README endpoint identities. Implemented report-first audit with a scoped strict vegetation-index gate, seven locally passed synthetic mutation tests, and workflow-scope safeguards. **Full repository suite not executed; draft only.** Keep shared schema-test refactors for a later separate mission if they can be justified without weakening assertions.
- [ ] **Mission 084 — Local integration assurance.** Execute the full modified Python test suite, group-description checker, registry/source consistency, generated catalogue reproducibility, source standards overlap, reference-server conformance, and any affected cross-language digest tests on the final stacked branch. Record exact commands and failure evidence.
- [ ] **Mission 085 — Merge and baseline closure.** Only after actual verification, merge the stacked PR sequence through normal repository policy, retargeting each dependent PR to `main`. Record resulting merge hashes, module counts and irreversible decisions. Do not bypass branch protection or change billing.

## Evidence categories and acceptance standard

For each reviewed module, record (1) **what the current schema requires**, (2) what is optional or unmodelled, (3) authoritative official BrAPI overlap where applicable, (4) scientific interpretation limits, (5) source-local evidence and open decision references, and (6) a regression assertion tied to actual source properties.

A retained numerical field, matrix URI (Uniform Resource Identifier), object map or identifier string is **not** evidence of population validity, calibrated statistics, referential integrity, security enforcement or deployed persistence.

## Draft Mission 079 checkpoint

Mission 079 adds three evidence-reviewed descriptions to the preceding 124, yielding **127 of 156** guarded modules and **29 deferred** on the stacked development branch only. This coverage is not reflected on `main` until reviewed and merged.

## Draft Mission 080 checkpoint

Mission 080 adds three reviewed descriptions to the preceding 127 for **130 of 156** guarded modules (**26 remain deferred**) on the stacked branch only. This is draft documentation coverage, not scientific validation or merged `main` state.

## Draft Mission 081 checkpoint

Mission 081 adds two reviewed group descriptions to the preceding 130, for **132 of 156** guarded modules and **24 deferred** on the unmerged stacked branch only. CrossingSchedule's explicit DEFERRED status remains untouched.

## Draft Mission 082 checkpoint

Mission 082 adds three reviewed descriptions to the preceding 132 for **135 of 156** evidence-reviewed modules (**21 deferred**) on the unmerged development stack only. These records are not meteorological certifications, validated soil tests, or calibrated geospatial observations.

## Draft Mission 083 assurance checkpoint

The reported 135/156 documentation-review count is unchanged. Mission 083 adds a new **source/README identity** control, not scientific maturity or additional reviewed groups. Only a previously reconciled VegetationIndex README is subject to a strict scope gate. Synthetic mutation tests passed; the full stacked branch still requires local integration assurance.

## Current review coverage

At the starting `main` baseline, 113 of 156 registered groups had protected evidence-reviewed descriptions. Draft Missions 074–077 add eight groups (121/156). Draft Mission 078 adds three more (124/156), with **32 groups still deferred**, subject to successful verification and integration. These figures are documentation evidence coverage, *not* completed scientific specification maturity.
