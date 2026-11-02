# BrAPI-GenX Scientific Domain Classification

- Status: proposed taxonomy for review; non-normative until explicitly accepted.
- Scope: classification of the BrAPI-GenX specification modules, not a claim of BrAPI community endorsement.
- Compatibility: BrAPI V2.1 contracts remain unchanged. This taxonomy does not change endpoint paths, schemas, operationIds, or runtime behavior.

## 1. Design principle

Classify by the primary scientific or operational domain of the resource, not by HTTP verb, implementation technology, owning team, or the fact that a resource is cross-cutting. Keep domain classes distinct from cross-cutting contract capabilities. A resource receives exactly one primary domain class and may receive several secondary facets for discovery. The primary class answers “what domain fact or process is this about?”; facets answer “what properties apply across domains?”

This avoids placing fundamentally different concepts—such as plant genetic material, scientific terminology, asynchronous job execution, and provenance—at the same taxonomic level.

## 2. Proposed top-level taxonomy

The proposal uses seven domain classes plus a separate cross-cutting layer. This is a classification for the expanded BrAPI-GenX scope, not an attempt to rename the existing four BrAPI V2.1 groups.

| Code | Class | Scientific/operational boundary | Typical content |
|---|---|---|---|
| D1 | Germplasm and Biological Resources | Identity, origin, conservation, and access to plant genetic resources and biological materials | Accessions, donors, collections, seed lots and material identity |
| D2 | Breeding Programs and Experimental Design | Intentional improvement of populations/varieties and the design and management of breeding experiments | Programs, objectives, crosses, pedigrees, populations, studies, trials, experimental designs |
| D3 | Genotyping and Molecular Genomics | Molecular measurements and representations of genotype, sequence, variants, alleles, markers, and genomic files | Calls, call sets, variant sets, sequencing metadata, VariantMatrix references |
| D4 | Phenotyping and Plant Observations | Measured or scored plant/plot/organism characteristics, their observation contexts and capture records | Observation units, observations, image-derived phenotype, repeated measurements |
| D5 | Environment, Agroecology and Field Context | External and managed environmental conditions that affect organisms, trials, and crop systems | Weather, soil, climate, abiotic stress, water, field telemetry |
| D6 | Crop Production and Material Operations | Operational custody, movement, treatment, and production-stage handling of biological material | Seed-lot movements, inventory, lot ledger, treatment and operational traceability |
| D7 | Scientific Analysis, Models and Derived Evidence | Computational transformation of source data into estimates, predictions, classifications, or model-derived outputs | Statistical analyses, breeding values, model artifacts, inference outputs, uncertainty-bearing results |

### Why seven

These classes separate biological entities and experimental processes from measured evidence, environmental context, material operations, and derived analytical results. This is more resilient than using current software module names as categories. New domains can be added through governance without forcing unrelated resources into “Core”.

## 3. Cross-cutting contract capabilities (not domain classes)

These concerns apply across domain classes and should be modeled as reusable specification components or facets, not peer scientific classes.

| Capability | Current GenX material | Rule |
|---|---|---|
| C1 Identity, versioning and capability negotiation | ServerInfoV3; namespaced IDs; VariableTerm versions | Governs discoverability and identity; does not own the scientific entity being identified |
| C2 Provenance, evidence and uncertainty | ProvenanceEnvelope; input digests; evidence links | Can accompany measurements, observations, analyses, models and packages |
| C3 Execution lifecycle and idempotency | Jobs; replay/conflict rules; cancellation | Describes how work is invoked and governed, not what scientific domain it belongs to |
| C4 Terminology and semantic governance | VariableTerm; Trait/Method/Scale references | Shared scientific semantics; should reference domain resources rather than duplicate them |
| C5 Data exchange, publication and access | FAIRPackage; license, embargo, persistent identifiers | Exchange/distribution envelope around payloads, not the payload's scientific class |
| C6 Integrity and external artifact references | VariantMatrix digests; model artifact digests | Reusable integrity pattern, with domain-specific resource identity |
| C7 Streaming, telemetry and temporal aggregation | TelemetryPoint | A data-delivery pattern. Classify by meaning: environmental readings belong primarily to D5; plant sensor-derived phenotype belongs primarily to D4; instrument telemetry unrelated to science may be platform operations and outside this scientific taxonomy |
| C8 Conformance and contract governance | Conformance probes, endpoint-overlaps register, decision log | Specification quality and interoperability controls; not scientific data domains |
| C9 Security, authority and tenancy | Authorization scopes, actor/tenant boundaries | Cross-cutting policy constraints; do not create a scientific class for them |

