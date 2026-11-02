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
| `CaptureWorkflow/` | `CaptureWorkflow` — capture workflow records (workflow type, provenance) | `GET /genx/v1/capture-workflows` (`genxListCaptureWorkflows`); `POST /genx/v1/capture-workflows` (`genxRegisterCaptureWorkflow`); `GET /genx/v1/capture-workflows/{captureWorkflowDbId}` (`genxGetCaptureWorkflow`) |
| `QualityFlag/` | `QualityFlag` — quality flag records (flag, provenance) | `GET /genx/v1/quality-flags` (`genxListQualityFlags`); `POST /genx/v1/quality-flags` (`genxRegisterQualityFlag`); `GET /genx/v1/quality-flags/{qualityFlagDbId}` (`genxGetQualityFlag`) |
| `ValueMissingness/` | `ValueMissingness` — value and missingness records (value, missing, provenance) | `GET /genx/v1/value-missingness` (`genxListValueMissingness`); `POST /genx/v1/value-missingness` (`genxRegisterValueMissingness`); `GET /genx/v1/value-missingness/{valueMissingnessDbId}` (`genxGetValueMissingness`) |
| `GenomicDatasets/` | `GenomicDataset` — prepared genomic dataset records (reference assembly, pipeline provenance, access policy, release status) | `GET /genx/v1/genomic-datasets` (`genxListGenomicDatasets`); `POST /genx/v1/genomic-datasets` (`genxRegisterGenomicDataset`); `GET /genx/v1/genomic-datasets/{genomicDatasetDbId}` (`genxGetGenomicDataset`) |
| `GenebankStorage/` | `StorageLocation` — genebank storage location records (capacity, environment, provenance) | `GET /genx/v1/genebank-storage` (`genxListStorageLocations`); `POST /genx/v1/genebank-storage` (`genxRegisterStorageLocation`); `GET /genx/v1/genebank-storage/{storageLocationDbId}` (`genxGetStorageLocation`) |
| `ResearchAssets/` | `ResearchAsset` — research asset records (type, title, license, access policy, persistent identifier, provenance) | `GET /genx/v1/research-assets` (`genxListResearchAssets`); `POST /genx/v1/research-assets` (`genxRegisterResearchAsset`); `GET /genx/v1/research-assets/{researchAssetDbId}` (`genxGetResearchAsset`) |
| `MeasurementMethods/` | `MeasurementMethod` — measurement method definitions (procedure, equipment, precision, provenance) | `GET /genx/v1/measurement-methods` (`genxListMeasurementMethods`); `POST /genx/v1/measurement-methods` (`genxRegisterMeasurementMethod`); `GET /genx/v1/measurement-methods/{measurementMethodDbId}` (`genxGetMeasurementMethod`) |
| `DevelopmentalStage/` | `DevelopmentalStage` — developmental stage vocabulary entries (code, name, definition, provenance) | `GET /genx/v1/developmental-stages` (`genxListDevelopmentalStages`); `POST /genx/v1/developmental-stages` (`genxRegisterDevelopmentalStage`); `GET /genx/v1/developmental-stages/{developmentalStageDbId}` (`genxGetDevelopmentalStage`) |
| `UnitsAndQuantity/` | `UnitsAndQuantity` — units and quantity semantics entries (unit, quantity, definition, provenance) | `GET /genx/v1/units-and-quantities` (`genxListUnitsAndQuantities`); `POST /genx/v1/units-and-quantities` (`genxRegisterUnitsAndQuantity`); `GET /genx/v1/units-and-quantities/{unitsAndQuantityDbId}` (`genxGetUnitsAndQuantity`) |
| `ExternalVocabulary/` | `ExternalVocabulary` — external vocabulary sync entries (source, target, mapping, provenance) | `GET /genx/v1/external-vocabularies` (`genxListExternalVocabularies`); `POST /genx/v1/external-vocabularies` (`genxRegisterExternalVocabulary`); `GET /genx/v1/external-vocabularies/{externalVocabularyDbId}` (`genxGetExternalVocabulary`) |
| `TerminologyVersion/` | `TerminologyVersion` — terminology version entries (terminology, version, provenance) | `GET /genx/v1/terminology-versions` (`genxListTerminologyVersions`); `POST /genx/v1/terminology-versions` (`genxRegisterTerminologyVersion`); `GET /genx/v1/terminology-versions/{terminologyVersionDbId}` (`genxGetTerminologyVersion`) |
| `OntologyTerm/` | `OntologyTermRecord` — ontology term and synonym entries (term, synonyms, ontology, provenance) | `GET /genx/v1/ontology-terms` (`genxListOntologyTerms`); `POST /genx/v1/ontology-terms` (`genxRegisterOntologyTerm`); `GET /genx/v1/ontology-terms/{ontologyTermDbId}` (`genxGetOntologyTerm`) |
| `OntologyMapping/` | `OntologyMapping` — ontology mapping and crosswalk entries (source, target, mapping, provenance) | `GET /genx/v1/ontology-mappings` (`genxListOntologyMappings`); `POST /genx/v1/ontology-mappings` (`genxRegisterOntologyMapping`); `GET /genx/v1/ontology-mappings/{ontologyMappingDbId}` (`genxGetOntologyMapping`) |
| `MeasurementScale/` | `MeasurementScale` — measurement scale and value domain entries (scale name, value domain, provenance) | `GET /genx/v1/measurement-scales` (`genxListMeasurementScales`); `POST /genx/v1/measurement-scales` (`genxRegisterMeasurementScale`); `GET /genx/v1/measurement-scales/{measurementScaleDbId}` (`genxGetMeasurementScale`) |
| `CropTraitDictionary/` | `CropTraitDictionary` — crop trait dictionary entries (crop, trait, definition, provenance) | `GET /genx/v1/crop-trait-dictionaries` (`genxListCropTraitDictionaries`); `POST /genx/v1/crop-trait-dictionaries` (`genxRegisterCropTraitDictionary`); `GET /genx/v1/crop-trait-dictionaries/{cropTraitDictionaryDbId}` (`genxGetCropTraitDictionary`) |
| `Project/` | `Project` — project and funding reference records (title, funding, provenance) | `GET /genx/v1/projects` (`genxListProjects`); `POST /genx/v1/projects` (`genxRegisterProject`); `GET /genx/v1/projects/{projectDbId}` (`genxGetProject`) |
| `ReusableList/` | `ReusableList` — reusable list and cohort records (name, members, provenance) | `GET /genx/v1/reusable-lists` (`genxListReusableLists`); `POST /genx/v1/reusable-lists` (`genxRegisterReusableList`); `GET /genx/v1/reusable-lists/{reusableListDbId}` (`genxGetReusableList`) |
| `Calendar/` | `Calendar` — calendar and time convention records (name, convention, provenance) | `GET /genx/v1/calendars` (`genxListCalendars`); `POST /genx/v1/calendars` (`genxRegisterCalendar`); `GET /genx/v1/calendars/{calendarDbId}` (`genxGetCalendar`) |
| `LocationGeometry/` | `LocationGeometry` — location geometry records (location reference, geometry URI, provenance) | `GET /genx/v1/location-geometries` (`genxListLocationGeometries`); `POST /genx/v1/location-geometries` (`genxRegisterLocationGeometry`); `GET /genx/v1/location-geometries/{locationGeometryDbId}` (`genxGetLocationGeometry`) |
| `ReferenceDataVersion/` | `ReferenceDataVersion` — reference data version records (source, version, provenance) | `GET /genx/v1/reference-data-versions` (`genxListReferenceDataVersions`); `POST /genx/v1/reference-data-versions` (`genxRegisterReferenceDataVersion`); `GET /genx/v1/reference-data-versions/{referenceDataVersionDbId}` (`genxGetReferenceDataVersion`) |
| `TaxonName/` | `TaxonName` — taxon name and synonym entries (scientific name, synonyms, provenance) | `GET /genx/v1/taxon-names` (`genxListTaxonNames`); `POST /genx/v1/taxon-names` (`genxRegisterTaxonName`); `GET /genx/v1/taxon-names/{taxonNameDbId}` (`genxGetTaxonName`) |
| `CommonCropName/` | `CommonCropName` — common crop name entries (scientific name, common name, provenance) | `GET /genx/v1/common-crop-names` (`genxListCommonCropNames`); `POST /genx/v1/common-crop-names` (`genxRegisterCommonCropName`); `GET /genx/v1/common-crop-names/{commonCropNameDbId}` (`genxGetCommonCropName`) |
| `CropSpecies/` | `CropSpecies` — crop and species registry entries (scientific name, crop name, provenance) | `GET /genx/v1/crop-species` (`genxListCropSpecies`); `POST /genx/v1/crop-species` (`genxRegisterCropSpecies`); `GET /genx/v1/crop-species/{cropSpeciesDbId}` (`genxGetCropSpecies`) |
| `InstitutionCode/` | `InstitutionCode` — institution and collection code entries (code, name, provenance) | `GET /genx/v1/institution-codes` (`genxListInstitutionCodes`); `POST /genx/v1/institution-codes` (`genxRegisterInstitutionCode`); `GET /genx/v1/institution-codes/{institutionCodeDbId}` (`genxGetInstitutionCode`) |
| `PersonReference/` | `PersonReference` — person reference entries (name, role, provenance) | `GET /genx/v1/person-references` (`genxListPersonReferences`); `POST /genx/v1/person-references` (`genxRegisterPersonReference`); `GET /genx/v1/person-references/{personReferenceDbId}` (`genxGetPersonReference`) |
| `ResearchProgram/` | `ResearchProgram` — research program records (title, provenance) | `GET /genx/v1/research-programs` (`genxListResearchPrograms`); `POST /genx/v1/research-programs` (`genxRegisterResearchProgram`); `GET /genx/v1/research-programs/{researchProgramDbId}` (`genxGetResearchProgram`) |
| `CapabilityMetadata/` | `CapabilityMetadata` — capability metadata records (profile, capabilities, provenance) | `GET /genx/v1/capability-metadata` (`genxListCapabilityMetadata`); `POST /genx/v1/capability-metadata` (`genxRegisterCapabilityMetadata`); `GET /genx/v1/capability-metadata/{capabilityMetadataDbId}` (`genxGetCapabilityMetadata`) |
| `ResearchLocation/` | `ResearchLocation` — research location records (name, provenance) | `GET /genx/v1/research-locations` (`genxListResearchLocations`); `POST /genx/v1/research-locations` (`genxRegisterResearchLocation`); `GET /genx/v1/research-locations/{researchLocationDbId}` (`genxGetResearchLocation`) |
| `CollectingMission/` | `CollectingMission` — collecting mission records (title, provenance) | `GET /genx/v1/collecting-missions` (`genxListCollectingMissions`); `POST /genx/v1/collecting-missions` (`genxRegisterCollectingMission`); `GET /genx/v1/collecting-missions/{collectingMissionDbId}` (`genxGetCollectingMission`) |
| `ConservationMembership/` | `ConservationMembership` — conservation membership records (member, program, provenance) | `GET /genx/v1/conservation-memberships` (`genxListConservationMemberships`); `POST /genx/v1/conservation-memberships` (`genxRegisterConservationMembership`); `GET /genx/v1/conservation-memberships/{conservationMembershipDbId}` (`genxGetConservationMembership`) |
| `McpdAdapter/` | `McpdAdapter` — MCPD adapter records (source, provenance) | `GET /genx/v1/mcpd-adapters` (`genxListMcpdAdapters`); `POST /genx/v1/mcpd-adapters` (`genxRegisterMcpdAdapter`); `GET /genx/v1/mcpd-adapters/{mcpdAdapterDbId}` (`genxGetMcpdAdapter`) |
| `DuplicateReview/` | `DuplicateReview` — duplicate review records (candidate, decision, provenance) | `GET /genx/v1/duplicate-reviews` (`genxListDuplicateReviews`); `POST /genx/v1/duplicate-reviews` (`genxRegisterDuplicateReview`); `GET /genx/v1/duplicate-reviews/{duplicateReviewDbId}` (`genxGetDuplicateReview`) |
| `Crosswalk/` | `Crosswalk` — crosswalk records (source, target, provenance) | `GET /genx/v1/crosswalks` (`genxListCrosswalks`); `POST /genx/v1/crosswalks` (`genxRegisterCrosswalk`); `GET /genx/v1/crosswalks/{crosswalkDbId}` (`genxGetCrosswalk`) |
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
| `VcfExport/` | `VcfExport` — VCF export records (status, provenance) | `GET /genx/v1/vcf-exports` (`genxListVcfExports`); `POST /genx/v1/vcf-exports` (`genxRegisterVcfExport`); `GET /genx/v1/vcf-exports/{vcfExportDbId}` (`genxGetVcfExport`) |
| `ReferenceAssembly/` | `ReferenceAssembly` — reference assembly records (accession, version, provenance) | `GET /genx/v1/reference-assemblies` (`genxListReferenceAssemblies`); `POST /genx/v1/reference-assemblies` (`genxRegisterReferenceAssembly`); `GET /genx/v1/reference-assemblies/{referenceAssemblyDbId}` (`genxGetReferenceAssembly`) |
| `PipelineProvenance/` | `PipelineProvenance` — pipeline provenance records (pipeline, version, provenance) | `GET /genx/v1/pipeline-provenances` (`genxListPipelineProvenances`); `POST /genx/v1/pipeline-provenances` (`genxRegisterPipelineProvenance`); `GET /genx/v1/pipeline-provenances/{pipelineProvenanceDbId}` (`genxGetPipelineProvenance`) |
| `ExperimentalProtocol/` | `ExperimentalProtocol` — experimental protocol records (design, treatments, provenance) | `GET /genx/v1/experimental-protocols` (`genxListExperimentalProtocols`); `POST /genx/v1/experimental-protocols` (`genxRegisterExperimentalProtocol`); `GET /genx/v1/experimental-protocols/{experimentalProtocolDbId}` (`genxGetExperimentalProtocol`) |
| `ArtifactCatalogue/` | `ArtifactCatalogue` — artefact catalogue records (type, storage reference, digest) | `GET /genx/v1/artifact-catalogues` (`genxListArtifactCatalogues`); `POST /genx/v1/artifact-catalogues` (`genxRegisterArtifactCatalogue`); `GET /genx/v1/artifact-catalogues/{artifactCatalogueDbId}` (`genxGetArtifactCatalogue`) |
| `ProtocolLibrary/` | `ProtocolLibrary` — protocol library records (type, version, methods) | `GET /genx/v1/protocol-libraries` (`genxListProtocolLibraries`); `POST /genx/v1/protocol-libraries` (`genxRegisterProtocolLibrary`); `GET /genx/v1/protocol-libraries/{protocolLibraryDbId}` (`genxGetProtocolLibrary`) |
| `PublicationReview/` | `PublicationReview` — publication review records (title, venue, year) | `GET /genx/v1/publication-reviews` (`genxListPublicationReviews`); `POST /genx/v1/publication-reviews` (`genxRegisterPublicationReview`); `GET /genx/v1/publication-reviews/{publicationReviewDbId}` (`genxGetPublicationReview`) |
| `BiodiversityExport/` | `BiodiversityExport` — biodiversity export records (specimen, occurrence, taxon) | `GET /genx/v1/biodiversity-exports` (`genxListBiodiversityExports`); `POST /genx/v1/biodiversity-exports` (`genxRegisterBiodiversityExport`); `GET /genx/v1/biodiversity-exports/{biodiversityExportDbId}` (`genxGetBiodiversityExport`) |
| `EvidencePack/` | `EvidencePack` — evidence pack records (type, contents, provenance) | `GET /genx/v1/evidence-packs` (`genxListEvidencePacks`); `POST /genx/v1/evidence-packs` (`genxRegisterEvidencePack`); `GET /genx/v1/evidence-packs/{evidencePackDbId}` (`genxGetEvidencePack`) |
| `DiseaseObservation/` | `DiseaseObservation` — disease observation records (type, pest/disease, severity) | `GET /genx/v1/disease-observations` (`genxListDiseaseObservations`); `POST /genx/v1/disease-observations` (`genxRegisterDiseaseObservation`); `GET /genx/v1/disease-observations/{diseaseObservationDbId}` (`genxGetDiseaseObservation`) |
| `DiagnosticEvidence/` | `DiagnosticEvidence` — diagnostic evidence records (type, method, result) | `GET /genx/v1/diagnostic-evidences` (`genxListDiagnosticEvidences`); `POST /genx/v1/diagnostic-evidences` (`genxRegisterDiagnosticEvidence`); `GET /genx/v1/diagnostic-evidences/{diagnosticEvidenceDbId}` (`genxGetDiagnosticEvidence`) |
| `IpmStrategy/` | `IpmStrategy` — IPM strategy records (target, type, tactics) | `GET /genx/v1/ipm-strategies` (`genxListIpmStrategies`); `POST /genx/v1/ipm-strategies` (`genxRegisterIpmStrategy`); `GET /genx/v1/ipm-strategies/{ipmStrategyDbId}` (`genxGetIpmStrategy`) |
| `ThresholdAlert/` | `ThresholdAlert` — threshold alert records (type, threshold, current value) | `GET /genx/v1/threshold-alerts` (`genxListThresholdAlerts`); `POST /genx/v1/threshold-alerts` (`genxRegisterThresholdAlert`); `GET /genx/v1/threshold-alerts/{thresholdAlertDbId}` (`genxGetThresholdAlert`) |
| `DiseaseResistance/` | `DiseaseResistance` — disease resistance records (type, target, level) | `GET /genx/v1/disease-resistances` (`genxListDiseaseResistances`); `POST /genx/v1/disease-resistances` (`genxRegisterDiseaseResistance`); `GET /genx/v1/disease-resistances/{diseaseResistanceDbId}` (`genxGetDiseaseResistance`) |
| `CropHealthImage/` | `CropHealthImage` — crop health image records (type, index, status) | `GET /genx/v1/crop-health-images` (`genxListCropHealthImages`); `POST /genx/v1/crop-health-images` (`genxRegisterCropHealthImage`); `GET /genx/v1/crop-health-images/{cropHealthImageDbId}` (`genxGetCropHealthImage`) |
| `CropRecommendation/` | `CropRecommendation` — crop recommendation records (type, variety, practice) | `GET /genx/v1/crop-recommendations` (`genxListCropRecommendations`); `POST /genx/v1/crop-recommendations` (`genxRegisterCropRecommendation`); `GET /genx/v1/crop-recommendations/{cropRecommendationDbId}` (`genxGetCropRecommendation`) |
| `SowingWindow/` | `SowingWindow` — sowing window records (type, dates, zone) | `GET /genx/v1/sowing-windows` (`genxListSowingWindows`); `POST /genx/v1/sowing-windows` (`genxRegisterSowingWindow`); `GET /genx/v1/sowing-windows/{sowingWindowDbId}` (`genxGetSowingWindow`) |
| `IrrigationAdvice/` | `IrrigationAdvice` — irrigation advice records (type, amount, frequency) | `GET /genx/v1/irrigation-advice` (`genxListIrrigationAdvice`); `POST /genx/v1/irrigation-advice` (`genxRegisterIrrigationAdvice`); `GET /genx/v1/irrigation-advice/{irrigationAdviceDbId}` (`genxGetIrrigationAdvice`) |
| `AssayDesign/` | `AssayDesign` — assay design records (platform, marker count, provenance) | `GET /genx/v1/assay-designs` (`genxListAssayDesigns`); `POST /genx/v1/assay-designs` (`genxRecordAssayDesign`); `GET /genx/v1/assay-designs/{assayDesignDbId}` (`genxGetAssayDesign`) |
| `AssayExecution/` | `AssayExecution` — assay execution records (assay reference, provenance) | `GET /genx/v1/assay-executions` (`genxListAssayExecutions`); `POST /genx/v1/assay-executions` (`genxRegisterAssayExecution`); `GET /genx/v1/assay-executions/{assayExecutionDbId}` (`genxGetAssayExecution`) |
| `VariantAnnotation/` | `VariantAnnotation` — variant annotation records (functional annotations, provenance) | `GET /genx/v1/variant-annotations` (`genxListVariantAnnotations`); `POST /genx/v1/variant-annotations` (`genxRecordVariantAnnotation`); `GET /genx/v1/variant-annotations/{variantAnnotationDbId}` (`genxGetVariantAnnotation`) |
| `GenotypeQc/` | `GenotypeQcReport` — genotype QC report records (metrics, thresholds, provenance) | `GET /genx/v1/genotype-qc-reports` (`genxListGenotypeQcReports`); `POST /genx/v1/genotype-qc-reports` (`genxRecordGenotypeQcReport`); `GET /genx/v1/genotype-qc-reports/{genotypeQcReportDbId}` (`genxGetGenotypeQcReport`) |
| `GenotypeCallSemantics/` | `GenotypeCallSemantics` — genotype call semantics records (missing-call policy, zygosity encoding, provenance) | `GET /genx/v1/genotype-call-semantics` (`genxListGenotypeCallSemantics`); `POST /genx/v1/genotype-call-semantics` (`genxRegisterGenotypeCallSemantics`); `GET /genx/v1/genotype-call-semantics/{genotypeCallSemanticsDbId}` (`genxGetGenotypeCallSemantics`) |
| `VendorOrder/` | `VendorOrderRecord` — vendor genotyping order records (vendor, platform, sample count, provenance) | `GET /genx/v1/vendor-orders` (`genxListVendorOrders`); `POST /genx/v1/vendor-orders` (`genxRegisterVendorOrder`); `GET /genx/v1/vendor-orders/{vendorOrderDbId}` (`genxGetVendorOrder`) |
| `MarkerProbe/` | `MarkerProbe` — marker probe records (marker linkage, platform, sequence, provenance) | `GET /genx/v1/marker-probes` (`genxListMarkerProbes`); `POST /genx/v1/marker-probes` (`genxRegisterMarkerProbe`); `GET /genx/v1/marker-probes/{markerProbeDbId}` (`genxGetMarkerProbe`) |
| `DisposalRecord/` | `DisposalRecord` — disposal records (reason, method, quantity, provenance) | `GET /genx/v1/disposal-records` (`genxListDisposalRecords`); `POST /genx/v1/disposal-records` (`genxRecordDisposalRecord`); `GET /genx/v1/disposal-records/{disposalRecordDbId}` (`genxGetDisposalRecord`) |
| `PlantingOperation/` | `PlantingOperation` — planting operation records (date, method, rate, provenance) | `GET /genx/v1/planting-operations` (`genxListPlantingOperations`); `POST /genx/v1/planting-operations` (`genxRecordPlantingOperation`); `GET /genx/v1/planting-operations/{plantingOperationDbId}` (`genxGetPlantingOperation`) |
| `CarbonStock/` | `CarbonStock` — carbon stock observations (pool, stock, depth, provenance) | `GET /genx/v1/carbon-stocks` (`genxListCarbonStocks`); `POST /genx/v1/carbon-stocks` (`genxRecordCarbonStock`); `GET /genx/v1/carbon-stocks/{carbonStockDbId}` (`genxGetCarbonStock`) |
| `Emissions/` | `Emissions` — emissions records (gas, quantity, unit, period, provenance) | `GET /genx/v1/emissions` (`genxListEmissions`); `POST /genx/v1/emissions` (`genxRegisterEmissions`); `GET /genx/v1/emissions/{emissionsDbId}` (`genxGetEmissions`) |
| `SoilChemistry/` | `SoilChemistry` — soil texture, chemistry, and moisture records (texture, chemistry, moisture depth, provenance) | `GET /genx/v1/soil-chemistry` (`genxListSoilChemistry`); `POST /genx/v1/soil-chemistry` (`genxRegisterSoilChemistry`); `GET /genx/v1/soil-chemistry/{soilChemistryDbId}` (`genxGetSoilChemistry`) |
| `EnvironmentalTreatment/` | `EnvironmentalTreatment` — environmental treatment and stress exposure records (type, exposure, provenance) | `GET /genx/v1/environmental-treatments` (`genxListEnvironmentalTreatments`); `POST /genx/v1/environmental-treatments` (`genxRegisterEnvironmentalTreatment`); `GET /genx/v1/environmental-treatments/{environmentalTreatmentDbId}` (`genxGetEnvironmentalTreatment`) |
| `WaterBalance/` | `WaterBalance` — water balance records (period, inputs, outputs, storage change, provenance) | `GET /genx/v1/water-balances` (`genxListWaterBalances`); `POST /genx/v1/water-balances` (`genxRecordWaterBalance`); `GET /genx/v1/water-balances/{waterBalanceDbId}` (`genxGetWaterBalance`) |
| `Farm/` | `Farm` — farm and site reference records (locations, area, provenance) | `GET /genx/v1/farms` (`genxListFarms`); `POST /genx/v1/farms` (`genxRegisterFarm`); `GET /genx/v1/farms/{farmDbId}` (`genxGetFarm`) |
| `FieldScouting/` | `FieldScouting` — field scouting and work order records (type, observations, provenance) | `GET /genx/v1/field-scouting` (`genxListFieldScouting`); `POST /genx/v1/field-scouting` (`genxRegisterFieldScouting`); `GET /genx/v1/field-scouting/{fieldScoutingDbId}` (`genxGetFieldScouting`) |
| `TreatmentAssignment/` | `TreatmentAssignment` — treatment assignment records (field, treatment, provenance) | `GET /genx/v1/treatment-assignments` (`genxListTreatmentAssignments`); `POST /genx/v1/treatment-assignments` (`genxRegisterTreatmentAssignment`); `GET /genx/v1/treatment-assignments/{treatmentAssignmentDbId}` (`genxGetTreatmentAssignment`) |
| `Plot/` | `Plot` — plot identity records (field, plot name, provenance) | `GET /genx/v1/plots` (`genxListPlots`); `POST /genx/v1/plots` (`genxRegisterPlot`); `GET /genx/v1/plots/{plotDbId}` (`genxGetPlot`) |
| `FieldBook/` | `FieldBook` — field book definition records (field, definition, provenance) | `GET /genx/v1/field-books` (`genxListFieldBooks`); `POST /genx/v1/field-books` (`genxRegisterFieldBook`); `GET /genx/v1/field-books/{fieldBookDbId}` (`genxGetFieldBook`) |
| `TrialNetwork/` | `TrialNetwork` — trial network and MET design records (name, provenance) | `GET /genx/v1/trial-networks` (`genxListTrialNetworks`); `POST /genx/v1/trial-networks` (`genxRegisterTrialNetwork`); `GET /genx/v1/trial-networks/{trialNetworkDbId}` (`genxGetTrialNetwork`) |
| `FieldBoundary/` | `FieldBoundary` — operational field boundary and history records (version, geometry reference, provenance) | `GET /genx/v1/field-boundaries` (`genxListFieldBoundaries`); `POST /genx/v1/field-boundaries` (`genxRegisterFieldBoundary`); `GET /genx/v1/field-boundaries/{fieldBoundaryDbId}` (`genxGetFieldBoundary`) |
| `SprayApplication/` | `SprayApplication` — spray application records (product, rate, timestamp, provenance) | `GET /genx/v1/spray-applications` (`genxListSprayApplications`); `POST /genx/v1/spray-applications` (`genxRegisterSprayApplication`); `GET /genx/v1/spray-applications/{sprayApplicationDbId}` (`genxGetSprayApplication`) |
| `YieldMap/` | `YieldMap` — yield map records (storage reference, resolution, digest, provenance) | `GET /genx/v1/yield-maps` (`genxListYieldMaps`); `POST /genx/v1/yield-maps` (`genxRegisterYieldMap`); `GET /genx/v1/yield-maps/{yieldMapDbId}` (`genxGetYieldMap`) |
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
[RFC-068-Water-Balance](./RFC-068-Water-Balance.md),
[RFC-069-Farm](./RFC-069-Farm.md),
[RFC-070-Yield-Map](./RFC-070-Yield-Map.md),
[RFC-071-Marker-Probe](./RFC-071-Marker-Probe.md),
[RFC-072-Genotype-Call-Semantics](./RFC-072-Genotype-Call-Semantics.md),
[RFC-073-Vendor-Order](./RFC-073-Vendor-Order.md),
[RFC-074-Field-Scouting](./RFC-074-Field-Scouting.md),
[RFC-075-Field-Boundary](./RFC-075-Field-Boundary.md),
[RFC-076-Emissions](./RFC-076-Emissions.md),
[RFC-077-Soil-Chemistry](./RFC-077-Soil-Chemistry.md),
[RFC-078-Environmental-Treatment](./RFC-078-Environmental-Treatment.md),
[RFC-079-Developmental-Stage](./RFC-079-Developmental-Stage.md),
[RFC-080-Taxon-Name](./RFC-080-Taxon-Name.md),
[RFC-081-Spray-Application](./RFC-081-Spray-Application.md),
[RFC-082-Units-And-Quantity](./RFC-082-Units-And-Quantity.md),
[RFC-083-External-Vocabulary](./RFC-083-External-Vocabulary.md),
[RFC-084-Terminology-Version](./RFC-084-Terminology-Version.md),
[RFC-085-Ontology-Term](./RFC-085-Ontology-Term.md),
[RFC-086-Ontology-Mapping](./RFC-086-Ontology-Mapping.md),
[RFC-087-Measurement-Scale](./RFC-087-Measurement-Scale.md),
[RFC-088-Crop-Trait-Dictionary](./RFC-088-Crop-Trait-Dictionary.md),
[RFC-089-Project](./RFC-089-Project.md),
[RFC-090-Reusable-List](./RFC-090-Reusable-List.md),
[RFC-091-Calendar](./RFC-091-Calendar.md),
[RFC-092-Location-Geometry](./RFC-092-Location-Geometry.md),
[RFC-093-Reference-Data-Version](./RFC-093-Reference-Data-Version.md),
[RFC-094-Common-Crop-Name](./RFC-094-Common-Crop-Name.md),
[RFC-095-Crop-Species](./RFC-095-Crop-Species.md),
[RFC-096-Institution-Code](./RFC-096-Institution-Code.md),
[RFC-097-Person-Reference](./RFC-097-Person-Reference.md),
[RFC-098-Research-Program](./RFC-098-Research-Program.md),
[RFC-099-Capability-Metadata](./RFC-099-Capability-Metadata.md),
[RFC-100-Research-Location](./RFC-100-Research-Location.md),
[RFC-101-Collecting-Mission](./RFC-101-Collecting-Mission.md),
[RFC-102-Conservation-Membership](./RFC-102-Conservation-Membership.md),
[RFC-103-Mcpd-Adapter](./RFC-103-Mcpd-Adapter.md),
[RFC-104-Duplicate-Review](./RFC-104-Duplicate-Review.md),
[RFC-105-Crosswalk](./RFC-105-Crosswalk.md),
[RFC-106-Treatment-Assignment](./RFC-106-Treatment-Assignment.md),
[RFC-107-Plot](./RFC-107-Plot.md),
[RFC-108-Field-Book](./RFC-108-Field-Book.md),
[RFC-109-Trial-Network](./RFC-109-Trial-Network.md),
[RFC-110-Capture-Workflow](./RFC-110-Capture-Workflow.md),
[RFC-111-Quality-Flag](./RFC-111-Quality-Flag.md),
[RFC-112-Value-Missingness](./RFC-112-Value-Missingness.md),
[RFC-113-Assay-Execution](./RFC-113-Assay-Execution.md),
[RFC-114-Vcf-Export](./RFC-114-Vcf-Export.md),
[RFC-115-Reference-Assembly](./RFC-115-Reference-Assembly.md),
[RFC-116-Pipeline-Provenance](./RFC-116-Pipeline-Provenance.md),
[RFC-117-ExperimentalProtocol](./RFC-117-ExperimentalProtocol.md),
[RFC-118-ArtifactCatalogue](./RFC-118-ArtifactCatalogue.md),
[RFC-119-ProtocolLibrary](./RFC-119-ProtocolLibrary.md),
[RFC-120-PublicationReview](./RFC-120-PublicationReview.md),
[RFC-121-BiodiversityExport](./RFC-121-BiodiversityExport.md),
[RFC-122-EvidencePack](./RFC-122-EvidencePack.md),
[RFC-123-DiseaseObservation](./RFC-123-DiseaseObservation.md),
[RFC-124-DiagnosticEvidence](./RFC-124-DiagnosticEvidence.md),
[RFC-125-IpmStrategy](./RFC-125-IpmStrategy.md),
[RFC-126-ThresholdAlert](./RFC-126-ThresholdAlert.md),
[RFC-127-DiseaseResistance](./RFC-127-DiseaseResistance.md),
[RFC-128-CropHealthImage](./RFC-128-CropHealthImage.md),
[RFC-129-CropRecommendation](./RFC-129-CropRecommendation.md),
[RFC-130-SowingWindow](./RFC-130-SowingWindow.md),
[RFC-131-IrrigationAdvice](./RFC-131-IrrigationAdvice.md).

[DECISIONS.md](./DECISIONS.md) logs deferred questions (D-01…D-20, need
authorization) and autonomous drafting decisions (A-01…A-12, reviewable).

[ENDPOINT-IDENTITY.md](./ENDPOINT-IDENTITY.md) defines stable operation identities and guards against semantic endpoint collisions.

[ADOPTION.md](./ADOPTION.md) is the incremental adoption guide for V2.1
servers (order, compat rules, conformance commands, anti-patterns).
