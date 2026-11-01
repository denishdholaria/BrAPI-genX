# BrAPI-GenX (proposal)

Next-generation BrAPI design surface. **Proposal status: not accepted, not normative.**

- V2.1 (`BrAPI-Core`, `BrAPI-Phenotyping`, `BrAPI-Genotyping`, `BrAPI-Germplasm`)
  stays frozen. Nothing in this directory changes V2.1 behavior.
- GenX objects are **additive and optional**: a V2.1 client must keep working
  against a GenX server, and a GenX client must tolerate a server that does not
  implement a GenX object.
- Start point: [RFC-001-GenX-Skeleton](./RFC-001-GenX-Skeleton.md) — principles,
  compatibility law, and the first three objects.
- Wiring into `generator/` and `BrAPI-Schema/` (built `Generated/` artifacts) is
  deferred as `requires decision` in the RFC. This directory is inert to the
  V2.1 build until that decision is taken.
- **Classification proposal:** [CLASSIFICATION.md](./CLASSIFICATION.md) defines
  a scientific domain taxonomy distinct from cross-cutting contract capabilities.
  [Conformance/domain-classification.yaml](./Conformance/domain-classification.yaml)
  provides the proposed machine-readable module registry. Both are proposals,
  not BrAPI community ratification.
- **Endpoint inventory:** [Inventory/](./Inventory/) contains a generated, reviewable
  mapping of ~1,849 legacy Bijmantra endpoints to the proposed D1–D7 / C* classes
  (see `Inventory/README.md`), to help plan which next-generation specs to author.
- **Master endpoint registry:** [../ENDPOINT-REGISTRY.json](../ENDPOINT-REGISTRY.json) contains 201 released BrAPI v2.1 operations and 21 proposed GenX operations with stable BrAPI-GenX catalogue identifiers, source links, semantic metadata, and implementation-evidence status. The generated human catalogue is [../ENDPOINT-CATALOG.md](../ENDPOINT-CATALOG.md), with the source crosswalk in [../BIJMANTRA-CROSSWALK.md](../BIJMANTRA-CROSSWALK.md).
- The GenX-only generated view is [GENX-ENDPOINT-CATALOG.md](./GENX-ENDPOINT-CATALOG.md); it is a filtered view, not a second source of truth.
- **Endpoint semantics and catalogue:** [GENX-ENDPOINT-CATALOG.md](./GENX-ENDPOINT-CATALOG.md) is the generated GenX-only view. The complete all-generation catalogue is [../ENDPOINT-CATALOG.md](../ENDPOINT-CATALOG.md), with canonical structured records in [../ENDPOINT-REGISTRY.json](../ENDPOINT-REGISTRY.json). Each proposed GenX operation carries `x-brapi-genx` metadata beside its OpenAPI contract; `Scripts/checkGenXEndpointCatalog.py` checks metadata and focused-catalogue coverage.

## Objects