## 4. Mapping current GenX modules

| Current module/object | Primary classification | Cross-cutting facets | Important boundary |
|---|---|---|---|
| Provenance / ProvenanceEnvelope | No standalone domain class; C2 | C1, C6 | Embedded evidence contract, not a standalone /provenance endpoint |
| Jobs / Job | Cross-cutting C3 | C1, C2, C9 | Job type determines the domain of the work; Jobs itself is not a scientific domain |
| ServerInfoV3 | Cross-cutting C1 | C8, C9 | Capability discovery only; not a domain resource |
| VariableTerms / VariableTerm | Cross-cutting C4 | C1, C2 | Semantic governance for Trait/Method/Scale and related definitions |
| LotLedger / LotLedgerEntry | D6 | C1, C2, C3, C6, C9 | Material-movement record; not automatically equivalent to V2.1 SeedLotTransaction |
| Models / ModelArtifact | D7 | C1, C2, C3, C5, C6, C9 | Registry of analytical model artifacts; model governance and approval workflow remain separate |
| Genomics / VariantMatrix | D3 | C1, C2, C5, C6, C9 | External matrix reference, not VariantSet alias and not byte transport |
| FAIR / FAIRPackage | Cross-cutting C5 | C1, C2, C6, C9 | Packaging, license and access envelope; class of payload is unchanged |
| Telemetry / TelemetryPoint | Context-dependent: D5 for environmental sensor readings; D4 for plant/phenotyping measurements | C1, C2, C3, C6, C7, C9 | Do not infer that all telemetry is an Observation or all telemetry is environmental data |
| SelectionDecisions / SelectionDecision | D2 | C1, C2, C3, C9 | Breeding selection verdicts; no BrAPI v2.1 equivalent; corrections are additional superseding records |
| BreedingPipeline / BreedingPipeline | D2 | C1, C2, C3, C6, C9 | Breeding pipeline definitions with stage gates; no BrAPI v2.1 equivalent |
| ExperimentalDesign / ExperimentalDesign | D2 | C1, C2, C3, C6, C9 | Trial layout, replication, randomization, treatment assignment; no BrAPI v2.1 equivalent |
| ProgenyRecords / ProgenyRecord | D2 | C1, C2, C3, C6, C9 | Progeny/family links with parents, generation, and provenance; no BrAPI v2.1 equivalent |
| DoubledHaploid / DoubledHaploidProgram | D2 | C1, C2, C3, C6, C9 | Doubled haploid program records; no BrAPI v2.1 equivalent |
| SpeedBreeding / SpeedBreedingProtocol | D2 | C1, C2, C3, C6, C9 | Speed breeding protocol records; no BrAPI v2.1 equivalent |
| SoilProfile / SoilProfile | D5 | C1, C2, C3, C6, C9 | Soil profile records; no BrAPI v2.1 equivalent |
| IrrigationOperation / IrrigationEvent | D6 | C1, C2, C3, C6, C9 | Irrigation event records; no BrAPI v2.1 equivalent |
| RepeatedMeasurement / MeasurementSeries | D4 | C1, C2, C3, C6, C7, C9 | Repeated measurement series; no BrAPI v2.1 equivalent |
| FertilizerApplication / FertilizerApplication | D6 | C1, C2, C3, C6, C9 | Fertilizer application records; no BrAPI v2.1 equivalent |
| PhenologyObservation / PhenologyObservation | D4 | C1, C2, C3, C6, C9 | Phenology observation records; no BrAPI v2.1 equivalent |
| ParentCandidateSelection / ParentCandidateSelection | D2 | C1, C2, C3, C6, C9 | Parent candidate selection records; no BrAPI v2.1 equivalent |
| CropCycle / CropCycle | D6 | C1, C2, C3, C6, C9 | Crop cycle records; no BrAPI v2.1 equivalent |
| Quarantine / QuarantineRecord | D1 | C1, C2, C3, C6, C9 | Quarantine records; no BrAPI v2.1 equivalent |
| CustodyTransfer / CustodyTransfer | D1 | C1, C2, C3, C6, C9 | Chain-of-custody transfer records; no BrAPI v2.1 equivalent |
| WeatherForecast / WeatherForecast | D5 | C1, C2, C3, C6, C7, C9 | Weather forecast records; no BrAPI v2.1 equivalent |
| ImageMetadata / ImageMetadata | D4 | C1, C2, C3, C6, C9 | Image metadata records; no BrAPI v2.1 equivalent |
| ClimateNormals / ClimateNormal | D5 | C1, C2, C3, C6, C9 | Climate normal records; no BrAPI v2.1 equivalent |
| SafetyDuplication / SafetyDuplication | D1 | C1, C2, C3, C6, C9 | Safety duplication records; no BrAPI v2.1 equivalent |
| Regeneration / RegenerationRecord | D1 | C1, C2, C3, C6, C9 | Regeneration records; no BrAPI v2.1 equivalent |
| PopulationAdvancement / PopulationAdvancement | D2 | C1, C2, C3, C6, C9 | Population advancement records; no BrAPI v2.1 equivalent |
| CrossingSchedule / CrossingSchedule | D2 | C1, C2, C3, C6, C9 | Crossing schedule records; no BrAPI v2.1 equivalent |
| Tillage / TillageRecord | D6 | C1, C2, C3, C6, C9 | Tillage records; no BrAPI v2.1 equivalent |
| CandidateVarietyLifecycle / CandidateVariety | D2 | C1, C2, C3, C6, C9 | Candidate variety lifecycle records; no BrAPI v2.1 equivalent |
| Acquisition / AcquisitionRecord | D1 | C1, C2, C3, C6, C9 | Acquisition records; no BrAPI v2.1 equivalent |
| PhenotypeAnnotation / PhenotypeAnnotation | D4 | C1, C2, C3, C6, C9 | Phenotype annotation records; no BrAPI v2.1 equivalent |
| ExtremeWeather / ExtremeWeatherEvent | D5 | C1, C2, C3, C6, C9 | Extreme weather event records; no BrAPI v2.1 equivalent |
| VcfImport / VcfImport | D3 | C1, C2, C3, C5, C6, C9 | VCF import records; no BrAPI v2.1 equivalent |
| AssayDesign / AssayDesign | D3 | C1, C2, C3, C6, C9 | Assay design records; no BrAPI v2.1 equivalent |
| VariantAnnotation / VariantAnnotation | D3 | C1, C2, C3, C6, C9 | Variant annotation records; no BrAPI v2.1 equivalent |
| GenotypeQc / GenotypeQcReport | D3 | C1, C2, C3, C6, C9 | Genotype QC report records; no BrAPI v2.1 equivalent |
| DisposalRecord / DisposalRecord | D1 | C1, C2, C3, C6, C9 | Disposal records; no BrAPI v2.1 equivalent |
| AnalysisResult / AnalysisResult | D7 | C1, C2, C3, C6, C9 | Analysis result records; no BrAPI v2.1 equivalent |
| GeneticGain / GeneticGainRecord | D7 | C1, C2, C3, C6, C9 | Genetic gain records; no BrAPI v2.1 equivalent |
| GwasResult / GwasResult | D7 | C1, C2, C3, C6, C9 | GWAS result records; no BrAPI v2.1 equivalent |
| MixedModel / MixedModelResult | D7 | C1, C2, C3, C6, C9 | Mixed model result records; no BrAPI v2.1 equivalent |
| StabilityAnalysis / StabilityAnalysisResult | D7 | C1, C2, C3, C6, C9 | Stability analysis result records; no BrAPI v2.1 equivalent |
| Heritability / HeritabilityEstimate | D7 | C1, C2, C3, C6, C9 | Heritability estimate records; no BrAPI v2.1 equivalent |
| GxeAnalysis / GxeAnalysisResult | D7 | C1, C2, C3, C6, C9 | GxE analysis result records; no BrAPI v2.1 equivalent |
| Kinship / KinshipMatrix | D7 | C1, C2, C3, C5, C6, C9 | Kinship matrix records; no BrAPI v2.1 equivalent |
| PcaResult / PcaResult | D7 | C1, C2, C3, C6, C9 | PCA result records; no BrAPI v2.1 equivalent |
| GenomicPrediction / GenomicPrediction | D7 | C1, C2, C3, C6, C9 | Genomic prediction result records; no BrAPI v2.1 equivalent |
| GenomicSelection / GenomicSelection | D7 | C1, C2, C3, C6, C9 | Genomic selection result records; no BrAPI v2.1 equivalent |
| GenomicRelationship / GenomicRelationship | D7 | C1, C2, C3, C5, C6, C9 | Genomic relationship matrix records; no BrAPI v2.1 equivalent |
| MethylationAnalysis / MethylationAnalysis | D7 | C1, C2, C3, C6, C9 | Methylation analysis result records; no BrAPI v2.1 equivalent |
| ExpressionQtl / ExpressionQtl | D7 | C1, C2, C3, C6, C9 | Expression QTL result records; no BrAPI v2.1 equivalent |
| HaplotypeAnalysis / HaplotypeAnalysis | D7 | C1, C2, C3, C6, C9 | Haplotype analysis result records; no BrAPI v2.1 equivalent |
| PedigreeAnalysis / PedigreeAnalysis | D7 | C1, C2, C3, C6, C9 | Pedigree analysis result records; no BrAPI v2.1 equivalent |
| BulkCapture / BulkCapture | D4 | C1, C2, C3, C6, C9 | Bulk capture records; no BrAPI v2.1 equivalent |
| AnalysisMethods / AnalysisMethod | D7 | C1, C2, C3, C6, C9 | Versioned analysis method registry; no BrAPI v2.1 equivalent; execution is via Jobs |
| WeatherObservations / WeatherObservation | D5 | C1, C2, C3, C6, C7, C9 | Environmental/weather observation records; no BrAPI v2.1 equivalent; complementary to Telemetry |
| HarvestRecords / HarvestRecord | D6 | C1, C2, C3, C6, C9 | Harvest-event records; no BrAPI v2.1 equivalent; not a SeedLotTransaction |
| PhenotypeCapture / PhenotypeCapture | D4 | C1, C2, C3, C6, C9 | Phenotype capture events; no BrAPI v2.1 equivalent; not a BrAPI Observation |
| GenomicDatasets / GenomicDataset | D3 | C1, C2, C3, C5, C6, C9 | Prepared genomic dataset records; no BrAPI v2.1 equivalent; not a VariantSet or VariantMatrix |
| GenebankStorage / StorageLocation | D1 | C1, C2, C3, C6, C9 | Genebank storage location records; no BrAPI v2.1 equivalent |
| ViabilityTesting / ViabilityTest | D1 | C1, C2, C3, C6, C9 | Viability/germination test records; no BrAPI v2.1 equivalent |
| ResearchAssets / ResearchAsset | (none, cross-cutting) | C1, C2, C3, C5, C6, C9 | Research asset records; no BrAPI v2.1 equivalent; builds on FAIRPackage |
| MeasurementMethods / MeasurementMethod | (none, cross-cutting) | C1, C2, C3, C4, C9 | Measurement method definitions; no BrAPI v2.1 equivalent; terminology governance |
| Conformance | Cross-cutting C8 | C1, C3 | Probes and fixtures establish contract evidence, not scientific-domain data |

