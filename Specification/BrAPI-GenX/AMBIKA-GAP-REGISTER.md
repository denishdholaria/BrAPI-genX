# BrAPI-GenX vs Ambika Ideal Module Catalog — Gap Register

- Status: proposal / working register, non-normative.
- Purpose: identify Ambika capabilities that are **not** present in BrAPI v2.1 and therefore
  are candidates for additive BrAPI-GenX (GenX) endpoint specs, without disturbing the
  BrAPI v2.1 standard set or implying equivalence.
- Source: `Ambika/ideal-module-catalog/` (24 domain groups, 47 packs, 402 modules).
- Rule: a capability already standardized in BrAPI v2.1 keeps its official V2.1 location and
  contract. GenX specs are additive (`/genx/v1/...`) and optional.

## Coverage key

- **Covered** — BrAPI v2.1 has a substantially equivalent resource/operation.
- **Partial** — BrAPI v2.1 covers an adjacent/parent resource; the Ambika capability is a gap.
- **None** — no BrAPI v2.1 coverage; candidate for GenX or out of BrAPI scope.
- **Disposition**: `GenX-candidate` (scientific interoperability), `Platform` (cross-cutting/product),
  `Out-of-scope` (business/UI/ops not appropriate for BrAPI).

## Domain-group gap matrix

