# BrAPI-GenX — Breeding Pipeline and Scheme Maintainer Decision Package

**Status:** Decision package for maintainer consideration; advisory, non-normative, not ratified.  
**Prepared:** 18 November 2026  
**Workstream:** BGX-P1-05 — Public contract boundary and RFC disposition  
**Repository baseline:** main at 52fd8cb1f4e7e88020f15cdf00577c0b0930dc40  
**Companion evidence:**
- [Breeding Pipeline Domain Preflight](./BRAPI-GENX-BREEDING-PIPELINE-DOMAIN-PREFLIGHT.md)
- [Breeding Pipeline and Scheme Design Proposal](./BRAPI-GENX-BREEDING-PIPELINE-DESIGN-PROPOSAL.md)
- [Pipeline and Scheme Candidate Contract Design](./BRAPI-GENX-BREEDING-PIPELINE-SCHEME-CONTRACT-DESIGN.md)
- [Breeding and Related RFC Overlap Review](./BRAPI-GENX-BREEDING-CROSS-RFC-OVERLAP-REVIEW.md)
- [Candidate Logical Model](./BRAPI-GENX-BREEDING-PIPELINE-LOGICAL-MODEL.md)
- [Candidate Fixture Corpus](./BRAPI-GENX-BREEDING-PIPELINE-CANDIDATE-FIXTURES.json)

## 1. Executive recommendation

The research and design slices are complete. The recommended direction is:

1. Keep **BreedingPipeline** as the durable, goal- and target-oriented workstream associated with an existing BrAPI Program.
2. Give **BreedingScheme** a distinct logical identity and immutable version identity. A scheme defines the process strategy; it is not a record of executed crosses, trials, or advancement events.
3. Model stages, transitions, and task definitions within the immutable scheme version. Use explicit directed transitions that can repeat or branch. Do not build a generic workflow engine.
4. Separate pipeline logical identity from pipeline revision identity. Preserve historical references to the exact revision and scheme version used by an execution event.
5. Keep existing BrAPI resources authoritative for Program, Germplasm, Pedigree, PlannedCross, Cross, CrossingProject, Trial, Study, and Observation.
6. Retain SelectionDecision and PopulationAdvancement as likely GenX execution records, subject to refinement. Do not promote ProgenyRecord, CrossingSchedule, or ResearchProgram without narrowing their semantics and demonstrating the remaining gap.
7. Keep all current RFCs at STRUCTURAL_DRAFT and all current BreedingPipeline endpoints non-normative until the maintainer chooses the public contract boundary.

The package is intended to turn the existing research into a small set of explicit decisions. It does not make those decisions on the maintainer's behalf.

## 2. Evidence completed

| Slice | Outcome | Evidence |
|---|---|---|
| Domain preflight | Complete | Pipeline/scheme distinction, published breeding literature, BrAPI/MIAPPE boundaries, current repository contradictions |
| Repository reconciliation | Complete for descriptive metadata and classification | One BreedingPipeline D2 classification entry; 462 GenX and 201 BrAPI v2.1 operations in the registry; no remaining operation-name, description, allowed-use, or decision-reference drift |
| Breeding contract design | Complete as advisory model | Pipeline, scheme, stage-transition, task, target-context, and immutable-version boundaries |
| Cross-RFC review | Complete | Six related RFCs checked against official BrAPI v2.1 source contracts |
| Logical model and fixtures | Complete as non-normative evidence | Cardinalities, 20 invariants, and nine candidate machine-readable scenarios; structural/semantic checks passed |

### 2.1 Known registry semantic-neighbour caveat

The source/registry audit still reports 147 semantic-neighbour mismatches across 49 modules and 153 registry-only operation-neighbour references across 153 operations. These are deliberately review-only. Automatically rewriting them could remove or invent scientific relationships. This is not a BreedingPipeline blocker and is not part of the contract decisions below.

## 3. Decision 1 — What is a pipeline and what is a scheme?

### Recommended direction

- Pipeline = durable workstream with purpose and target context.
- Scheme = versioned blueprint of crossing, generation advancement, multiplication, evaluation, and selection activities/decisions.
- Stage = local stage definition within one scheme version.
- Transition = permitted relationship between two stages, not an actual advancement.
- Task = design-time activity definition, not evidence of execution.
- Cohort, generation, and breeding-cycle identities belong to execution, not the pipeline's single mutable state.

