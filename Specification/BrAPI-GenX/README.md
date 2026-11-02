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
| `CustodyTransfer/` | `CustodyTransfer` — chain-of-custody transfer records (parties, condition, provenance) | `GET /genx/v1/custody-transfers` (`genxListCustodyTransfers`); `POST /genx/v1/custody-transfers` (`genxRecordCustodyTransfer`); `GET /genx/v1/custody-transfers/{custodyTransferDbId}` (`genxGetCustodyTransfer`) |
| `WeatherForecast/` | `WeatherForecast` — weather forecast records (predicted conditions, validity window, provenance) | `GET /genx/v1/weather-forecasts` (`genxListWeatherForecasts`); `POST /genx/v1/weather-forecasts` (`genxRegisterWeatherForecast`); `GET /genx/v1/weather-forecasts/{weatherForecastDbId}` (`genxGetWeatherForecast`) |
| `PopulationAdvancement/` | `PopulationAdvancement` — population advancement records (stages, dates, provenance) | `GET /genx/v1/population-advancements` (`genxListPopulationAdvancements`); `POST /genx/v1/population-advancements` (`genxRecordPopulationAdvancement`); `GET /genx/v1/population-advancements/{populationAdvancementDbId}` (`genxGetPopulationAdvancement`) |
| `CrossingSchedule/` | `CrossingSchedule` — crossing schedule records (parents, date, mating design, provenance) | `GET /genx/v1/crossing-schedules` (`genxListCrossingSchedules`); `POST /genx/v1/crossing-schedules` (`genxRegisterCrossingSchedule`); `GET /genx/v1/crossing-schedules/{crossingScheduleDbId}` (`genxGetCrossingSchedule`) |
| `ImageMetadata/` | `ImageMetadata` — image metadata records (capture details, camera, resolution, provenance) | `GET /genx/v1/image-metadata` (`genxListImageMetadata`); `POST /genx/v1/image-metadata` (`genxRegisterImageMetadata`); `GET /genx/v1/image-metadata/{imageMetadataDbId}` (`genxGetImageMetadata`) |
| `ClimateNormals/` | `ClimateNormal` — climate normal records (mean/min/max, period, provenance) | `GET /genx/v1/climate-normals` (`genxListClimateNormals`); `POST /genx/v1/climate-normals` (`genxRegisterClimateNormal`); `GET /genx/v1/climate-normals/{climateNormalDbId}` (`genxGetClimateNormal`) |
| `SafetyDuplication/` | `SafetyDuplication` — safety duplication records (backup site, quantity, provenance) | `GET /genx/v1/safety-duplications` (`genxListSafetyDuplications`); `POST /genx/v1/safety-duplications` (`genxRegisterSafetyDuplication`); `GET /genx/v1/safety-duplications/{safetyDuplicationDbId}` (`genxGetSafetyDuplication`) |
| `Regeneration/` | `RegenerationRecord` — regeneration records (method, quantity, provenance) | `GET /genx/v1/regeneration-records` (`genxListRegenerations`); `POST /genx/v1/regeneration-records` (`genxRecordRegeneration`); `GET /genx/v1/regeneration-records/{regenerationRecordDbId}` (`genxGetRegeneration`) |
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
| `Tillage/` | `TillageRecord` — tillage records (method, depth, provenance) | `GET /genx/v1/tillage-records` (`genxListTillageRecords`); `POST /genx/v1/tillage-records` (`genxRecordTillage`); `GET /genx/v1/tillage-records/{tillageRecordDbId}` (`genxGetTillage`) |
| `BulkCapture/` | `BulkCapture` — bulk capture records (entries, quality flags, provenance) | `GET /genx/v1/bulk-captures` (`genxListBulkCaptures`); `POST /genx/v1/bulk-captures` (`genxRecordBulkCapture`); `GET /genx/v1/bulk-captures/{bulkCaptureDbId}` (`genxGetBulkCapture`) |
| `CandidateVarietyLifecycle/` | `CandidateVariety` — candidate variety lifecycle records (status, registration, provenance) | `GET /genx/v1/candidate-varieties` (`genxListCandidateVarieties`); `POST /genx/v1/candidate-varieties` (`genxRegisterCandidateVariety`); `GET /genx/v1/candidate-varieties/{candidateVarietyDbId}` (`genxGetCandidateVariety`) |
| `Acquisition/` | `AcquisitionRecord` — acquisition records (source, method, provenance) | `GET /genx/v1/acquisitions` (`genxListAcquisitions`); `POST /genx/v1/acquisitions` (`genxRecordAcquisition`); `GET /genx/v1/acquisitions/{acquisitionRecordDbId}` (`genxGetAcquisition`) |
| `GeneticGain/` | `GeneticGainRecord` — genetic gain records (value, trait, period, provenance) | `GET /genx/v1/genetic-gains` (`genxListGeneticGains`); `POST /genx/v1/genetic-gains` (`genxRecordGeneticGain`); `GET /genx/v1/genetic-gains/{geneticGainRecordDbId}` (`genxGetGeneticGain`) |
| `StabilityAnalysis/` | `StabilityAnalysisResult` — stability analysis results (index, provenance) | `GET /genx/v1/stability-analyses` (`genxListStabilityAnalyses`); `POST /genx/v1/stability-analyses` (`genxRecordStabilityAnalysis`); `GET /genx/v1/stability-analyses/{stabilityAnalysisResultDbId}` (`genxGetStabilityAnalysis`) |
| `PhenotypeAnnotation/` | `PhenotypeAnnotation` — phenotype annotation records (score, variable, provenance) | `GET /genx/v1/phenotype-annotations` (`genxListPhenotypeAnnotations`); `POST /genx/v1/phenotype-annotations` (`genxRecordPhenotypeAnnotation`); `GET /genx/v1/phenotype-annotations/{phenotypeAnnotationDbId}` (`genxGetPhenotypeAnnotation`) |
| `ExtremeWeather/` | `ExtremeWeatherEvent` — extreme weather event records (type, severity, provenance) | `GET /genx/v1/extreme-weather-events` (`genxListExtremeWeatherEvents`); `POST /genx/v1/extreme-weather-events` (`genxRecordExtremeWeather`); `GET /genx/v1/extreme-weather-events/{extremeWeatherEventDbId}` (`genxGetExtremeWeatherEvent`) |
| `VcfImport/` | `VcfImport` — VCF import records (source format, counts, provenance) | `GET /genx/v1/vcf-imports` (`genxListVcfImports`); `POST /genx/v1/vcf-imports` (`genxRecordVcfImport`); `GET /genx/v1/vcf-imports/{vcfImportDbId}` (`genxGetVcfImport`) |
| `AssayDesign/` | `AssayDesign` — assay design records (platform, marker count, provenance) | `GET /genx/v1/assay-designs` (`genxListAssayDesigns`); `POST /genx/v1/assay-designs` (`genxRecordAssayDesign`); `GET /genx/v1/assay-designs/{assayDesignDbId}` (`genxGetAssayDesign`) |
| `VariantAnnotation/` | `VariantAnnotation` — variant annotation records (functional annotations, provenance) | `GET /genx/v1/variant-annotations` (`genxListVariantAnnotations`); `POST /genx/v1/variant-annotations` (`genxRecordVariantAnnotation`); `GET /genx/v1/variant-annotations/{variantAnnotationDbId}` (`genxGetVariantAnnotation`) |
| `GenotypeQc/` | `GenotypeQcReport` — genotype QC report records (metrics, thresholds, provenance) | `GET /genx/v1/genotype-qc-reports` (`genxListGenotypeQcReports`); `POST /genx/v1/genotype-qc-reports` (`genxRecordGenotypeQcReport`); `GET /genx/v1/genotype-qc-reports/{genotypeQcReportDbId}` (`genxGetGenotypeQcReport`) |
| `DisposalRecord/` | `DisposalRecord` — disposal records (reason, method, quantity, provenance) | `GET /genx/v1/disposal-records` (`genxListDisposalRecords`); `POST /genx/v1/disposal-records` (`genxRecordDisposalRecord`); `GET /genx/v1/disposal-records/{disposalRecordDbId}` (`genxGetDisposalRecord`) |
| `PlantingOperation/` | `PlantingOperation` — planting operation records (date, method, rate, provenance) | `GET /genx/v1/planting-operations` (`genxListPlantingOperations`); `POST /genx/v1/planting-operations` (`genxRecordPlantingOperation`); `GET /genx/v1/planting-operations/{plantingOperationDbId}` (`genxGetPlantingOperation`) |
| `CarbonStock/` | `CarbonStock` — carbon stock observations (pool, stock, depth, provenance) | `GET /genx/v1/carbon-stocks` (`genxListCarbonStocks`); `POST /genx/v1/carbon-stocks` (`genxRecordCarbonStock`); `GET /genx/v1/carbon-stocks/{carbonStockDbId}` (`genxGetCarbonStock`) |
| `WaterBalance/` | `WaterBalance` — water balance records (period, inputs, outputs, storage change, provenance) | `GET /genx/v1/water-balances` (`genxListWaterBalances`); `POST /genx/v1/water-balances` (`genxRecordWaterBalance`); `GET /genx/v1/water-balances/{waterBalanceDbId}` (`genxGetWaterBalance`) |
| `MixedModel/` | `MixedModelResult` — mixed model result records (variance components, BLUPs, provenance) | `GET /genx/v1/mixed-model-results` (`genxListMixedModelResults`); `POST /genx/v1/mixed-model-results` (`genxRecordMixedModelResult`); `GET /genx/v1/mixed-model-results/{mixedModelResultDbId}` (`genxGetMixedModelResult`) |
| `Heritability/` | `HeritabilityEstimate` — heritability estimate records (value, provenance) | `GET /genx/v1/heritability-estimates` (`genxListHeritabilityEstimates`); `POST /genx/v1/heritability-estimates` (`genxRecordHeritability`); `GET /genx/v1/heritability-estimates/{heritabilityEstimateDbId}` (`genxGetHeritabilityEstimate`) |
| `GxeAnalysis/` | `GxeAnalysisResult` — GxE analysis result records (interaction effect, provenance) | `GET /genx/v1/gxe-analyses` (`genxListGxeAnalyses`); `POST /genx/v1/gxe-analyses` (`genxRecordGxeAnalysis`); `GET /genx/v1/gxe-analyses/{gxeAnalysisResultDbId}` (`genxGetGxeAnalysis`) |
| `GwasResult/` | `GwasResult` — GWAS result records (significant markers, top p-value, provenance) | `GET /genx/v1/gwas-results` (`genxListGwasResults`); `POST /genx/v1/gwas-results` (`genxRecordGwasResult`); `GET /genx/v1/gwas-results/{gwasResultDbId}` (`genxGetGwasResult`) |
| `Kinship/` | `KinshipMatrix` — kinship matrix records (method, storage reference, provenance) | `GET /genx/v1/kinship-matrices` (`genxListKinshipMatrices`); `POST /genx/v1/kinship-matrices` (`genxRegisterKinshipMatrix`); `GET /genx/v1/kinship-matrices/{kinshipMatrixDbId}` (`genxGetKinshipMatrix`) |
| `PcaResult/` | `PcaResult` — PCA result records (components, explained variance, provenance) | `GET /genx/v1/pca-results` (`genxListPcaResults`); `POST /genx/v1/pca-results` (`genxRecordPcaResult`); `GET /genx/v1/pca-results/{pcaResultDbId}` (`genxGetPcaResult`) |
| `GenomicPrediction/` | `GenomicPrediction` — genomic prediction result records (predictions, accuracy, provenance) | `GET /genx/v1/genomic-predictions` (`genxListGenomicPredictions`); `POST /genx/v1/genomic-predictions` (`genxRecordGenomicPrediction`); `GET /genx/v1/genomic-predictions/{genomicPredictionDbId}` (`genxGetGenomicPrediction`) |
| `GenomicSelection/` | `GenomicSelection` — genomic selection result records (selections, threshold, provenance) | `GET /genx/v1/genomic-selections` (`genxListGenomicSelections`); `POST /genx/v1/genomic-selections` (`genxRecordGenomicSelection`); `GET /genx/v1/genomic-selections/{genomicSelectionDbId}` (`genxGetGenomicSelection`) |
| `GenomicRelationship/` | `GenomicRelationship` — genomic relationship matrix records (method, storage reference, provenance) | `GET /genx/v1/genomic-relationships` (`genxListGenomicRelationships`); `POST /genx/v1/genomic-relationships` (`genxRegisterGenomicRelationship`); `GET /genx/v1/genomic-relationships/{genomicRelationshipDbId}` (`genxGetGenomicRelationship`) |
| `MethylationAnalysis/` | `MethylationAnalysis` — methylation analysis result records (regions, provenance) | `GET /genx/v1/methylation-analyses` (`genxListMethylationAnalyses`); `POST /genx/v1/methylation-analyses` (`genxRecordMethylationAnalysis`); `GET /genx/v1/methylation-analyses/{methylationAnalysisDbId}` (`genxGetMethylationAnalysis`) |
| `ExpressionQtl/` | `ExpressionQtl` — expression QTL result records (QTLs, provenance) | `GET /genx/v1/expression-qtls` (`genxListExpressionQtls`); `POST /genx/v1/expression-qtls` (`genxRecordExpressionQtl`); `GET /genx/v1/expression-qtls/{expressionQtlDbId}` (`genxGetExpressionQtl`) |
| `HaplotypeAnalysis/` | `HaplotypeAnalysis` — haplotype analysis result records (haplotypes, provenance) | `GET /genx/v1/haplotype-analyses` (`genxListHaplotypeAnalyses`); `POST /genx/v1/haplotype-analyses` (`genxRecordHaplotypeAnalysis`); `GET /genx/v1/haplotype-analyses/{haplotypeAnalysisDbId}` (`genxGetHaplotypeAnalysis`) |
| `PedigreeAnalysis/` | `PedigreeAnalysis` — pedigree analysis result records (metrics, provenance) | `GET /genx/v1/pedigree-analyses` (`genxListPedigreeAnalyses`); `POST /genx/v1/pedigree-analyses` (`genxRecordPedigreeAnalysis`); `GET /genx/v1/pedigree-analyses/{pedigreeAnalysisDbId}` (`genxGetPedigreeAnalysis`) |
| `AnalysisResult/` | `AnalysisResult` — analysis result records (method, job, payload, provenance) | `GET /genx/v1/analysis-results` (`genxListAnalysisResults`); `POST /genx/v1/analysis-results` (`genxRecordAnalysisResult`); `GET /genx/v1/analysis-results/{analysisResultDbId}` (`genxGetAnalysisResult`) |
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
[RFC-033-Climate-Normals](./RFC-033-Climate-Normals.md),
[RFC-034-Safety-Duplication](./RFC-034-Safety-Duplication.md),
[RFC-035-Population-Advancement](./RFC-035-Population-Advancement.md),
[RFC-036-Regeneration](./RFC-036-Regeneration.md),
[RFC-037-Crossing-Schedule](./RFC-037-Crossing-Schedule.md),
[RFC-038-Tillage](./RFC-038-Tillage.md),
[RFC-039-Candidate-Variety-Lifecycle](./RFC-039-Candidate-Variety-Lifecycle.md),
[RFC-040-Bulk-Capture](./RFC-040-Bulk-Capture.md),
[RFC-041-Acquisition](./RFC-041-Acquisition.md),
[RFC-042-Extreme-Weather](./RFC-042-Extreme-Weather.md),
[RFC-043-Vcf-Import](./RFC-043-Vcf-Import.md),
[RFC-044-Phenotype-Annotation](./RFC-044-Phenotype-Annotation.md),
[RFC-045-Analysis-Result](./RFC-045-Analysis-Result.md),
[RFC-046-Genetic-Gain](./RFC-046-Genetic-Gain.md),
[RFC-047-Gwas-Result](./RFC-047-Gwas-Result.md),
[RFC-048-Mixed-Model](./RFC-048-Mixed-Model.md),
[RFC-049-Stability-Analysis](./RFC-049-Stability-Analysis.md),
[RFC-050-Heritability](./RFC-050-Heritability.md),
[RFC-051-Gxe-Analysis](./RFC-051-Gxe-Analysis.md),
[RFC-052-Kinship](./RFC-052-Kinship.md),
[RFC-053-Pca-Result](./RFC-053-Pca-Result.md),
[RFC-054-Genomic-Prediction](./RFC-054-Genomic-Prediction.md),
[RFC-055-Genomic-Selection](./RFC-055-Genomic-Selection.md),
[RFC-056-Genomic-Relationship](./RFC-056-Genomic-Relationship.md),
[RFC-057-Methylation-Analysis](./RFC-057-Methylation-Analysis.md),
[RFC-058-Expression-Qtl](./RFC-058-Expression-Qtl.md),
[RFC-059-Haplotype-Analysis](./RFC-059-Haplotype-Analysis.md),
[RFC-060-Pedigree-Analysis](./RFC-060-Pedigree-Analysis.md),
[RFC-061-Assay-Design](./RFC-061-Assay-Design.md),
[RFC-062-Variant-Annotation](./RFC-062-Variant-Annotation.md),
[RFC-063-Custody-Transfer](./RFC-063-Custody-Transfer.md),
[RFC-064-Genotype-Qc](./RFC-064-Genotype-Qc.md),
[RFC-065-Disposal-Record](./RFC-065-Disposal-Record.md),
[RFC-066-Planting-Operation](./RFC-066-Planting-Operation.md),
[RFC-067-Carbon-Stock](./RFC-067-Carbon-Stock.md),
[RFC-068-Water-Balance](./RFC-068-Water-Balance.md).

[DECISIONS.md](./DECISIONS.md) logs deferred questions (D-01…D-20, need
authorization) and autonomous drafting decisions (A-01…A-12, reviewable).

[ENDPOINT-IDENTITY.md](./ENDPOINT-IDENTITY.md) defines stable operation identities and guards against semantic endpoint collisions.

[ADOPTION.md](./ADOPTION.md) is the incremental adoption guide for V2.1
servers (order, compat rules, conformance commands, anti-patterns).
