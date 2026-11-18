# BrAPI-GenX — Breeding Pipeline Candidate Logical Model

**Status:** Candidate logical model; advisory, non-normative, not accepted or ratified.  
**Prepared:** 18 November 2026  
**Workstream:** BGX-P1-04 — Pipeline/scheme relationships and validation cases  
**Related design:** [Pipeline and Scheme Candidate Contract Design](./BRAPI-GENX-BREEDING-PIPELINE-SCHEME-CONTRACT-DESIGN.md)  
**Overlap review:** [Breeding and Related RFC Overlap Review](./BRAPI-GENX-BREEDING-CROSS-RFC-OVERLAP-REVIEW.md)  
**Candidate fixtures:** [Breeding Pipeline Candidate Fixtures](./BRAPI-GENX-BREEDING-PIPELINE-CANDIDATE-FIXTURES.json)  
**Terminology:** BrAPI (Breeding Application Programming Interface); RFC (Request for Comments); JSON (JavaScript Object Notation); API (Application Programming Interface); ID (identifier); URL (Uniform Resource Locator); URI (Uniform Resource Identifier); YAML (YAML Ain't Markup Language).
**Repository baseline:** main at fc42722dbdbf4a613314ca3850f8db3924553e09.

## 1. Purpose and boundary

This document converts the preceding domain design into a candidate relationship model with cardinalities, invariants, and validation scenarios.

It is not an OpenAPI definition, JSON Schema, public API proposal, or accepted domain contract. Field names in the examples are illustrative. The candidate fixture file is machine-readable design evidence only; it is deliberately not wired into production conformance.

No endpoint, operation identifier, existing RFC, official BrAPI contract, or maturity state is changed by this model.

## 2. Conceptual model

~~~text
BrAPI Program (authority-qualified reference)
   1
   |
   | owns / contextualizes
   |
   N
BreedingPipeline (stable logical identity)
   |
   | 1 : N
   v
BreedingPipelineRevision (immutable published snapshot)
   |                         \
   |                          \ 0 : N exact scheme-version bindings
   |                           \
   |                            v
   |                     BreedingSchemeVersion
   |                            ^
   |                            | N : 1
   |                     BreedingScheme (stable logical identity)
   |                            |
   |                            | 1 : N immutable versions
   |                            |
   |                            +---- 1 : N StageDefinitions
   |                            |          |
   |                            |          +---- 0 : N TaskDefinitions
   |                            |
   |                            +---- 0 : N Transitions
   |
   +---- 0 : N TargetContexts

Execution records (actual events; version references are optional only
when the activity did not operate under a registered GenX scheme):
   |
   +---- PopulationAdvancement (actual material progression)
   +---- SelectionDecision (actual selection verdict)
   +---- BrAPI PlannedCross / Cross / CrossingProject
   +---- BrAPI Trial / Study / Observation
   +---- BrAPI Germplasm / Pedigree / Progeny relationships
~~~

The diagram separates persistent identity, immutable definition snapshots, and actual events. It does not imply every concept must receive its own endpoint.

## 3. Candidate entities and cardinalities

| Entity / reference | Candidate cardinality | Ownership and meaning |
|---|---|---|
| BrAPI Program reference | Exactly 1 owning Program per pipeline; a Program may own 0..N pipelines | Existing BrAPI identity; must retain authority/server context |
| BreedingPipeline | 1 stable identity | Persistent breeding workstream |
| BreedingPipelineRevision | 1..N per pipeline over its lifetime | Immutable snapshot of pipeline purpose, target context, and scheme bindings |
| TargetContext | 0..N per pipeline revision | Describes a purpose-specific goal, product concept, target segment/environment, and trait targets; not yet an independent public resource |
| BreedingScheme | 1 stable identity | Persistent process blueprint |
| BreedingSchemeVersion | 1..N per scheme | Immutable process definition; referenced by exact version ID |
| SchemeBinding | 0..N per pipeline revision | Relationship to exact scheme versions; role may identify principal, experimental, or other local use |
| StageDefinition | 1..N per scheme version | Named stage local to that scheme version |
| Transition | 0..N per scheme version | Permitted directed edge between two stages in that same version |
| TaskDefinition | 0..N per stage | Design-time activity specification; not evidence of execution |
| ExecutionEvent | 0..N per pipeline/scheme version | Actual event, if one occurred; retains exact version context when applicable |
| Cohort / selection stream | 0..N execution contexts | Groups actual materials progressing through stages; no standalone endpoint proposed now |
| Generation / breeding cycle | 0..N execution contexts | Biological/operational execution context; not a StageDefinition or CropCycle alias |

### 3.1 Program ownership versus participation

The baseline candidate assumes one owning BrAPI Program per pipeline, because the pipeline is managed within a breeding program in the researched models. Cross-institutional networks or joint programs may participate in the workstream; that is a separate relationship and should not be represented by multiple ambiguous owner fields.

Whether the model needs a distinct network/partner reference is left open. It must not be solved by creating a GenX ResearchProgram duplicate.

### 3.2 Scheme binding cardinality

A pipeline revision may bind zero or more scheme versions:
- zero permits a pipeline to exist before a strategy is published or where the scheme is external;
- one supports a single principal strategy;
- multiple supports principal and experimental strategies or multiple target-specific strategies.

A scheme version may be bound by more than one pipeline only if a concrete reuse requirement supports that relationship. The present evidence establishes multiple schemes per pipeline, not necessarily one scheme shared across independent pipelines.

### 3.3 Target-context cardinality

Target context is not a single scalar trait. It is a set of purpose-specific contexts. Product-development pipelines will normally need one or more product/market/environment contexts; trait-discovery or population-improvement pipelines may require a different target description.

Do not require the exact same target fields for every pipeline purpose. The published contract should make target context typed and resolvable while permitting purpose-specific profiles.

## 4. Identity and reference rules

### 4.1 Two identity layers

| Logical identity | Version identity |
|---|---|
| BreedingPipeline ID identifies the continuing workstream | PipelineRevision ID identifies one immutable configuration |
| BreedingScheme ID identifies the continuing process blueprint | SchemeVersion ID identifies one immutable process definition |

A pipeline revision contains the exact scheme-version IDs it adopts. An execution event that is scheme-specific refers to the exact scheme version and, where known, the pipeline revision that governed it.

Do not use a mutable pointer such as currentSchemeVersion as the only historical reference. A current-version convenience property may be considered later, but it cannot replace the immutable version reference.

### 4.2 BrAPI reference context

BrAPI database identifiers are server-owned identifiers. A bare Program/Germplasm/Trial/Study/PlannedCross ID is not globally resolvable across independent servers.

Candidate BrAPI reference data therefore needs, at minimum, the API generation, resource type, source server/authority, and source dbId. The exact encoding—server base URL, authority URI, external reference, or another governed identifier—remains open. The contract must define canonical resolution and normalization rules; implementations must not guess an authority from an unqualified string.

### 4.3 Scheme-local stage identifiers

A stageId is unique only within its SchemeVersion. For example, F2 in one scheme is not automatically equivalent to F2 in another scheme, crop, breeding method, or organization.

Any execution event carrying a stageId must carry the exact SchemeVersion ID that defines that stage. Stage IDs must not be reused across revisions with different meanings unless the versioning rules explicitly preserve their semantics.

## 5. Definition-time versus execution-time ownership

| Concept | Definition-time owner | Execution-time owner |
|---|---|---|
| Pipeline purpose and target | PipelineRevision | Not an execution event |
| Scheme version and process topology | SchemeVersion | Not an execution event |
| Permitted stage transition | SchemeVersion | Actual movement is a PopulationAdvancement or other event |
| Crossing method and strategy | Scheme task definition, referencing BrAPI BreedingMethod | BrAPI PlannedCross, CrossingProject, and Cross |
| Evaluation plan | Scheme task definition | BrAPI Trial, Study, ObservationUnit, Observation |
| Selection rule/criterion | Scheme task definition or resolvable criterion reference | GenX SelectionDecision |
| Material identity/parentage | BrAPI Germplasm and Pedigree | The actual BrAPI material and pedigree records |
| Family/generation/cohort context | Strategy may describe expected grouping | Actual material and execution records |

A task definition is never evidence that the corresponding activity happened. A Transition is never an actual advancement event. An actual PopulationAdvancement does not rewrite the scheme's permitted-transition graph.

## 6. Candidate invariants

The following invariant IDs correspond to the candidate JSON fixture corpus. They are design-level acceptance conditions, not current production probes.

| ID | Invariant | Failure condition |
|---|---|---|
| BM-01 | Pipeline identity describes the workstream, not a current material stage | Pipeline carries one scalar currentStage as its definitive progress state |
| BM-02 | Stage occupancy belongs to cohorts/material execution | Multiple concurrent cohorts are collapsed into one pipeline stage |
| BM-03 | Published revisions are immutable | Content changes while the same published version identity is retained |
| BM-04 | Pipeline and scheme logical identities are distinct from immutable revisions | A stable ID cannot identify both continuing resource and exact historical version unambiguously |
| BM-05 | Stage IDs are unique within a scheme version | Duplicate stage IDs occur within one version |
| BM-06 | BrAPI-owned objects remain authoritative | GenX creates a second conflicting Program, Cross, Germplasm, Pedigree, Trial, or Study record for the same object |
| BM-07 | Historical execution refers to exact version identities | Event resolves only to the latest version, or its scheme version is ambiguous |
| BM-08 | Concurrent cohorts may occupy different stages of one scheme version | Model requires all materials in a pipeline to share one current stage |
| BM-09 | Definitions and execution evidence are distinct | A task definition or transition is treated as proof that work occurred |
| BM-10 | Transition endpoints must resolve within the same scheme version | From/to stage IDs are absent or resolve outside that version |
| BM-11 | Scheme-local stage references require a scheme version | Event supplies a stage ID without schemeVersionId |
| BM-12 | Pipeline and scheme version bindings must agree | Event references a scheme version not adopted by its referenced pipeline revision |
| BM-13 | A changed published scheme receives a new version identity | Same schemeVersionId is reused for changed process content |
| BM-14 | There is one authoritative source for a material's parentage graph | GenX progeny record conflicts with BrAPI Pedigree for the same Germplasm |
| BM-15 | A scheme version's transitions are directed and explicit | Display order alone is treated as full process semantics |
| BM-16 | Stage labels and mappings do not imply global equivalence | The contract forces a universal crop-independent stage vocabulary |
| BM-17 | Planned and completed crosses remain distinguishable | A planned crossing task is interpreted as an actual Cross |
| BM-18 | A decision criterion is not itself a decision | A planned selection rule is represented as an actual SelectionDecision |
| BM-19 | Breeding cycle is not CropCycle | Planting-to-harvest interval is used as a substitute for a recurrent breeding cycle |
| BM-20 | A BrAPI reference preserves authority/server context | A bare dbId is resolved against an unspecified server |

## 7. Candidate event-reference rules

The scheme and pipeline reference fields should be optional where an event was not governed by a registered GenX scheme, but strict when they are present.

1. If an event has a scheme-local stage identifier, it must identify the exact SchemeVersion.
2. If an event has both a PipelineRevision and SchemeVersion, that SchemeVersion must be included in that PipelineRevision's scheme bindings.
3. If an event has only a SchemeVersion and no PipelineRevision, it is still resolvable to a process blueprint, but its pipeline context is not asserted.
4. If the event has neither, it is a valid event outside the registered pipeline/scheme model; it must not invent a stage identifier.
5. The event's domain-specific identity and evidence remain owned by the event's own resource. Version references add context; they do not transfer ownership.

These rules allow incremental adoption without forcing every existing BrAPI or GenX event to be retrofitted immediately.

## 8. Cohorts, generations, and breeding cycles

The logical model must support two cohorts using the same SchemeVersion at the same time and occupying different stages. Cohort A may be at F3 while Cohort B is at F2. A selection stream can combine material from multiple cohorts or generations depending on the breeding design.

Do not create a full BreedingCycle or Cohort endpoint in this slice. First identify the minimal execution identity required by supported use cases:
- cohort/selection-stream identity;
- generation label or structured generation semantics;
- breeding-cycle identity where a recurrent cycle must be distinguished from crop season or calendar year;
- relationship to BrAPI Germplasm/Population and actual events.

RFC-029 CropCycle remains a crop-production interval and must not be overloaded to satisfy these needs.

## 9. Cross-resource acceptance conditions

| Resource relationship | Candidate validation |
|---|---|
| Pipeline → BrAPI Program | Program reference includes resolvable server/authority context |
| PipelineRevision → SchemeVersion | Exact scheme-version ID exists and is bound by this pipeline revision |
| SchemeVersion → StageDefinition | Stage IDs are unique within the version |
| SchemeVersion → Transition | Both endpoints exist in the same version |
| StageDefinition → TaskDefinition | Task type is one of the governed categories or a declared extension |
| PopulationAdvancement → Stage | Exact SchemeVersion exists and source/destination stage IDs resolve |
| SelectionDecision → Evidence | Linked BrAPI Observation/Study/Germplasm IDs resolve under their source server |
| Planned crossing task → BrAPI PlannedCross | PlannedCross remains authoritative for actual planned mating identities and parent links |
| Progeny/Pedigree | Exactly one authoritative parentage graph is maintained |
| Trial/Study/Observation | These represent evaluation execution/evidence, not duplicated strategy definitions |

## 10. Candidate fixture corpus

The companion JSON fixture file contains nine design scenarios:
- three positive scenarios: recurrent overlapping cohorts, immutable scheme-version history, and BrAPI execution crosswalk;
- six negative scenarios: dangling stage transition, stage without scheme version, pipeline/scheme mismatch, published scheme mutation, duplicate parentage authority, and pipeline-wide current stage.

The corpus is not production conformance. Its current job is to make the logical model falsifiable and to provide stable examples when the accepted schema is later designed.

Minimum checks before promotion:
1. The JSON file parses.
2. Scenario identifiers are unique and each scenario declares its expected validity.
3. Positive scenarios satisfy their referenced identity and transition constraints.
4. Negative scenarios fail for the declared invariant, not for unrelated malformed JSON.
5. Each example remains independent of BijMantra-specific storage or implementation assumptions.

## 11. Decisions still required before normative schema work

1. Public surface: first-class BreedingScheme resource versus nested versioned scheme object.
2. Ownership/cardinality: whether a scheme version can be reused by more than one pipeline.
3. Pipeline owner cardinality and representation of breeding networks/partners.
4. Pipeline and scheme logical/revision identifier syntax and names.
5. Authority-qualified BrAPI reference structure and canonical URL/authority behavior.
6. Target-context submodel and which pipeline purposes require which target elements.
7. Initial task categories and their typed category-specific properties.
8. Publication, withdrawal, supersession, and correction lifecycles.
9. Whether cohort, generation, and breeding-cycle identities need a separate execution resource.
10. RFC-019, RFC-037, and RFC-098 dispositions following the overlap evidence.
11. Whether current three BreedingPipeline operations remain justified after the resource boundary is selected.

These decisions belong to the project maintainer. This model is a recommendation for review, not an approval.

## 12. Next slice

**Slice 3C — Candidate logical model and fixtures: completed as non-normative design evidence.**

The next useful step is a consolidated maintainer decision packet containing:
- recommended resource boundary and nested/first-class scheme alternatives;
- exact cardinalities and invariants;
- migration implications for the current scalar pipelineStage contract;
- RFC-008/019/029/035/037/098 overlap recommendations;
- unresolved identity, version, reference, and lifecycle decisions;
- a scoped implementation sequence after the maintainer selects the public contract boundary.

No endpoint YAML or schemas should be revised before that direction is established.

## 13. Source baseline

- Official BrAPI v2.1 source branch pinned to commit 0a562640f44bce7217b982ec22980b8a47561dda: https://github.com/plantbreeding/BrAPI/tree/0a562640f44bce7217b982ec22980b8a47561dda
- BrAPI v2.1 Program, PlannedCross, CrossingProject, Cross, Pedigree, Trial, and Study source links are listed in [the cross-RFC overlap review](./BRAPI-GENX-BREEDING-CROSS-RFC-OVERLAP-REVIEW.md#8-references).
- Covarrubias-Pazaran et al. (2022), *Breeding Schemes: What Are They, How to Formalize Them, and How to Improve Them?*, https://doi.org/10.3389/fpls.2021.791859
- Bhosale et al. (2025), *Onerice breeding framework: An end-to-end system to develop better varieties faster*, https://doi.org/10.1002/csc2.70087