## 5. Relationship to BrAPI V2.1

Keep the existing BrAPI V2.1 categories and contracts unchanged:

- BrAPI-Core
- BrAPI-Germplasm
- BrAPI-Genotyping
- BrAPI-Phenotyping

The proposed D1–D7 taxonomy is a broader BrAPI-GenX classification for the expanded proposal. It is not a retrospective reclassification of the BrAPI community's published groups and should not be described as officially endorsed by the BrAPI community.

Crosswalk rules:
- A resource already standardized in V2.1 retains its official V2.1 location and contract.
- The taxonomy adds a classification index; it does not move or duplicate specification files merely to make folder names match.
- Shared infrastructure is tagged as cross-cutting rather than incorrectly assigned to Core.
- Where a resource crosses boundaries, its primary class follows the resource's authoritative meaning; secondary facets are additive and never used to imply wire compatibility.

## 6. Scientific classification rules

1. **Primary-owner rule:** each schema has one primary semantic owner.
2. **Phenomenon-versus-method rule:** classify a record by the phenomenon or entity represented, not the instrument used to collect it. A soil moisture sensor reading is D5; a plant leaf-area measurement is D4.
3. **Observation-versus-derived-result rule:** measured/scored evidence belongs to D4 or D5 as appropriate; model estimates and predictions belong to D7 and must reference inputs and methods.
4. **Biological material rule:** accession identity and conserved diversity belong to D1; production/custody/movement operations belong to D6.
5. **Experiment-versus-breeding-intent rule:** experimental layout and trial design belong to D2; observations collected in a trial belong to D4 and link back to D2's study/trial context.
6. **Cross-cutting rule:** provenance, jobs, capability negotiation, access policies and conformance must not become catch-all scientific classes.
7. **No implied equivalence:** classification proximity never asserts schema equivalence, one-to-one mapping, or safe dual-write behavior.
8. **Extension rule:** new classes require a rationale showing that the concept is an enduring domain with its own vocabulary and lifecycle, not simply a new endpoint, technology, workflow, or team.
9. **Version rule:** existing identifiers, schemas, routes and operationIds are not renamed solely to match taxonomy.
10. **Evidence rule:** claims of standards alignment must cite a specific adopted standard or decision; implementation evidence from BijMantra is evidence only, not authority for the standard.

