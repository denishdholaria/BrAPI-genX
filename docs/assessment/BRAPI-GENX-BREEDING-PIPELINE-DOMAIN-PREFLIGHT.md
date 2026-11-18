# BrAPI-GenX — Breeding Pipeline Domain Preflight

**Status:** Research assessment; non-normative; no specification acceptance or implementation authorization.  
**Assessment date:** 18 November 2026  
**Initial repository baseline:** \`main\` at \`2d696fb677c0efa8f956981032160b0a1a49cd58\`  
**Current inspected code baseline:** \`main\` at \`569a75e194df2ee540ecd60615bad2790523c022\` (subsequent commits before this update change only \`LICENSE\`).  
**Companion design proposal:** [Breeding Pipeline and Breeding Scheme Design Proposal](./BRAPI-GENX-BREEDING-PIPELINE-DESIGN-PROPOSAL.md)  
**Related project:** \`denishdholaria/bijmantra-project\` — Ambika ideal-module catalog  
**Workstream:** BGX-P1-00 — BreedingPipeline specification identity and domain preflight

## 1. Executive conclusion

Do not proceed by merely expanding the current \`pipelineStage\` string into a larger array.

The existing proposal appears to conflate at least two related but distinct domain concepts:

1. **Breeding pipeline:** a goal- and product-oriented breeding effort within a breeding program, directed at a market or target segment and an intended deliverable.
2. **Breeding scheme:** the detailed technical strategy or blueprint describing crossing, evaluation, and selection tasks and decisions across breeding stages and cycles.

The distinction is material. Published plant-breeding work describes a program as containing multiple pipelines; a pipeline may address one or more market segments and product profiles and may use one or more schemes. A scheme describes the crossing, evaluation, and selection tasks and decisions that implement the strategy. Recurrent selection can repeat stage-gate cycles, and breeding programs may operate multiple generations and cohorts in parallel. A single linear stage sequence is therefore not a generally sufficient representation of breeding practice.

A 2025 rice-breeding framework describes a breeding program as managing multiple prioritized pipelines, defines a pipeline in relation to a product concept and market segment, and explicitly distinguishes the overall framework from the evolving breeding scheme. Definitions vary somewhat across published operational frameworks, so BrAPI-GenX must record its chosen meanings explicitly and validate them with breeders from more than one crop and institution.

**Recommended direction:** preserve the existing work, reconcile RFC-014 and RFC-154, and conduct a domain-model decision exercise around a pipeline/scheme boundary before changing any endpoint or schema. Keep the design-time blueprint separate from the actual advancement, selection, trial, crossing, and germplasm records that it references.

## 2. Scope and evidence

This assessment is based on read-only inspection of:

- BrAPI-GenX \`main\`, including RFC-014, RFC-154, BreedingPipeline schemas, the endpoint registry, domain classification, maturity register, README, and governance documents.
- The parent repository’s Ambika catalog for the E1 breeding-records-and-planning capability pack and its related module responsibilities.
- Official BrAPI v2.1 specification material and the BrAPI v2.1 source contracts for Programs, Trials, Studies, Germplasm, BreedingMethods, CrossingProjects, PlannedCrosses, and Crosses.
- MIAPPE’s published scope and release information.
- Peer-reviewed and community breeding-system references listed in section 12.

This document does not change official BrAPI, authorize a GenX normative decision, or authorize implementation. Ambika is used as a domain-ownership reference, not as an endpoint-generation checklist.

## 3. Scientific terminology and candidate domain model

### 3.1 Distinguish the concepts

| Concept | Working definition for investigation | Important boundary |
|---|---|---|
| BrAPI Program | Existing BrAPI organizational/research program reference | Reuse the official resource; do not create a GenX duplicate of Program |
| Breeding pipeline | A goal- and product-oriented breeding effort associated with a breeding program, intended deliverables, target segment(s), and product concept(s) | Not a Trial, Study, or synonym for the whole breeding program |
| Market segment | A group of users or customers and target environments with sufficiently related product needs | May be referenced by multiple pipelines; public resource status is undecided |
| Product concept/profile | A description of the intended product and target traits, including thresholds or acceptable ranges where defined | Do not assume every program has one fixed profile or that all traits are numeric |
| Breeding scheme | A detailed, versioned strategy or blueprint of crossing, evaluation, and selection tasks and decisions | A pipeline may use one or more schemes; schemes may evolve over breeding cycles |
| Breeding stage | A named phase or context in a scheme where specified activities and decisions occur | Do not assume a universal crop-independent stage vocabulary or strictly linear order |
| Breeding cycle | A biologically and operationally meaningful cycle, often measured from making crosses until selected progeny are recycled as parents | Do not equate cycle, generation, season, trial, and stage |
| Cohort / selection stream | A set of materials progressing through a scheme or cycle | Cohorts may overlap; several generations can be active at once |
| Population advancement | An actual progression or advancement record for a population, family, or set of lines | Execution/result record; should not be confused with a scheme definition |
| Selection decision | An actual decision about material, candidates, or advancement, with criteria and evidence | Decision record; not simply a free-text stage attribute |

The 2022 paper by Covarrubias-Pazaran and colleagues describes a breeding program as a set of pipelines serving market/target segments. Each pipeline has a deliverable and customer; it may target multiple segments and product profiles and may use one or more breeding schemes. The paper defines breeding schemes in terms of crossing, evaluation, and selection (CES) tasks and decisions that vary across stages.

The 2025 OneRice framework defines a breeding program as a program of work managing prioritized pipelines, defines pipelines in relation to crosses and selections for a product concept mapped to a market segment and breeding network, and defines a breeding cycle as the duration from making crosses until the best progeny are recycled as parents. It explicitly distinguishes the overall breeding framework from the evolving breeding scheme.

These references are complementary, but they do not establish a single universally mandated ontology. BrAPI-GenX should state its adopted definitions, document alternative usage, and support justified mappings rather than silently treating local vocabulary as universal.

### 3.2 Why a flat ordered list is insufficient

The current stage-gate proposal needs to account for more than a sequence of labels:

- Crossing decisions can include parent selection, mating allocation, cross type, number of crosses, and progeny numbers.
- Evaluation decisions can include locations, replication, checks, experimental design, plot dimensions, and testing arrangements.
- Selection decisions can include selection unit, method, intensity, recycling choices, and evidence used.
- Stage-gate processes may repeat cyclically.
- Programs can run multiple generations in parallel.
- Cohorts or selection streams can overlap across generations.
- A pipeline may have a principal scheme and one or more experimental schemes.

A flat array with a unique integer order might still be useful as a presentation order, but it must not be treated as the complete scientific model. Research should determine whether scheme topology needs explicit transitions, repeat/cycle semantics, cohort flows, parallel paths, or a more general activity graph. Do not select a graph representation merely because it is technically convenient; derive it from validated breeding use cases.

### 3.3 Separate design-time definitions from execution-time records

The following distinction should guide resource boundaries:

- **Design-time:** pipeline purpose, product concept, target segment, scheme definition, stage/decision rules, planned resource allocation, and versioned strategy.
- **Execution-time:** actual crosses, germplasm, trial and study records, observations, genomic data, selection verdicts, population advancement, and evidence of outcomes.

Execution records should reference the relevant pipeline/scheme version where useful. They should not be embedded wholesale in a pipeline definition or cause a historical scheme to be silently rewritten when actual material advances.

## 4. Relationship to official BrAPI and other standards

### 4.1 Preserve and reuse official BrAPI v2.1 resources

The BrAPI v2.1 source contracts already provide related resources that GenX should reference rather than duplicate:

| Existing resource | Existing responsibility | GenX design implication |
|---|---|---|
| Program | High-level organizational/research program context | A GenX pipeline can reference a BrAPI Program; it is not a replacement for Program |
| Trial | Groups related studies and provides trial-level context | A pipeline can reference related trials where justified; it is not itself a trial |
| Study | Describes an experiment at a location and carries experimental design and related study metadata | Link studies as evidence or evaluation executions; do not reproduce Study fields in a pipeline |
| BreedingMethod | Describes a method used to produce germplasm/crosses | Reference the official breeding-method identity where applicable |
| CrossingProject | Organizes planned and executed crossing work | Reuse for crossing project context |
| PlannedCross | Represents intended mating activity | Reuse for planned mating records |
| Cross | Represents an actual cross and parent relationships | Reuse for actual crossing outcomes |
| Germplasm, Pedigree, Progeny | Represents biological material and lineage | Reference the official material and relationship records |

The exact foreign-key and lifecycle mapping must be checked against the BrAPI v2.1 source schemas during RFC revision. Similar labels do not establish semantic equivalence.

The BrAPI website currently identifies v2.1 as the latest stable release and labels the working-group New Concept Preview as subject to change until formal release. GenX should therefore keep its v2.1 compatibility analysis anchored to the stable v2.1 contracts and treat preview material only as research input, not as a released contract.

### 4.2 MIAPPE alignment

MIAPPE is a community-driven standard for harmonizing plant-phenotyping experiment metadata and provides a checklist and data model. MIAPPE v1.2 was released in October 2024 and remains compatible with v1.1.

For the pipeline/scheme work:

- Use BrAPI Trial and Study contracts and MIAPPE mappings for experiment/phenotyping context.
- Do not turn a breeding pipeline into an experimental investigation.
- Do not copy all MIAPPE experimental metadata into a pipeline or scheme.
- Define references and crosswalks for trials, studies, treatment context, observation units, variables, and data links where needed.
- Preserve MIAPPE’s role in adequately describing phenotyping experiments rather than inventing an alternative experiment metadata model.

## 5. BrAPI-genX repository findings

### 5.1 Duplicate RFC ownership

The current repository has two RFCs for the same BreedingPipeline object and the same three operation identifiers/routes:

- RFC-014 — Breeding Pipeline (Stage Gates)
- RFC-154 — Breeding Pipeline

Both describe:
- GET /genx/v1/breeding-pipelines
- POST /genx/v1/breeding-pipelines
- GET /genx/v1/breeding-pipelines/{breedingPipelineDbId}

The module README links to RFC-154. The maturity register lists both as separate structural drafts. The current domain-classification registry has two BreedingPipeline entries for the same module path.

The historical RFC-014 schema (from the commit that introduced the module on 1 November 2026) required a Program reference, pipeline name, and stages array. Its stage structure included stage name, stage order, entry criteria, exit criteria, and selection method. The current main-branch schema instead uses a scalar pipelineStage, plus pipelineType, breedingProgram, targetTrait, status, supersedes, and provenance. RFC-154 describes that scalar form.

This is not a harmless documentation duplicate: the resource’s intended meaning and field structure changed while the endpoint identity remained the same.

**Current repository linkage:** the module README, current schemas, and endpoint-operation metadata use RFC-154 as the working document. RFC-014 is the earlier stage-gate proposal. This makes RFC-154 the current editorial surface, but does not make its scalar-stage schema semantically adequate or ratified. Neither RFC should be treated as the accepted canonical contract at this point. Retain both as evidence; select one canonical RFC or split the pipeline and scheme into separate RFCs only after the domain boundary is settled. Any supersession or withdrawal must be recorded explicitly; do not delete or renumber either RFC.

### 5.2 Endpoint registry metadata defect

The master endpoint registry has three BreedingPipeline entries. GET and list operations reference RFC-014; POST references RFC-154.

The POST entry contains unrelated ArtifactCatalogue / VCF-export description content, including an ArtifactCatalogue operation name and vcfExportDbId examples. This indicates semantic metadata contamination, even though structural registry validation currently passes.

The registry root metadata is also stale relative to the current repository:
- generatedAt is 2026-10-22;
- the GenX source metadata names denishdholaria/BrAPI-Den and a historical proposal ref;
- expectedOperationCount remains 21 while buildIntegrity.genxEntriesAdded is 462.

This requires a separate source-of-truth and generation audit. Do not hand-edit the generated registry or its derived catalogues as an isolated patch. Correct the authoritative source records, regenerate, and validate the results in a bounded control-plane workstream.

### 5.3 Classification and maturity records

The machine-readable domain classification has duplicate BreedingPipeline module-path entries: one classified as D2 and another with a null primary domain. The maturity register independently lists RFC-014 and RFC-154 as structural drafts.

Reconciliation must update all references consistently:
- RFC index and module README;
- maturity register;
- machine-readable domain classification;
- endpoint registry source records;
- generated endpoint catalogue;
- relevant decision references and crosswalks.

Do not promote the module’s maturity status merely because the YAML passes schema validation.

## 6. Parent-repository Ambika boundary crosswalk

The parent repository’s E1 capability pack contains distinct proposed responsibilities, including:

- breeding_pipeline_and_stage_gates;
- breeding_program_and_objectives;
- population_and_line_advancement;
- selection_decisions_and_verdicts;
- crossing_projects;
- planned_crosses_and_mating_design;
- executed_crosses_and_parent_links;
- progeny_and_family_records;
- candidate_variety_lifecycle_reference;
- pedigree_and_lineage.

This supports the need to distinguish pipeline planning, program objectives, actual advancement, selection decisions, crossing, and biological lineage. It does not prove that each responsibility requires a separate public GenX endpoint.

Ambika explicitly describes itself as a target-state catalog, not implementation authorization. Use it to test responsibility ownership and identify candidate interoperability gaps. Each proposed public resource must still demonstrate cross-organization value, stable identity, meaningful relationships, mature semantics, and independent implementability.

## 7. Candidate conceptual relationship model

The following is a research model, not an approved contract:

**BrAPI Program**  
→ **GenX BreedingPipeline**  
→ one or more **Market Segment / Product Concept references**  
→ one or more **BreedingScheme versions**  
→ stage and CES task/decision definitions  
→ references to official BrAPI resources and separate execution records.

Potential links:

- Pipeline → official Program.
- Pipeline → market segment and product concept/profile, if reusable identities and cross-organization exchange are justified.
- Pipeline → one or more versioned schemes.
- Scheme → stage definitions and crossing/evaluation/selection task definitions.
- Scheme crossing tasks → BreedingMethod, CrossingProject, PlannedCross, Cross, and Germplasm references.
- Scheme evaluation tasks → Trial, Study, ObservationUnit, ObservationVariable, and MIAPPE-aligned experiment metadata.
- Actual selection and advancement → separate SelectionDecision and PopulationAdvancement records, linked to the pipeline/scheme version and relevant germplasm/study evidence.

Open modelling questions:

1. Is BreedingScheme a first-class independently exchangeable resource, or can it initially be an embedded versioned component of BreedingPipeline?
2. Are MarketSegment and ProductConcept reusable reference resources, embedded snapshots, or external references?
3. Does a pipeline target multiple market segments and product concepts, and can different schemes serve the same target?
4. How should crop-specific stage vocabulary coexist with portable identifiers and local terminology?
5. What is the minimum model for cycles, parallel generations, cohorts, selection streams, and repeated stage gates?
6. Which CES decisions belong in a reusable scheme blueprint versus an actual selection, advancement, trial, or crossing record?
7. How should a scheme version relate to execution records created under earlier versions?
8. Which operations are needed for discovery, registration, retrieval, versioning, and lifecycle management, and which are better left to the linked BrAPI resources?

## 8. Specification-quality gates for the pilot

Before any resource is advanced beyond structural draft, require evidence for each area:

1. **Use case:** real cross-organization scenario, actors, information exchanged, and intended interoperability outcome.
2. **Terminology:** operational definitions of breeding program, pipeline, scheme, cycle, stage, cohort, market segment, and product concept.
3. **Authority:** source of truth and lifecycle owner for every field and relationship.
4. **Boundary:** exact comparison with BrAPI Program, Trial, Study, BreedingMethod, CrossingProject, PlannedCross, Cross, Germplasm, and MIAPPE.
5. **Identity:** authority namespace, stable identifiers, version identity, supersession rules, and external identifiers.
6. **Structure:** entity relationships, cardinalities, requiredness, stage topology, cycles, cohorts, and parallel streams.
7. **Semantics:** controlled vocabularies, units, quantities, temporal and spatial meaning, criteria and evidence.
8. **Lifecycle:** draft, approved, active, retired/superseded, and correction semantics, with distinction between definition and execution.
9. **Operations:** justified HTTP methods, query filters, pagination, sorting, status codes, errors, idempotency, concurrency, and side effects.
10. **Security:** confidentiality and authorization boundaries for breeding strategy, partner contributions, germplasm, and decision evidence.
11. **Examples:** realistic examples across at least two materially different crop-breeding contexts, including one recurrent/overlapping-generation case.
12. **Falsifiability:** invalid examples and explicit observations that would disprove the proposed model.
13. **Independent implementation:** an implementer must be able to represent and exchange the concept without BijMantra-specific assumptions.

## 9. Recommended bounded next sequence

### Step A — Model and repository reconciliation

- Use the companion design proposal as the working model recommendation, not as a ratified contract.
- Keep RFC-014 and RFC-154 at \`STRUCTURAL_DRAFT\` while the maintainer decides the pipeline/scheme boundary and RFC disposition.
- Remove the duplicate \`BreedingPipeline/\` domain-classification entry, retaining the D2-classified entry.
- Correct contaminated endpoint metadata at its authoritative source, then regenerate derived catalogues and validate the registry. Do not hand-edit a generated registry as an isolated repair.
- Keep historical RFCs, operation identifiers, and decision references traceable.

### Step B — Scientific model review

- Test the definitions against published breeding examples from at least two materially different crop and breeding contexts; external participation is not a prerequisite for this internal design work.
- Include at least one recurrent-selection or population-improvement example and one product-development example.
- Include crop-specific variation rather than assuming a universal stage list.
- Determine whether market segment and product concept should remain external references, embedded target-context descriptions, or independent resources; do not create public endpoints before that boundary is justified.

### Step C — Contract design

Only after Steps A and B:
- define canonical resource boundaries and ownership;
- define versioned schema(s), references, lifecycle and operation contracts;
- create valid/invalid fixtures and conformance probes;
- assess official BrAPI compatibility and MIAPPE mapping;
- obtain independent implementability review.

### Explicit exclusions from the current preflight

- No deletion or renumbering of RFCs.
- No change to official BrAPI v2.1 routes, operation IDs, schemas, or generated release artifacts.
- No new public endpoint or schema promotion.
- No Ambika catalog change.
- No assumption that every Ambika module needs a GenX resource.
- No claim of community acceptance or production conformance.

## 10. Related engineering finding: live conformance startup regression — resolved

The live-reference conformance workflow initially failed because the job installed PyYAML but omitted the pinned \`rfc8785==0.1.4\` dependency imported by the JSON Canonicalization Scheme (JCS) module. The reference server exited before live probes could run.

The dependency and startup-failure diagnostics were corrected directly on \`main\` in commit [`cbba636`](https://github.com/denishdholaria/BrAPI-genX/commit/cbba6361ec00758fe8b27531719e7beb48b785b0).

Verification on the resulting code baseline:
- Conformance workflow run [44281104026](https://github.com/denishdholaria/BrAPI-genX/actions/runs/44281104026): \`live-reference-conformance\` and \`static-conformance\` both completed successfully.
- Specification-build workflow run [44281111071](https://github.com/denishdholaria/BrAPI-genX/actions/runs/44281111071): both \`check\` and \`generate\` completed successfully, including specification validation and generated-artifact comparison.
- The later commits [`3f5f0fb`](https://github.com/denishdholaria/BrAPI-genX/commit/3f5f0fb0da1fbd1d1a77c0ad5ef3bebb4ea8c1d5) and [`569a75e`](https://github.com/denishdholaria/BrAPI-genX/commit/569a75e194df2ee540ecd60615bad2790523c022) changed only the \`LICENSE\` file; they did not alter the tested specification or conformance code.

The temporary draft pull requests used to stage these changes were closed after the changes were committed directly to \`main\`. There is no remaining pull-request dependency for this engineering fix.

## 11. Preflight recommendation

The next design artifact is the companion [Breeding Pipeline and Breeding Scheme Design Proposal](./BRAPI-GENX-BREEDING-PIPELINE-DESIGN-PROPOSAL.md). It recommends a pipeline + scheme domain boundary but remains advisory and non-normative. The best first scientific pilot remains breeding pipeline development, but it should be treated as a **pipeline + scheme domain-boundary exercise**, not as a task to fill out the current BreedingPipeline schema.

Keep RFC-014 and RFC-154 as history, reconcile the owner, and define the intended separation between:
- program-level/product-oriented pipeline;
- technical breeding scheme and its stage/cycle strategy;
- actual crossing, evaluation, selection, advancement, and germplasm records.

Only then should BrAPI-GenX decide whether the first release contains a single BreedingPipeline resource with a well-defined embedded scheme, two related resources, or a different minimal interoperable surface. The answer must follow validated domain need, not the existing three-operation template.

## 12. References

### BrAPI and interoperability
- Official BrAPI specification and release status: https://brapi.org/specification
- BrAPI v2.1 source repository: https://github.com/plantbreeding/BrAPI/tree/brapi-V2.1
- MIAPPE overview and scope: https://www.miappe.org/
- MIAPPE releases (v1.2, October 2024): https://www.miappe.org/releases/

### Breeding-pipeline and scheme literature
- Covarrubias-Pazaran, G., Gebeyehu, Z., & Sirak, S. (2022). *Breeding Schemes: What Are They, How to Formalize Them, and How to Improve Them?* Frontiers in Plant Science. https://doi.org/10.3389/fpls.2021.791859
- Bhosale, S., Prakash, P. T., et al. (2025). *Onerice breeding framework: An end-to-end system to develop better varieties faster.* Crop Science. https://doi.org/10.1002/csc2.70087
- Excellence in Breeding — Breeding Pipeline Manager: https://excellenceinbreeding.org/toolbox/tools/breeding-pipeline-manager-1
- Excellence in Breeding — Breeding definitions: https://excellenceinbreeding.org/toolbox/tools/breeding-definitions
- Excellence in Breeding — Breeding scheme optimization toolbox: https://excellenceinbreeding.org/toolbox/collections/4

### BijMantra/Ambika source
- E1 breeding records and planning pack: https://github.com/denishdholaria/bijmantra-project/tree/main/Ambika/ideal-module-catalog/E-plant_breeding_and_variety_development/E1-breeding_records_and_planning