A pipeline may use multiple scheme versions, for example a principal strategy and an experimental strategy. Multiple cohorts may be at different stages in the same scheme version.

**Why this is preferred:** published breeding frameworks distinguish target/product-oriented pipelines from the process strategy used by a scheme. The 2022 breeding-scheme paper also describes repeated stage-gate cycles, parallel generations, and overlapping cohorts. The OneRice 2025 framework describes pipeline/product targets and the scheme as an evolving process blueprint.

### Rejected alternatives

| Alternative | Reason not recommended |
|---|---|
| Scalar pipelineStage | Cannot represent simultaneous cohorts at different stages or multiple strategies |
| Pipeline with only an ordered stage list | Does not adequately express loops, branches, or recurrent paths; conflates target/workstream identity and process strategy |
| Generic executable workflow graph | Adds scheduling, orchestration, and engine semantics not justified by the breeding use cases |

## 4. Decision 2 — How should schemes be represented?

| Option | Model | Benefits | Costs / risks |
|---|---|---|---|
| A — Fully nested scheme | Scheme content exists only inside each pipeline revision | Smallest API surface; simple deployment; no separate scheme lookup | Hard to share/reuse; scheme history tied to pipeline history; duplication across pipelines |
| B — First-class scheme with separate API | Independent Scheme and SchemeVersion resources with their own endpoints and lifecycle | Clear independent identity, discovery, reuse, version retrieval, and governance | More endpoints, authorization, tenancy, lifecycle, registry, fixtures, and compatibility work |
| C — First-class logical identity, embedded version initially | Scheme has a stable logical ID and immutable version ID, while the version definition is embedded in a PipelineRevision for initial exchange | Preserves correct identity/version semantics without prematurely creating a separate endpoint surface | Independent discovery/reuse is limited until a later API surface is justified |

**Recommendation: Option C for the initial contract.**

This preserves a real Scheme identity and immutable SchemeVersion ID while avoiding premature public CRUD operations. The immutable scheme definition travels with the pipeline revision that adopts it. If independent retrieval or cross-pipeline reuse later becomes necessary, a dedicated scheme endpoint can expose the same logical model without changing the meaning of scheme identity.

If the maintainer wants immediate independent scheme discovery/reuse as a core requirement, Option B is the alternative. Option A is the simplest fallback but should not be selected if multiple schemes per pipeline and independent scheme evolution are required.

## 5. Decision 3 — Pipeline and scheme version identity

### Recommended identity layers

| Logical identity | Immutable revision identity |
|---|---|
| BreedingPipeline ID — continuing workstream | BreedingPipelineVersion ID — exact published configuration |
| BreedingScheme ID — continuing process blueprint | BreedingSchemeVersion ID — exact published process definition |

A pipeline revision contains the exact scheme-version IDs it adopts. An execution event records the exact pipeline revision and scheme version that governed it, where applicable.

### Existing field migration

The current BreedingPipeline draft uses one namespaced breedingPipelineDbId with immutable create/replay semantics: the same ID and identical body replays, while the same ID with a different body is rejected. That design cannot also represent multiple revisions under one continuing pipeline identity.

Recommended migration before any public release:
- retain breedingPipelineDbId as the stable pipeline identity;
- add a required breedingPipelineVersionDbId for the immutable revision record;
- key idempotent revision registration by breedingPipelineVersionDbId;
- permit a new revision under the same breedingPipelineDbId;
- require GET/list semantics to distinguish “current pipeline view” from exact historical revision retrieval.

Apply the same distinction to BreedingScheme and BreedingSchemeVersion.

This changes the current draft contract. Since the existing routes/schemas are non-normative proposals rather than a published BrAPI release, this is the appropriate point to make the identity semantics explicit. The exact route form and naming convention remain an implementation/specification decision after acceptance.

### Lifecycle dimensions

Do not overload one status property for:
- draft versus published;
- adopted/active versus no longer used;
- current versus superseded;
- governance approval;
- governmental variety release or registration.