| Directory | Object | Kind |
|---|---|---|
| `Provenance/` | `ProvenanceEnvelope` — method/algorithm version, inputs digest, assumptions, uncertainty, evidence links | Embedded schema, no endpoints |
| `Jobs/` | `Job` — async execution with idempotency key, status, cancel | `GET /genx/v1/jobs` (`genxListJobs`); `POST /genx/v1/jobs` (`genxSubmitAsyncJob`); `GET /genx/v1/jobs/{jobDbId}` (`genxGetAsyncJobById`); `DELETE /genx/v1/jobs/{jobDbId}` (`genxRequestAsyncJobCancellation`) |
| `ServerInfoV3/` | `ServerInfoV3` — capability negotiation under `/genx/v1` | `GET /genx/v1/serverinfo` (`genxGetServerInfoV3`) |
| `VariableTerms/` | `VariableTerm` — versioned, namespaced observation-variable terms; conflicts rejected | `GET /genx/v1/variable-terms` (`genxListVariableTermVersions`); `POST /genx/v1/variable-terms` (`genxPublishVariableTermVersion`); `GET /genx/v1/variable-terms/{variableDbId}` (`genxGetVariableTermVersion`) |
| `LotLedger/` | `LotLedgerEntry` — append-only, idempotent lot movements | `GET /genx/v1/seedlots/{seedLotDbId}/ledger` (`genxListSeedLotLedgerEntries`); `POST /genx/v1/seedlots/{seedLotDbId}/ledger` (`genxAppendSeedLotLedgerEntry`) |
| `Models/` | `ModelArtifact` — registered models; inference binds by digest | `GET /genx/v1/models` (`genxListModelVersions`); `POST /genx/v1/models` (`genxRegisterModelVersion`); `GET /genx/v1/models/{modelDbId}` (`genxGetModelVersion`); execute inference through `POST /genx/v1/jobs` (`genxSubmitAsyncJob`) with a declared inference `jobType` |
| `Genomics/` | `VariantMatrix` — content-addressed matrix references | `GET /genx/v1/variantmatrices` (`genxListVariantMatrixReferences`); `POST /genx/v1/variantmatrices` (`genxRegisterVariantMatrixReference`); `GET /genx/v1/variantmatrices/{matrixDbId}` (`genxGetVariantMatrixReference`) |
| `SelectionDecisions/` | `SelectionDecision` — breeding selection verdicts (selected/rejected/deferred/advanced) | `GET /genx/v1/selection-decisions` (`genxListSelectionDecisions`); `POST /genx/v1/selection-decisions` (`genxRecordSelectionDecision`); `GET /genx/v1/selection-decisions/{selectionDecisionDbId}` (`genxGetSelectionDecision`) |
| `BreedingPipeline/` | `BreedingPipeline` — breeding pipeline definitions with ordered stage gates | `GET /genx/v1/breeding-pipelines` (`genxListBreedingPipelines`); `POST /genx/v1/breeding-pipelines` (`genxRegisterBreedingPipeline`); `GET /genx/v1/breeding-pipelines/{breedingPipelineDbId}` (`genxGetBreedingPipeline`) |
| `ExperimentalDesign/` | `ExperimentalDesign` — trial layout, replication, randomization, and treatment assignment | `GET /genx/v1/experimental-designs` (`genxListExperimentalDesigns`); `POST /genx/v1/experimental-designs` (`genxRegisterExperimentalDesign`); `GET /genx/v1/experimental-designs/{experimentalDesignDbId}` (`genxGetExperimentalDesign`) |
| `ProgenyRecords/` | `ProgenyRecord` — progeny/family links with parents, generation, and provenance | `GET /genx/v1/progeny-records` (`genxListProgenyRecords`); `POST /genx/v1/progeny-records` (`genxRecordProgeny`); `GET /genx/v1/progeny-records/{progenyRecordDbId}` (`genxGetProgenyRecord`) |
| `DoubledHaploid/` | `DoubledHaploidProgram` — doubled haploid program records (method, donor, counts, provenance) | `GET /genx/v1/doubled-haploid-programs` (`genxListDoubledHaploidPrograms`); `POST /genx/v1/doubled-haploid-programs` (`genxRegisterDoubledHaploidProgram`); `GET /genx/v1/doubled-haploid-programs/{doubledHaploidProgramDbId}` (`genxGetDoubledHaploidProgram`) |
| `ViabilityTesting/` | `ViabilityTest` — viability/germination test records (results, method, provenance) | `GET /genx/v1/viability-tests` (`genxListViabilityTests`); `POST /genx/v1/viability-tests` (`genxRecordViabilityTest`); `GET /genx/v1/viability-tests/{viabilityTestDbId}` (`genxGetViabilityTest`) |
| `SpeedBreeding/` | `SpeedBreedingProtocol` — speed breeding protocol records (conditions, generation time, provenance) | `GET /genx/v1/speed-breeding-protocols` (`genxListSpeedBreedingProtocols`); `POST /genx/v1/speed-breeding-protocols` (`genxRegisterSpeedBreedingProtocol`); `GET /genx/v1/speed-breeding-protocols/{speedBreedingProtocolDbId}` (`genxGetSpeedBreedingProtocol`) |
| `SoilProfile/` | `SoilProfile` — soil profile records (texture, chemistry, moisture, nutrients, provenance) | `GET /genx/v1/soil-profiles` (`genxListSoilProfiles`); `POST /genx/v1/soil-profiles` (`genxRegisterSoilProfile`); `GET /genx/v1/soil-profiles/{soilProfileDbId}` (`genxGetSoilProfile`) |
| `IrrigationOperation/` | `IrrigationEvent` — irrigation event records (volume, duration, method, provenance) | `GET /genx/v1/irrigation-operations` (`genxListIrrigations`); `POST /genx/v1/irrigation-operations` (`genxRecordIrrigation`); `GET /genx/v1/irrigation-operations/{irrigationEventDbId}` (`genxGetIrrigation`) |
| `RepeatedMeasurement/` | `MeasurementSeries` — repeated measurement series (time-ordered values, quality flags, provenance) | `GET /genx/v1/repeated-measurements` (`genxListMeasurementSeries`); `POST /genx/v1/repeated-measurements` (`genxRecordMeasurementSeries`); `GET /genx/v1/repeated-measurements/{measurementSeriesDbId}` (`genxGetMeasurementSeries`) |
| `FertilizerApplication/` | `FertilizerApplication` — fertilizer application records (product, quantity, method, provenance) | `GET /genx/v1/fertilizer-applications` (`genxListFertilizerApplications`); `POST /genx/v1/fertilizer-applications` (`genxRecordFertilizerApplication`); `GET /genx/v1/fertilizer-applications/{fertilizerApplicationDbId}` (`genxGetFertilizerApplication`) |
| `CropCycle/` | `CropCycle` — crop cycle records (planting/harvest dates, crop, provenance) | `GET /genx/v1/crop-cycles` (`genxListCropCycles`); `POST /genx/v1/crop-cycles` (`genxRegisterCropCycle`); `GET /genx/v1/crop-cycles/{cropCycleDbId}` (`genxGetCropCycle`) |
| `Quarantine/` | `QuarantineRecord` — quarantine records (reason, status, release, provenance) | `GET /genx/v1/quarantine-records` (`genxListQuarantineRecords`); `POST /genx/v1/quarantine-records` (`genxRecordQuarantine`); `GET /genx/v1/quarantine-records/{quarantineRecordDbId}` (`genxGetQuarantineRecord`) |
| `WeatherForecast/` | `WeatherForecast` — weather forecast records (predicted conditions, validity window, provenance) | `GET /genx/v1/weather-forecasts` (`genxListWeatherForecasts`); `POST /genx/v1/weather-forecasts` (`genxRegisterWeatherForecast`); `GET /genx/v1/weather-forecasts/{weatherForecastDbId}` (`genxGetWeatherForecast`) |
| `ImageMetadata/` | `ImageMetadata` — image metadata records (capture details, camera, resolution, provenance) | `GET /genx/v1/image-metadata` (`genxListImageMetadata`); `POST /genx/v1/image-metadata` (`genxRegisterImageMetadata`); `GET /genx/v1/image-metadata/{imageMetadataDbId}` (`genxGetImageMetadata`) |
| `ClimateNormals/` | `ClimateNormal` — climate normal records (mean/min/max, period, provenance) | `GET /genx/v1/climate-normals` (`genxListClimateNormals`); `POST /genx/v1/climate-normals` (`genxRegisterClimateNormal`); `GET /genx/v1/climate-normals/{climateNormalDbId}` (`genxGetClimateNormal`) |
| `PhenologyObservation/` | `PhenologyObservation` — phenology observation records (stage, BBCH code, provenance) | `GET /genx/v1/phenology-observations` (`genxListPhenologyObservations`); `POST /genx/v1/phenology-observations` (`genxRecordPhenologyObservation`); `GET /genx/v1/phenology-observations/{phenologyObservationDbId}` (`genxGetPhenologyObservation`) |
| `ParentCandidateSelection/` | `ParentCandidateSelection` — parent candidate selection records (criterion, outcome, provenance) | `GET /genx/v1/parent-candidate-selections` (`genxListParentCandidateSelections`); `POST /genx/v1/parent-candidate-selections` (`genxRecordParentCandidateSelection`); `GET /genx/v1/parent-candidate-selections/{parentCandidateSelectionDbId}` (`genxGetParentCandidateSelection`) |
| `AnalysisMethods/` | `AnalysisMethod` — versioned analysis method registry (identity, type, contracts, lifecycle) | `GET /genx/v1/analysis-methods` (`genxListAnalysisMethods`); `POST /genx/v1/analysis-methods` (`genxRegisterAnalysisMethod`); `GET /genx/v1/analysis-methods/{analysisMethodDbId}` (`genxGetAnalysisMethod`) |
| `WeatherObservations/` | `WeatherObservation` — environmental/weather observation records (measurements, quality, provenance) | `GET /genx/v1/weather-observations` (`genxListWeatherObservations`); `POST /genx/v1/weather-observations` (`genxRecordWeatherObservation`); `GET /genx/v1/weather-observations/{weatherObservationDbId}` (`genxGetWeatherObservation`) |
| `HarvestRecords/` | `HarvestRecord` — harvest-event records (quantity, quality, moisture, provenance) | `GET /genx/v1/harvest-records` (`genxListHarvestRecords`); `POST /genx/v1/harvest-records` (`genxRecordHarvest`); `GET /genx/v1/harvest-records/{harvestRecordDbId}` (`genxGetHarvestRecord`) |
| `PhenotypeCapture/` | `PhenotypeCapture` — phenotype capture events (entries, quality flags, missingness, corrections, image linkage) | `GET /genx/v1/phenotype-captures` (`genxListPhenotypeCaptures`); `POST /genx/v1/phenotype-captures` (`genxRecordPhenotypeCapture`); `GET /genx/v1/phenotype-captures/{phenotypeCaptureDbId}` (`genxGetPhenotypeCapture`) |
| `GenomicDatasets/` | `GenomicDataset` — prepared genomic dataset records (reference assembly, pipeline provenance, access policy, release status) | `GET /genx/v1/genomic-datasets` (`genxListGenomicDatasets`); `POST /genx/v1/genomic-datasets` (`genxRegisterGenomicDataset`); `GET /genx/v1/genomic-datasets/{genomicDatasetDbId}` (`genxGetGenomicDataset`) |
| `GenebankStorage/` | `StorageLocation` — genebank storage location records (capacity, environment, provenance) | `GET /genx/v1/genebank-storage` (`genxListStorageLocations`); `POST /genx/v1/genebank-storage` (`genxRegisterStorageLocation`); `GET /genx/v1/genebank-storage/{storageLocationDbId}` (`genxGetStorageLocation`) |
| `ResearchAssets/` | `ResearchAsset` — research asset records (type, title, license, access policy, persistent identifier, provenance) | `GET /genx/v1/research-assets` (`genxListResearchAssets`); `POST /genx/v1/research-assets` (`genxRegisterResearchAsset`); `GET /genx/v1/research-assets/{researchAssetDbId}` (`genxGetResearchAsset`) |
| `MeasurementMethods/` | `MeasurementMethod` — measurement method definitions (procedure, equipment, precision, provenance) | `GET /genx/v1/measurement-methods` (`genxListMeasurementMethods`); `POST /genx/v1/measurement-methods` (`genxRegisterMeasurementMethod`); `GET /genx/v1/measurement-methods/{measurementMethodDbId}` (`genxGetMeasurementMethod`) |
| `FAIR/` | `FAIRPackage` — licensed, embargo-aware payload envelopes | `GET /genx/v1/fair-packages` (`genxListFairPackageMetadata`); `POST /genx/v1/fair-packages` (`genxRegisterFairPackage`); `GET /genx/v1/fair-packages/{packageDbId}` (`genxGetFairPackageMetadata`) |
| `Telemetry/` | `TelemetryPoint` — sensor streams, idempotent ingest, aggregates | `GET /genx/v1/telemetry` (`genxQueryTelemetrySamplesOrAggregates`); `POST /genx/v1/telemetry` (`genxAppendTelemetryBatch`) |
| `Conformance/` | Probes + fixtures + runner contract (`probes.yaml`) | Static tier runs now; live tier needs `--server` |

