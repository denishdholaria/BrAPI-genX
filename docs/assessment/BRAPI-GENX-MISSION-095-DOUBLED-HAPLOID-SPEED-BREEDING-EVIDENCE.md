# Mission 095 — Doubled-haploid outcomes and speed-breeding protocol evidence

**Parent:** Mission 094 branch `b3d5eee444038bcdc92acf0af076c5783af08f91`. This is a source-contract interpretation and documentation safeguard, not a modification or approval of normative scientific claims.

## DoubledHaploid (RFC-020, D-57–D-59)

The draft requires `doubledHaploidProgramDbId`, `programDbId` and `method` at registration; the response adds lifecycle `status` including `completed`. Donor Germplasm, induced haploid count, successful doubled count, starting and completion dates, and provenance are **all optional**. No conditional rule links `completed` status to measured offspring, valid counts, ploidy confirmation, observed progeny, an induction denominator, or a traceable chromosome-doubling procedure. Counts are integers without nonnegative constraints.

Official Breeding Application Programming Interface (BrAPI) version 2.1 CrossNewRequest already has `crossType: DOUBLE_HAPLOID` and parent information. That operation is not a complete haploid induction program; however, the candidate must not imply that the official standard cannot represent the related Cross category. The GenX record does not create official Cross, Pedigree or Germplasm evidence.

## SpeedBreeding (RFC-022, D-63–D-65)

Registration requires `speedBreedingProtocolDbId`, raw `programDbId`, and `protocolName`. Light and temperature regimes are optional free text; `photoperiod` (number, hours) and `generationTime` (integer, days) are optional, with no bounds or validation against a crop, environment, generation outcome or photoperiod schedule. Provenance is optional, no actual treatment or measured gain is established, and **no `breedingPipelineDbId` link exists**, contrary to earlier RFC D-64 wording.

Official BrAPI version 2.1 Study already contains `environmentParameters`, `growthFacility`, `culturalPractices`, and `experimentalDesign` metadata; Events describe actual interventions. The GenX draft is a candidate protocol descriptor, not an Event or controlled-environment measurement record.

## Changes, guardrails and verification

- Replaced two title-only GroupDescriptions; corrected both module overviews and RFC-020/RFC-022.
- Pinned the reviewed modules and added source-driven regression assertions for requiredness, missing measurements, actual official overlap, no typed BreedingPipeline link and operation identity.
- **Provisional coverage after Mission 095**: **151/156** source-reviewed descriptions, **5 evidence-deferred**: CrossingSchedule (D-BP-11), ProgenyRecords (D-BP-08), SpatialIndex, SpatialQuery and YieldMap (Mission 090 spatial decision package).
- No official BrAPI source, GenX wire schema, operation identifier, endpoint registry, maturity register or decision state is changed. No independently verified scientific outcomes, conformance or maturity promotion is inferred.

```sh
python Scripts/check_genx_group_descriptions.py
python Scripts/test_genx_group_descriptions.py
python Scripts/report_genx_evidence_coverage.py --check
python Scripts/checkEndpointRegistry.py
python Scripts/auditEndpointRegistrySourceConsistency.py --strict
python Scripts/generateEndpointArtifacts.py --check
python Scripts/checkGenXConformance.py
```

Require hosted static and live-reference conformance plus specification generation on final branch head before integration. A source inspection is not a recorded successful test execution.