Published versions are immutable. Substantive changes create new version identities. Historical events keep the exact version IDs they used.

## 6. Decision 4 — Stage and transition model

### Recommended contract shape

A scheme version contains:
- one or more StageDefinitions;
- zero or more directed Transitions;
- zero or more TaskDefinitions assigned to a stage.

A transition identifies source and target stages within the same scheme version. It may represent a forward advance, branch, or recurrent return. Display order is presentation metadata only.

Stage IDs are local to the scheme version. Labels remain crop- and organization-specific. Optional mappings to external vocabularies may be provided; GenX should not impose a universal plant-breeding stage vocabulary.

The first version should not include:
- executable condition scripts;
- generic workflow gateways;
- event routing or scheduling;
- distributed task orchestration;
- live cohort state.

### Candidate task categories

Start with crossing, generation advancement, multiplication, evaluation, and selection. Keep task data bounded: identity, stage context, activity category, method/protocol reference, optional planned scale, and expected evidence. Detailed task-specific quantity/criteria structures should be introduced only where a validated use case requires them.

## 7. Decision 5 — Target context

A single targetTrait string is insufficient. A pipeline revision should support zero or more purpose-appropriate target contexts; product-development pipelines will typically have one or more contexts containing:
- product concept/profile reference or snapshot;
- market segment reference or description;
- target population of environments (TPE) reference or description;
- a list of trait requirements, with resolvable trait/variable references, direction, and typed threshold/range where defined;
- provenance and source-version information.

Do not create independent MarketSegment, ProductConcept, or TPE public resources in this pilot. Their separate identities, authoritative ownership, and lifecycle have not been demonstrated.

A target trait is a breeding objective, not an observation. Quantitative targets need unit and precision semantics. BrAPI references must preserve the owning server/authority context; a bare dbId is not globally resolvable across independent servers.

## 8. Decision 6 — BrAPI and GenX ownership boundaries

| Concern | Recommended authority | Consequence |
|---|---|---|
| Program/breeding-program context | BrAPI Program | Do not create a GenX ResearchProgram duplicate |
| Pipeline target/workstream | GenX BreedingPipeline | Workstream, purpose, target contexts, scheme bindings |
| Strategy blueprint | GenX BreedingSchemeVersion | Stages, transitions, and task definitions |
| Breeding method | BrAPI BreedingMethod | Reference the existing method |
| Planned and actual crossing | BrAPI CrossingProject, PlannedCross, Cross | Keep mating intent/parents and actual crossing authoritative in BrAPI |
| Germplasm and pedigree | BrAPI Germplasm and Pedigree | Keep parent/progeny graph authoritative in BrAPI |
| Evaluation experiment | BrAPI Trial and Study | Strategy references execution evidence; do not duplicate trials |
| Phenotyping evidence | BrAPI ObservationUnit, Observation, ObservationVariable; MIAPPE alignment | Keep measurements and experiment metadata in their existing standards |
| Selection verdict | GenX SelectionDecision, if refined | Actual verdict/rationale/evidence |
| Actual population progression | GenX PopulationAdvancement, if refined | Actual event, linked to exact scheme version/stages where applicable |

### Important BrAPI v2.1 evidence

- Program already represents a high-level organization/group responsible for trials and studies and explicitly includes breeding programs and funded projects.
- PlannedCross represents the intention to mate specific organisms and includes parents, cross type, project, and planned-cross status.
- CrossingProject groups planned and actual crossing work.
- Cross records the mating event that actually occurred.
- PedigreeNode represents Germplasm parents, siblings, progeny, familyCode, crossingYear, breeding method, and crossing-project context.
- Trial and Study represent multi-location trial and individual experiment contexts; Study includes location, study design, observation-variable wishlist, and experiment metadata.

These boundaries are documented in the Cross-RFC Overlap Review with the official BrAPI v2.1 source pinned to commit 0a562640f44bce7217b982ec22980b8a47561dda.

## 9. Decision 7 — Existing RFC disposition

The following are recommended dispositions for the maintainer to accept, alter, or reject. No disposition has been applied.

