# Ambika-to-GenX Coverage Matrix

**Status:** proposal / working matrix, non-normative.
**Baseline commit:** `6c09dff4c8f68fc89df541fc1fdcb09abc95e30c`
**Ambika source:** `Ambika/ideal-module-catalog/` (24 domain groups, 47 packs, 402 modules) — read-only input.

## 1. Purpose and rules

Ambika is a domain architecture catalogue, **not** a list of mandatory public API
endpoints. A module, pack, or domain group does not automatically require a
public GenX resource. Every proposed resource must pass the API-candidacy test in
section 3.

This matrix records, for each Ambika domain group, the disposition of its
capabilities relative to official BrAPI v2.1 and BrAPI-GenX. Module-level detail
lives in `AMBIKA-GAP-REGISTER.md` (which enumerates all 24 groups) and in the
machine-readable `Conformance/domain-classification.yaml`.

## 2. Disposition vocabulary

1. **Existing official BrAPI coverage** — reuse the official contract.
2. **GenX extension candidate** — a demonstrable interoperability gap exists.
3. **Cross-cutting GenX capability** — reusable capability (provenance, terminology, integrity, execution).
4. **Bijmantra platform capability** — application architecture, not automatically public GenX.
5. **Internal implementation capability** — implementation detail, no independent API exposure.
6. **Out of scope** — not an appropriate breeding-data interoperability resource.
7. **Requires research or decision** — insufficient information.

## 3. API-candidacy test

Before a module becomes a GenX resource, all of the following must be answerable:

- Is the underlying concept meaningful outside Bijmantra?
- Do independent organisations need to exchange it?
- Is there an actual interoperability problem?
- Does official BrAPI already represent the concept?
- Can existing BrAPI resources be extended or composed?
- Does the concept have stable identity?
- Does it have well-defined relationships?
- Are its scientific semantics sufficiently mature?
- Is there a reason to expose it as a public resource?
- Can an external implementation implement it without using Bijmantra internals?

Where these cannot be answered, the disposition is **Requires research or
decision** and no endpoint specification is generated.

## 4. Domain-group disposition summary

| # | Ambika domain group | Modules | BrAPI v2.1 | Disposition | GenX module(s) (where present) |
|---:|---|---:|---|---|---|
| 1 | A-platform_foundation_and_trust | 27 | None | Platform | Capability negotiation, identity (cross-cutting) |
| 2 | B-reference_data_and_organizational_research_context | 14 | Partial | GenX-candidate | ResearchProgram, ResearchLocation |
| 3 | C-germplasm_and_genetic_resources | 10 | Partial | GenX-candidate | (seed lots via LotLedger) |
| 4 | D-genebank_seed_lots_and_material_custody | 21 | None | GenX-candidate | LotLedger, ViabilityTesting, SafetyDuplication, Regeneration, Quarantine, CustodyTransfer |
| 5 | E-plant_breeding_and_variety_development | 15 | Partial | GenX-candidate | SelectionDecisions, BreedingPipeline, ProgenyRecords, DoubledHaploid, SpeedBreeding, PopulationAdvancement, CrossingSchedule, ParentCandidateSelection |
| 6 | F-trials_studies_and_experimental_design | 12 | Partial | GenX-candidate | ExperimentalDesign, TreatmentAssignment, FieldBook |
| 7 | G-trait_semantics_ontologies_and_reference_vocabulary | 11 | Partial | GenX-candidate | VariableTerms, OntologyTerm, UnitsAndQuantity, DevelopmentalStage, InstitutionCode, TerminologyVersion, CropSpecies |
| 8 | H-phenotyping_field_observations_and_plant_measurements | 12 | Partial | GenX-candidate | RepeatedMeasurement, PhenologyObservation, ImageMetadata, BulkCapture, FieldGeometry |
| 9 | I-genotyping_sequencing_and_genomic_data | 19 | Partial | GenX-candidate | Genomics/VariantMatrix, ReferenceAssembly, VcfImport, VcfExport, GenotypeQc, GenomicRelationship |
| 10 | J-scientific_compute_statistics_and_analytical_results | 26 | None | GenX-candidate | Heritability, StabilityAnalysis, GxeAnalysis, YieldMap, CalibrationQuality, YieldForecast, CropHealthImage, CropRecommendation, CropSuitability, IrrigationAdvice, NutrientAdvice, PestDiseaseRisk, SowingWindow |
| 11 | K-field_agronomy_and_crop_operations | 19 | None | GenX-candidate | CropCycle, IrrigationOperation, FertilizerApplication, Tillage, Plot, ResearchLocation |
| 12 | L-environment_soil_weather_and_climate | 11 | None | GenX-candidate | SoilProfile, WeatherObservations, WeatherForecast, ClimateNormals |
| 13 | M-geospatial_earth_observation_and_sensing | 22 | None | GenX-candidate | SpatialIndex, SpatialQuery, CrsTransform, FieldGeometry, RasterCatalogue, VegetationIndex, CloudMask, Telemetry, TelemetryNormalization, SensorDevice, EdgeGatewayHealth, RemoteSensingMetadata |
| 14 | N-crop_health_plant_protection_and_integrated_pest_management | 11 | None | GenX-candidate | DiseaseObservation, DiagnosticEvidence, IpmStrategy, ThresholdAlert, DiseaseResistance, CropHealthImage |
| 15 | O-advisory_forecasting_and_decision_support | 11 | None | GenX-candidate | CropRecommendation, SowingWindow, IrrigationAdvice, NutrientAdvice, PestDiseaseRisk, YieldForecast, CropSuitability, HumanReview, ExplanationEvidence, OutcomeFeedback, LocalConstraint |
| 16 | P-variety_regulation_intellectual_property_and_legal_rights | 16 | None | Out-of-scope | Evidence bundles only |
| 17 | Q-seed_production_quality_and_commercial_inventory | 16 | None | Out-of-scope | Lot traceability only |
| 18 | R-marketplace_sales_and_customer_operations | 10 | None | Out-of-scope | — |
| 19 | S-research_assets_knowledge_and_publication | 19 | None | GenX-candidate | ArtifactCatalogue, ProtocolLibrary, PublicationReview, BiodiversityExport, EvidencePack |
| 20 | T-data_stewardship_interoperability_and_synchronization | 25 | None | Platform | SchemaMapping, CapabilityNegotiation, ConformanceProbe (tooling) |
| 21 | U-collaboration_tasks_and_workflow | 12 | None | Platform | — |
| 22 | V-reevu_and_ai_assisted_scientific_work | 25 | None | Platform | Models/ModelArtifact |
| 23 | W-administration_developer_experience_and_operations | 25 | None | Platform | ServerInfoV3, Conformance |
| 24 | X-client_experiences | 13 | None | Out-of-scope | — |

## 5. Traceability pointers

- Module-level Ambika IDs and names: `Ambika/ideal-module-catalog/` (read-only).
- Domain-group detail and named gaps: `AMBIKA-GAP-REGISTER.md`.
- Machine-readable classification of GenX modules: `Conformance/domain-classification.yaml`.
- Official BrAPI operation baseline: `ENDPOINT-REGISTRY.json` (201 v2.1 entries).

## 6. Outstanding scientific decisions

Many GenX modules above are STRUCTURAL_DRAFT or lower maturity (see RFC maturity
register). Their scientific semantics, units, identifiers, lifecycles, and security
requirements remain to be established. No module is promoted to accepted status in
Phase 0.