RFCs: [RFC-001-GenX-Skeleton](./RFC-001-GenX-Skeleton.md) (principles + first
three objects), [RFC-002-Variable-Term-Governance](./RFC-002-Variable-Term-Governance.md),
[RFC-003-Seed-Lot-Ledger](./RFC-003-Seed-Lot-Ledger.md),
[RFC-004-Model-Registry](./RFC-004-Model-Registry.md),
[RFC-005-Variant-Matrix-References](./RFC-005-Variant-Matrix-References.md),
[RFC-006-FAIR-Packages](./RFC-006-FAIR-Packages.md),
[RFC-007-Telemetry-Streams](./RFC-007-Telemetry-Streams.md),
[RFC-008-Selection-Decisions](./RFC-008-Selection-Decisions.md),
[RFC-009-Analysis-Methods](./RFC-009-Analysis-Methods.md),
[RFC-010-Weather-Observations](./RFC-010-Weather-Observations.md),
[RFC-011-Harvest-Records](./RFC-011-Harvest-Records.md),
[RFC-012-Phenotype-Capture](./RFC-012-Phenotype-Capture.md),
[RFC-013-Genomic-Datasets](./RFC-013-Genomic-Datasets.md),
[RFC-014-Breeding-Pipeline](./RFC-014-Breeding-Pipeline.md),
[RFC-015-Genebank-Storage](./RFC-015-Genebank-Storage.md),
[RFC-016-Research-Assets](./RFC-016-Research-Assets.md),
[RFC-017-Measurement-Methods](./RFC-017-Measurement-Methods.md),
[RFC-018-Experimental-Design](./RFC-018-Experimental-Design.md),
[RFC-019-Progeny-Records](./RFC-019-Progeny-Records.md),
[RFC-020-Doubled-Haploid](./RFC-020-Doubled-Haploid.md),
[RFC-021-Viability-Testing](./RFC-021-Viability-Testing.md),
[RFC-022-Speed-Breeding](./RFC-022-Speed-Breeding.md),
[RFC-023-Soil-Profile](./RFC-023-Soil-Profile.md),
[RFC-024-Irrigation-Operation](./RFC-024-Irrigation-Operation.md),
[RFC-025-Repeated-Measurement](./RFC-025-Repeated-Measurement.md),
[RFC-026-Fertilizer-Application](./RFC-026-Fertilizer-Application.md),
[RFC-027-Phenology-Observation](./RFC-027-Phenology-Observation.md),
[RFC-028-Parent-Candidate-Selection](./RFC-028-Parent-Candidate-Selection.md),
[RFC-029-Crop-Cycle](./RFC-029-Crop-Cycle.md),
[RFC-030-Quarantine](./RFC-030-Quarantine.md),
[RFC-031-Weather-Forecast](./RFC-031-Weather-Forecast.md),
[RFC-032-Image-Metadata](./RFC-032-Image-Metadata.md),
[RFC-033-Climate-Normals](./RFC-033-Climate-Normals.md).

[DECISIONS.md](./DECISIONS.md) logs deferred questions (D-01…D-20, need
authorization) and autonomous drafting decisions (A-01…A-12, reviewable).

[ENDPOINT-IDENTITY.md](./ENDPOINT-IDENTITY.md) defines stable operation identities and guards against semantic endpoint collisions.

[ADOPTION.md](./ADOPTION.md) is the incremental adoption guide for V2.1
servers (order, compat rules, conformance commands, anti-patterns).
