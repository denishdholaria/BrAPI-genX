# BrAPI-GenX — Breeding Pipeline and Breeding Scheme Design Proposal

**Status:** Advisory design proposal; non-normative; not accepted or ratified.  
**Prepared:** 18 November 2026  
**Workstream:** BGX-P1-01 — BreedingPipeline / BreedingScheme domain boundary  
**Parent assessment:** [Breeding Pipeline Domain Preflight](./BRAPI-GENX-BREEDING-PIPELINE-DOMAIN-PREFLIGHT.md)  
**Candidate contract design:** [Breeding Pipeline and Scheme Candidate Contract Design](./BRAPI-GENX-BREEDING-PIPELINE-SCHEME-CONTRACT-DESIGN.md)  
**Repository baseline:** `main` at `315ba3c524bb09fde0c3580fdb4512b070cc0300` (inspection baseline after the candidate contract-design slice).
**Terminology:** BrAPI (Breeding Application Programming Interface); API (Application Programming Interface); RFC (Request for Comments); CES (crossing, evaluation, and selection); MIAPPE (Minimum Information About a Plant Phenotyping Experiment); CI (Continuous Integration); YAML (YAML Ain't Markup Language).

## 1. Purpose and decision boundary

This proposal converts the domain preflight into a model recommendation that can guide the next specification revision. It is deliberately not an API contract.

It does not:
- ratify a scientific ontology or a normative GenX resource;
- choose the final canonical owner or disposition of RFC-014 and RFC-154;
- change official BrAPI v2.1 paths, schemas, operation identifiers, or semantics;
- create new endpoint YAML, schemas, generated artifacts, or implementation code;
- require external community participation before internal progress can continue.

The repository's decision-authority policy reserves final architecture, scientific/domain, and normative-specification decisions to the project maintainer. This document records an evidence-based recommendation and its alternatives for that decision.

## 2. Research finding: terminology is not fully uniform

The literature supports a meaningful distinction between a product/goal-oriented breeding pipeline and the technical breeding scheme that describes how breeding work is carried out. It does not establish one universal definition used identically by every organization.

The 2022 paper *Breeding Schemes: What Are They, How to Formalize Them, and How to Improve Them?* describes a breeding program as a set of pipelines serving market or target segments. A pipeline can target one or more segments and associated product profiles and can use one or more breeding schemes. In that treatment, a breeding scheme is a collection of crossing, evaluation, and selection (CES) tasks and decisions that vary across breeding stages. The paper also describes recurrent stage-gate cycles, multiple generations being run in parallel, and cohorts or selection streams that can overlap.

The 2025 OneRice framework uses related but not identical wording. It defines a breeding program as work managing prioritized pipelines, and defines a pipeline in terms of crosses and selections for a product concept mapped to a market segment and breeding network. It separately distinguishes the overall breeding framework from the evolving scheme: the framework integrates the program's components, while the scheme describes the breeding process that changes over cycles.

These are operational frameworks, not a universally binding ontology. GenX should state its own chosen boundary, cite the usage it follows, and preserve mappings to alternative local terminology. It should not claim that its definition is the sole scientifically correct definition.

## 3. Recommended GenX conceptual boundary

### 3.1 BreedingPipeline — product/goal-oriented workstream

For the purpose of this GenX design, define a **BreedingPipeline** as:

> A managed, goal-oriented breeding workstream associated with an existing BrAPI Program, organized around one or more intended product or breeding targets, and realized through one or more breeding-scheme versions.

A pipeline is a durable planning and coordination identity. It may cover product development, population improvement, trait discovery, trait introgression, product dissemination, or a justified combination of these purposes.

The pipeline is not:
- the entire BrAPI Program;
- a Trial or Study;
- a single breeding stage;
- a single generation or breeding cycle;
- a collection of all germplasm and execution records;
- a variety-release or regulatory approval record.

**Implication for the current schema:** a scalar `pipelineStage` does not describe the identity or purpose of a whole pipeline. A pipeline can have many active stages and cohorts at the same time. Stage position belongs to scheme definitions and actual execution/progression records, not as a single state-like field on the pipeline itself.

### 3.2 BreedingScheme — versioned process blueprint

For this GenX design, define a **BreedingScheme** as:

> A versioned description of the crossing, evaluation, and selection activities, decisions, and stage relationships used to pursue one or more breeding targets.

A scheme is design-time information. It describes intended process structure and decision rules, not the actual result of a cross, trial, observation, selection, or advancement event.

A BreedingPipeline should be able to reference more than one scheme version. Examples include a principal scheme and a parallel experimental scheme, or a scheme revision adopted after review. This is supported by the 2022 paper's description of pipelines using multiple schemes; whether a single scheme version may be shared by different pipelines remains open.

A scheme version should be immutable once published. A revised scheme should receive a new version identity; it must not silently rewrite the meaning of past execution records.

### 3.3 Stage, cycle, generation, cohort, and selection stream

These terms must not be interchangeable:

| Term | Proposed meaning | Modelling consequence |
|---|---|---|
| **Stage** | A named phase or context in a scheme, such as crossing, multiplication, early testing, or advanced testing | A stage definition is part of the scheme blueprint; its label and local vocabulary can vary by crop and program |
| **Stage transition / gate** | A permitted movement between scheme stages, possibly conditional on specified evidence or decisions | A simple display order must not be mistaken for the full process topology |
| **Breeding cycle** | A repeat of a breeding process, often described from making crosses until selected progeny are recycled as parents | A cycle is not necessarily a season, generation, trial, or stage |
| **Generation** | A biological generation in the crop's reproductive and advancement context | Generation numbering must not be used as a universal substitute for scheme stage or cycle |
| **Cohort / selection stream** | A group of materials progressing through stages in a cycle or overlapping cycles | Several cohorts may be active concurrently; cohort membership is execution-time information |
| **CES task / decision** | A crossing, evaluation, or selection activity or decision occurring in a stage or transition | Multiple tasks and decisions can occur in one stage and can recur in later cycles |

The scientific literature explicitly describes repeated stage-gate processes, parallel generations, and overlapping cohorts. Therefore, `stageOrder` can be a presentation aid, but it is insufficient as the only representation of scheme flow.

## 4. Candidate relationship model

The following is a conceptual proposal. Cardinalities marked **proposed** are modelling recommendations, not accepted contract requirements.

```text
BrAPI Program
    1
    |
    | owns / organizes
    | proposed: one Program -> zero or more pipelines
    v
GenX BreedingPipeline
    |
    | describes one or more target contexts
    | (product concept, market segment, target environments)
    |
    | references one or more exact scheme versions
    v
GenX BreedingSchemeVersion
    |
    | contains
    v
Stage definitions ---- Stage transitions / gates
    |
    | organizes
    v
Crossing / Evaluation / Selection task definitions
    |
    | referenced by actual execution records
    v
BrAPI Crosses, CrossingProjects, PlannedCrosses,
Trials, Studies, Germplasm, Pedigree, Progeny,
and GenX SelectionDecision where applicable
```

Recommended ownership boundaries:

1. **Program:** reuse the official BrAPI Program identity. Do not create a GenX duplicate of Program.
2. **Pipeline:** own the durable workstream identity, purpose, target references, and links to scheme versions.
3. **Scheme:** own the process blueprint, stage definitions, transitions, CES task definitions, and their version history.
4. **Stage and task definitions:** initially remain nested within a scheme version unless independent exchange or reuse is demonstrated.
5. **Cycle and cohort execution:** do not put actual cycle instances, cohorts, germplasm membership, or actual decisions into the reusable scheme blueprint.
6. **Execution evidence:** retain the relevant BrAPI or separately specified GenX records as authoritative. Link them to the exact pipeline and scheme version under which they were produced.

A pipeline and scheme should have separate identities and version histories. An execution record should identify the exact scheme version it used, not merely a mutable "current scheme" pointer.

## 5. Target context: product concepts, market segments, and environments

The current `targetTrait` scalar is too narrow to represent a product concept. Published frameworks describe product concepts/profiles through multiple desired traits and associated thresholds or value ranges. Target contexts can also depend on market segments and target environments.

Recommended direction for the first design iteration:

- Replace the conceptual role of a single `targetTrait` field with one or more **target-context references**.
- A target context should be capable of identifying the relevant product concept/profile, market segment, and target population of environments when these exist.
- Resolve traits and observation variables through existing BrAPI concepts where applicable; do not copy an independent trait ontology into BreedingPipeline.
- Preserve the source authority, persistent identifier, version, and resolvable location of an external target profile.
- Where an external profile cannot be resolved later, consider an immutable descriptive snapshot for historical interpretation. The rules for snapshot content and authority require a later decision.

Do not introduce standalone MarketSegment, ProductConcept, or TargetPopulationOfEnvironments endpoints in this pilot. Their resource boundaries, reuse, authorities, and lifecycle are not yet justified. Keep them as references or a bounded embedded descriptor until a concrete cross-organization exchange use case demonstrates the need for independent resources.

## 6. Scheme structure: model the process, not just a list

A scheme needs to represent at least:

- stage definitions, with stable identifiers within the scheme version;
- one or more crossing, evaluation, and selection task definitions associated with stages;
- decision criteria or references to the criteria and evidence used;
- permitted transitions between stages;
- repeat or cycle semantics where a process returns to an earlier stage;
- parallel paths where different streams progress concurrently;
- references to the target context and relevant resource types.

Do not assume a universal crop-independent stage vocabulary. A scheme may use local stage labels while exposing stable scheme-local identifiers and an optional mapping to an established vocabulary where one is genuinely applicable.

A simple ordered list may be retained for display and human readability. It must not carry all transition semantics. The model should permit:
- a linear sequence where that is accurate;
- branching after evaluation or selection;
- repeated or cyclic paths;
- more than one concurrently active path;
- tasks repeated at different stages or cycles.

The next specification-design slice should compare a small directed process graph with an explicit stage-and-transition model using concrete breeding examples. It should not select a graph data structure simply because it is convenient to implement.

### 6.1 Keep definitions separate from execution

| Design-time scheme content | Execution-time evidence and records |
|---|---|
| Stage and transition definitions | Actual stage/advancement events, if separately modelled |
| Crossing strategy and mating-allocation rules | PlannedCrosses, CrossingProjects, and actual Crosses |
| Evaluation strategy and testing design | Trials, Studies, locations, observations, and experimental records |
| Selection rules and criteria | Actual selection decisions and their evidence |
| Expected cohort flow | Actual germplasm, families, progeny, and cohort membership |
| Planned resource allocation | Actual resource use and measured outcomes |

A scheme can describe what should happen; it must not be treated as proof that the activity happened. The associated execution records remain the source of truth for actual crosses, trials, observations, materials, and verdicts.

## 7. Reuse of existing standards and GenX contracts

The official BrAPI v2.1 specification already includes Program, Trial, Study, Germplasm, and related breeding and experimental resources. Its Germplasm module includes Crosses, Pedigree, and Progeny; BrAPI also provides CrossingProjects and PlannedCrosses. GenX should reference these contracts rather than duplicate their records.

| Concern | Preferred authority / mapping |
|---|---|
| Owning breeding or research program | BrAPI v2.1 Program |
| Crossing project, planned mating, executed cross | BrAPI CrossingProject, PlannedCross, Cross |
| Biological material and lineage | BrAPI Germplasm, Pedigree, Progeny |
| Evaluation experiment and location context | BrAPI Trial, Study, Location |
| Phenotypic traits and observation data | BrAPI Phenotyping resources, with MIAPPE-aligned metadata where relevant |
| Actual selection verdict | Existing GenX SelectionDecision proposal (RFC-008), subject to its own maturity and contract review |
| Pipeline purpose, target context, scheme definition and version | Candidate GenX-specific responsibility |

MIAPPE (Minimum Information About a Plant Phenotyping Experiment) harmonizes metadata for plant-phenotyping experiments. It should inform the description and mapping of the evaluation evidence, not become a substitute for a pipeline or scheme model.

A BrAPI Program reference must identify the source authority or server context when records cross independent BrAPI implementations. A bare unqualified string is not sufficient for globally interoperable reference resolution. Exact reference encoding is a later contract decision.

## 8. Versioning and lifecycle recommendations

The current immutable-record and supersession approach is directionally useful, but the logical resource identity and immutable revision identity should be distinguished.

Candidate model:

- A stable pipeline identifier identifies the continuing workstream.
- Each published pipeline revision has its own immutable revision identifier or version token.
- A stable scheme identifier identifies the continuing process blueprint.
- Each published scheme revision has its own immutable version identity.
- A pipeline revision references the exact scheme versions it adopts.
- Corrections, replacements, and retirement are explicit and preserve historical resolution.
- Actual execution records retain the pipeline and scheme version references that applied when the activity occurred.

This avoids treating every scheme revision as an entirely different pipeline and avoids silently changing the meaning of an old pipeline record.

The current enum `active / superseded / withdrawn` is not yet a complete lifecycle specification. The later contract must distinguish draft, publication/approval, active use, supersession, withdrawal, and correction as appropriate, and define who is authorized to perform each transition. These states must not imply regulatory approval or variety release.

## 9. Alternatives considered

| Option | Description | Assessment |
|---|---|---|
| **A — Pipeline contains an ordered stages array** | Expand RFC-014's stages array and retain all process design inside BreedingPipeline | Better than a scalar stage, but still risks conflating pipeline purpose and scheme structure; difficult to support independent scheme evolution or multiple schemes |
| **B — Pipeline plus first-class versioned scheme** | Pipeline identifies the workstream and target context; one or more scheme versions describe the CES process | **Recommended for further design.** Best fit to the 2022 pipeline/scheme distinction and multiple-scheme use case; requires explicit identity and relationship design |
| **C — Pipeline as a single stage/progression record** | Keep a scalar pipelineStage or treat each stage as a separate pipeline record | Reject as the primary domain model. It collapses pipeline identity into current progress and cannot represent concurrent stages, cohorts, or multiple schemes |
| **D — Fully general workflow/activity graph** | A generic graph engine for all breeding and execution activities | Defer. May be expressive, but is premature without validating the smallest required breeding concepts and risks creating a generic workflow platform |

Option B is a modelling direction, not approval to add a public BreedingScheme endpoint. The first implementation-independent contract exercise should determine whether a scheme version needs independent endpoint identity, or whether a versioned nested resource is sufficient. The evidence favours independent identity; the operation surface remains undecided.

## 10. Consequences for the current RFCs and module

Current repository state:

- RFC-014 describes a pipeline with ordered stages and gate criteria.
- RFC-154 and the current module schemas describe a pipeline record with a scalar `pipelineStage`, pipeline type, breeding program, and target trait.
- The module README, operation metadata, and schemas currently direct readers to RFC-154.
- Both RFCs currently declare the same three endpoint paths and operation identifiers.
- The domain-classification YAML contains exactly one `BreedingPipeline/` entry, classified D2. The duplicate unclassified entry was removed as an engineering-only consistency correction.

Recommended editorial handling:

1. Do not delete or renumber either RFC.
2. Treat RFC-154 as the current module's working-document surface because the README and present schemas refer to it; this is an observation about current repository linkage, not a claim that its schema is semantically correct.
3. Treat RFC-014 as historical stage-gate material and a source of requirements to evaluate, not as a schema to restore wholesale.
4. After the maintainer chooses the pipeline/scheme boundary, consolidate the valid requirements into one canonical RFC, or split pipeline and scheme into separate RFCs if each has an independent contract.
5. Mark any retained predecessor explicitly as superseded or withdrawn only when the maintainer has approved that disposition.
6. Keep endpoint identifiers and routes provisional until the domain model is settled. Do not preserve a three-operation template merely for continuity if a different resource boundary is justified.

The domain-classification duplication is resolved. This engineering-only correction does not decide the scientific model or RFC ownership.

## 11. Validation scenarios for the next design slice

Use published, documented breeding contexts as test cases. External participation is not a prerequisite.

### Scenario 1 — Recurrent population improvement

A pipeline performs recurrent selection. It runs successive breeding cycles, with new crosses created while prior cohorts are still being evaluated. Some cohorts overlap, and parents may be recycled from different cohort streams.

The model must distinguish:
- the persistent pipeline;
- its scheme version;
- cycle instances;
- generation identity;
- cohort or selection-stream membership;
- actual crossing and selection events.

It must not force one active stage or one current cohort on the whole pipeline.

### Scenario 2 — Product development across target environments

A pipeline is organized around a product concept for a market segment and target population of environments. Its evaluation strategy references multiple trials/studies at relevant locations. The product target may contain multiple traits with thresholds or ranges.

The model must distinguish:
- the target product concept from the trait definitions;
- the pipeline from its evaluation trials;
- the scheme's evaluation design from actual trial records;
- a pipeline's target profile from a regulatory release decision.

### Scenario 3 — Multiple strategies for a shared target

A pipeline maintains a principal breeding scheme and an experimental alternative. The experimental version is evaluated, revised, and possibly adopted.

The model must preserve both scheme versions and identify which exact version was used by each execution record. A later adoption must not rewrite earlier evidence.

### Scenario 4 — Crop-specific stage terminology

A scheme from a self-pollinated crop and a scheme from a clonally propagated crop use different stage terminology and process shapes.

The model must permit local stage vocabularies, alternative transitions, and crop-specific process patterns without claiming that the two stage labels are equivalent.

## 12. Proposed acceptance gates for a revised contract

Before revising the schemas or operation definitions, require:

1. An explicit definition of Program, Pipeline, Scheme, Stage, Transition, Cycle, Generation, Cohort, and Selection Stream.
2. A relationship and cardinality table, including the identity owner for each relationship.
3. A stable-identity and immutable-version policy for both pipeline and scheme.
4. A typed target-context reference that can represent product concepts, market segments, and target environments without inventing new public resources prematurely.
5. A scheme model that supports linear, branched, cyclic, and concurrent process paths.
6. A clear separation between design-time task definitions and execution-time records.
7. A BrAPI v2.1 crosswalk covering Program, CrossingProject, PlannedCross, Cross, Germplasm, Pedigree, Progeny, Trial, Study, and relevant phenotyping resources.
8. A mapping to MIAPPE for evaluation/phenotyping experiment metadata, without duplicating its responsibilities.
9. Positive and negative examples for the four scenarios above, with machine-testable invariants.
10. A security and sharing model that recognizes that breeding targets, product strategy, and selection evidence may be restricted.
11. An independent-implementability test using only this proposal and public standards, with no BijMantra-specific assumptions.
12. A maintainer decision on the final domain boundary and RFC disposition before any normative schema promotion.

## 13. Recommended next sequence

**Slice 1 — Model review (this proposal):** complete. Record the pipeline/scheme distinction, alternatives, target-context boundaries, and test scenarios.

**Slice 2 — Repository reconciliation:** completed for the classification and operation-metadata baseline. The duplicate unclassified domain entry has been removed; BreedingPipeline operation descriptions and allowed-use metadata were reconciled against authoritative operation YAML; endpoint catalogue and crosswalk outputs were regenerated and checked. The registry contains 462 proposed GenX operations and 201 official BrAPI v2.1 operations. The source/registry audit examines all 462 GenX source operations with zero loading errors and no remaining drift in operation names, descriptions, allowed-use metadata, or decision references. Semantic-neighbour differences remain review-only: 147 source/registry mismatches across 49 modules and 153 registry-only operation-neighbour references across 153 operations. Do not automatically rewrite these relationships without domain review. RFC maturity remains `STRUCTURAL_DRAFT`.

**Slice 3A — Candidate contract design:** completed as advisory design in [the Pipeline and Scheme Candidate Contract Design](./BRAPI-GENX-BREEDING-PIPELINE-SCHEME-CONTRACT-DESIGN.md). It defines the candidate pipeline/scheme boundary, explicit stage transitions, design-time task definitions, target context, immutable versioning, and an execution-record crosswalk. No endpoint YAML, schema, or operation was changed.

**Slice 3B — Cross-RFC overlap review:** completed in [the Cross-RFC Overlap Review](./BRAPI-GENX-BREEDING-CROSS-RFC-OVERLAP-REVIEW.md). It confirms the strongest GenX-only candidates (SelectionDecision and PopulationAdvancement), identifies high overlap in ProgenyRecord and CrossingSchedule, and finds the current ResearchProgram premise contradicted by BrAPI Program. No RFC or API contract changed.

**Slice 3C — Candidate logical model and fixtures:** completed in [the Candidate Logical Model](./BRAPI-GENX-BREEDING-PIPELINE-LOGICAL-MODEL.md) and [Candidate Fixture Corpus](./BRAPI-GENX-BREEDING-PIPELINE-CANDIDATE-FIXTURES.json). The non-normative model defines relationships, cardinalities, versioning, execution-reference rules, and 20 invariants. Nine machine-readable scenarios cover three positive and six negative cases; structural and semantic checks passed. These are not production conformance fixtures. Their structural and declared design-invariant checks run as a separate preliminary step in the specification-build workflow.

**Slice 4 — Maintainer contract decision package:** completed in [the Maintainer Decision Package](./BRAPI-GENX-BREEDING-PIPELINE-MAINTAINER-DECISION-PACKAGE.md). It consolidates the preferred public resource boundary, scheme representation alternatives, identity/reference/versioning choices, migration impact on the scalar pipelineStage contract, and proposed RFC dispositions. It identifies 13 maintainer decisions. No endpoint YAML, schema, RFC maturity state, or accepted-decision register was changed.

## 14. References

### Breeding domain

- Covarrubias-Pazaran, G. et al. (2022). *Breeding Schemes: What Are They, How to Formalize Them, and How to Improve Them?* Frontiers in Plant Science, 12:791859. https://doi.org/10.3389/fpls.2021.791859
- Bhosale, S. et al. (2025). *Onerice breeding framework: An end-to-end system to develop better varieties faster.* Crop Science, 65(3), e70087. https://doi.org/10.1002/csc2.70087

### Standards and interoperability

- Official BrAPI specification — v2.1 is identified as the latest stable release; its preview material is explicitly subject to change before formal release: https://brapi.org/specification
- BrAPI v2.1 source repository: https://github.com/plantbreeding/BrAPI/tree/brapi-V2.1
- MIAPPE overview: https://www.miappe.org/
- MIAPPE releases — v1.2 (October 2024): https://www.miappe.org/releases/
- BrAPI v2.1 Program reference documentation (rOpenSci brapiR2): https://docs.ropensci.org/brapiR2/reference/brapi_program.html
- BrAPI v2.1 CrossingProject reference documentation (rOpenSci brapiR2): https://docs.ropensci.org/brapiR2/reference/brapi_crossing_projects.html
- BrAPI v2.1 Cross reference documentation (rOpenSci brapiR2): https://docs.ropensci.org/brapiR2/reference/brapi_crosses.html
