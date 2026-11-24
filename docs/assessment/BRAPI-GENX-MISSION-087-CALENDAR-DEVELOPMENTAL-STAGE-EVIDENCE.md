# Mission 087 — Calendar and developmental-stage source evidence

**Base:** `8295c1763294be8f598cf7ddcc2f99f936f5a39c` (Mission 084B integrated `main`).  
**Scope:** evidence review and regression test only. No official BrAPI (Breeding Application Programming Interface) v2.1 sources, GenX wire schemas, endpoint registry, operation identity, accepted decisions or maturity statuses changed.

## Independently verified source boundaries

### ReferenceData/Calendar (RFC-091, D-271–D-273)

- Current `CalendarNewRequest` requires **only** `calendarDbId`. The response adds `status` as required.
- `name`, `convention`, `supersedes` and `provenance` are optional. A free-form convention such as `ISO-8601` is not proof of a valid time-system implementation.
- **Contradiction corrected:** the RFC previously claimed a reference to BrAPI `Study`, but neither request nor response contains `studyDbId`.
- **Standards overlap qualified:** the official BrAPI Core `Season` schema already provides `seasonDbId`, optional `seasonName` and `year`. GenX Calendar does not contain `seasonDbId` or a verified mapping to an official Season. The proposal cannot be advertised as addressing a wholly absent official time/season domain.
- No timezone/locale, calendar-system code, start/end validity interval, authoritative Study join, or time-conversion correctness can be inferred.

### ReferenceData/DevelopmentalStage (RFC-079, D-235–D-237)

- Current `DevelopmentalStageNewRequest` requires **only** `developmentalStageDbId`; response additionally requires `status`.
- `cropDbId`, `stageCode`, `stageName`, `definition`, `supersedes` and `provenance` are optional. `stageCode` is free-form. A `BBCH-31` example is not a controlled crop-specific vocabulary or independent scientific validation.
- Official BrAPI `ObservationVariable` already describes a Trait–Method–Scale observational context; no dedicated `DevelopmentalStage` resource appears in the checked official source. It is misleading to imply that official BrAPI cannot represent phenology at all.
- The optional `cropDbId` string does not establish an authority-matched Germplasm relationship; neither official `observationVariableDbId` nor GenX `variableDbId` is modelled.

## Changes and assurance

1. Replaced two title-only `GroupDescription.md` placeholders with `STRUCTURAL_DRAFT`, source-linked, limitations-aware descriptions.
2. Qualified the two module overviews and their RFCs, correcting the unsupported Calendar→Study claim and overbroad assertions about official standardization.
3. Expanded the protected description inventory from **135/156** to **137/156**, leaving **19 evidence-deferred** if hosted checks pass.
4. Added `test_calendar_and_developmental_stage_source_boundaries` to pin exact request/response required fields, optional scientific parameters, absent relationship properties, status enum, existing official `Season`/ObservationVariable semantics, and corrected RFC source claims.

**Not done:** approving any deferred decisions, creating `studyDbId`, defining a universal crop stage scale, enforcing BrAPI joins, validating calendars, or claiming production implementation/conformance.

## Verification required

```sh
python Scripts/check_genx_group_descriptions.py
python Scripts/test_genx_group_descriptions.py
python Scripts/report_genx_evidence_coverage.py --check
python Scripts/checkGenXConformance.py
python Scripts/checkEndpointRegistry.py
python Scripts/auditEndpointRegistrySourceConsistency.py --strict
python Scripts/generateEndpointArtifacts.py --check
```

Full GitHub-hosted static and live conformance must pass before merging. A source inspection and GitHub tree audit are not equivalent to executed tests.

**Status:** draft evidence changes committed, hosted verification pending at authoring time.
