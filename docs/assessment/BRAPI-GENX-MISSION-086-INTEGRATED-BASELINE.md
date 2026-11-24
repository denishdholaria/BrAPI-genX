# Mission 086 — Post-integration baseline and remaining evidence queue

**Date:** 2026-11-24  
**Starting main:** `32de809d52147a1c204da781abae5eea427cc43b` (Mission 073).  
**Integrated main:** `8295c1763294be8f598cf7ddcc2f99f936f5a39c` (Mission 084B).  
**Scope:** audit/record only. This mission does not change an official BrAPI (Breeding Application Programming Interface) 2.1 contract, GenX endpoint, schema, registry, maturity register or governance decision.

## Sequential GitHub integration ledger

All twelve former draft pull requests were retargeted to `main`, marked ready only after verification, and merged using the normal GitHub merge-commit method with an expected source-head commit. No branch was force-pushed; no branch-protection rule was bypassed.

| Pull request | Mission | Merge commit |
| --- | --- | --- |
| [#24](https://github.com/denishdholaria/BrAPI-genX/pull/24) | 074 | `546affa8e093b01b7bb81d91240cbef0cfe4b6cb` |
| [#25](https://github.com/denishdholaria/BrAPI-genX/pull/25) | 075 | `db40c72b86ab68fe00db1a16aac39b245e54407c` |
| [#26](https://github.com/denishdholaria/BrAPI-genX/pull/26) | 076 | `cfb2ee189c3ec92b0d68bc391411e4afd5668b9e` |
| [#27](https://github.com/denishdholaria/BrAPI-genX/pull/27) | 077 | `9b2585d67a4ed5eabdc8c5ac2bc5697e9fa7d794` |
| [#28](https://github.com/denishdholaria/BrAPI-genX/pull/28) | 078 | `557c1bf351a3b8fa5cba653abc3702aa34f9f37b` |
| [#29](https://github.com/denishdholaria/BrAPI-genX/pull/29) | 079 | `af542169b8be970f4f669eb3c2496aca6fbca9a5` |
| [#30](https://github.com/denishdholaria/BrAPI-genX/pull/30) | 080 | `7b877ac6e652495549dbbca0662d4da7e832a45a` |
| [#31](https://github.com/denishdholaria/BrAPI-genX/pull/31) | 081 | `d6b057b2bbcf66b6a04f88c5777f16bde56734d7` |
| [#32](https://github.com/denishdholaria/BrAPI-genX/pull/32) | 082 | `fbe3c9dacc8c7c1d7dbdff10b6d2ada161fa2044` |
| [#33](https://github.com/denishdholaria/BrAPI-genX/pull/33) | 083 | `320302ce1b0a8c868b25c9eda055892ba7a0d1b5` |
| [#34](https://github.com/denishdholaria/BrAPI-genX/pull/34) | 084 | `15eeee2621963ff3839e3e1bc8b5ea8a67874e9b` |
| [#35](https://github.com/denishdholaria/BrAPI-genX/pull/35) | 084B | `8295c1763294be8f598cf7ddcc2f99f936f5a39c` |

## Evidence and remaining gate

- The final pre-integration [conformance run 45433889545](https://github.com/denishdholaria/BrAPI-genX/actions/runs/45433889545) passed both hosted static and live-reference jobs. [Generation run 45433851270](https://github.com/denishdholaria/BrAPI-genX/actions/runs/45433851270) passed its check and generation jobs.
- Original ancestor failures in #30–#34 were traced to a missing `D-93` ImageMetadata description reference and a workflow regression mismatch (`--strict` versus `--strict --require-coverage`). Both corrections were backported to their origin branches and subsequently verified with green hosted checks.
- A GitHub source/tree comparison of the entire development stack before integration found only Markdown source descriptions/assessments, Python assurance scripts and a workflow YAML (YAML Ain't Markup Language) file changed; no official version 2.1 wire contract, GenX wire schema or endpoint registry was modified.
- The final integrated `main` was checked at `8295c176`: the three deferred ImageMetadata decisions and the full route-coverage regression assertion are present. The immediately subsequent `main` build workflow was in progress when this document was prepared. Do not conflate green pre-integration branch checks with a completed final `main` build or final `main` static run.

## Evidence-review inventory

The repository has **156** GenX `GroupDescription.md` modules. **135** are protected as source-backed *documentation review*, and **21** are **evidence-deferred**. These numbers are not counts of scientifically validated contracts, conformant server implementations, approved scientific relationships, or production-ready endpoints.

The **21 deferred modules** on the integrated baseline are:

- Breeding (9): `CrossingSchedule`, `DoubledHaploid`, `ExperimentalDesign`, `ExperimentalProtocol`, `ParentCandidateSelection`, `ProgenyRecords`, `SelectionDecisions`, `SpeedBreeding`, `TreatmentAssignment`.
- Environment (3): `CarbonStock`, `Emissions`, `EnvironmentalTreatment`.
- Geospatial (5): `CloudMask`, `RasterCatalogue`, `SpatialIndex`, `SpatialQuery`, `YieldMap`.
- Interoperability (1): `BiodiversityExport`.
- Phenotyping (1): `BulkCapture`.
- ReferenceData (2): `Calendar`, `DevelopmentalStage`.

**Hold decisions:** `Breeding/CrossingSchedule` remains explicitly deferred under D-BP-11 and `Breeding/ProgenyRecords` under D-BP-08. A reviewed description must never silently reopen these decisions or imply promotion from `STRUCTURAL_DRAFT`.

## Next bounded slices

- **Mission 087:** source-grounded, scientifically conservative review of `ReferenceData/Calendar` and `ReferenceData/DevelopmentalStage`. Investigate overlaps with official `Season` and `ObservationVariable`; correct unsupported link/standardization claims, preserve deferred decisions, add schema-derived regressions. Target 137/156 reviewed descriptions only after tests.
- **Mission 088:** inspect `Geospatial/CloudMask` and `Geospatial/RasterCatalogue` as optional metadata, not evidence of raster pixels, reflectance, quality assurance or calibration; explicitly consider imagery source and coordinate system.
- **Mission 089:** review `Phenotyping/BulkCapture` against official Observation and existing GenX CaptureWorkflow; do not infer atomicity, validated batching or instrument calibration.
- **Mission 090:** prepare remaining unresolved research/official-overlap issues for maintainer decision; maintain evidence-deferred status where source models are insufficient.

## Reproducible verification commands

```sh
python Scripts/check_genx_group_descriptions.py
python Scripts/report_genx_evidence_coverage.py --check
python Scripts/test_genx_group_descriptions.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/audit_genx_readme_routes.py --module Geospatial/VegetationIndex --strict --require-coverage
python Scripts/test_genx_readme_routes.py
python Scripts/checkEndpointRegistry.py
python Scripts/auditEndpointRegistrySourceConsistency.py --strict
python Scripts/generateEndpointArtifacts.py --check
python Scripts/checkGenXConformance.py
```

**Acceptance:** complete hosted static and live reference conformance, reproducible generated catalogue, unchanged official-source/wire contract diff, explicit source links, and no unapproved scientific maturity or relationship transitions.
