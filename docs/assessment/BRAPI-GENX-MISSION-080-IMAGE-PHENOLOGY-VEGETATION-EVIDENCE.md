# Mission 080 — Image metadata, phenology and vegetation-index evidence

**Parent:** `e7272923408491a957e5bd0d5fbec250e290308d` (Mission 079 branch), 2026-11-24.  
**Scope:** three previously title-only draft module descriptions, README/RFC (Request for Comments) corrections and schema-derived safeguards. Official Breeding Application Programming Interface (BrAPI) version 2.1 source contracts, GenX wire schemas, operation identifiers and registry remain unchanged.

## Verified source findings

1. **ImageMetadata** (RFC-032, D-93–D-95) requires `imageMetadataDbId`, `imageDbId`, and `capturedAt` in registration, plus `status` in the response. `camera`, `resolution`, study/observation-unit links and provenance are optional. `resolution` is plain text. The earlier RFC incorrectly claimed that official BrAPI version 2.1 does not standardize image metadata. In fact, official `ImageNewRequest` already defines `imageTimeStamp`, `imageWidth`, `imageHeight`, `imageLocation`, `observationUnitDbId` and `additionalInfo`. The GenX record remains a **separate** draft lifecycle, not an authoritative replacement or automatically synchronized representation. D-94's proposed PhenotypeCapture link is not modelled.
2. **PhenologyObservation** (RFC-027, D-78–D-80) requires study/observation-unit identifiers, timestamp and a free-text stage. `bbchCode` is optional, without a schema-enforced stage code list, species-specific scale, measurement validity or observation-variable equivalence. Official BrAPI Observations remain authoritative and can represent phenology through appropriate observation variables; this draft has its own separate event identity. D-79's MeasurementSeries link is not modelled.
3. **VegetationIndex** (RFC-146, D-436–D-438) requires **only** the record identifier in registration. Index type/name, acquisition date, coordinate reference, resolution and provenance are optional. No numeric vegetation index, raster identifier, sensor-band mapping or index-computation formula is modelled. Its authoritative source is `/vegetation-indexes` with operation `genxListVegetationIndexes`; the old README incorrectly used singular `/vegetation-index` / `genxListVegetationIndex`. The README is corrected **without changing source operations**.

## Assurance work

- Source-linked `STRUCTURAL_DRAFT` GroupDescriptions for these three modules.
- README and RFC corrections where statements exceeded actually modelled evidence or contradicted the source wire contract.
- Reviewed-description guard expanded to **130 of 156**, with **26 deferred** on the full stacked branch.
- Schema-driven assertions pin exact required sets, optional sensor and growth-stage fields, official image overlap, non-structured vegetation metadata, and the actual vegetation-index operations.

## Verification and limitations

Before integrating, execute the group-description tests/guard, official/source-registry consistency checks, generator reproducibility and applicable static/live conformance tests. Remote GitHub source inspection and link resolution do not substitute for actual Python test execution.

No phenotypic validity, vegetation calibration, genotype comparability, or official BrAPI equivalence is ratified.