| RFC | Current issue | Recommendation |
|---|---|---|
| RFC-014 and RFC-154 | Both define the same three pipeline operations; stage-array and scalar-stage framing conflict; module README and current schema link to RFC-154 | Keep RFC-154 as the current working surface because current module references point there; consolidate valid stage-gate requirements from RFC-014 into the accepted contract; mark RFC-014 historical/superseded only after maintainer approval |
| RFC-008 SelectionDecision | Actual verdict is not a first-class BrAPI resource | Retain and refine; link to pipeline/scheme version and execution evidence where applicable |
| RFC-019 ProgenyRecords | BrAPI Pedigree already represents parents/progeny/familyCode; generation or immutable formation event may be a gap | Do not promote as written; narrow to a distinct immutable event or typed generation/cohort association, otherwise defer |
| RFC-029 CropCycle | Crop planting-to-harvest interval, not a breeding cycle | Retain separately in D6; do not reuse for recurrent breeding cycles |
| RFC-035 PopulationAdvancement | Actual progression event; current stage strings are unqualified | Retain and refine; source/destination stage IDs must resolve through exact scheme version when applicable |
| RFC-037 CrossingSchedule | PlannedCross already represents parent mating intent, cross type, project, and status; dedicated scheduled date/time absent | Narrow to genuine schedule/booking semantics that reference BrAPI PlannedCross/CrossingProject, otherwise defer |
| RFC-098 ResearchProgram | Premise that BrAPI has no research-program resource is contradicted by BrAPI Program; current schema has no distinct higher-level concept | Defer/withdraw the standalone resource unless a distinct portfolio/network/governance concept is defined |

Do not remove or renumber historical RFCs. Retain their evidence and update status only when the maintainer directs the disposition.

## 10. Decision 8 — Initial endpoint surface

The current BreedingPipeline proposal contains three operations: list, register, and get. The same three operations are duplicated across RFC-014 and RFC-154.

These operations should remain provisional until the identity and scheme-binding decisions are accepted. In particular:
- registration must be version-aware;
- GET by logical pipeline identity must have defined behavior when several revisions exist;
- historical version retrieval must be possible if published events cite exact versions;
- scheme definitions embedded in PipelineRevision must be returned consistently;
- no separate Scheme CRUD endpoints should be added in the initial Option C design.

Do not implement update/delete semantics that mutate published versions. Corrections create new versions. Collection filters must distinguish current versus all revisions if both are exposed.

## 11. Migration and implementation consequences

After acceptance, the bounded implementation sequence should be:

1. Resolve the two existing RFCs into one canonical pipeline/scheme design; preserve the historical predecessor with a clear cross-reference.
2. Update candidate domain definitions and identity/version fields.
3. Define the typed BrAPI reference object and exact authority-resolution rule.
4. Replace scalar pipelineStage with scheme version, stage definitions, transitions, and task definitions.
5. Define pipeline target-context representation and lifecycle semantics.
6. Refine SelectionDecision and PopulationAdvancement references without duplicating evidence or material identities.
7. Make a separate accept/defer decision for ProgenyRecords, CrossingSchedule, and ResearchProgram.
8. Update OpenAPI YAML, catalogue, registry, crosswalk, conformance probes, positive/negative fixtures, and generated artifacts.
9. Run source/registry audits, schema generation, static conformance, live conformance, and compatibility checks.
10. Promote RFC maturity only after all semantic, schema, fixture, and interoperability gates pass.

### Expected impact on current BreedingPipeline fields

| Current field | Candidate direction |
|---|---|
| breedingPipelineDbId | Retain as stable logical pipeline identity; add version identity |
| pipelineName | Retain as descriptive name |
| pipelineType | Define purpose/type vocabulary or purpose set; distinguish pipeline purpose from scheme type |
| breedingProgram | Replace/align with typed BrAPI Program reference; avoid opaque unqualified string |
| pipelineStage | Remove from pipeline-level state; stage belongs to scheme definition or cohort/event context |
| targetTrait | Replace with target-context collection and typed target trait requirements |
| status | Separate publication state, adoption/lifecycle, and supersession |
| supersedes | Define at version/revision level; a new revision must preserve logical resource identity |
| provenance | Retain and define coverage for pipeline and scheme revisions |

## 12. Risks if the current draft is promoted unchanged