| # | Ambika domain group | Modules | BrAPI v2.1 | Disposition | Notes / first GenX candidates |
|---:|---|---:|---|---|---|
| 1 | A-platform_foundation_and_trust | 27 | None | Platform | Identity/tenancy/policy/audit; mostly cross-cutting (C1, C9). Candidate: capability negotiation/identity extensions only. |
| 2 | B-reference_data_and_organizational_research_context | 14 | Partial | GenX-candidate | Programs/studies/locations/seasons/people/lists covered. Gaps: project/funding, reusable lists/cohorts, calendars, location geometry, taxon names, reference data versioning. |
| 3 | C-germplasm_and_genetic_resources | 10 | Partial | GenX-candidate | Accessions/samples/seed lots covered. Gaps: collecting missions, conservation membership, MCPD adapter, duplicate review, crosswalks. |
| 4 | D-genebank_seed_lots_and_material_custody | 21 | None | GenX-candidate | Seed-lot ledger exists (GenX). Gaps: storage/conservation, viability, quarantine, sample custody/transfer, retention/disposal. |
| 5 | E-plant_breeding_and_variety_development | 15 | Partial | GenX-candidate | Crosses/trials/pedigree covered. Gaps: breeding pipeline/stage gates, selection decisions (GenX started), doubled haploid, speed breeding, population advancement, progeny/family. |
| 6 | F-trials_studies_and_experimental_design | 12 | Partial | GenX-candidate | Studies/trials/observation units covered. Gaps: block/replication/randomization, treatment assignment, plot identity, experimental protocol/design, field book definition, trial network/MET design. |
| 7 | G-trait_semantics_ontologies_and_reference_vocabulary | 11 | Partial | GenX-candidate | Traits/variables/methods/scales/ontologies covered. Gaps: crop-specific trait dictionary, developmental stage vocab, external vocab sync, measurement method catalogue, units/quantity semantics, terminology versioning/provenance. |
| 8 | H-phenotyping_field_observations_and_plant_measurements | 12 | Partial | GenX-candidate | Observations/units/images/events covered. Gaps: capture workflow, quality flags/corrections, value/missingness, repeated measurement/time series, phenology observations, bulk capture, image metadata linkage. |
| 9 | I-genotyping_sequencing_and_genomic_data | 19 | Partial | GenX-candidate | Variants/callsets/calls/references/maps/markers/plates/samples/allele matrices covered. Gaps: assay/plate workflow, QC reports, genotype call semantics, marker/probe registry, VCF import/export, vendor order/result ingestion, genomic dataset release/access, reference assembly versioning, bioinformatics pipeline provenance. |
| 10 | J-scientific_compute_statistics_and_analytical_results | 26 | None | GenX-candidate | No BrAPI coverage. Gaps: analysis method registry/versions, GWAS/QTL, mixed models/BLUP, heritability, stability, GxE, genomic prediction, kinship, LD/haplotype, PCA, GDD, reproducible job contracts, result provenance/uncertainty. |
| 11 | K-field_agronomy_and_crop_operations | 19 | None | GenX-candidate | No BrAPI coverage. Gaps: farm/site reference, crop cycle/rotation, sowing/planting, irrigation, fertilizer/fertigation, tillage, harvest/yield, field scouting/work orders, yield maps, operational field boundary/history. |
| 12 | L-environment_soil_weather_and_climate | 11 | None | GenX-candidate | No BrAPI coverage (locations only). Gaps: weather station/observation, forecast, climate normals/extremes, soil profile/texture/chemistry/moisture, carbon stock/emissions, water balance, environmental treatments/stress, provenance/quality. |
| 13 | M-geospatial_earth_observation_and_sensing | 22 | None | GenX-candidate | No BrAPI coverage. Gaps: CRS/transforms, spatial index/geometry validation, field/plot/station geometry, spatial query/zonal stats, vector/raster catalogues, satellite/UAV metadata, vegetation index pipeline, cloud masking, telemetry ingestion/normalization, sensor device registry, calibration/quality, edge gateway health. |
| 14 | N-crop_health_plant_protection_and_integrated_pest_management | 11 | None | GenX-candidate | No BrAPI coverage. Gaps: disease/pest observations and scouting, diagnostic evidence, spray application records, IPM strategies, thresholds/alerts, disease resistance characterization, abiotic stress observations, crop health image/model results. |
| 15 | O-advisory_forecasting_and_decision_support | 11 | None | GenX-candidate | No BrAPI coverage. Gaps: crop/variety recommendation, sowing window, irrigation/water advice, nutrient advice, pest/disease risk advisory, yield forecast delivery, crop suitability/site selection, human review accept/reject, explanation/uncertainty/evidence, outcome feedback/evaluation, constraints/local rules. |
| 16 | P-variety_regulation_intellectual_property_and_legal_rights | 16 | None | Out-of-scope | Regulatory/IP business domain. Candidate only for evidence bundles/access policy; otherwise product API. |
| 17 | Q-seed_production_quality_and_commercial_inventory | 16 | None | Out-of-scope | Commercial production/quality/fulfilment. Candidate only for lot traceability interoperability; otherwise product API. |
| 18 | R-marketplace_sales_and_customer_operations | 10 | None | Out-of-scope | Sales/commerce. Not BrAPI scientific interoperability. |
| 19 | S-research_assets_knowledge_and_publication | 19 | None | GenX-candidate | FAIR packages exist (GenX). Gaps: research asset registry, persistent identifiers/DOI, dataset/model artifact catalogue, protocol/method library, license/access metadata, publication review/release, embargo management, biodiversity occurrence/specimen export, evidence packs. |
| 20 | T-data_stewardship_interoperability_and_synchronization | 25 | None | Platform | Import/validation/dedup/crosswalk/sync/replay. Mostly product/platform; GenX-relevant: idempotency/replay already in Jobs; schema mapping adapters. |
| 21 | U-collaboration_tasks_and_workflow | 12 | None | Platform | Collaboration/workflow. Not BrAPI scientific interoperability. |
| 22 | V-reevu_and_ai_assisted_scientific_work | 25 | None | Platform | AI/runtime/model lifecycle/inference provenance. GenX-relevant: model registry exists; inference via Jobs. |
| 23 | W-administration_developer_experience_and_operations | 25 | None | Platform | Admin/dev/ops. GenX-relevant: serverinfo, capability negotiation, conformance. |
| 24 | X-client_experiences | 13 | None | Out-of-scope | UI composition; no API ownership. |

## Coverage status (verified against the filesystem and endpoint registry)

This section records which named gaps above already have a GenX module. It is evidence of
implementation, not a claim of production readiness or of scientific validation.

