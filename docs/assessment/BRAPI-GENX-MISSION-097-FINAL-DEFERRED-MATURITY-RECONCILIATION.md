# Mission 097 — Deferred modules, scientific maturity and governance closure

**Baseline:** Mission 096 branch `9202549a98e8a7d930bc40a23e892825f28871b9`, stacked through Missions 093–096 on integrated Mission 092. **Nature:** read-only source-backed status reconciliation; not a proposal for automatic normative promotion, an implementation of missing capabilities or ratification of open decisions.

## Reviewed-description inventory

On the proposed cumulative branch there are **156** GenX modules with `GroupDescription.md` files. **151** have documented, source-backed candidate descriptions and **5** remain evidence-deferred. This inventory can be independently computed by `python Scripts/report_genx_evidence_coverage.py --json`. The coverage guard protects the reviewed set; evidence review is **not** a scientific maturity status, deployed behavior, or interoperability certification.

| Still evidence-deferred | Request for Comments (RFC) status | Authority / reason for deferral |
| --- | --- | --- |
| `Breeding/CrossingSchedule` | RFC-037 **DEFERRED** | Approved D-BP-11: official BrAPI PlannedCross/CrossingProject owns mating intent; revisit only real calendar/resource conflict or booking semantics |
| `Breeding/ProgenyRecords` | RFC-019 **DEFERRED** | Approved D-BP-08: official BrAPI Pedigree and Cross own parentage; revisit only distinct formation/family/cohort events with proven nonduplication |
| `Geospatial/SpatialIndex` | RFC-141 **STRUCTURAL_DRAFT** | Unratified G-090-1 (metadata descriptor versus executable indexing or continued deferral) |
| `Geospatial/SpatialQuery` | RFC-143 **STRUCTURAL_DRAFT** | Unratified G-090-2 (saved description versus executable, authorized query job or continued deferral) |
| `Geospatial/YieldMap` | RFC-070 **STRUCTURAL_DRAFT** | Unratified G-090-3 (optional metadata versus published byte/digest integrity lifecycle or continued deferral) |

The latter three have title-only GroupDescriptions **by deliberate governance preflight** and retain source-backed assessments in Missions 090/096, not an implied production-ready capability. They may be reviewed and promoted only after the relevant evidence and decision approval are recorded. D-BP-08/11 are **already approved decisions to defer**, not unratified decisions; the proposed features themselves remain deferred.

## Recently evidence-reviewed but not promoted

The seven scientific modules reviewed in Missions 093–095 remain **STRUCTURAL_DRAFT** in the maturity register:
`ExperimentalDesign` (RFC-018), `ExperimentalProtocol` (RFC-117), `TreatmentAssignment` (RFC-106), `ParentCandidateSelection` (RFC-028), `SelectionDecisions` (RFC-008), `DoubledHaploid` (RFC-020) and `SpeedBreeding` (RFC-022).

Their enriched documentation pinpoints source limitations: design/official Study overlap; optional protocol and treatment data; incompatible Boolean and enumerated selection verdicts; absent decision authority and scientific evidence; unverified haploid chromosome doubling; and unvalidated acceleration regimes. A source-backed description is **not** a normative contract or proof of scientific reproducibility.

## Remaining maintainer actions, not automatically approved

- **SpatialIndex:** decide metadata-only, separately specified executable service, or deferral; require dataset identity and coordinate reference/authority if executable.
- **SpatialQuery:** decide saved descriptor, independently testable query execution with strict geometry, target dataset, authorization, result contract, or deferral.
- **YieldMap:** decide optional metadata, formally defined published asset with required URI/digest, coordinate reference, units, content verification and lifecycle, or deferral.
- **CrossingSchedule and ProgenyRecords:** preserve D-BP-11 and D-BP-08 respectively unless a genuinely distinct, evidence-backed interoperability use case justifies an explicit new maintainer decision.
- **Scientific maturity:** require the specification quality and interoperability conformance gates separately from successful hosted static/live-reference generation. Source and reference-server checks cannot establish behavior of an independent implementation.

**No decisions are granted by this assessment.** Do not modify official BrAPI version 2.1 contracts or GenX wire schemas to increase documentation completion statistics.

## Verification and change boundary

- Added a repository-grounded regression asserting the exact five pending modules, distinguishing RFC **DEFERRED** from **STRUCTURAL_DRAFT**, and ensuring seven newly documented modules were not silently promoted.
- Confirm through the hosted static-conformance, live-reference-conformance and specification-generation workflows on the final pull-request commit. Keep the branch stacked until dependencies are integrated.
- No official source, GenX route/operation/schema, endpoint registry or maturity register edited in this mission.

```sh
python Scripts/report_genx_evidence_coverage.py --json
python Scripts/test_genx_evidence_coverage.py
python Scripts/check_genx_group_descriptions.py
python Scripts/generateEndpointArtifacts.py --check
python Scripts/checkGenXConformance.py
```

**Proposed result:** 151/156 source-reviewed, 5 evidence-deferred, 0 newly ratified spatial decisions and 0 newly promoted scientific RFCs, subject to hosted verification and integration.