| Risk | Consequence | Mitigation |
|---|---|---|
| Scalar pipelineStage | Wrong for parallel cohorts or multiple schemes | Versioned scheme stages and transitions |
| One ID for identity and revision | Cannot safely append new immutable versions | Separate logical and version IDs |
| Bare BrAPI IDs | Cross-server ambiguity or accidental wrong-resource lookup | Authority-qualified typed references |
| Duplicate Progeny/Crossing/Program records | Conflicting sources of truth and extra synchronization | BrAPI-first resource ownership and evidence-based GenX gap |
| Stage names treated as global codes | Incorrect cross-crop semantics | Scheme-local IDs plus vocabulary mappings |
| Definition confused with execution | Planned activity mistaken for actual event | Separate task definitions from execution records |
| RFC-014/RFC-154 divergence | Conflicting schemas and duplicate operations | One maintainer-approved canonical design |

## 13. Decisions requested from the maintainer

Only the decisions below are required before normative contract work begins. The evidence and recommendations are already recorded in the companion documents.

| ID | Decision required | Recommended choice |
|---|---|---|
| D-BP-01 | Conceptual relationship of Pipeline and Scheme | Distinct concepts: Pipeline = workstream; Scheme = process blueprint |
| D-BP-02 | Initial scheme representation | Option C: first-class logical identity/version, embedded version definition, no separate Scheme endpoints initially |
| D-BP-03 | Pipeline/scheme identity | Stable logical ID plus immutable version ID for each |
| D-BP-04 | Stage semantics | Scheme-local stage IDs, explicit directed transitions, no generic workflow engine |
| D-BP-05 | Target contexts | Typed collection, purpose-specific, no independent target-context endpoints initially |
| D-BP-06 | BrAPI reference format | Authority-qualified typed reference; exact URI encoding to be finalized in contract |
| D-BP-07 | RFC-014/RFC-154 | Keep RFC-154 current working surface; consolidate stage-gate requirements from RFC-014; preserve predecessor historically |
| D-BP-08 | RFC-019 | Narrow to a proven immutable family/progeny event or defer; do not duplicate Pedigree |
| D-BP-09 | RFC-029 | Retain as crop-production cycle; do not treat as breeding cycle |
| D-BP-10 | RFC-035 | Retain/refine as actual population-advancement event |
| D-BP-11 | RFC-037 | Narrow to schedule-specific semantics linked to PlannedCross, or defer |
| D-BP-12 | RFC-098 | Defer/withdraw standalone ResearchProgram unless a separate higher-level concept is defined |
| D-BP-13 | Endpoint surface | Keep operations provisional until identity/version and lookup semantics are agreed |

A decision on D-BP-02 may be separated from D-BP-03 and D-BP-06 if the maintainer prefers, but the implementation should not begin before the dependent identity/reference rules are coherent.

## 14. Explicit non-actions

Until the maintainer directs otherwise:
- do not change the current BreedingPipeline OpenAPI files;
- do not add BreedingScheme endpoint YAML;
- do not change RFC maturity or accepted-decision registers;
- do not delete, renumber, or merge RFC-014, RFC-154, RFC-019, RFC-037, or RFC-098;
- do not add candidate fixture files to production conformance;
- do not regenerate official BrAPI v2.1 artifacts or alter official BrAPI files.

## 15. Evidence references

### Breeding-domain literature

- Covarrubias-Pazaran, G. et al. (2022). *Breeding Schemes: What Are They, How to Formalize Them, and How to Improve Them?* Frontiers in Plant Science, 12:791859. https://doi.org/10.3389/fpls.2021.791859
- Bhosale, S. et al. (2025). *Onerice breeding framework: An end-to-end system to develop better varieties faster.* Crop Science, 65(3), e70087. https://doi.org/10.1002/csc2.70087

### Standards

- Official BrAPI v2.1 specification: https://brapi.org/specification
- Pinned official BrAPI v2.1 source: https://github.com/plantbreeding/BrAPI/tree/0a562640f44bce7217b982ec22980b8a47561dda
- MIAPPE (Minimum Information About a Plant Phenotyping Experiment): https://www.miappe.org/

### Governance

- Project decision authority: docs/governance/BRAPI-GENX-PROJECT-DECISION-AUTHORITY.md