| Domain | Gap named above | GenX module | RFC |
|---|---|---|---|
| D2 | Selection decisions | `SelectionDecisions/` | RFC-008 |
| D3 | VCF import / export (import side) | `VcfImport/` | RFC-043 |
| D3 | VCF import / export (export side) | `VcfExport/` | RFC-114 |
| D3 | Reference assembly versioning | `ReferenceAssembly/` | RFC-115 |
| D3 | Bioinformatics pipeline provenance | `PipelineProvenance/` | RFC-116 |
| D2 | Experimental design and protocol | `ExperimentalProtocol/` | RFC-117 |
| S | Dataset/model artefact catalogue | `ArtifactCatalogue/` | RFC-118 |
| D3 | Genomic dataset release/access, reference assembly versioning, pipeline provenance | `GenomicDatasets/` | RFC-013 |
| D3 | Assay / plate workflow (design side) | `AssayDesign/` | RFC-061 |
| D3 | Assay / plate workflow (execution side) | `AssayExecution/` | RFC-113 |
| D3 | Variant functional annotation | `VariantAnnotation/` | RFC-062 |
| D4 | Phenotype capture / entry | `PhenotypeCapture/` | RFC-012 |
| D4 | Capture workflow | `CaptureWorkflow/` | RFC-110 |
| D4 | Quality flags / corrections | `QualityFlag/` | RFC-111 |
| D4 | Value / missingness | `ValueMissingness/` | RFC-112 |
| D4 | Confirmations / corrections | `PhenotypeAnnotation/` | RFC-044 |
| D4 | Repeated measurement / time series | `RepeatedMeasurement/` | RFC-025 |
| D4 | Bulk capture | `BulkCapture/` | RFC-040 |
| D4 | Image metadata linkage | `ImageMetadata/` | RFC-032 |
| D5 | Weather observations | `WeatherObservations/` | RFC-010 |
| D5 | Weather forecast | `WeatherForecast/` | RFC-031 |
| D5 | Climate normals / extremes | `ClimateNormals/`, `ExtremeWeather/` | RFC-033, RFC-042 |
| D5 | Soil profile | `SoilProfile/` | RFC-023 |
| D6 | Crop cycle | `CropCycle/` | RFC-029 |
| D6 | Irrigation operation | `IrrigationOperation/` | RFC-024 |
| D6 | Fertilizer application | `FertilizerApplication/` | RFC-026 |
| D6 | Harvest / yield | `HarvestRecords/` | RFC-011 |
| D7 | AnalysisMethod registry | `AnalysisMethods/` | RFC-009 |
| D7 | Reproducible job contracts | `Jobs/` | RFC-001 |
| D7 | Result provenance | `AnalysisResult/`, `Provenance/` | RFC-045 |
| D1 | Sample custody / transfer | `CustodyTransfer/` | RFC-063 |
| D3 | Genotype QC reports | `GenotypeQc/` | RFC-064 |
| D3 | Genotype call and missing call semantics | `GenotypeCallSemantics/` | RFC-072 |
| D3 | Vendor order submission and result ingestion | `VendorOrder/` | RFC-073 |
| D3 | Marker/probe registry | `MarkerProbe/` | RFC-071 |
| D1 | Retention / disposal | `DisposalRecord/` | RFC-065 |
| D6 | Farm / site reference | `Farm/` | RFC-069 |
| D6 | Operational field boundary and history | `FieldBoundary/` | RFC-075 |
| N | Spray application records | `SprayApplication/` | RFC-081 |
| D6 | Field scouting / work orders | `FieldScouting/` | RFC-074 |
| F | Treatment assignment | `TreatmentAssignment/` | RFC-106 |
| F | Plot identity | `Plot/` | RFC-107 |
| F | Field book definition | `FieldBook/` | RFC-108 |
| F | Trial network / MET design | `TrialNetwork/` | RFC-109 |
| D6 | Yield maps | `YieldMap/` | RFC-070 |
| D6 | Sowing / planting | `PlantingOperation/` | RFC-066 |
| D5 | Carbon stock | `CarbonStock/` | RFC-067 |
| D5 | Emissions | `Emissions/` | RFC-076 |
| D5 | Soil texture, chemistry, and moisture | `SoilChemistry/` | RFC-077 |
| D5 | Environmental treatments and stress exposures | `EnvironmentalTreatment/` | RFC-078 |
| D5 | Water balance | `WaterBalance/` | RFC-068 |
| B | Project and funding reference | `Project/` | RFC-089 |
| B | Reusable lists and cohorts | `ReusableList/` | RFC-090 |
| B | Calendars and time conventions | `Calendar/` | RFC-091 |
| B | Taxon names and synonyms | `TaxonName/` | RFC-080 |
| B | Common crop names | `CommonCropName/` | RFC-094 |
| B | Crop and species registry | `CropSpecies/` | RFC-095 |
| B | Institution and collection codes | `InstitutionCode/` | RFC-096 |
| B | People references | `PersonReference/` | RFC-097 |
| B | Research programs | `ResearchProgram/` | RFC-098 |
| B | Server and profile capability metadata | `CapabilityMetadata/` | RFC-099 |
| B | Research locations | `ResearchLocation/` | RFC-100 |
| C | Collecting missions | `CollectingMission/` | RFC-101 |
| C | Conservation membership | `ConservationMembership/` | RFC-102 |
| C | MCPD adapter | `McpdAdapter/` | RFC-103 |
| C | Duplicate review | `DuplicateReview/` | RFC-104 |
| C | Crosswalks | `Crosswalk/` | RFC-105 |
| B | Location geometry reference | `LocationGeometry/` | RFC-092 |
| B | Reference data versioning | `ReferenceDataVersion/` | RFC-093 |
| G | Developmental stage vocabulary | `DevelopmentalStage/` | RFC-079 |
| G | Units and quantity semantics | `UnitsAndQuantity/` | RFC-082 |
| G | External vocabulary sync | `ExternalVocabulary/` | RFC-083 |
| G | Terminology versioning and provenance | `TerminologyVersion/` | RFC-084 |
| G | Ontology term and synonym registry | `OntologyTerm/` | RFC-085 |
| G | Ontology mapping and crosswalks | `OntologyMapping/` | RFC-086 |
| G | Measurement scale and value domain | `MeasurementScale/` | RFC-087 |
| G | Crop-specific trait dictionary | `CropTraitDictionary/` | RFC-088 |
| I | Genomic dataset release/access | `GenomicDatasets/` | RFC-013 |
| S | FAIR packages | `FAIR/` | RFC-006 |
| S | Research asset registry, persistent identifiers / DOI, license/access, embargo | `ResearchAssets/` | RFC-016 |

