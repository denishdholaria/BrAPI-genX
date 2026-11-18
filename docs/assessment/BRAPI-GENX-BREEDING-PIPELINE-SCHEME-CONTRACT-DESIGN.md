# BrAPI-GenX — Breeding Pipeline and Scheme Candidate Contract Design

**Status:** Advisory candidate design; non-normative, not accepted or ratified.  
**Prepared:** 18 November 2026  
**Workstream:** BGX-P1-02 — Pipeline, scheme, and execution-record boundaries  
**Parent assessment:** [Breeding Pipeline Domain Preflight](./BRAPI-GENX-BREEDING-PIPELINE-DOMAIN-PREFLIGHT.md)  
**Parent proposal:** [Breeding Pipeline and Breeding Scheme Design Proposal](./BRAPI-GENX-BREEDING-PIPELINE-DESIGN-PROPOSAL.md)  
**Repository baseline:** \`main\` at \`32e43fdf49a6bb6fd2d642ecf1220e7d4b8f8ade\`  
**Terminology:** BrAPI (Breeding Application Programming Interface); API (Application Programming Interface); RFC (Request for Comments); CES (crossing, evaluation, and selection); MIAPPE (Minimum Information About a Plant Phenotyping Experiment); JSON (JavaScript Object Notation); TPE (target population of environments); URL (Uniform Resource Locator); CI (Continuous Integration); YAML (YAML Ain't Markup Language).
**Scope:** Candidate domain model, resource boundaries, identity/versioning, stage topology, and cross-resource mappings. No schema or endpoint change is made by this document.

## 1. Executive recommendation

Continue with this bounded conceptual model:

1. **BreedingPipeline** — a durable, goal- and target-oriented breeding workstream associated with an existing BrAPI Program.
2. **BreedingScheme** — a separately identifiable, versioned process blueprint describing the crossing, generation-advance, evaluation, and selection activities and decisions used by a pipeline.
3. **Stage definitions, transitions, and task definitions** — initially nested in an immutable BreedingScheme version. Do not create separate public endpoints for these subordinate concepts.
4. **Execution records** — actual crosses, trials, studies, germplasm, progeny, selection decisions, and population-advancement events remain in their existing BrAPI or separately scoped GenX resources. They reference the exact pipeline and scheme version where justified.

Use an explicit stage-transition relation rather than treating a sorted stage array as the whole scheme. The transition relation may express linear, branching, and recurrent paths. It is not a generic workflow engine. Cohorts, generations, and cycle instances are execution-time concepts and must not become mutable properties of the whole pipeline.

**Do not add endpoint operations or revise the current BreedingPipeline YAML schemas yet.** This document advances the design only. Public identity shape, operation surface, and RFC (Request for Comments) disposition remain maintainer decisions.

## 2. Evidence and terminology

Breeding terminology varies across organizations. GenX should publish its chosen definitions and preserve mappings to local vocabulary rather than claim universal terminology.

Two complementary published frameworks support this separation:

- Covarrubias-Pazaran et al. (2022) describe a breeding pipeline as potentially serving one or more market segments and product profiles through one or more breeding schemes. They describe a scheme as crossing, evaluation, and selection (CES) tasks and decisions across breeding stages. Their account includes repeated stage-gate cycles, parallel generations, and overlapping cohorts or selection streams.
- Bhosale et al. (2025), in the OneRice breeding framework, define a pipeline in terms of crosses and selections directed at a product concept mapped to a market segment and breeding network. They distinguish the overall breeding framework from the evolving breeding scheme, and describe a scheme through crossing, generation advancement, evaluation, and selection.

These publications are operational frameworks, not a binding universal ontology. The model below adopts their useful distinction while retaining crop- and organization-specific terminology.

### 2.1 Terms to keep distinct

| Term | Candidate GenX meaning | Must not be confused with |
|---|---|---|
| BrAPI Program | Existing organizational/research-program context | GenX pipeline or scheme |
| Breeding pipeline | Persistent goal- and target-oriented breeding workstream | A single stage, cohort, cycle, trial, or scheme |
| Target context | Product concept/profile, market segment, target population of environments, and associated trait targets | A single trait or experimental study |
| Breeding scheme | Versioned blueprint for the process used to pursue a target | Actual crossing or advancement history |
| Scheme version | Immutable published revision of a scheme definition | A breeding cycle or generation |
| Stage | Named phase or process context in a scheme | A universal crop-independent stage code |
| Transition / gate | Permitted relationship between scheme stages, potentially conditioned on criteria or decisions | An actual advancement event |
| Task definition | Planned crossing, generation-advance, multiplication, evaluation, or selection activity | Evidence that the task was performed |
| Breeding cycle | An execution instance of a biological/operational breeding loop | Season, generation, or stage |
| Generation | Biological generation in the crop’s reproductive context | Pipeline stage or breeding cycle |
| Cohort / selection stream | Group of materials progressing through a scheme/cycle | A scheme stage definition |
| Selection decision | Actual verdict about material, with rationale and evidence | A planned selection rule |
| Population advancement | Actual recorded movement/progression of a population or family | A permitted transition in the scheme |

## 3. Candidate resource boundaries

### 3.1 BreedingPipeline

The pipeline owns the durable workstream identity and target context. It associates with an existing BrAPI Program and may use one or more exact BreedingScheme versions.

Candidate responsibilities:

- persistent pipeline identity and human-readable name;
- relationship to the owning BrAPI Program;
- purpose or program intent, such as product development, population improvement, trait discovery, or trait introgression;
- one or more target-context references or bounded target-context descriptions;
- references to the exact scheme versions adopted or evaluated;
- pipeline-level lifecycle and provenance.

Candidate exclusions:

- current stage of every material in the pipeline;
- actual cycle, generation, cohort, or selection-stream membership;
- actual crosses, trials, studies, observations, or germplasm;
- actual selection verdicts or advancement events;
- variety registration, release, or regulatory approval.

A pipeline does not have one meaningful scalar \`pipelineStage\` when multiple schemes, cohorts, generations, or evaluation streams can be active concurrently. The present scalar should not be treated as a viable long-term domain representation.

### 3.2 BreedingScheme and BreedingSchemeVersion

A scheme describes how breeding work is intended to proceed. Its definition should have a stable logical identity and immutable published versions.

Candidate responsibilities:

- stable scheme identity and descriptive name;
- version identity and version metadata;
- one or more stage definitions;
- explicit permitted transitions between stages;
- crossing, generation-advance, multiplication, evaluation, and selection task definitions;
- references to decision criteria, methods, evidence types, and target contexts where appropriate;
- provenance, authorship, and lifecycle metadata.

A published scheme version should not be edited in place. A substantive revision produces a new version. A pipeline revision references the exact scheme version it adopted, not a mutable \`currentScheme\` pointer.

A scheme may initially be scoped to one pipeline. Reuse by multiple pipelines is an open relationship question: the evidence establishes that one pipeline may use multiple schemes, but does not by itself prove that one scheme definition should be shared across independent pipelines. Do not enforce or prohibit cross-pipeline reuse until a use case requires the rule.

### 3.3 Stage definitions, transitions, and task definitions

These are subordinate structures, not independent resources in the first design.

A stage definition needs:
- a stable identifier within the scheme version;
- a human-readable label and optional description;
- an optional local code and optional mapping to an external vocabulary;
- an optional display order, used only for presentation;
- zero or more task definitions.

A transition needs:
- source and target stage identifiers;
- a transition kind or rationale where that distinction is useful;
- optional decision criteria or references to criteria;
- optional description of the gate and evidence needed.

A task definition needs:
- a stable task identifier within the scheme version;
- an activity category;
- the stage or transition context in which it occurs;
- optional method or protocol references;
- optional planned scale/resource assumptions;
- optional expected evidence types and linked execution-resource types.

Do not impose one universal list of stage labels. Stage IDs are local to the immutable scheme version; labels may reflect crop- and organization-specific terminology. An optional external vocabulary mapping is preferable to pretending that stages in different reproductive systems are equivalent.

## 4. Scheme topology: explicit transitions, not a generic workflow engine

A flat ordered array of stages can support a simple display, but it cannot be the complete scientific model where breeding processes branch, repeat, or run multiple generations at once.

The candidate model should contain:

- \`stages[]\` — stage definitions;
- \`transitions[]\` — permitted directed relationships between stage definitions;
- task definitions within stages and, where needed, transition/gate contexts.

\`displayOrder\` is a human-interface hint only. It does not define process semantics. A transition relation can express a linear path where appropriate, alternative routes after a selection/evaluation gate, and return to an earlier stage for recurrent selection.

### 4.1 Deliberate exclusions

Do not turn the scheme into an execution orchestrator. The first contract should not include:

- generic workflow-engine state machines;
- runtime scheduling or task dispatch;
- event subscriptions, retries, or job execution;
- executable expressions or arbitrary scripts in gate conditions;
- generic AND/OR gateways, join semantics, or distributed workflow coordination;
- live cohort membership or the current status of every material.

A scheme describes permitted strategy. Execution systems record what actually happened.

### 4.2 Cycles, generations, and concurrent cohorts

A recurrent path can be represented by a transition that returns to a prior stage or crossing-task context. That records the intended repeatable structure; it does not create a cycle instance.

Actual cycle instances, generation numbers, cohort identities, and selection-stream membership belong to execution records. Multiple cohorts can traverse the same scheme version at the same time. This concurrency does not require a workflow-engine “parallel gateway” in the scheme definition.

Where a program truly runs distinct concurrent strategy paths, the scheme may describe multiple permitted paths. Execution records identify which path and exact scheme version applied to each cohort or material group.

The current GenX \`CropCycle\` proposal must not be assumed to represent a breeding cycle: an agronomic crop cycle and a breeding cycle can have different biological and operational boundaries.

## 5. Crossing, generation advancement, evaluation, and selection

Published work supports at least four common activity categories: crossing, generation advancement, evaluation, and selection. Covarrubias-Pazaran et al. (2022) also emphasize detail in crossing, evaluation, and selection decisions, including parent counts, mating allocation, progeny numbers, locations, replication, checks, experimental design, selection intensity, selection method, and selection unit.

The candidate model should allow multiple task definitions in one stage and repeated task categories across stages. Do not assume one task per stage.

| Activity | Design-time scheme definition may describe | Actual execution/evidence should remain in |
|---|---|---|
| Crossing | Parent-selection strategy, mating/allocation approach, intended cross type, planned scale | BrAPI CrossingProject, PlannedCross, Cross, Germplasm and applicable execution records |
| Generation advancement | Intended advancement method, process, and expected scale | Actual germplasm/population/progeny and advancement records |
| Multiplication | Intended multiplication step and material-handling strategy | Actual germplasm/seed-lot/operation records under their owning contracts |
| Evaluation | Testing strategy, environments, trial/study design expectations, replication/check approach | BrAPI Trial, Study, Location, ObservationUnit, Observation, and MIAPPE-aligned experiment metadata |
| Selection | Selection criteria, method, intensity, selection unit, expected evidence | Actual GenX SelectionDecision (RFC-008) and linked evidence |

A task definition is not proof of performance. It must never be interpreted as a completed cross, a conducted trial, an observed phenotype, or a selection verdict.

### 5.1 Task detail and boundedness

The first design should define a common envelope for task identity, category, stage context, method references, and expected evidence. It should not attempt to encode every crop-specific mating design, selection index, statistical model, trial design, or production plan in one generic task object.

Detailed operational quantities can be modelled as typed properties in the relevant task category only when required by a supported exchange scenario. Avoid a free-form \`parameters\` object that merely moves unresolved domain semantics into opaque JSON.

## 6. Target context

A pipeline may target multiple product concepts or market segments and may be supported by more than one scheme. A single \`targetTrait\` string is not an adequate representation of a product concept.

Candidate target-context content may include:

- product concept/profile reference or immutable descriptive snapshot;
- market-segment reference or description;
- target population of environments (TPE) reference or description;
- target-trait requirements, including trait identity, desired direction, threshold/range where defined, unit, and authority;
- provenance and source version for external target profiles.

Do not create public MarketSegment, ProductConcept, or TPE endpoints in this pilot. Independent identities, lifecycle, authoritative ownership, and cross-program reuse have not been demonstrated by the current evidence.

Where a trait target refers to a BrAPI trait or observation variable, use the official identifier and preserve the BrAPI server/authority context needed to resolve it. A target threshold is not itself an observed value. Any typed numeric quantity must preserve unit and precision semantics; scientific decimal normalization must not be silently delegated to generic JSON canonicalization.

An external target-profile reference may be accompanied by a bounded immutable snapshot of fields needed to interpret the historical pipeline. Snapshot/reference precedence and required contents remain later contract decisions.

## 7. Identity, references, versioning, and lifecycle

### 7.1 Separate logical identity from immutable revision identity

The candidate model needs two levels of identity:

| Logical identity | Immutable revision identity |
|---|---|
| Continuing pipeline/workstream | Exact published pipeline revision |
| Continuing scheme/process blueprint | Exact published scheme version |

The current \`breedingPipelineDbId\` field identifies an immutable record but does not clearly distinguish the continuing workstream from a specific revision. The next contract should not assume that the current identifier already solves both jobs.

Candidate references should distinguish:
- the logical resource identity;
- the exact immutable version/revision;
- the authority or server that owns the identity.

The exact field names and reference encoding are deliberately unresolved. A BrAPI \`programDbId\` is generally meaningful within its source BrAPI server context; a bare identifier string is not always sufficient across independent servers. Use an authority-qualified reference pattern consistent with project identity rules rather than invent an ad hoc string convention for this module.

### 7.2 Immutability and corrections

- A published pipeline or scheme version is immutable.
- A change in strategy, target meaning, stage structure, or gate criteria creates a new version.
- A correction preserves the original record and identifies the corrected version.
- Historical execution records keep the exact version they used.
- A later pipeline/scheme version does not rewrite historical decisions or advancements.

Define whether editorial metadata changes (for example, a spelling correction) require a new version or a separately governed correction event. Do not solve this by allowing silent mutation.

### 7.3 Keep different lifecycle dimensions separate

Do not overload one \`status\` field to mean:
- publication state of a definition (draft versus published);
- operational adoption (active versus no longer used);
- revision relationship (current versus superseded);
- governance approval;
- regulatory variety approval or release.

The pipeline/scheme contract must define which lifecycle states are visible externally and who can transition them. No GenX status may imply governmental release, registration, or approval of a variety.

## 8. Cross-resource boundary and current RFC impact

Several existing GenX drafts describe concepts related to a pipeline or scheme. This is a boundary review, not a decision to accept, remove, or merge any RFC.

| Concern | Preferred authority/boundary | Pipeline/scheme design implication |
|---|---|---|
| Breeding/research program context | BrAPI v2.1 Program | Pipeline references Program; do not duplicate it |
| Breeding workstream and target context | Candidate GenX BreedingPipeline | Own purpose, targets, and scheme bindings |
| Breeding strategy/process blueprint | Candidate GenX BreedingScheme | Own immutable stage, transition, and task definitions |
| Breeding method | BrAPI BreedingMethod | Reference the existing method; do not define a parallel method catalogue |
| Planned/actual crossing work | BrAPI CrossingProject, PlannedCross, Cross | Prefer existing contracts; prove a specific gap before retaining additional GenX crossing operations |
| Germplasm and lineage | BrAPI Germplasm, Pedigree, Progeny | Reuse existing material/lineage identities |
| Evaluation experiment | BrAPI Trial, Study, Location | Evaluation task references actual studies/trials; no trial duplication |
| Phenotyping evidence | BrAPI ObservationUnit, Observation, ObservationVariable and MIAPPE-aligned metadata | Keep observations and experiment metadata out of pipeline/scheme payloads |
| Actual selection verdict | GenX SelectionDecision (RFC-008), pending its own review | Candidate link from the actual decision to pipeline/scheme version and execution context |
| Actual population movement | GenX PopulationAdvancement (RFC-035), pending its own review | Candidate link to pipeline/scheme version and stage IDs; not the transition definition |
| CrossingSchedule (RFC-037) | Potential overlap with BrAPI PlannedCross and CrossingProject | Dedicated overlap assessment before expanding/promoting this draft |
| ProgenyRecords (RFC-019) | Potential overlap with BrAPI Progeny and Germplasm | Identify the precise missing semantics before claiming a separate resource is required |
| CropCycle (RFC-029) | Crop-production cycle context | Do not equate it with a biological/operational breeding-cycle execution |

### 8.1 RFC-035 PopulationAdvancement

The current draft records \`fromStage\` and \`toStage\` as free strings. If it is intended to record actual movement through a scheme, a future revision should consider:
- exact pipeline logical/revision reference;
- exact scheme-version reference;
- scheme-local source and destination stage identifiers;
- population/family/germplasm references;
- actual advancement date/time and decision/evidence link.

The advancement record remains an execution event. It must not own the permitted transition graph.

### 8.2 RFC-008 SelectionDecision

A selection decision is an actual verdict, not a rule. Its future crosswalk should consider references to the pipeline, scheme version, stage, cycle/cohort context, candidate germplasm/population, study/evidence, and decision criteria. The decision record remains authoritative for the verdict and rationale; the scheme describes the intended decision process.

### 8.3 RFC-037 CrossingSchedule and RFC-019 ProgenyRecords

Do not assume these drafts require independent public APIs merely because a GenX folder or RFC already exists. BrAPI v2.1 already contains PlannedCross, CrossingProject, Cross, and Progeny concepts. A separate GenX resource needs a documented semantic gap, identity ownership, lifecycle, and exchange scenario. This document does not change either RFC.

## 9. Candidate illustrative structure

The JSON below is conceptual, not a valid OpenAPI schema, accepted payload, or implementation instruction. It demonstrates the proposed separation.

### 9.1 Pipeline with two scheme versions

\`\`\`json
{
  "breedingPipelineId": "institute-a:breeding-pipeline:rice-lowland-product-development",
  "breedingPipelineVersionId": "institute-a:breeding-pipeline-version:rice-lowland-product-development:2",
  "name": "Lowland rice product development",
  "programReference": {
    "apiGeneration": "brapi-v2.1",
    "resourceType": "Program",
    "server": "https://brapi.example.org/brapi/v2.1",
    "dbId": "rice-breeding-program"
  },
  "purpose": ["productDevelopment", "populationImprovement"],
  "targetContexts": [
    {
      "targetContextId": "south-asia-irrigated-lowland",
      "marketSegment": {
        "authority": "https://example.org/market-segments",
        "id": "south-asia-irrigated-lowland"
      },
      "productConcept": {
        "authority": "https://example.org/product-concepts",
        "id": "rice-lowland-short-duration-v1",
        "version": "1"
      },
      "targetPopulationOfEnvironments": {
        "authority": "https://example.org/tpe",
        "id": "south-asia-irrigated-lowland"
      },
      "traitTargets": [
        {
          "traitReference": {
            "apiGeneration": "brapi-v2.1",
            "resourceType": "ObservationVariable",
            "server": "https://brapi.example.org/brapi/v2.1",
            "dbId": "grain-yield"
          },
          "desiredDirection": "increase",
          "targetRange": {
            "minimum": "6.0",
            "maximum": "8.0",
            "unit": "t/ha"
          }
        }
      ]
    }
  ],
  "schemeBindings": [
    {
      "schemeVersionId": "institute-a:breeding-scheme-version:rice-recurrent-selection:4",
      "role": "principal"
    },
    {
      "schemeVersionId": "institute-a:breeding-scheme-version:rice-rapid-generation-advance:2",
      "role": "experimental"
    }
  ]
}
\`\`\`

The authorities, identifiers, server URLs, and trait values are illustrative. This does not settle the exact reference structure or whether target data should be embedded, referenced, or both.

### 9.2 Scheme version with stage transitions and task definitions

\`\`\`json
{
  "breedingSchemeId": "institute-a:breeding-scheme:rice-recurrent-selection",
  "breedingSchemeVersionId": "institute-a:breeding-scheme-version:rice-recurrent-selection:4",
  "version": "4",
  "status": "published",
  "stages": [
    {
      "stageId": "crossing",
      "label": "Crossing block",
      "displayOrder": 10,
      "tasks": [
        {
          "taskId": "make-crosses",
          "activityType": "crossing",
          "methodReference": {
            "apiGeneration": "brapi-v2.1",
            "resourceType": "BreedingMethod",
            "server": "https://brapi.example.org/brapi/v2.1",
            "dbId": "two-way-cross"
          },
          "expectedEvidence": ["PlannedCross", "Cross", "Germplasm"]
        }
      ]
    },
    {
      "stageId": "early-evaluation",
      "label": "Early generation evaluation",
      "displayOrder": 20,
      "tasks": [
        {
          "taskId": "evaluate-progeny",
          "activityType": "evaluation",
          "expectedEvidence": ["Trial", "Study", "Observation"]
        },
        {
          "taskId": "select-lines",
          "activityType": "selection",
          "expectedEvidence": ["SelectionDecision"]
        }
      ]
    }
  ],
  "transitions": [
    {
      "transitionId": "crossing-to-evaluation",
      "fromStageId": "crossing",
      "toStageId": "early-evaluation",
      "transitionType": "advance"
    },
    {
      "transitionId": "recurrent-cycle",
      "fromStageId": "early-evaluation",
      "toStageId": "crossing",
      "transitionType": "recurrent"
    }
  ]
}
\`\`\`

The example shows that a scheme may define a recurrent return path. Actual cohort A may be in evaluation while cohort B is already in the next crossing cycle. This concurrency belongs in material, cycle, cohort, and event records rather than a mutable \`currentStage\` on the pipeline.

## 10. Alternatives and trade-offs

| Option | Description | Assessment |
|---|---|---|
| A — Scalar stage on pipeline | Retain \`pipelineStage\` as current pipeline state | Reject as the domain model; cannot represent multiple stages/cohorts/schemes |
| B — Pipeline with ordered stages array | Put stage definitions directly in Pipeline | Better than a scalar, but mixes target/workstream identity with changing process strategy and cannot cleanly support multiple independently versioned schemes |
| C — Pipeline plus nested versioned scheme | Keep scheme versions nested within pipeline revisions | Viable minimum if independent scheme reuse and discovery are not required |
| D — Pipeline plus first-class scheme identity/version | Distinct logical identities; pipeline revisions reference exact scheme versions | **Recommended for further contract design.** Best fit for multiple schemes per pipeline and independent evolution; endpoint need remains unproven |
| E — Generic workflow engine / arbitrary graph | General-purpose executable task graph | Defer; excessive abstraction and implementation burden for demonstrated breeding use cases |

The preferred conceptual model is Option D, while endpoint exposure remains open. A first-class identity does not automatically require a public collection endpoint. Contract design must test whether independent discovery, version retrieval, reuse, and lifecycle management are real cross-organization needs or can be served with nested versioned records.

## 11. Validation scenarios and falsifiers

| Scenario | Required model behavior | Falsifier |
|---|---|---|
| Recurrent population improvement | A cycle can repeat; multiple cohorts/generations may progress concurrently; pipeline has no single current stage | Model forces one active stage or one cohort on the pipeline |
| Product development across target environments | Multiple trait targets, market segments, or environment targets can be associated with the workstream | Model permits only one scalar target trait or one fixed target context |
| Principal plus experimental scheme | A pipeline references multiple exact scheme versions; adoption does not rewrite history | One mutable scheme field makes past execution ambiguous |
| Crop-specific stage terminology | Local stage labels and mappings can differ without implying equivalence | Model forces one universal ordered stage vocabulary |
| Separate population-improvement and product-development paths | Distinct pathways can be described while keeping execution cohorts and outcomes external | Model merges strategy and actual progress into one flattened list |
| Planned versus actual crossing | Scheme describes strategy; BrAPI records planned/actual crossing | A scheme task is interpreted as proof a cross occurred |
| Strategy change during a breeding cycle | An execution record can retain the exact scheme version that governed it | Historical event resolves only to the scheme's latest revision |

## 12. Decisions intentionally left open

1. Whether BreedingScheme requires a public endpoint or remains nested within Pipeline initially.
2. Whether a scheme version may be referenced by more than one pipeline.
3. Exact authority-qualified BrAPI reference encoding and whether server URL, external reference, or another authority identifier is canonical.
4. Exact logical-identity and revision-identity field names.
5. Whether pipeline and scheme publication/lifecycle states use one shared vocabulary or separate state machines.
6. Typed structure for product concepts, market segments, target populations of environments, and quantitative trait targets.
7. Which CES task categories are in the initial contract and which remain extension points.
8. How decision criteria are represented: typed values, vocabulary terms, external rule references, or a combination.
9. Whether cycle/cohort execution needs its own GenX resource or can be represented by existing population, germplasm, and advancement records.
10. Whether RFC-037 CrossingSchedule and RFC-019 ProgenyRecords demonstrate semantic gaps beyond BrAPI v2.1.

These questions do not block further domain research. They do block schema promotion or a claim that the Application Programming Interface (API) contract is complete.

## 13. Recommended next slices

### Slice 3A — Contract model refinement (this document)

**Completed as advisory design.** Define the resource boundary, stage-transition model, task definitions, target context, immutable versioning, and execution crosswalk. No schema or endpoint changes.

### Slice 3B — Cross-RFC overlap review

**Completed as assessment** in [the Cross-RFC Overlap Review](./BRAPI-GENX-BREEDING-CROSS-RFC-OVERLAP-REVIEW.md). The review verified official BrAPI v2.1 coverage and GenX draft boundaries for RFC-008, RFC-019, RFC-029, RFC-035, RFC-037, and RFC-098. It identifies SelectionDecision and PopulationAdvancement as the strongest GenX-only candidates, flags ProgenyRecord and CrossingSchedule for narrowing, and finds the current ResearchProgram premise contradicted by BrAPI Program. No RFC or API contract changed.

### Slice 3C — Candidate logical model and fixtures

**Completed as non-normative design evidence** in [the Candidate Logical Model](./BRAPI-GENX-BREEDING-PIPELINE-LOGICAL-MODEL.md) and [the Candidate Fixture Corpus](./BRAPI-GENX-BREEDING-PIPELINE-CANDIDATE-FIXTURES.json). The model defines candidate cardinalities, identity/versioning rules, execution-reference constraints, and 20 invariants. The nine machine-readable scenarios include three positive and six negative cases. A lightweight structural/semantic check confirmed unique scenario IDs and the declared positive/negative conditions. These are not production conformance fixtures and are not wired into CI.

### Slice 4 — Maintainer contract decision package

**Prepared** in [the Maintainer Decision Package](./BRAPI-GENX-BREEDING-PIPELINE-MAINTAINER-DECISION-PACKAGE.md). It consolidates the preferred Pipeline/Scheme boundary, nested-versus-first-class scheme alternatives, logical/revision identity migration, typed BrAPI references, stage/transition rules, target-context boundaries, and proposed RFC dispositions. It identifies 13 maintainer decisions. No endpoint YAML, schema, or RFC maturity state was changed.

The next action is maintainer direction on the public resource boundary and dependent identity/reference choices.

## 14. References

### Breeding-domain literature

- Covarrubias-Pazaran, G., Gebeyehu, Z., Gemenet, D., Werner, C., Labroo, M., Sirak, S., Coaldrake, P., Rabbi, I., Kayondo, S. I., Parkes, E., Kanju, E., Mbanjo, E. G. N., Agbona, A., Kulakow, P., Quinn, M., and Debaene, J. (2022). *Breeding Schemes: What Are They, How to Formalize Them, and How to Improve Them?* Frontiers in Plant Science, 12:791859. https://doi.org/10.3389/fpls.2021.791859
- Bhosale, S., Prakash, P. T., et al. (2025). *Onerice breeding framework: An end-to-end system to develop better varieties faster.* Crop Science, 65(3), e70087. https://doi.org/10.1002/csc2.70087

### Standards and interoperability

- Official BrAPI specification — v2.1 is identified as the latest stable release; preview material remains subject to change until formal release: https://brapi.org/specification
- BrAPI v2.1 source contracts: https://github.com/plantbreeding/BrAPI/tree/brapi-V2.1
- MIAPPE (Minimum Information About a Plant Phenotyping Experiment) overview and data model: https://www.miappe.org/
- MIAPPE releases, including v1.2 (October 2024): https://www.miappe.org/releases/

### Existing GenX contracts under review

- RFC-008 — Selection Decisions: \`Specification/BrAPI-GenX/RFC-008-Selection-Decisions.md\`
- RFC-019 — Progeny Records: \`Specification/BrAPI-GenX/RFC-019-Progeny-Records.md\`
- RFC-029 — Crop Cycle: \`Specification/BrAPI-GenX/RFC-029-Crop-Cycle.md\`
- RFC-035 — Population Advancement: \`Specification/BrAPI-GenX/RFC-035-Population-Advancement.md\`
- RFC-037 — Crossing Schedule: \`Specification/BrAPI-GenX/RFC-037-Crossing-Schedule.md\`
- RFC-098 — Research Program: \`Specification/BrAPI-GenX/RFC-098-Research-Program.md\`