## 7. Proposed folder and documentation strategy

Do not immediately relocate the current modules. First add a stable classification registry that maps module, schema and operationId to primary domain class and facets. A later review can choose whether physical folders should follow the taxonomy.

Suggested additions:
- `Specification/BrAPI-GenX/CLASSIFICATION.md` — this policy and rationale.
- `Specification/BrAPI-GenX/Conformance/domain-classification.yaml` — machine-readable module/schema/operation mappings.
- An automated conformance check: every GenX module/schema/operation must be classified or explicitly marked cross-cutting; no duplicate primary owners; all cross-generation semantic overlaps remain documented.

## 8. Open design questions

These should remain explicit rather than silently treated as solved:
- Whether D2 should be named “Breeding and Experimental Design” or separate into breeding intent versus trial infrastructure if the future resource set grows.
- Whether seed-lot custody and material operations should sit under D1 or D6. This proposal assigns identity/conservation to D1 and custody/movement/handling to D6.
- Whether analytical model registry is large enough to merit a distinct D7 subdomain later. For now, it belongs with analysis and derived evidence.
- Whether future telemetry must be split into common transport plus context-specific D4/D5 domain payloads. The current TelemetryPoint schema is deliberately generic.
- Whether the proposed seven classes should become folder names. Classification should be validated before restructuring files.

## 9. Status and adoption

This document is a proposal, not a normative BrAPI community standard. It does not amend BrAPI V2.1 and does not accept any deferred item in `DECISIONS.md`. Acceptance requires explicit maintainer decision, review of D-20 and other relevant semantic overlaps, and tests demonstrating that classification does not create hidden equivalence or endpoint duplication.