D3 row 9 named gaps are now covered (genotype call semantics, marker/probe registry, vendor order/result ingestion). D1 row 4 named gaps are now covered. D6 row 11 named gaps are now covered (field scouting/work orders, operational field boundary/history). Still open
D5 row 12 named gaps are now covered (emissions, soil texture/chemistry/moisture depth, environmental treatments/stress).

## Suggested GenX sequencing (scientific gaps first)

1. **D2 Breeding pipeline & selection** — started with `SelectionDecisions` (RFC-008). Next: breeding pipeline/stage gates, population/line advancement, progeny/family, doubled haploid, speed breeding, parent candidate selection, crossing schedule/worklist.
2. **D7 Scientific compute & analysis results** — method registry/versions, result provenance/uncertainty, reproducible job contracts; builds on GenX `Jobs` and `Models`.
3. **D5 Environment & weather/soil** — weather station/observation, forecast, climate normals, soil profile, carbon/emissions, water balance; builds on GenX `Telemetry`.
4. **D6 Field agronomy & harvest** — farm/site, crop cycle, sowing/planting, irrigation, fertilizer, harvest/yield, yield maps.
5. **D4 Phenotyping capture workflow** — capture/entry, quality flags/corrections, value/missingness, repeated measurement/time series, bulk capture, image metadata linkage.
6. **D3 Genomics pipeline provenance** — VCF import/export, reference assembly versioning, bioinformatics pipeline provenance, genomic dataset release/access.
7. **D1 Genebank storage/conservation** — storage location/capacity, viability/germination, quarantine, safety duplication, regeneration, sample custody/transfer, retention/disposal.
8. **S Research assets & publication** — builds on GenX `FAIRPackage`; add research asset registry, persistent identifiers/DOI, dataset/model catalogue, protocol/method library, embargo management.
9. **G Terminology depth** — builds on GenX `VariableTerm`; measurement method catalogue, measurement scales, and crop trait dictionary covered.
10. **B/F reference data & experimental design depth** — block/replication/randomization, treatment assignment, plot identity, experimental protocol/design, field book definition, trial network/MET design.

## Rules for adding new GenX specs

- Only add an object when BrAPI v2.1 has no substantially equivalent resource.
- Reuse BrAPI v2.1 identifiers (Program, Study, Germplasm, Observation, etc.) by reference; do not duplicate them.
- Follow the GenX module pattern: `README.md`, `GroupDescription.md`, `Schemas/*`, `*_GET_POST.yaml`, `*_DbId_GET.yaml`, RFC, classification registry entry, endpoint registry entry, generated catalog update.
- Run `BrAPI-GenX/Scripts/checkGenXEndpointCatalog.py` after changes.
- Classify each new module/operation in `Conformance/domain-classification.yaml` with exactly one primary domain class or explicit cross-cutting.
- Keep platform/business/UI modules out of BrAPI scientific classes.