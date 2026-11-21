# brapi-genx Specification — File and Folder Tree

Generated: 2026-11-21 09:22:52 UTC

Root: `brapi-genx/Specification`

```text
Specification
├── BrAPI-Core
│   ├── Common Crop Names
│   │   ├── CommonCropNames_GET.yaml
│   │   ├── GroupDescription.md
│   │   └── README.md
│   ├── Lists
│   │   ├── Schemas
│   │   │   ├── ListBaseFields.yaml
│   │   │   ├── ListDetails.yaml
│   │   │   ├── ListNewRequest.yaml
│   │   │   ├── ListSearchRequest.yaml
│   │   │   ├── ListSummary.yaml
│   │   │   └── ListTypes.yaml
│   │   ├── GroupDescription.md
│   │   ├── Lists_GET_POST.yaml
│   │   ├── Lists_ListDbId_Data_POST.yaml
│   │   ├── Lists_ListDbId_GET_PUT.yaml
│   │   ├── Lists_ListDbId_Items_POST.yaml
│   │   ├── README.md
│   │   ├── Search_Lists_POST.yaml
│   │   └── Search_Lists_SearchResultsDbId_GET.yaml
│   ├── Locations
│   │   ├── Schemas
│   │   │   ├── Location.yaml
│   │   │   ├── LocationNewRequest.yaml
│   │   │   └── LocationSearchRequest.yaml
│   │   ├── GroupDescription.md
│   │   ├── Locations_GET_POST.yaml
│   │   ├── Locations_LocationDbId_GET_PUT.yaml
│   │   ├── README.md
│   │   ├── Search_Locations_POST.yaml
│   │   └── Search_Locations_SearchResultsDbId_GET.yaml
│   ├── People
│   │   ├── Schemas
│   │   │   ├── Person.yaml
│   │   │   ├── PersonNewRequest.yaml
│   │   │   └── PersonSearchRequest.yaml
│   │   ├── GroupDescription.md
│   │   ├── People_GET_POST.yaml
│   │   ├── People_PersonDbId_GET_PUT.yaml
│   │   ├── README.md
│   │   ├── Search_People_POST.yaml
│   │   └── Search_People_SearchResultsDbId_GET.yaml
│   ├── Programs
│   │   ├── Schemas
│   │   │   ├── Program.yaml
│   │   │   ├── ProgramNewRequest.yaml
│   │   │   └── ProgramSearchRequest.yaml
│   │   ├── GroupDescription.md
│   │   ├── Programs_GET_POST.yaml
│   │   ├── Programs_ProgramDbId_GET_PUT.yaml
│   │   ├── README.md
│   │   ├── Search_Programs_POST.yaml
│   │   └── Search_Programs_SearchResultsDbId_GET.yaml
│   ├── Seasons
│   │   ├── Schemas
│   │   │   └── Season.yaml
│   │   ├── GroupDescription.md
│   │   ├── README.md
│   │   ├── Seasons_GET_POST.yaml
│   │   └── Seasons_SeasonDbId_GET_PUT.yaml
│   ├── ServerInfo
│   │   ├── Schemas
│   │   │   ├── ServerInfo.yaml
│   │   │   └── Service.yaml
│   │   ├── GroupDescription.md
│   │   ├── README.md
│   │   └── ServerInfo_GET.yaml
│   ├── Studies
│   │   ├── Schemas
│   │   │   ├── DataLink.yaml
│   │   │   ├── EnvironmentParameter.yaml
│   │   │   ├── Study.yaml
│   │   │   ├── StudyNewRequest.yaml
│   │   │   └── StudySearchRequest.yaml
│   │   ├── GroupDescription.md
│   │   ├── README.md
│   │   ├── Search_Studies_POST.yaml
│   │   ├── Search_Studies_SearchResultsDbId_GET.yaml
│   │   ├── Studies_GET_POST.yaml
│   │   ├── Studies_StudyDbId_GET_PUT.yaml
│   │   └── StudyTypes_GET.yaml
│   ├── Trials
│   │   ├── Schemas
│   │   │   ├── Contact.yaml
│   │   │   ├── Trial.yaml
│   │   │   ├── TrialNewRequest.yaml
│   │   │   └── TrialSearchRequest.yaml
│   │   ├── GroupDescription.md
│   │   ├── README.md
│   │   ├── Search_Trials_POST.yaml
│   │   ├── Search_Trials_SearchResultsDbId_GET.yaml
│   │   ├── Trials_GET_POST.yaml
│   │   └── Trials_TrialDbId_GET_PUT.yaml
│   ├── README.md
│   └── swaggerMetaData.yaml
├── BrAPI-GenX
│   ├── Breeding
│   │   ├── BreedingPipeline
│   │   │   ├── Schemas
│   │   │   │   ├── BreedingPipeline.yaml
│   │   │   │   └── BreedingPipelineNewRequest.yaml
│   │   │   ├── BreedingPipeline_BreedingPipelineDbId_GET.yaml
│   │   │   ├── BreedingPipeline_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── CandidateVarietyLifecycle
│   │   │   ├── Schemas
│   │   │   │   ├── CandidateVariety.yaml
│   │   │   │   └── CandidateVarietyNewRequest.yaml
│   │   │   ├── CandidateVarietyLifecycle_CandidateVarietyDbId_GET.yaml
│   │   │   ├── CandidateVarietyLifecycle_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── CrossingSchedule
│   │   │   ├── Schemas
│   │   │   │   ├── CrossingSchedule.yaml
│   │   │   │   └── CrossingScheduleNewRequest.yaml
│   │   │   ├── CrossingSchedule_CrossingScheduleDbId_GET.yaml
│   │   │   ├── CrossingSchedule_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── DoubledHaploid
│   │   │   ├── Schemas
│   │   │   │   ├── DoubledHaploidProgram.yaml
│   │   │   │   └── DoubledHaploidProgramNewRequest.yaml
│   │   │   ├── DoubledHaploid_DoubledHaploidProgramDbId_GET.yaml
│   │   │   ├── DoubledHaploid_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── ExperimentalDesign
│   │   │   ├── Schemas
│   │   │   │   ├── ExperimentalDesign.yaml
│   │   │   │   └── ExperimentalDesignNewRequest.yaml
│   │   │   ├── ExperimentalDesign_ExperimentalDesignDbId_GET.yaml
│   │   │   ├── ExperimentalDesign_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── ExperimentalProtocol
│   │   │   ├── Schemas
│   │   │   │   ├── ExperimentalProtocol.yaml
│   │   │   │   └── ExperimentalProtocolNewRequest.yaml
│   │   │   ├── ExperimentalProtocol_ExperimentalProtocolDbId_GET.yaml
│   │   │   ├── ExperimentalProtocol_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── FieldBook
│   │   │   ├── Schemas
│   │   │   │   ├── FieldBook.yaml
│   │   │   │   └── FieldBookNewRequest.yaml
│   │   │   ├── FieldBook_FieldBookDbId_GET.yaml
│   │   │   ├── FieldBook_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── GeneticGain
│   │   │   ├── Schemas
│   │   │   │   ├── GeneticGainRecord.yaml
│   │   │   │   └── GeneticGainRecordNewRequest.yaml
│   │   │   ├── GeneticGain_GET_POST.yaml
│   │   │   ├── GeneticGain_GeneticGainRecordDbId_GET.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── GenomicPrediction
│   │   │   ├── Schemas
│   │   │   │   ├── GenomicPrediction.yaml
│   │   │   │   └── GenomicPredictionNewRequest.yaml
│   │   │   ├── GenomicPrediction_GET_POST.yaml
│   │   │   ├── GenomicPrediction_GenomicPredictionDbId_GET.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── GenomicSelection
│   │   │   ├── Schemas
│   │   │   │   ├── GenomicSelection.yaml
│   │   │   │   └── GenomicSelectionNewRequest.yaml
│   │   │   ├── GenomicSelection_GET_POST.yaml
│   │   │   ├── GenomicSelection_GenomicSelectionDbId_GET.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── GxeAnalysis
│   │   │   ├── Schemas
│   │   │   │   ├── GxeAnalysisResult.yaml
│   │   │   │   └── GxeAnalysisResultNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── GxeAnalysis_GET_POST.yaml
│   │   │   ├── GxeAnalysis_GxeAnalysisResultDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── Heritability
│   │   │   ├── Schemas
│   │   │   │   ├── HeritabilityEstimate.yaml
│   │   │   │   └── HeritabilityEstimateNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── Heritability_GET_POST.yaml
│   │   │   ├── Heritability_HeritabilityEstimateDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── Kinship
│   │   │   ├── Schemas
│   │   │   │   ├── KinshipMatrix.yaml
│   │   │   │   └── KinshipMatrixNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── Kinship_GET_POST.yaml
│   │   │   ├── Kinship_KinshipMatrixDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── ParentCandidateSelection
│   │   │   ├── Schemas
│   │   │   │   ├── ParentCandidateSelection.yaml
│   │   │   │   └── ParentCandidateSelectionNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── ParentCandidateSelection_GET_POST.yaml
│   │   │   ├── ParentCandidateSelection_ParentCandidateSelectionDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── PedigreeAnalysis
│   │   │   ├── Schemas
│   │   │   │   ├── PedigreeAnalysis.yaml
│   │   │   │   └── PedigreeAnalysisNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── PedigreeAnalysis_GET_POST.yaml
│   │   │   ├── PedigreeAnalysis_PedigreeAnalysisDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── Plot
│   │   │   ├── Schemas
│   │   │   │   ├── Plot.yaml
│   │   │   │   └── PlotNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── Plot_GET_POST.yaml
│   │   │   ├── Plot_PlotDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── PopulationAdvancement
│   │   │   ├── Schemas
│   │   │   │   ├── PopulationAdvancement.yaml
│   │   │   │   └── PopulationAdvancementNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── PopulationAdvancement_GET_POST.yaml
│   │   │   ├── PopulationAdvancement_PopulationAdvancementDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── ProgenyRecords
│   │   │   ├── Schemas
│   │   │   │   ├── ProgenyRecord.yaml
│   │   │   │   └── ProgenyRecordNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── ProgenyRecords_GET_POST.yaml
│   │   │   ├── ProgenyRecords_ProgenyRecordDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── SelectionDecisions
│   │   │   ├── Schemas
│   │   │   │   ├── SelectionDecision.yaml
│   │   │   │   └── SelectionDecisionNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── SelectionDecisions_GET_POST.yaml
│   │   │   └── SelectionDecisions_SelectionDecisionDbId_GET.yaml
│   │   ├── SpeedBreeding
│   │   │   ├── Schemas
│   │   │   │   ├── SpeedBreedingProtocol.yaml
│   │   │   │   └── SpeedBreedingProtocolNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── SpeedBreeding_GET_POST.yaml
│   │   │   └── SpeedBreeding_SpeedBreedingProtocolDbId_GET.yaml
│   │   ├── StabilityAnalysis
│   │   │   ├── Schemas
│   │   │   │   ├── StabilityAnalysisResult.yaml
│   │   │   │   └── StabilityAnalysisResultNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── StabilityAnalysis_GET_POST.yaml
│   │   │   └── StabilityAnalysis_StabilityAnalysisResultDbId_GET.yaml
│   │   ├── TreatmentAssignment
│   │   │   ├── Schemas
│   │   │   │   ├── TreatmentAssignment.yaml
│   │   │   │   └── TreatmentAssignmentNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── TreatmentAssignment_GET_POST.yaml
│   │   │   └── TreatmentAssignment_TreatmentAssignmentDbId_GET.yaml
│   │   ├── TrialNetwork
│   │   │   ├── Schemas
│   │   │   │   ├── TrialNetwork.yaml
│   │   │   │   └── TrialNetworkNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── TrialNetwork_GET_POST.yaml
│   │   │   └── TrialNetwork_TrialNetworkDbId_GET.yaml
│   │   └── README.md
│   ├── Conformance
│   │   ├── fixtures
│   │   │   ├── job_accepted.json
│   │   │   ├── job_completed.json
│   │   │   ├── job_submit.json
│   │   │   ├── job_submit_conflict.json
│   │   │   ├── job_submit_replay.json
│   │   │   ├── ledger_accepted.json
│   │   │   ├── ledger_submit.json
│   │   │   ├── ledger_submit_conflict.json
│   │   │   ├── ledger_submit_replay.json
│   │   │   ├── matrix_accepted.json
│   │   │   ├── matrix_submit.json
│   │   │   ├── matrix_submit_conflict.json
│   │   │   ├── matrix_submit_replay.json
│   │   │   ├── model_accepted.json
│   │   │   ├── model_submit.json
│   │   │   ├── model_submit_conflict.json
│   │   │   ├── model_submit_replay.json
│   │   │   ├── package_accepted.json
│   │   │   ├── package_embargoed.json
│   │   │   ├── package_submit.json
│   │   │   ├── package_submit_conflict.json
│   │   │   ├── package_submit_replay.json
│   │   │   ├── provenanced_observation.json
│   │   │   ├── serverinfo_v21_only.json
│   │   │   ├── serverinfov3.json
│   │   │   ├── telemetry_batch.json
│   │   │   ├── telemetry_batch_conflict.json
│   │   │   ├── telemetry_batch_replay.json
│   │   │   ├── term_accepted.json
│   │   │   ├── term_submit.json
│   │   │   ├── term_submit_conflict.json
│   │   │   └── term_submit_replay.json
│   │   ├── DIGEST-DECISION-BRIEF.md
│   │   ├── DIGEST-INTEROPERABILITY.md
│   │   ├── DIGEST-SCOPE-INVENTORY.md
│   │   ├── README.md
│   │   ├── RESULTS.md
│   │   ├── capability-registry.json
│   │   ├── digest-vectors.json
│   │   ├── domain-classification.yaml
│   │   ├── endpoint-overlaps.yaml
│   │   └── probes.yaml
│   ├── Core
│   │   ├── CapabilityMetadata
│   │   │   ├── Schemas
│   │   │   │   ├── CapabilityMetadata.yaml
│   │   │   │   └── CapabilityMetadataNewRequest.yaml
│   │   │   ├── CapabilityMetadata_CapabilityMetadataDbId_GET.yaml
│   │   │   ├── CapabilityMetadata_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── CapabilityNegotiation
│   │   │   ├── Schemas
│   │   │   │   ├── CapabilityNegotiation.yaml
│   │   │   │   └── CapabilityNegotiationNewRequest.yaml
│   │   │   ├── CapabilityNegotiation_CapabilityNegotiationDbId_GET.yaml
│   │   │   ├── CapabilityNegotiation_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── Jobs
│   │   │   ├── Schemas
│   │   │   │   ├── Job.yaml
│   │   │   │   └── JobNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── Jobs_GET_POST.yaml
│   │   │   ├── Jobs_JobDbId_GET_DELETE.yaml
│   │   │   └── README.md
│   │   ├── Provenance
│   │   │   ├── Schemas
│   │   │   │   └── ProvenanceEnvelope.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── ServerInfoV3
│   │   │   ├── Schemas
│   │   │   │   └── ServerInfoV3.yaml
│   │   │   ├── CAPABILITY-NEGOTIATION.md
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   └── ServerInfoV3_GET.yaml
│   │   └── README.md
│   ├── CropProduction
│   │   ├── CropCycle
│   │   │   ├── Schemas
│   │   │   │   ├── CropCycle.yaml
│   │   │   │   └── CropCycleNewRequest.yaml
│   │   │   ├── CropCycle_CropCycleDbId_GET.yaml
│   │   │   ├── CropCycle_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── CropRecommendation
│   │   │   ├── Schemas
│   │   │   │   ├── CropRecommendation.yaml
│   │   │   │   └── CropRecommendationNewRequest.yaml
│   │   │   ├── CropRecommendation_CropRecommendationDbId_GET.yaml
│   │   │   ├── CropRecommendation_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── CropSuitability
│   │   │   ├── Schemas
│   │   │   │   ├── CropSuitability.yaml
│   │   │   │   └── CropSuitabilityNewRequest.yaml
│   │   │   ├── CropSuitability_CropSuitabilityDbId_GET.yaml
│   │   │   ├── CropSuitability_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── Farm
│   │   │   ├── Schemas
│   │   │   │   ├── Farm.yaml
│   │   │   │   └── FarmNewRequest.yaml
│   │   │   ├── Farm_FarmDbId_GET.yaml
│   │   │   ├── Farm_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── FertilizerApplication
│   │   │   ├── Schemas
│   │   │   │   ├── FertilizerApplication.yaml
│   │   │   │   └── FertilizerApplicationNewRequest.yaml
│   │   │   ├── FertilizerApplication_FertilizerApplicationDbId_GET.yaml
│   │   │   ├── FertilizerApplication_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── HarvestRecords
│   │   │   ├── Schemas
│   │   │   │   ├── HarvestRecord.yaml
│   │   │   │   └── HarvestRecordNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── HarvestRecords_GET_POST.yaml
│   │   │   ├── HarvestRecords_HarvestRecordDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── IrrigationAdvice
│   │   │   ├── Schemas
│   │   │   │   ├── IrrigationAdvice.yaml
│   │   │   │   └── IrrigationAdviceNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── IrrigationAdvice_GET_POST.yaml
│   │   │   ├── IrrigationAdvice_IrrigationAdviceDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── IrrigationOperation
│   │   │   ├── Schemas
│   │   │   │   ├── IrrigationEvent.yaml
│   │   │   │   └── IrrigationEventNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── IrrigationOperation_GET_POST.yaml
│   │   │   ├── IrrigationOperation_IrrigationEventDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── LocalConstraint
│   │   │   ├── Schemas
│   │   │   │   ├── LocalConstraint.yaml
│   │   │   │   └── LocalConstraintNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── LocalConstraint_GET_POST.yaml
│   │   │   ├── LocalConstraint_LocalConstraintDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── LotLedger
│   │   │   ├── Schemas
│   │   │   │   ├── LotLedgerEntry.yaml
│   │   │   │   └── LotLedgerEntryNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── Ledger_GET_POST.yaml
│   │   │   └── README.md
│   │   ├── NutrientAdvice
│   │   │   ├── Schemas
│   │   │   │   ├── NutrientAdvice.yaml
│   │   │   │   └── NutrientAdviceNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── NutrientAdvice_GET_POST.yaml
│   │   │   ├── NutrientAdvice_NutrientAdviceDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── PlantingOperation
│   │   │   ├── Schemas
│   │   │   │   ├── PlantingOperation.yaml
│   │   │   │   └── PlantingOperationNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── PlantingOperation_GET_POST.yaml
│   │   │   ├── PlantingOperation_PlantingOperationDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── SowingWindow
│   │   │   ├── Schemas
│   │   │   │   ├── SowingWindow.yaml
│   │   │   │   └── SowingWindowNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── SowingWindow_GET_POST.yaml
│   │   │   └── SowingWindow_SowingWindowDbId_GET.yaml
│   │   ├── SprayApplication
│   │   │   ├── Schemas
│   │   │   │   ├── SprayApplication.yaml
│   │   │   │   └── SprayApplicationNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── SprayApplication_GET_POST.yaml
│   │   │   └── SprayApplication_SprayApplicationDbId_GET.yaml
│   │   ├── Tillage
│   │   │   ├── Schemas
│   │   │   │   ├── TillageRecord.yaml
│   │   │   │   └── TillageRecordNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── Tillage_GET_POST.yaml
│   │   │   └── Tillage_TillageRecordDbId_GET.yaml
│   │   ├── YieldForecast
│   │   │   ├── Schemas
│   │   │   │   ├── YieldForecast.yaml
│   │   │   │   └── YieldForecastNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── YieldForecast_GET_POST.yaml
│   │   │   └── YieldForecast_YieldForecastDbId_GET.yaml
│   │   └── README.md
│   ├── Environment
│   │   ├── CarbonStock
│   │   │   ├── Schemas
│   │   │   │   ├── CarbonStock.yaml
│   │   │   │   └── CarbonStockNewRequest.yaml
│   │   │   ├── CarbonStock_CarbonStockDbId_GET.yaml
│   │   │   ├── CarbonStock_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── ClimateNormals
│   │   │   ├── Schemas
│   │   │   │   ├── ClimateNormal.yaml
│   │   │   │   └── ClimateNormalNewRequest.yaml
│   │   │   ├── ClimateNormals_ClimateNormalDbId_GET.yaml
│   │   │   ├── ClimateNormals_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── Emissions
│   │   │   ├── Schemas
│   │   │   │   ├── Emissions.yaml
│   │   │   │   └── EmissionsNewRequest.yaml
│   │   │   ├── Emissions_EmissionsDbId_GET.yaml
│   │   │   ├── Emissions_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── EnvironmentalTreatment
│   │   │   ├── Schemas
│   │   │   │   ├── EnvironmentalTreatment.yaml
│   │   │   │   └── EnvironmentalTreatmentNewRequest.yaml
│   │   │   ├── EnvironmentalTreatment_EnvironmentalTreatmentDbId_GET.yaml
│   │   │   ├── EnvironmentalTreatment_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── ExtremeWeather
│   │   │   ├── Schemas
│   │   │   │   ├── ExtremeWeatherEvent.yaml
│   │   │   │   └── ExtremeWeatherEventNewRequest.yaml
│   │   │   ├── ExtremeWeather_ExtremeWeatherEventDbId_GET.yaml
│   │   │   ├── ExtremeWeather_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── SoilChemistry
│   │   │   ├── Schemas
│   │   │   │   ├── SoilChemistry.yaml
│   │   │   │   └── SoilChemistryNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── SoilChemistry_GET_POST.yaml
│   │   │   └── SoilChemistry_SoilChemistryDbId_GET.yaml
│   │   ├── SoilProfile
│   │   │   ├── Schemas
│   │   │   │   ├── SoilProfile.yaml
│   │   │   │   └── SoilProfileNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── SoilProfile_GET_POST.yaml
│   │   │   └── SoilProfile_SoilProfileDbId_GET.yaml
│   │   ├── WaterBalance
│   │   │   ├── Schemas
│   │   │   │   ├── WaterBalance.yaml
│   │   │   │   └── WaterBalanceNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── WaterBalance_GET_POST.yaml
│   │   │   └── WaterBalance_WaterBalanceDbId_GET.yaml
│   │   ├── WeatherForecast
│   │   │   ├── Schemas
│   │   │   │   ├── WeatherForecast.yaml
│   │   │   │   └── WeatherForecastNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── WeatherForecast_GET_POST.yaml
│   │   │   └── WeatherForecast_WeatherForecastDbId_GET.yaml
│   │   ├── WeatherObservations
│   │   │   ├── Schemas
│   │   │   │   ├── WeatherObservation.yaml
│   │   │   │   └── WeatherObservationNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── WeatherObservations_GET_POST.yaml
│   │   │   └── WeatherObservations_WeatherObservationDbId_GET.yaml
│   │   └── README.md
│   ├── Genotyping
│   │   ├── AssayDesign
│   │   │   ├── Schemas
│   │   │   │   ├── AssayDesign.yaml
│   │   │   │   └── AssayDesignNewRequest.yaml
│   │   │   ├── AssayDesign_AssayDesignDbId_GET.yaml
│   │   │   ├── AssayDesign_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── AssayExecution
│   │   │   ├── Schemas
│   │   │   │   ├── AssayExecution.yaml
│   │   │   │   └── AssayExecutionNewRequest.yaml
│   │   │   ├── AssayExecution_AssayExecutionDbId_GET.yaml
│   │   │   ├── AssayExecution_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── ExpressionQtl
│   │   │   ├── Schemas
│   │   │   │   ├── ExpressionQtl.yaml
│   │   │   │   └── ExpressionQtlNewRequest.yaml
│   │   │   ├── ExpressionQtl_ExpressionQtlDbId_GET.yaml
│   │   │   ├── ExpressionQtl_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── GenomicDatasets
│   │   │   ├── Schemas
│   │   │   │   ├── GenomicDataset.yaml
│   │   │   │   └── GenomicDatasetNewRequest.yaml
│   │   │   ├── GenomicDatasets_GET_POST.yaml
│   │   │   ├── GenomicDatasets_GenomicDatasetDbId_GET.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── GenomicRelationship
│   │   │   ├── Schemas
│   │   │   │   ├── GenomicRelationship.yaml
│   │   │   │   └── GenomicRelationshipNewRequest.yaml
│   │   │   ├── GenomicRelationship_GET_POST.yaml
│   │   │   ├── GenomicRelationship_GenomicRelationshipDbId_GET.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── Genomics
│   │   │   ├── Schemas
│   │   │   │   ├── VariantMatrix.yaml
│   │   │   │   └── VariantMatrixNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── VariantMatrices_GET_POST.yaml
│   │   │   └── VariantMatrices_MatrixDbId_GET.yaml
│   │   ├── GenotypeCallSemantics
│   │   │   ├── Schemas
│   │   │   │   ├── GenotypeCallSemantics.yaml
│   │   │   │   └── GenotypeCallSemanticsNewRequest.yaml
│   │   │   ├── GenotypeCallSemantics_GET_POST.yaml
│   │   │   ├── GenotypeCallSemantics_GenotypeCallSemanticsDbId_GET.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── GenotypeQc
│   │   │   ├── Schemas
│   │   │   │   ├── GenotypeQcReport.yaml
│   │   │   │   └── GenotypeQcReportNewRequest.yaml
│   │   │   ├── GenotypeQcReport_GET_POST.yaml
│   │   │   ├── GenotypeQcReport_GenotypeQcReportDbId_GET.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── GwasResult
│   │   │   ├── Schemas
│   │   │   │   ├── GwasResult.yaml
│   │   │   │   └── GwasResultNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── GwasResult_GET_POST.yaml
│   │   │   ├── GwasResult_GwasResultDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── HaplotypeAnalysis
│   │   │   ├── Schemas
│   │   │   │   ├── HaplotypeAnalysis.yaml
│   │   │   │   └── HaplotypeAnalysisNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── HaplotypeAnalysis_GET_POST.yaml
│   │   │   ├── HaplotypeAnalysis_HaplotypeAnalysisDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── MarkerProbe
│   │   │   ├── Schemas
│   │   │   │   ├── MarkerProbe.yaml
│   │   │   │   └── MarkerProbeNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── MarkerProbe_GET_POST.yaml
│   │   │   ├── MarkerProbe_MarkerProbeDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── MethylationAnalysis
│   │   │   ├── Schemas
│   │   │   │   ├── MethylationAnalysis.yaml
│   │   │   │   └── MethylationAnalysisNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── MethylationAnalysis_GET_POST.yaml
│   │   │   ├── MethylationAnalysis_MethylationAnalysisDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── PipelineProvenance
│   │   │   ├── Schemas
│   │   │   │   ├── PipelineProvenance.yaml
│   │   │   │   └── PipelineProvenanceNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── PipelineProvenance_GET_POST.yaml
│   │   │   ├── PipelineProvenance_PipelineProvenanceDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── ReferenceAssembly
│   │   │   ├── Schemas
│   │   │   │   ├── ReferenceAssembly.yaml
│   │   │   │   └── ReferenceAssemblyNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── ReferenceAssembly_GET_POST.yaml
│   │   │   └── ReferenceAssembly_ReferenceAssemblyDbId_GET.yaml
│   │   ├── VariantAnnotation
│   │   │   ├── Schemas
│   │   │   │   ├── VariantAnnotation.yaml
│   │   │   │   └── VariantAnnotationNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── VariantAnnotation_GET_POST.yaml
│   │   │   └── VariantAnnotation_VariantAnnotationDbId_GET.yaml
│   │   ├── VcfExport
│   │   │   ├── Schemas
│   │   │   │   ├── VcfExport.yaml
│   │   │   │   └── VcfExportNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── VcfExport_GET_POST.yaml
│   │   │   └── VcfExport_VcfExportDbId_GET.yaml
│   │   ├── VcfImport
│   │   │   ├── Schemas
│   │   │   │   ├── VcfImport.yaml
│   │   │   │   └── VcfImportNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── VcfImport_GET_POST.yaml
│   │   │   └── VcfImport_VcfImportDbId_GET.yaml
│   │   ├── VendorOrder
│   │   │   ├── Schemas
│   │   │   │   ├── VendorOrder.yaml
│   │   │   │   └── VendorOrderNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── VendorOrder_GET_POST.yaml
│   │   │   └── VendorOrder_VendorOrderDbId_GET.yaml
│   │   └── README.md
│   ├── Geospatial
│   │   ├── CloudMask
│   │   │   ├── Schemas
│   │   │   │   ├── CloudMask.yaml
│   │   │   │   └── CloudMaskNewRequest.yaml
│   │   │   ├── CloudMask_CloudMaskDbId_GET.yaml
│   │   │   ├── CloudMask_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── CrsTransform
│   │   │   ├── Schemas
│   │   │   │   ├── CrsTransform.yaml
│   │   │   │   └── CrsTransformNewRequest.yaml
│   │   │   ├── CrsTransform_CrsTransformDbId_GET.yaml
│   │   │   ├── CrsTransform_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── FieldBoundary
│   │   │   ├── Schemas
│   │   │   │   ├── FieldBoundary.yaml
│   │   │   │   └── FieldBoundaryNewRequest.yaml
│   │   │   ├── FieldBoundary_FieldBoundaryDbId_GET.yaml
│   │   │   ├── FieldBoundary_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── FieldGeometry
│   │   │   ├── Schemas
│   │   │   │   ├── FieldGeometry.yaml
│   │   │   │   └── FieldGeometryNewRequest.yaml
│   │   │   ├── FieldGeometry_FieldGeometryDbId_GET.yaml
│   │   │   ├── FieldGeometry_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── LocationGeometry
│   │   │   ├── Schemas
│   │   │   │   ├── LocationGeometry.yaml
│   │   │   │   └── LocationGeometryNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── LocationGeometry_GET_POST.yaml
│   │   │   ├── LocationGeometry_LocationGeometryDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── RasterCatalogue
│   │   │   ├── Schemas
│   │   │   │   ├── RasterCatalogue.yaml
│   │   │   │   └── RasterCatalogueNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── RasterCatalogue_GET_POST.yaml
│   │   │   └── RasterCatalogue_RasterCatalogueDbId_GET.yaml
│   │   ├── RemoteSensingMetadata
│   │   │   ├── Schemas
│   │   │   │   ├── RemoteSensingMetadata.yaml
│   │   │   │   └── RemoteSensingMetadataNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── RemoteSensingMetadata_GET_POST.yaml
│   │   │   └── RemoteSensingMetadata_RemoteSensingMetadataDbId_GET.yaml
│   │   ├── SpatialIndex
│   │   │   ├── Schemas
│   │   │   │   ├── SpatialIndex.yaml
│   │   │   │   └── SpatialIndexNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── SpatialIndex_GET_POST.yaml
│   │   │   └── SpatialIndex_SpatialIndexDbId_GET.yaml
│   │   ├── SpatialQuery
│   │   │   ├── Schemas
│   │   │   │   ├── SpatialQuery.yaml
│   │   │   │   └── SpatialQueryNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── SpatialQuery_GET_POST.yaml
│   │   │   └── SpatialQuery_SpatialQueryDbId_GET.yaml
│   │   ├── VegetationIndex
│   │   │   ├── Schemas
│   │   │   │   ├── VegetationIndex.yaml
│   │   │   │   └── VegetationIndexNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── VegetationIndex_GET_POST.yaml
│   │   │   └── VegetationIndex_VegetationIndexDbId_GET.yaml
│   │   ├── YieldMap
│   │   │   ├── Schemas
│   │   │   │   ├── YieldMap.yaml
│   │   │   │   └── YieldMapNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── YieldMap_GET_POST.yaml
│   │   │   └── YieldMap_YieldMapDbId_GET.yaml
│   │   └── README.md
│   ├── Germplasm
│   │   ├── Acquisition
│   │   │   ├── Schemas
│   │   │   │   ├── AcquisitionRecord.yaml
│   │   │   │   └── AcquisitionRecordNewRequest.yaml
│   │   │   ├── Acquisition_AcquisitionRecordDbId_GET.yaml
│   │   │   ├── Acquisition_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── CollectingMission
│   │   │   ├── Schemas
│   │   │   │   ├── CollectingMission.yaml
│   │   │   │   └── CollectingMissionNewRequest.yaml
│   │   │   ├── CollectingMission_CollectingMissionDbId_GET.yaml
│   │   │   ├── CollectingMission_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── ConservationMembership
│   │   │   ├── Schemas
│   │   │   │   ├── ConservationMembership.yaml
│   │   │   │   └── ConservationMembershipNewRequest.yaml
│   │   │   ├── ConservationMembership_ConservationMembershipDbId_GET.yaml
│   │   │   ├── ConservationMembership_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── CustodyTransfer
│   │   │   ├── Schemas
│   │   │   │   ├── CustodyTransfer.yaml
│   │   │   │   └── CustodyTransferNewRequest.yaml
│   │   │   ├── CustodyTransfer_CustodyTransferDbId_GET.yaml
│   │   │   ├── CustodyTransfer_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── DisposalRecord
│   │   │   ├── Schemas
│   │   │   │   ├── DisposalRecord.yaml
│   │   │   │   └── DisposalRecordNewRequest.yaml
│   │   │   ├── DisposalRecord_DisposalRecordDbId_GET.yaml
│   │   │   ├── DisposalRecord_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── DuplicateReview
│   │   │   ├── Schemas
│   │   │   │   ├── DuplicateReview.yaml
│   │   │   │   └── DuplicateReviewNewRequest.yaml
│   │   │   ├── DuplicateReview_DuplicateReviewDbId_GET.yaml
│   │   │   ├── DuplicateReview_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── GenebankStorage
│   │   │   ├── Schemas
│   │   │   │   ├── StorageLocation.yaml
│   │   │   │   └── StorageLocationNewRequest.yaml
│   │   │   ├── GenebankStorage_GET_POST.yaml
│   │   │   ├── GenebankStorage_StorageLocationDbId_GET.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── McpdAdapter
│   │   │   ├── Schemas
│   │   │   │   ├── McpdAdapter.yaml
│   │   │   │   └── McpdAdapterNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── McpdAdapter_GET_POST.yaml
│   │   │   ├── McpdAdapter_McpdAdapterDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── Quarantine
│   │   │   ├── Schemas
│   │   │   │   ├── QuarantineRecord.yaml
│   │   │   │   └── QuarantineRecordNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── Quarantine_GET_POST.yaml
│   │   │   ├── Quarantine_QuarantineRecordDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── Regeneration
│   │   │   ├── Schemas
│   │   │   │   ├── RegenerationRecord.yaml
│   │   │   │   └── RegenerationRecordNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── Regeneration_GET_POST.yaml
│   │   │   └── Regeneration_RegenerationRecordDbId_GET.yaml
│   │   ├── SafetyDuplication
│   │   │   ├── Schemas
│   │   │   │   ├── SafetyDuplication.yaml
│   │   │   │   └── SafetyDuplicationNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── SafetyDuplication_GET_POST.yaml
│   │   │   └── SafetyDuplication_SafetyDuplicationDbId_GET.yaml
│   │   ├── ViabilityTesting
│   │   │   ├── Schemas
│   │   │   │   ├── ViabilityTest.yaml
│   │   │   │   └── ViabilityTestNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── ViabilityTesting_GET_POST.yaml
│   │   │   └── ViabilityTesting_ViabilityTestDbId_GET.yaml
│   │   └── README.md
│   ├── Instrumentation
│   │   ├── CalibrationQuality
│   │   │   ├── Schemas
│   │   │   │   ├── CalibrationQuality.yaml
│   │   │   │   └── CalibrationQualityNewRequest.yaml
│   │   │   ├── CalibrationQuality_CalibrationQualityDbId_GET.yaml
│   │   │   ├── CalibrationQuality_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── EdgeGatewayHealth
│   │   │   ├── Schemas
│   │   │   │   ├── EdgeGatewayHealth.yaml
│   │   │   │   └── EdgeGatewayHealthNewRequest.yaml
│   │   │   ├── EdgeGatewayHealth_EdgeGatewayHealthDbId_GET.yaml
│   │   │   ├── EdgeGatewayHealth_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── SensorDevice
│   │   │   ├── Schemas
│   │   │   │   ├── SensorDevice.yaml
│   │   │   │   └── SensorDeviceNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── SensorDevice_GET_POST.yaml
│   │   │   └── SensorDevice_SensorDeviceDbId_GET.yaml
│   │   ├── Telemetry
│   │   │   ├── Schemas
│   │   │   │   └── TelemetryPoint.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   └── Telemetry_GET_POST.yaml
│   │   ├── TelemetryNormalization
│   │   │   ├── Schemas
│   │   │   │   ├── TelemetryNormalization.yaml
│   │   │   │   └── TelemetryNormalizationNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── TelemetryNormalization_GET_POST.yaml
│   │   │   └── TelemetryNormalization_TelemetryNormalizationDbId_GET.yaml
│   │   └── README.md
│   ├── Interoperability
│   │   ├── BiodiversityExport
│   │   │   ├── Schemas
│   │   │   │   ├── BiodiversityExport.yaml
│   │   │   │   └── BiodiversityExportNewRequest.yaml
│   │   │   ├── BiodiversityExport_BiodiversityExportDbId_GET.yaml
│   │   │   ├── BiodiversityExport_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── ConformanceProbe
│   │   │   ├── Schemas
│   │   │   │   ├── ConformanceProbe.yaml
│   │   │   │   └── ConformanceProbeNewRequest.yaml
│   │   │   ├── ConformanceProbe_ConformanceProbeDbId_GET.yaml
│   │   │   ├── ConformanceProbe_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── Crosswalk
│   │   │   ├── Schemas
│   │   │   │   ├── Crosswalk.yaml
│   │   │   │   └── CrosswalkNewRequest.yaml
│   │   │   ├── Crosswalk_CrosswalkDbId_GET.yaml
│   │   │   ├── Crosswalk_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── FAIR
│   │   │   ├── Schemas
│   │   │   │   ├── FAIRPackage.yaml
│   │   │   │   └── FAIRPackageNewRequest.yaml
│   │   │   ├── FairPackages_GET_POST.yaml
│   │   │   ├── FairPackages_PackageDbId_GET.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── SchemaMapping
│   │   │   ├── Schemas
│   │   │   │   ├── SchemaMapping.yaml
│   │   │   │   └── SchemaMappingNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── SchemaMapping_GET_POST.yaml
│   │   │   └── SchemaMapping_SchemaMappingDbId_GET.yaml
│   │   └── README.md
│   ├── Inventory
│   │   ├── README.md
│   │   ├── by_class.csv
│   │   ├── by_module.csv
│   │   ├── inventory.csv
│   │   └── top_modules.csv
│   ├── Phenotyping
│   │   ├── BulkCapture
│   │   │   ├── Schemas
│   │   │   │   ├── BulkCapture.yaml
│   │   │   │   └── BulkCaptureNewRequest.yaml
│   │   │   ├── BulkCapture_BulkCaptureDbId_GET.yaml
│   │   │   ├── BulkCapture_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── CaptureWorkflow
│   │   │   ├── Schemas
│   │   │   │   ├── CaptureWorkflow.yaml
│   │   │   │   └── CaptureWorkflowNewRequest.yaml
│   │   │   ├── CaptureWorkflow_CaptureWorkflowDbId_GET.yaml
│   │   │   ├── CaptureWorkflow_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── ImageMetadata
│   │   │   ├── Schemas
│   │   │   │   ├── ImageMetadata.yaml
│   │   │   │   └── ImageMetadataNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── ImageMetadata_GET_POST.yaml
│   │   │   ├── ImageMetadata_ImageMetadataDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── PhenologyObservation
│   │   │   ├── Schemas
│   │   │   │   ├── PhenologyObservation.yaml
│   │   │   │   └── PhenologyObservationNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── PhenologyObservation_GET_POST.yaml
│   │   │   ├── PhenologyObservation_PhenologyObservationDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── PhenotypeAnnotation
│   │   │   ├── Schemas
│   │   │   │   ├── PhenotypeAnnotation.yaml
│   │   │   │   └── PhenotypeAnnotationNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── PhenotypeAnnotation_GET_POST.yaml
│   │   │   ├── PhenotypeAnnotation_PhenotypeAnnotationDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── PhenotypeCapture
│   │   │   ├── Schemas
│   │   │   │   ├── PhenotypeCapture.yaml
│   │   │   │   └── PhenotypeCaptureNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── PhenotypeCapture_GET_POST.yaml
│   │   │   ├── PhenotypeCapture_PhenotypeCaptureDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── QualityFlag
│   │   │   ├── Schemas
│   │   │   │   ├── QualityFlag.yaml
│   │   │   │   └── QualityFlagNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── QualityFlag_GET_POST.yaml
│   │   │   ├── QualityFlag_QualityFlagDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── RepeatedMeasurement
│   │   │   ├── Schemas
│   │   │   │   ├── MeasurementSeries.yaml
│   │   │   │   └── MeasurementSeriesNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── RepeatedMeasurement_GET_POST.yaml
│   │   │   └── RepeatedMeasurement_MeasurementSeriesDbId_GET.yaml
│   │   ├── ValueMissingness
│   │   │   ├── Schemas
│   │   │   │   ├── ValueMissingness.yaml
│   │   │   │   └── ValueMissingnessNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── ValueMissingness_GET_POST.yaml
│   │   │   └── ValueMissingness_ValueMissingnessDbId_GET.yaml
│   │   └── README.md
│   ├── PlantHealth
│   │   ├── CropHealthImage
│   │   │   ├── Schemas
│   │   │   │   ├── CropHealthImage.yaml
│   │   │   │   └── CropHealthImageNewRequest.yaml
│   │   │   ├── CropHealthImage_CropHealthImageDbId_GET.yaml
│   │   │   ├── CropHealthImage_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── DiagnosticEvidence
│   │   │   ├── Schemas
│   │   │   │   ├── DiagnosticEvidence.yaml
│   │   │   │   └── DiagnosticEvidenceNewRequest.yaml
│   │   │   ├── DiagnosticEvidence_DiagnosticEvidenceDbId_GET.yaml
│   │   │   ├── DiagnosticEvidence_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── DiseaseObservation
│   │   │   ├── Schemas
│   │   │   │   ├── DiseaseObservation.yaml
│   │   │   │   └── DiseaseObservationNewRequest.yaml
│   │   │   ├── DiseaseObservation_DiseaseObservationDbId_GET.yaml
│   │   │   ├── DiseaseObservation_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── DiseaseResistance
│   │   │   ├── Schemas
│   │   │   │   ├── DiseaseResistance.yaml
│   │   │   │   └── DiseaseResistanceNewRequest.yaml
│   │   │   ├── DiseaseResistance_DiseaseResistanceDbId_GET.yaml
│   │   │   ├── DiseaseResistance_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── FieldScouting
│   │   │   ├── Schemas
│   │   │   │   ├── FieldScouting.yaml
│   │   │   │   └── FieldScoutingNewRequest.yaml
│   │   │   ├── FieldScouting_FieldScoutingDbId_GET.yaml
│   │   │   ├── FieldScouting_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── IpmStrategy
│   │   │   ├── Schemas
│   │   │   │   ├── IpmStrategy.yaml
│   │   │   │   └── IpmStrategyNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── IpmStrategy_GET_POST.yaml
│   │   │   ├── IpmStrategy_IpmStrategyDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── PestDiseaseRisk
│   │   │   ├── Schemas
│   │   │   │   ├── PestDiseaseRisk.yaml
│   │   │   │   └── PestDiseaseRiskNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── PestDiseaseRisk_GET_POST.yaml
│   │   │   ├── PestDiseaseRisk_PestDiseaseRiskDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── ThresholdAlert
│   │   │   ├── Schemas
│   │   │   │   ├── ThresholdAlert.yaml
│   │   │   │   └── ThresholdAlertNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── ThresholdAlert_GET_POST.yaml
│   │   │   └── ThresholdAlert_ThresholdAlertDbId_GET.yaml
│   │   └── README.md
│   ├── RFCs
│   │   ├── README.md
│   │   ├── RFC-001-GenX-Skeleton.md
│   │   ├── RFC-002-Variable-Term-Governance.md
│   │   ├── RFC-003-Seed-Lot-Ledger.md
│   │   ├── RFC-004-Model-Registry.md
│   │   ├── RFC-005-Variant-Matrix-References.md
│   │   ├── RFC-006-FAIR-Packages.md
│   │   ├── RFC-007-Telemetry-Streams.md
│   │   ├── RFC-008-Selection-Decisions.md
│   │   ├── RFC-009-Analysis-Methods.md
│   │   ├── RFC-010-Weather-Observations.md
│   │   ├── RFC-011-Harvest-Records.md
│   │   ├── RFC-012-Phenotype-Capture.md
│   │   ├── RFC-013-Genomic-Datasets.md
│   │   ├── RFC-014-Breeding-Pipeline.md
│   │   ├── RFC-015-Genebank-Storage.md
│   │   ├── RFC-016-Research-Assets.md
│   │   ├── RFC-017-Measurement-Methods.md
│   │   ├── RFC-018-Experimental-Design.md
│   │   ├── RFC-019-Progeny-Records.md
│   │   ├── RFC-020-Doubled-Haploid.md
│   │   ├── RFC-021-Viability-Testing.md
│   │   ├── RFC-022-Speed-Breeding.md
│   │   ├── RFC-023-Soil-Profile.md
│   │   ├── RFC-024-Irrigation-Operation.md
│   │   ├── RFC-025-Repeated-Measurement.md
│   │   ├── RFC-026-Fertilizer-Application.md
│   │   ├── RFC-027-Phenology-Observation.md
│   │   ├── RFC-028-Parent-Candidate-Selection.md
│   │   ├── RFC-029-Crop-Cycle.md
│   │   ├── RFC-030-Quarantine.md
│   │   ├── RFC-031-Weather-Forecast.md
│   │   ├── RFC-032-Image-Metadata.md
│   │   ├── RFC-033-Climate-Normals.md
│   │   ├── RFC-034-Safety-Duplication.md
│   │   ├── RFC-035-Population-Advancement.md
│   │   ├── RFC-036-Regeneration.md
│   │   ├── RFC-037-Crossing-Schedule.md
│   │   ├── RFC-038-Tillage.md
│   │   ├── RFC-039-Candidate-Variety-Lifecycle.md
│   │   ├── RFC-040-Bulk-Capture.md
│   │   ├── RFC-041-Acquisition.md
│   │   ├── RFC-042-Extreme-Weather.md
│   │   ├── RFC-043-Vcf-Import.md
│   │   ├── RFC-044-Phenotype-Annotation.md
│   │   ├── RFC-045-Analysis-Result.md
│   │   ├── RFC-046-Genetic-Gain.md
│   │   ├── RFC-047-Gwas-Result.md
│   │   ├── RFC-048-Mixed-Model.md
│   │   ├── RFC-049-Stability-Analysis.md
│   │   ├── RFC-050-Heritability.md
│   │   ├── RFC-051-Gxe-Analysis.md
│   │   ├── RFC-052-Kinship.md
│   │   ├── RFC-053-Pca-Result.md
│   │   ├── RFC-054-Genomic-Prediction.md
│   │   ├── RFC-055-Genomic-Selection.md
│   │   ├── RFC-056-Genomic-Relationship.md
│   │   ├── RFC-057-Methylation-Analysis.md
│   │   ├── RFC-058-Expression-Qtl.md
│   │   ├── RFC-059-Haplotype-Analysis.md
│   │   ├── RFC-060-Pedigree-Analysis.md
│   │   ├── RFC-061-Assay-Design.md
│   │   ├── RFC-062-Variant-Annotation.md
│   │   ├── RFC-063-Custody-Transfer.md
│   │   ├── RFC-064-Genotype-Qc.md
│   │   ├── RFC-065-Disposal-Record.md
│   │   ├── RFC-066-Planting-Operation.md
│   │   ├── RFC-067-Carbon-Stock.md
│   │   ├── RFC-068-Water-Balance.md
│   │   ├── RFC-069-Farm.md
│   │   ├── RFC-070-Yield-Map.md
│   │   ├── RFC-071-Marker-Probe.md
│   │   ├── RFC-072-Genotype-Call-Semantics.md
│   │   ├── RFC-073-Vendor-Order.md
│   │   ├── RFC-074-Field-Scouting.md
│   │   ├── RFC-075-Field-Boundary.md
│   │   ├── RFC-076-Emissions.md
│   │   ├── RFC-077-Soil-Chemistry.md
│   │   ├── RFC-078-Environmental-Treatment.md
│   │   ├── RFC-079-Developmental-Stage.md
│   │   ├── RFC-080-Taxon-Name.md
│   │   ├── RFC-081-Spray-Application.md
│   │   ├── RFC-082-Units-And-Quantity.md
│   │   ├── RFC-083-External-Vocabulary.md
│   │   ├── RFC-084-Terminology-Version.md
│   │   ├── RFC-085-Ontology-Term.md
│   │   ├── RFC-086-Ontology-Mapping.md
│   │   ├── RFC-087-Measurement-Scale.md
│   │   ├── RFC-088-Crop-Trait-Dictionary.md
│   │   ├── RFC-089-Project.md
│   │   ├── RFC-090-Reusable-List.md
│   │   ├── RFC-091-Calendar.md
│   │   ├── RFC-092-Location-Geometry.md
│   │   ├── RFC-093-Reference-Data-Version.md
│   │   ├── RFC-094-Common-Crop-Name.md
│   │   ├── RFC-095-Crop-Species.md
│   │   ├── RFC-096-Institution-Code.md
│   │   ├── RFC-097-Person-Reference.md
│   │   ├── RFC-098-Research-Program.md
│   │   ├── RFC-099-Capability-Metadata.md
│   │   ├── RFC-100-Research-Location.md
│   │   ├── RFC-101-Collecting-Mission.md
│   │   ├── RFC-102-Conservation-Membership.md
│   │   ├── RFC-103-Mcpd-Adapter.md
│   │   ├── RFC-104-Duplicate-Review.md
│   │   ├── RFC-105-Crosswalk.md
│   │   ├── RFC-106-Treatment-Assignment.md
│   │   ├── RFC-107-Plot.md
│   │   ├── RFC-108-Field-Book.md
│   │   ├── RFC-109-Trial-Network.md
│   │   ├── RFC-110-Capture-Workflow.md
│   │   ├── RFC-111-Quality-Flag.md
│   │   ├── RFC-112-Value-Missingness.md
│   │   ├── RFC-113-Assay-Execution.md
│   │   ├── RFC-114-Vcf-Export.md
│   │   ├── RFC-115-Reference-Assembly.md
│   │   ├── RFC-116-Pipeline-Provenance.md
│   │   ├── RFC-117-ExperimentalProtocol.md
│   │   ├── RFC-118-ArtifactCatalogue.md
│   │   ├── RFC-119-ProtocolLibrary.md
│   │   ├── RFC-120-PublicationReview.md
│   │   ├── RFC-121-BiodiversityExport.md
│   │   ├── RFC-122-EvidencePack.md
│   │   ├── RFC-123-DiseaseObservation.md
│   │   ├── RFC-124-DiagnosticEvidence.md
│   │   ├── RFC-125-IpmStrategy.md
│   │   ├── RFC-126-ThresholdAlert.md
│   │   ├── RFC-127-DiseaseResistance.md
│   │   ├── RFC-128-CropHealthImage.md
│   │   ├── RFC-129-CropRecommendation.md
│   │   ├── RFC-130-SowingWindow.md
│   │   ├── RFC-131-IrrigationAdvice.md
│   │   ├── RFC-132-NutrientAdvice.md
│   │   ├── RFC-133-PestDiseaseRisk.md
│   │   ├── RFC-134-YieldForecast.md
│   │   ├── RFC-135-CropSuitability.md
│   │   ├── RFC-136-HumanReview.md
│   │   ├── RFC-137-ExplanationEvidence.md
│   │   ├── RFC-138-OutcomeFeedback.md
│   │   ├── RFC-139-LocalConstraint.md
│   │   ├── RFC-140-CrsTransform.md
│   │   ├── RFC-141-SpatialIndex.md
│   │   ├── RFC-142-FieldGeometry.md
│   │   ├── RFC-143-SpatialQuery.md
│   │   ├── RFC-144-RasterCatalogue.md
│   │   ├── RFC-145-RemoteSensingMetadata.md
│   │   ├── RFC-146-VegetationIndex.md
│   │   ├── RFC-147-CloudMask.md
│   │   ├── RFC-148-TelemetryNormalization.md
│   │   ├── RFC-149-SensorDevice.md
│   │   ├── RFC-150-CalibrationQuality.md
│   │   ├── RFC-151-EdgeGatewayHealth.md
│   │   ├── RFC-152-SchemaMapping.md
│   │   ├── RFC-153-CapabilityNegotiation.md
│   │   ├── RFC-154-BreedingPipeline.md
│   │   └── RFC-155-ConformanceProbe.md
│   ├── ReferenceData
│   │   ├── Calendar
│   │   │   ├── Schemas
│   │   │   │   ├── Calendar.yaml
│   │   │   │   └── CalendarNewRequest.yaml
│   │   │   ├── Calendar_CalendarDbId_GET.yaml
│   │   │   ├── Calendar_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── CommonCropName
│   │   │   ├── Schemas
│   │   │   │   ├── CommonCropName.yaml
│   │   │   │   └── CommonCropNameNewRequest.yaml
│   │   │   ├── CommonCropName_CommonCropNameDbId_GET.yaml
│   │   │   ├── CommonCropName_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── CropSpecies
│   │   │   ├── Schemas
│   │   │   │   ├── CropSpecies.yaml
│   │   │   │   └── CropSpeciesNewRequest.yaml
│   │   │   ├── CropSpecies_CropSpeciesDbId_GET.yaml
│   │   │   ├── CropSpecies_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── CropTraitDictionary
│   │   │   ├── Schemas
│   │   │   │   ├── CropTraitDictionary.yaml
│   │   │   │   └── CropTraitDictionaryNewRequest.yaml
│   │   │   ├── CropTraitDictionary_CropTraitDictionaryDbId_GET.yaml
│   │   │   ├── CropTraitDictionary_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── DevelopmentalStage
│   │   │   ├── Schemas
│   │   │   │   ├── DevelopmentalStage.yaml
│   │   │   │   └── DevelopmentalStageNewRequest.yaml
│   │   │   ├── DevelopmentalStage_DevelopmentalStageDbId_GET.yaml
│   │   │   ├── DevelopmentalStage_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── ExternalVocabulary
│   │   │   ├── Schemas
│   │   │   │   ├── ExternalVocabulary.yaml
│   │   │   │   └── ExternalVocabularyNewRequest.yaml
│   │   │   ├── ExternalVocabulary_ExternalVocabularyDbId_GET.yaml
│   │   │   ├── ExternalVocabulary_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── InstitutionCode
│   │   │   ├── Schemas
│   │   │   │   ├── InstitutionCode.yaml
│   │   │   │   └── InstitutionCodeNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── InstitutionCode_GET_POST.yaml
│   │   │   ├── InstitutionCode_InstitutionCodeDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── MeasurementMethods
│   │   │   ├── Schemas
│   │   │   │   ├── MeasurementMethod.yaml
│   │   │   │   └── MeasurementMethodNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── MeasurementMethods_GET_POST.yaml
│   │   │   ├── MeasurementMethods_MeasurementMethodDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── MeasurementScale
│   │   │   ├── Schemas
│   │   │   │   ├── MeasurementScale.yaml
│   │   │   │   └── MeasurementScaleNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── MeasurementScale_GET_POST.yaml
│   │   │   ├── MeasurementScale_MeasurementScaleDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── OntologyMapping
│   │   │   ├── Schemas
│   │   │   │   ├── OntologyMapping.yaml
│   │   │   │   └── OntologyMappingNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── OntologyMapping_GET_POST.yaml
│   │   │   ├── OntologyMapping_OntologyMappingDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── OntologyTerm
│   │   │   ├── Schemas
│   │   │   │   ├── OntologyTerm.yaml
│   │   │   │   └── OntologyTermNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── OntologyTerm_GET_POST.yaml
│   │   │   ├── OntologyTerm_OntologyTermDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── PersonReference
│   │   │   ├── Schemas
│   │   │   │   ├── PersonReference.yaml
│   │   │   │   └── PersonReferenceNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── PersonReference_GET_POST.yaml
│   │   │   ├── PersonReference_PersonReferenceDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── ReferenceDataVersion
│   │   │   ├── Schemas
│   │   │   │   ├── ReferenceDataVersion.yaml
│   │   │   │   └── ReferenceDataVersionNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── ReferenceDataVersion_GET_POST.yaml
│   │   │   └── ReferenceDataVersion_ReferenceDataVersionDbId_GET.yaml
│   │   ├── ReusableList
│   │   │   ├── Schemas
│   │   │   │   ├── ReusableList.yaml
│   │   │   │   └── ReusableListNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── ReusableList_GET_POST.yaml
│   │   │   └── ReusableList_ReusableListDbId_GET.yaml
│   │   ├── TaxonName
│   │   │   ├── Schemas
│   │   │   │   ├── TaxonName.yaml
│   │   │   │   └── TaxonNameNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── TaxonName_GET_POST.yaml
│   │   │   └── TaxonName_TaxonNameDbId_GET.yaml
│   │   ├── TerminologyVersion
│   │   │   ├── Schemas
│   │   │   │   ├── TerminologyVersion.yaml
│   │   │   │   └── TerminologyVersionNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── TerminologyVersion_GET_POST.yaml
│   │   │   └── TerminologyVersion_TerminologyVersionDbId_GET.yaml
│   │   ├── UnitsAndQuantity
│   │   │   ├── Schemas
│   │   │   │   ├── UnitsAndQuantity.yaml
│   │   │   │   └── UnitsAndQuantityNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── UnitsAndQuantity_GET_POST.yaml
│   │   │   └── UnitsAndQuantity_UnitsAndQuantityDbId_GET.yaml
│   │   ├── VariableTerms
│   │   │   ├── Schemas
│   │   │   │   ├── VariableTerm.yaml
│   │   │   │   └── VariableTermNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── VariableTerms_GET_POST.yaml
│   │   │   └── VariableTerms_VariableDbId_GET.yaml
│   │   └── README.md
│   ├── Research
│   │   ├── AnalysisMethods
│   │   │   ├── Schemas
│   │   │   │   ├── AnalysisMethod.yaml
│   │   │   │   └── AnalysisMethodNewRequest.yaml
│   │   │   ├── AnalysisMethods_AnalysisMethodDbId_GET.yaml
│   │   │   ├── AnalysisMethods_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── AnalysisResult
│   │   │   ├── Schemas
│   │   │   │   ├── AnalysisResult.yaml
│   │   │   │   └── AnalysisResultNewRequest.yaml
│   │   │   ├── AnalysisResult_AnalysisResultDbId_GET.yaml
│   │   │   ├── AnalysisResult_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── ArtifactCatalogue
│   │   │   ├── Schemas
│   │   │   │   ├── ArtifactCatalogue.yaml
│   │   │   │   └── ArtifactCatalogueNewRequest.yaml
│   │   │   ├── ArtifactCatalogue_ArtifactCatalogueDbId_GET.yaml
│   │   │   ├── ArtifactCatalogue_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── EvidencePack
│   │   │   ├── Schemas
│   │   │   │   ├── EvidencePack.yaml
│   │   │   │   └── EvidencePackNewRequest.yaml
│   │   │   ├── EvidencePack_EvidencePackDbId_GET.yaml
│   │   │   ├── EvidencePack_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── ExplanationEvidence
│   │   │   ├── Schemas
│   │   │   │   ├── ExplanationEvidence.yaml
│   │   │   │   └── ExplanationEvidenceNewRequest.yaml
│   │   │   ├── ExplanationEvidence_ExplanationEvidenceDbId_GET.yaml
│   │   │   ├── ExplanationEvidence_GET_POST.yaml
│   │   │   ├── GroupDescription.md
│   │   │   └── README.md
│   │   ├── HumanReview
│   │   │   ├── Schemas
│   │   │   │   ├── HumanReview.yaml
│   │   │   │   └── HumanReviewNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── HumanReview_GET_POST.yaml
│   │   │   ├── HumanReview_HumanReviewDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── MixedModel
│   │   │   ├── Schemas
│   │   │   │   ├── MixedModelResult.yaml
│   │   │   │   └── MixedModelResultNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── MixedModel_GET_POST.yaml
│   │   │   ├── MixedModel_MixedModelResultDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── Models
│   │   │   ├── Schemas
│   │   │   │   ├── ModelArtifact.yaml
│   │   │   │   └── ModelArtifactNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── Models_GET_POST.yaml
│   │   │   ├── Models_ModelDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── OutcomeFeedback
│   │   │   ├── Schemas
│   │   │   │   ├── OutcomeFeedback.yaml
│   │   │   │   └── OutcomeFeedbackNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── OutcomeFeedback_GET_POST.yaml
│   │   │   ├── OutcomeFeedback_OutcomeFeedbackDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── PcaResult
│   │   │   ├── Schemas
│   │   │   │   ├── PcaResult.yaml
│   │   │   │   └── PcaResultNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── PcaResult_GET_POST.yaml
│   │   │   ├── PcaResult_PcaResultDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── Project
│   │   │   ├── Schemas
│   │   │   │   ├── Project.yaml
│   │   │   │   └── ProjectNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── Project_GET_POST.yaml
│   │   │   ├── Project_ProjectDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── ProtocolLibrary
│   │   │   ├── Schemas
│   │   │   │   ├── ProtocolLibrary.yaml
│   │   │   │   └── ProtocolLibraryNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── ProtocolLibrary_GET_POST.yaml
│   │   │   ├── ProtocolLibrary_ProtocolLibraryDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── PublicationReview
│   │   │   ├── Schemas
│   │   │   │   ├── PublicationReview.yaml
│   │   │   │   └── PublicationReviewNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── PublicationReview_GET_POST.yaml
│   │   │   ├── PublicationReview_PublicationReviewDbId_GET.yaml
│   │   │   └── README.md
│   │   ├── ResearchAssets
│   │   │   ├── Schemas
│   │   │   │   ├── ResearchAsset.yaml
│   │   │   │   └── ResearchAssetNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── ResearchAssets_GET_POST.yaml
│   │   │   └── ResearchAssets_ResearchAssetDbId_GET.yaml
│   │   ├── ResearchLocation
│   │   │   ├── Schemas
│   │   │   │   ├── ResearchLocation.yaml
│   │   │   │   └── ResearchLocationNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── ResearchLocation_GET_POST.yaml
│   │   │   └── ResearchLocation_ResearchLocationDbId_GET.yaml
│   │   ├── ResearchProgram
│   │   │   ├── Schemas
│   │   │   │   ├── ResearchProgram.yaml
│   │   │   │   └── ResearchProgramNewRequest.yaml
│   │   │   ├── GroupDescription.md
│   │   │   ├── README.md
│   │   │   ├── ResearchProgram_GET_POST.yaml
│   │   │   └── ResearchProgram_ResearchProgramDbId_GET.yaml
│   │   └── README.md
│   ├── ADOPTION.md
│   ├── AMBIKA-GAP-REGISTER.md
│   ├── AMBIKA-GENX-COVERAGE-MATRIX.md
│   ├── CLASSIFICATION.md
│   ├── DECISIONS.md
│   ├── ENDPOINT-IDENTITY.md
│   ├── GENX-ENDPOINT-CATALOG.md
│   ├── README.md
│   └── swaggerMetaData.yaml
├── BrAPI-Genotyping
│   ├── AlleleMatrix
│   │   ├── Schemas
│   │   │   ├── AlleleMatrix.yaml
│   │   │   ├── AlleleMatrixParameters.yaml
│   │   │   └── AlleleMatrixSearchRequest.yaml
│   │   ├── AlleleMatrix_GET.yaml
│   │   ├── GroupDescription.md
│   │   ├── README.md
│   │   ├── Search_AlleleMatrix_POST.yaml
│   │   └── Search_AlleleMatrix_SearchResultsDbId_GET.yaml
│   ├── CallSets
│   │   ├── Schemas
│   │   │   ├── CallSet.yaml
│   │   │   ├── CallSetsListResponse.yaml
│   │   │   └── CallSetsSearchRequest.yaml
│   │   ├── CallSets_CallSetId_Calls_GET.yaml
│   │   ├── CallSets_CallSetId_GET.yaml
│   │   ├── CallSets_GET.yaml
│   │   ├── GroupDescription.md
│   │   ├── README.md
│   │   ├── Search_CallSets_POST.yaml
│   │   └── Search_CallSets_SearchResultsDbId_GET.yaml
│   ├── Calls
│   │   ├── Schemas
│   │   │   ├── Call.yaml
│   │   │   ├── CallsListResponse.yaml
│   │   │   ├── CallsSearchRequest.yaml
│   │   │   └── ListValue.yaml
│   │   ├── Calls_GET_PUT.yaml
│   │   ├── GroupDescription.md
│   │   ├── README.md
│   │   ├── Search_Calls_POST.yaml
│   │   └── Search_Calls_SearchResultsDbId_GET.yaml
│   ├── GenomeMaps
│   │   ├── Schemas
│   │   │   ├── GenomeMap.yaml
│   │   │   ├── LinkageGroup.yaml
│   │   │   ├── MarkerPosition.yaml
│   │   │   └── MarkerPositionSearchRequest.yaml
│   │   ├── GroupDescription.md
│   │   ├── Maps_GET.yaml
│   │   ├── Maps_MapDbId_GET.yaml
│   │   ├── Maps_MapDbId_LinkageGroups_GET.yaml
│   │   ├── MarkerPositions_GET.yaml
│   │   ├── README.md
│   │   ├── Search_MarkerPositions_POST.yaml
│   │   └── Search_MarkerPositions_SearchResultsDbId_GET.yaml
│   ├── Plates
│   │   ├── Schemas
│   │   │   ├── Plate.yaml
│   │   │   ├── PlateNewRequest.yaml
│   │   │   └── PlateSearchRequest.yaml
│   │   ├── GroupDescription.md
│   │   ├── Plates_GET_POST_PUT.yaml
│   │   ├── Plates_PlateDbId_GET.yaml
│   │   ├── README.md
│   │   ├── Search_Plates_POST.yaml
│   │   └── Search_Plates_SearchResultsDbId_GET.yaml
│   ├── ReferenceSets
│   │   ├── Schemas
│   │   │   ├── ReferenceSet.yaml
│   │   │   └── ReferenceSetsSearchRequest.yaml
│   │   ├── GroupDescription.md
│   │   ├── README.md
│   │   ├── ReferenceSets_GET.yaml
│   │   ├── ReferenceSets_RefernceSetId_GET.yaml
│   │   ├── Search_ReferenceSets_POST.yaml
│   │   └── Search_ReferenceSets_SearchResultsDbId_GET.yaml
│   ├── References
│   │   ├── Schemas
│   │   │   ├── OntologyTerm.yaml
│   │   │   ├── Reference.yaml
│   │   │   ├── ReferenceBases.yaml
│   │   │   └── ReferencesSearchRequest.yaml
│   │   ├── GroupDescription.md
│   │   ├── README.md
│   │   ├── References_GET.yaml
│   │   ├── References_ReferenceId_Bases_GET.yaml
│   │   ├── References_ReferenceId_GET.yaml
│   │   ├── Search_References_POST.yaml
│   │   └── Search_References_SearchResultsDbId_GET.yaml
│   ├── Samples
│   │   ├── Schemas
│   │   │   ├── Sample.yaml
│   │   │   ├── SampleNewRequest.yaml
│   │   │   └── SampleSearchRequest.yaml
│   │   ├── GroupDescription.md
│   │   ├── README.md
│   │   ├── Samples_GET_POST_PUT.yaml
│   │   ├── Samples_SampleDbId_GET_PUT.yaml
│   │   ├── Search_Samples_POST.yaml
│   │   └── Search_Samples_SearchResultsDbId_GET.yaml
│   ├── VariantSets
│   │   ├── Schemas
│   │   │   ├── Analysis.yaml
│   │   │   ├── AvailableFormat.yaml
│   │   │   ├── VariantSet.yaml
│   │   │   ├── VariantSetsExtractRequest.yaml
│   │   │   └── VariantSetsSearchRequest.yaml
│   │   ├── GroupDescription.md
│   │   ├── README.md
│   │   ├── Search_VariantSets_POST.yaml
│   │   ├── Search_VariantSets_SearchResultsDbId_GET.yaml
│   │   ├── VariantSets_Extract_POST.yaml
│   │   ├── VariantSets_GET.yaml
│   │   ├── VariantSets_VariantSetId_CallSets_GET.yaml
│   │   ├── VariantSets_VariantSetId_Calls_GET.yaml
│   │   ├── VariantSets_VariantSetId_GET.yaml
│   │   └── VariantSets_VariantSetId_Variants_GET.yaml
│   ├── Variants
│   │   ├── Schemas
│   │   │   ├── Variant.yaml
│   │   │   ├── VariantsListResponse.yaml
│   │   │   └── VariantsSearchRequest.yaml
│   │   ├── GroupDescription.md
│   │   ├── README.md
│   │   ├── Search_Variants_POST.yaml
│   │   ├── Search_Variants_SearchResultsDbId_GET.yaml
│   │   ├── Variants_GET.yaml
│   │   ├── Variants_VariantId_Calls_GET.yaml
│   │   └── Variants_VariantId_GET.yaml
│   ├── VendorSamples
│   │   ├── Schemas
│   │   │   ├── PlateFormat.yaml
│   │   │   ├── VendorContact.yaml
│   │   │   ├── VendorOrder.yaml
│   │   │   ├── VendorOrderSubmission.yaml
│   │   │   ├── VendorOrderSubmissionRequest.yaml
│   │   │   ├── VendorPlate.yaml
│   │   │   ├── VendorPlateSubmission.yaml
│   │   │   ├── VendorPlateSubmissionId.yaml
│   │   │   ├── VendorPlateSubmissionRequest.yaml
│   │   │   ├── VendorResultFile.yaml
│   │   │   ├── VendorSample.yaml
│   │   │   ├── VendorSpecification.yaml
│   │   │   └── VendorSpecificationService.yaml
│   │   ├── GroupDescription.md
│   │   ├── README.md
│   │   ├── Vendor_Orders_GET_POST.yaml
│   │   ├── Vendor_Orders_OrderId_Plates_GET.yaml
│   │   ├── Vendor_Orders_OrderId_Results_GET.yaml
│   │   ├── Vendor_Orders_OrderId_Status_GET.yaml
│   │   ├── Vendor_Plates_POST.yaml
│   │   ├── Vendor_Plates_SubmissionId_GET.yaml
│   │   └── Vendor_Specifications_GET.yaml
│   ├── README.md
│   └── swaggerMetaData.yaml
├── BrAPI-Germplasm
│   ├── Crosses
│   │   ├── Schemas
│   │   │   ├── Cross.yaml
│   │   │   ├── CrossNewRequest.yaml
│   │   │   └── CrossParent.yaml
│   │   ├── Crosses_GET_POST_PUT.yaml
│   │   ├── GroupDescription.md
│   │   └── README.md
│   ├── CrossingProjects
│   │   ├── Schemas
│   │   │   ├── CrossingProject.yaml
│   │   │   └── CrossingProjectNewRequest.yaml
│   │   ├── CrossingProjects_CrossingProjectDbId_GET_PUT.yaml
│   │   ├── CrossingProjects_GET_POST.yaml
│   │   ├── GroupDescription.md
│   │   └── README.md
│   ├── Germplasm
│   │   ├── Schemas
│   │   │   ├── BreedingMethod.yaml
│   │   │   ├── Germplasm.yaml
│   │   │   ├── GermplasmMCPD.yaml
│   │   │   ├── GermplasmNewRequest.yaml
│   │   │   ├── GermplasmOrigin.yaml
│   │   │   ├── GermplasmSearchRequest.yaml
│   │   │   ├── ParentTypeDEP.yaml
│   │   │   ├── PedigreeNodeDEP.yaml
│   │   │   ├── ProgenyNodeDEP.yaml
│   │   │   └── TaxonID.yaml
│   │   ├── BreedingMethods_BreedingMethodDbId_GET.yaml
│   │   ├── BreedingMethods_GET.yaml
│   │   ├── Germplasm_GET_POST.yaml
│   │   ├── Germplasm_GermplasmDbId_GET_PUT.yaml
│   │   ├── Germplasm_GermplasmDbId_MCPD_GET.yaml
│   │   ├── Germplasm_GermplasmDbId_Pedigree_GET.yaml
│   │   ├── Germplasm_GermplasmDbId_Progeny_GET.yaml
│   │   ├── GroupDescription.md
│   │   ├── README.md
│   │   ├── Search_Germplasm_POST.yaml
│   │   └── Search_Germplasm_SearchResultsDbId_GET.yaml
│   ├── Germplasm_Attribute_Values
│   │   ├── Schemas
│   │   │   ├── GermplasmAttributeValue.yaml
│   │   │   ├── GermplasmAttributeValueNewRequest.yaml
│   │   │   └── GermplasmAttributeValueSearchRequest.yaml
│   │   ├── AttributeValues_AttributeValueDbId_GET_PUT.yaml
│   │   ├── AttributesValues_GET_POST.yaml
│   │   ├── GroupDescription.md
│   │   ├── README.md
│   │   ├── Search_AttributeValues_POST.yaml
│   │   └── Search_AttributeValues_SearchResultsDbId_GET.yaml
│   ├── Germplasm_Attributes
│   │   ├── Schemas
│   │   │   ├── GermplasmAttribute.yaml
│   │   │   ├── GermplasmAttributeNewRequest.yaml
│   │   │   ├── GermplasmAttributeSearchRequest.yaml
│   │   │   ├── Method.yaml
│   │   │   ├── Scale.yaml
│   │   │   └── Trait.yaml
│   │   ├── Attributes_AttributeDbId_GET_PUT.yaml
│   │   ├── Attributes_Categories_GET.yaml
│   │   ├── Attributes_GET_POST.yaml
│   │   ├── GroupDescription.md
│   │   ├── README.md
│   │   ├── Search_Attributes_POST.yaml
│   │   └── Search_Attributes_SearchResultsDbId_GET.yaml
│   ├── Pedigree
│   │   ├── Schemas
│   │   │   ├── ParentType.yaml
│   │   │   ├── PedigreeNode.yaml
│   │   │   └── PedigreeSearchRequest.yaml
│   │   ├── GroupDescription.md
│   │   ├── Pedigree_GET_POST_PUT.yaml
│   │   ├── README.md
│   │   ├── Search_Pedigree_POST.yaml
│   │   └── Search_Pedigree_SearchResultsDbId_GET.yaml
│   ├── PlannedCrosses
│   │   ├── Schemas
│   │   │   ├── PlannedCross.yaml
│   │   │   └── PlannedCrossNewRequest.yaml
│   │   ├── GroupDescription.md
│   │   ├── PlannedCrosses_GET_POST_PUT.yaml
│   │   └── README.md
│   ├── SeedLots
│   │   ├── Schemas
│   │   │   ├── SeedLot.yaml
│   │   │   ├── SeedLotNewRequest.yaml
│   │   │   ├── SeedLotTransaction.yaml
│   │   │   └── SeedLotTransactionNewRequest.yaml
│   │   ├── GroupDescription.md
│   │   ├── README.md
│   │   ├── SeedLots_GET_POST.yaml
│   │   ├── SeedLots_SeedLotDbId_GET_PUT.yaml
│   │   ├── SeedLots_SeedLotDbId_Transactions_GET.yaml
│   │   └── SeedLots_Transactions_GET_POST.yaml
│   ├── README.md
│   └── swaggerMetaData.yaml
├── BrAPI-Phenotyping
│   ├── Events
│   │   ├── Schemas
│   │   │   └── Event.yaml
│   │   ├── Events_GET.yaml
│   │   ├── GroupDescription.md
│   │   └── README.md
│   ├── Images
│   │   ├── Schemas
│   │   │   ├── Image.yaml
│   │   │   ├── ImageNewRequest.yaml
│   │   │   └── ImageSearchRequest.yaml
│   │   ├── Delete_Images_POST.yaml
│   │   ├── GroupDescription.md
│   │   ├── Images_GET_POST.yaml
│   │   ├── Images_ImageDbId_GET_PUT.yaml
│   │   ├── Images_ImageDbId_ImageContent_PUT.yaml
│   │   ├── README.md
│   │   ├── Search_Images_POST.yaml
│   │   └── Search_Images_SearchResultsDbId_GET.yaml
│   ├── Methods
│   │   ├── schemas
│   │   │   ├── Method.yaml
│   │   │   └── MethodNewRequest.yaml
│   │   ├── GroupDescription.md
│   │   ├── Methods_GET_POST.yaml
│   │   ├── Methods_MethodDbId_GET_PUT.yaml
│   │   └── README.md
│   ├── ObservationUnits
│   │   ├── Schemas
│   │   │   ├── ObservationTreatment.yaml
│   │   │   ├── ObservationUnit.yaml
│   │   │   ├── ObservationUnitLevel.yaml
│   │   │   ├── ObservationUnitLevelRelationship.yaml
│   │   │   ├── ObservationUnitNewRequest.yaml
│   │   │   ├── ObservationUnitPosition.yaml
│   │   │   ├── ObservationUnitSearchRequest.yaml
│   │   │   └── ObservationUnitTable.yaml
│   │   ├── GroupDescription.md
│   │   ├── ObservationLevels_GET.yaml
│   │   ├── ObservationUnits_GET_POST_PUT.yaml
│   │   ├── ObservationUnits_ObservationUnitDbId_GET_PUT.yaml
│   │   ├── ObservationUnits_Table_GET.yaml
│   │   ├── README.md
│   │   ├── Search_ObservationUnits_POST.yaml
│   │   └── Search_ObservationUnits_SearchResultsDbId_GET.yaml
│   ├── ObservationVariables
│   │   ├── Schemas
│   │   │   ├── ObservationVariable.yaml
│   │   │   ├── ObservationVariableNewRequest.yaml
│   │   │   └── ObservationVariableSearchRequest.yaml
│   │   ├── GroupDescription.md
│   │   ├── README.md
│   │   ├── Search_Variables_POST.yaml
│   │   ├── Search_Variables_SearchResultsDbId_GET.yaml
│   │   ├── Variables_GET_POST.yaml
│   │   └── Variables_ObservationVariableDbId_GET_PUT.yaml
│   ├── Observations
│   │   ├── Schemas
│   │   │   ├── Observation.yaml
│   │   │   ├── ObservationNewRequest.yaml
│   │   │   ├── ObservationSearchRequest.yaml
│   │   │   ├── ObservationTable.yaml
│   │   │   └── SeasonObs.yaml
│   │   ├── Delete_Observations_POST.yaml
│   │   ├── GroupDescription.md
│   │   ├── Observations_GET_POST_PUT.yaml
│   │   ├── Observations_ObservationDbId_GET_PUT.yaml
│   │   ├── Observations_Table_GET.yaml
│   │   ├── README.md
│   │   ├── Search_Observations_POST.yaml
│   │   └── Search_Observations_SearchResultsDbId_GET.yaml
│   ├── Ontologies
│   │   ├── Schemas
│   │   │   ├── Ontology.yaml
│   │   │   └── OntologyNewRequest.yaml
│   │   ├── GroupDescription.md
│   │   ├── Ontologies_GET_POST.yaml
│   │   ├── Ontologies_OntologyDbId_GET_PUT.yaml
│   │   └── README.md
│   ├── Scales
│   │   ├── schemas
│   │   │   ├── Scale.yaml
│   │   │   └── ScaleNewRequest.yaml
│   │   ├── GroupDescription.md
│   │   ├── README.md
│   │   ├── Scales_GET_POST.yaml
│   │   └── Scales_ScaleDbId_GET_PUT.yaml
│   ├── Traits
│   │   ├── Schemas
│   │   │   ├── Trait.yaml
│   │   │   └── TraitNewRequest.yaml
│   │   ├── GroupDescription.md
│   │   ├── README.md
│   │   ├── Traits_GET_POST.yaml
│   │   └── Traits_TraitDbId_GET_PUT.yaml
│   ├── README.md
│   └── swaggerMetaData.yaml
├── BrAPI-Schema
│   ├── BrAPI-Common
│   │   ├── AdditionalInfo.json
│   │   ├── Attribute.json
│   │   ├── ExternalReference.json
│   │   ├── GeoJSON.json
│   │   ├── GeoJSONGeometry.json
│   │   ├── ObservationUnitHierarchyLevel.json
│   │   ├── OntologyTerm.json
│   │   ├── TraitDataType.json
│   │   └── Variable.json
│   ├── BrAPI-Core
│   │   ├── Contact.json
│   │   ├── DataLink.json
│   │   ├── List.json
│   │   ├── ListType.json
│   │   ├── Location.json
│   │   ├── Person.json
│   │   ├── Program.json
│   │   ├── Season.json
│   │   ├── Study.json
│   │   └── Trial.json
│   ├── BrAPI-Genotyping
│   │   ├── AlleleMatrix.json
│   │   ├── Call.json
│   │   ├── CallSet.json
│   │   ├── GenomeMap.json
│   │   ├── MarkerPosition.json
│   │   ├── Plate.json
│   │   ├── Reference.json
│   │   ├── ReferenceSet.json
│   │   ├── Sample.json
│   │   ├── Variant.json
│   │   └── VariantSet.json
│   ├── BrAPI-Germplasm
│   │   ├── BreedingMethod.json
│   │   ├── Cross.json
│   │   ├── CrossParent.json
│   │   ├── CrossType.json
│   │   ├── CrossingProject.json
│   │   ├── Germplasm.json
│   │   ├── GermplasmAttribute.json
│   │   ├── GermplasmAttributeValue.json
│   │   ├── ParentType.json
│   │   ├── PedigreeNode.json
│   │   ├── PlannedCross.json
│   │   ├── SeedLot.json
│   │   └── SeedLotTransaction.json
│   ├── BrAPI-Phenotyping
│   │   ├── Event.json
│   │   ├── Image.json
│   │   ├── Method.json
│   │   ├── Observation.json
│   │   ├── ObservationUnit.json
│   │   ├── ObservationUnitLevel.json
│   │   ├── ObservationUnitLevelRelationship.json
│   │   ├── ObservationVariable.json
│   │   ├── Ontology.json
│   │   ├── OntologyReference.json
│   │   ├── Scale.json
│   │   └── Trait.json
│   ├── Requests
│   │   ├── Parameters
│   │   │   ├── CommonCropNamesParameters.json
│   │   │   ├── ExternalReferencesParameters.json
│   │   │   ├── GermplasmParameters.json
│   │   │   ├── LocationParameters.json
│   │   │   ├── ObservationVariableParameters.json
│   │   │   ├── OntologyParameters.json
│   │   │   ├── PagingParameters.json
│   │   │   ├── ProgramParameters.json
│   │   │   ├── README.md
│   │   │   ├── StudyParameters.json
│   │   │   ├── TokenPagingParameters.json
│   │   │   ├── TrialParameters.json
│   │   │   └── VariableBaseClassParameters.json
│   │   ├── Schemas
│   │   │   ├── GeoJSONSearchArea.json
│   │   │   └── README.md
│   │   ├── AlleleMatrixRequest.json
│   │   ├── CallRequest.json
│   │   ├── CallSetRequest.json
│   │   ├── CrossRequest.json
│   │   ├── CrossingProjectRequest.json
│   │   ├── EventRequest.json
│   │   ├── GenomeMapRequest.json
│   │   ├── GermplasmAttributeRequest.json
│   │   ├── GermplasmAttributeValueRequest.json
│   │   ├── GermplasmRequest.json
│   │   ├── ImageRequest.json
│   │   ├── ListRequest.json
│   │   ├── LocationRequest.json
│   │   ├── MarkerPositionRequest.json
│   │   ├── MethodRequest.json
│   │   ├── ObservationRequest.json
│   │   ├── ObservationUnitHierarchyLevelRequest.json
│   │   ├── ObservationUnitRequest.json
│   │   ├── ObservationVariableRequest.json
│   │   ├── OntologyRequest.json
│   │   ├── PedigreeNodeRequest.json
│   │   ├── PersonRequest.json
│   │   ├── PlannedCrossRequest.json
│   │   ├── PlateRequest.json
│   │   ├── ProgramRequest.json
│   │   ├── ReferenceBasesRequest.json
│   │   ├── ReferenceRequest.json
│   │   ├── ReferenceSetRequest.json
│   │   ├── SampleRequest.json
│   │   ├── ScaleRequest.json
│   │   ├── SeasonRequest.json
│   │   ├── SeedLotRequest.json
│   │   ├── SeedLotTransactionRequest.json
│   │   ├── StudyRequest.json
│   │   ├── TraitRequest.json
│   │   ├── TrialRequest.json
│   │   ├── VariantSetsExtractRequest.json
│   │   ├── VarientRequest.json
│   │   └── VarientSetRequest.json
│   ├── Responses
│   │   └── CallListResponse.json
│   └── README.md
├── Components
│   ├── Parameters
│   │   ├── Germplasm.yaml
│   │   ├── ProgramTrialStudy.yaml
│   │   ├── acceptHeader.yaml
│   │   ├── authorizationHeader.yaml
│   │   ├── commonCropName.yaml
│   │   ├── externalReferences.yaml
│   │   ├── observationLevel.yaml
│   │   ├── ontologyDbId.yaml
│   │   ├── page.yaml
│   │   ├── pageSize.yaml
│   │   ├── pageToken.yaml
│   │   ├── searchResultsDbId.yaml
│   │   └── variables.yaml
│   ├── Responses
│   │   ├── 202AcceptedSearchResponse.yaml
│   │   ├── 400BadRequest.yaml
│   │   ├── 401Unauthorized.yaml
│   │   ├── 403Forbidden.yaml
│   │   └── 404NotFound.yaml
│   ├── Schemas
│   │   ├── SearchRequestSchemas
│   │   │   ├── SearchRequestParametersCommonCropNames.yaml
│   │   │   ├── SearchRequestParametersExternalReferences.yaml
│   │   │   ├── SearchRequestParametersGermplasm.yaml
│   │   │   ├── SearchRequestParametersLocations.yaml
│   │   │   ├── SearchRequestParametersObservationVariables.yaml
│   │   │   ├── SearchRequestParametersPaging.yaml
│   │   │   ├── SearchRequestParametersPrograms.yaml
│   │   │   ├── SearchRequestParametersStudies.yaml
│   │   │   ├── SearchRequestParametersTokenPaging.yaml
│   │   │   ├── SearchRequestParametersTrials.yaml
│   │   │   └── SearchRequestParametersVariableBaseClass.yaml
│   │   ├── Context.yaml
│   │   ├── DataTypes.yaml
│   │   ├── ExternalReferences.yaml
│   │   ├── MethodBaseClass.yaml
│   │   ├── ObservationUnitHierarchyLevel.yaml
│   │   ├── OntologyReference.yaml
│   │   ├── ScaleBaseClass.yaml
│   │   ├── TraitBaseClass.yaml
│   │   ├── VariableBaseClass.yaml
│   │   ├── geoJSON.yaml
│   │   ├── geoJSONSearchArea.yaml
│   │   └── metadata.yaml
│   ├── securitySchemes
│   │   └── AuthorizationToken.yaml
│   ├── GroupDescription.md
│   └── README.md
├── GeneralInfo
│   ├── Date_Time_Encoding.md
│   ├── Error_Handling.md
│   ├── Location_Encoding.md
│   ├── README.md
│   ├── Response_Structure.md
│   ├── Search_Services.md
│   └── URL_Structure.md
├── Generated
│   ├── BrAPI-Core.yaml
│   ├── BrAPI-Genotyping.yaml
│   ├── BrAPI-Germplasm.yaml
│   ├── BrAPI-Phenotyping.yaml
│   ├── README.md
│   ├── brapi_generated.graphqls
│   ├── brapi_generated.json
│   ├── brapi_generated.ttl
│   ├── brapi_openapi.json
│   └── brapi_openapi_comparison.md
├── OpenAPI-Components
│   ├── Parameters
│   │   ├── acceptHeader.yaml
│   │   ├── authorizationHeader.yaml
│   │   ├── externalReferences.yaml
│   │   ├── page.yaml
│   │   ├── pageSize.yaml
│   │   ├── pageToken.yaml
│   │   └── searchResultsDbId.yaml
│   ├── Responses
│   │   ├── 202AcceptedSearchResponse.yaml
│   │   ├── 400BadRequest.yaml
│   │   ├── 401Unauthorized.yaml
│   │   ├── 403Forbidden.yaml
│   │   └── 404NotFound.yaml
│   ├── Schemas
│   │   ├── ContentTypes.yaml
│   │   ├── Context.yaml
│   │   └── metadata.yaml
│   ├── securitySchemes
│   │   └── AuthorizationToken.yaml
│   └── README.md
├── BIJMANTRA-CROSSWALK.md
├── ENDPOINT-CATALOG.md
├── ENDPOINT-REGISTRY.json
├── FILE-TREE.md
├── README.md
└── swaggerMetaData.yaml

431 directories, 1711 files
```
