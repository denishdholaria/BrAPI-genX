# BrAPI-GenX — Breeding and Related RFC Overlap Review

**Status:** Evidence-based assessment; advisory, non-normative, not accepted or ratified.  
**Prepared:** 18 November 2026  
**Workstream:** BGX-P1-03 — Cross-RFC and BrAPI boundary review  
**Related design:** [Pipeline and Scheme Candidate Contract Design](./BRAPI-GENX-BREEDING-PIPELINE-SCHEME-CONTRACT-DESIGN.md)  
**Repository baseline:** main at 3b2075c3feac59e4391fb4923baea4a43f40cf27  
**Official baseline inspected:** BrAPI v2.1 branch brapi-V2.1, commit 0a562640f44bce7217b982ec22980b8a47561dda.

## 1. Executive findings

The current GenX breeding-related Request for Comments (RFC) set contains several different situations. They should not be treated uniformly.

| RFC | Current object | BrAPI overlap | Assessment |
|---|---|---|---|
| RFC-008 | SelectionDecision | Low direct overlap | Keep as a candidate GenX-only record for an actual breeder verdict; refine execution context and evidence links |
| RFC-019 | ProgenyRecord | High structural overlap, with a possible generation/family-event gap | Do not promote as written; narrow to semantics not already represented by BrAPI Germplasm and Pedigree |
| RFC-029 | CropCycle | Low direct overlap with pipeline/scheme | Keep separate as a crop-production interval; explicitly distinguish it from a breeding cycle |
| RFC-035 | PopulationAdvancement | Low direct overlap | Keep as a candidate GenX execution event; link it to exact scheme version/stage identities rather than free-text stages |
| RFC-037 | CrossingSchedule | High overlap for planned mating; possible scheduling-specific gap | Do not duplicate PlannedCross; investigate a narrower time/resource scheduling concept |
| RFC-098 | ResearchProgram | Very high/direct overlap | Current premise is contradicted by BrAPI v2.1 Program; a separate resource is not justified by the current schema |

The most consequential correction is **RFC-098**: BrAPI v2.1 explicitly covers breeding programs and funded projects through its Program resource. The GenX ResearchProgram draft currently contains only title, status, supersession, and provenance. It does not define a distinct research-program concept.

The most consequential partial overlaps are **RFC-019** and **RFC-037**. BrAPI already models pedigree/progeny relationships and planned/actual crosses. GenX can still add value where it records a different immutable event or an operational schedule not represented by those contracts, but the semantic gap must be made explicit.

No RFC was deleted, renumbered, merged, promoted, or edited during this review. No BrAPI v2.1 contract was changed.

## 2. Review method and evidence boundary

The review compared:
- current GenX RFC text, README files, and resource schemas on main;
- official BrAPI v2.1 OpenAPI paths and schemas from the pinned brapi-V2.1 branch;
- published breeding-domain literature for pipeline/scheme and activity terminology.

The BrAPI v2.1 source branch inspected includes:
- Core: Programs, Trials, Studies;
- Germplasm: Germplasm, BreedingMethods, CrossingProjects, PlannedCrosses, Crosses, Pedigree;
- Phenotyping: ObservationVariables and related observation resources.

BrAPI identifies v2.1 as its latest stable release and recommends it for new development. Its working-group preview is explicitly subject to change until formal release. This assessment compares against the released v2.1 branch, not the preview.

## 3. RFC-by-RFC findings

### 3.1 RFC-008 — Selection Decisions

**Current GenX semantics:** an immutable verdict for a breeding candidate, such as selected, rejected, deferred, or advanced, including decision date, decision maker, rationale, and evidence references.

**BrAPI coverage:** BrAPI supplies the surrounding objects:
- Program for the breeding program;
- Trial and Study for experiment context;
- Germplasm for the candidate material;
- Observation and ObservationVariable for measured evidence;
- jobs and analytical outputs are separate GenX execution concerns.

The reviewed BrAPI v2.1 contracts do not provide a first-class record whose central meaning is the breeder's selection verdict together with its rationale and decision provenance.

**Assessment:** this is a strong candidate GenX-only resource. It should reference, not replicate, Program, Study, Germplasm, Observation, and relevant analysis outputs.

**Required refinement before promotion:**
- retain the decision as an actual event/verdict, not a scheme rule;
- define the subject of a decision (individual germplasm, population/family, or another defined unit);
- make decision criteria resolvable and preserve the method/version used;
- distinguish decision evidence from the decision rationale;
- consider exact pipeline revision, scheme version, stage, cycle, and cohort references where they materially explain the decision;
- define correction/supersession and authority to record or correct the verdict.

No new BrAPI overlap issue was found that invalidates the basic RFC-008 premise.

### 3.2 RFC-019 — Progeny Records

**Current GenX semantics:** an immutable record connecting a program, progeny germplasm, parent germplasm, generation, family identity, optional BrAPI Cross, and provenance.

**BrAPI coverage is substantial:**
- Germplasm describes the genetically unique organism/material.
- PedigreeNode represents a germplasm node and its parents, siblings, and children.
- PedigreeNode includes familyCode, crossingYear, breedingMethodDbId, breedingMethodName, crossingProjectDbId, parents, and progeny.
- GET /pedigree supports family-code and program filters, parent/progeny inclusion, and pedigree/progeny depth.
- The older GET /germplasm/{germplasmDbId}/progeny path is deprecated in v2.1 in favour of GET /pedigree?germplasmDbId=...

The current GenX ProgenyRecord duplicates much of this graph:
- progenyDbId corresponds to BrAPI Germplasm;
- parentDbIds repeat the BrAPI pedigree edges;
- crossDbId repeats a BrAPI Cross relationship;
- familyId is close to BrAPI familyCode;
- programDbId repeats the BrAPI Program context.

The inspected BrAPI Germplasm/Pedigree models do not expose a dedicated generation field matching GenX's current generation string. The GenX draft also treats the progeny/family relationship as an immutable record, whereas BrAPI Pedigree is a graph representation with update operations. These are possible differences, but they do not yet justify the present duplicate payload.

**Assessment:** high overlap with a plausible residual need around generation assignment, family-level grouping, or immutable family-formation/lineage events. Do not promote RFC-019 in its current form.

**Potential narrowing directions for later design:**
1. a focused immutable family-formation event that references BrAPI Cross and related Germplasm rather than repeating parent/progeny edges;
2. a typed generation/cohort assignment or membership record, if this is not adequately represented by existing BrAPI identifiers or project metadata;
3. no independent resource, if a verified BrAPI extension/reference pattern can carry the required data without semantic loss.

The choice requires a concrete use case, not a presumption that BrAPI has no progeny support. A future proposal must specify what is authoritative: BrAPI Pedigree, a GenX formation event, or a separate family/cohort record. Two competing sources of parentage truth must not be created.

### 3.3 RFC-029 — Crop Cycle

**Current GenX semantics:** a planting-to-harvest crop-production interval associated with a Location and optionally a Study.

This is distinct from a **breeding cycle**, which is an execution loop that may span generations and can be defined from crossing through selection and recycling of parents. A breeding cycle is not necessarily equal to a season, crop cycle, trial, or generation.

**Assessment:** the current RFC-029 problem statement is internally coherent as a crop-production concept. It should remain in D6 and must not be reused as the pipeline's breeding-cycle identity.

**Boundary rule:** a BreedingPipeline or scheme may reference studies and crop-production context when relevant, but must not equate a CropCycle record with a BreedingCycle execution instance. A breeding-cycle resource is not currently authorized or justified.

### 3.4 RFC-035 — Population Advancement

**Current GenX semantics:** an immutable record that a population or family moved from one stage to another on a date, under a BrAPI Program, with provenance.

**BrAPI coverage:** BrAPI represents germplasm, pedigree, crosses, studies, and trials, but the reviewed v2.1 contracts do not provide a dedicated immutable population-advancement verdict/event with the current GenX semantics.

**Assessment:** this is a plausible GenX-only execution record. Its concept must be separated from the BreedingScheme transition graph:
- a scheme transition describes that progression from Stage A to Stage B is allowed under defined criteria;
- a PopulationAdvancement record states that a particular population actually advanced from A to B at a given time, with its evidence/decision.

**Required refinement before promotion:**
- define what populationDbId actually identifies and whether it is a BrAPI Germplasm or another registered entity;
- reference the pipeline and exact scheme version where applicable;
- use scheme-local stage identifiers where the advancement occurred under a scheme;
- link to the SelectionDecision or other evidence that authorized the advancement;
- define treatment of advancement outside a formally registered scheme;
- preserve the actual event's historical record even if the scheme is later superseded.

Do not add transition rules to this event schema. Do not treat fromStage and toStage as unconstrained universal vocabulary strings if they refer to a specific scheme version.

### 3.5 RFC-037 — Crossing Schedule

**Current GenX semantics:** a record containing a Program, scheduled date, a list of parent germplasm IDs, a mating-design string, and lifecycle status.

**BrAPI coverage is substantial for the planned mating itself:**
- CrossingProject is a project structure under a Program, with potential parents and associated planned/actual crosses.
- PlannedCross is explicitly an intention to mate specific organisms; its request includes parent1, parent2, cross type, status, project ID/name, and planned-cross name.
- Cross records the mating event that actually occurred and can refer back to its PlannedCross and CrossingProject.

The currently inspected BrAPI PlannedCrossNewRequest does not define a dedicated scheduled date/time. This leaves a possible scheduling-specific gap. However, the GenX draft currently stores a date and a parent list without a link to a BrAPI PlannedCross or CrossingProject. It risks creating a second record of the planned mating rather than adding a clear scheduling dimension.

**Assessment:** high overlap for the mating-intent part; possible independent value for operational scheduling. Do not promote the current RFC-037 payload unchanged.

**Potential narrowing direction:** if a real operational use case exists, define a scheduling/booking record that groups or schedules one or more BrAPI PlannedCross identifiers and records the extra scheduling semantics not in PlannedCross, such as a time slot, location/facility, assigned operator/resources, capacity, or schedule status. Keep parents, cross type, and mating identity authoritative in BrAPI PlannedCross/Cross. The actual fields and resource boundary need a separate use-case review; this is not approval to implement them.

If the date is merely an attribute of a planned cross in the target deployment, prefer a compatible BrAPI extension/additional-info approach over an independent GenX resource.

### 3.6 RFC-098 — Research Program

**Current GenX semantics:** an immutable record with a research-program ID, title, status, supersession, and provenance. It optionally links to a BrAPI Study.

**BrAPI coverage:** the v2.1 Program description explicitly says it represents the high-level organization or group responsible for conducting trials and studies, including breeding programs and funded projects. ProgramNewRequest includes program name, objective, program type (STANDARD or PROJECT), crop, lead person, funding information, documentation URL, and external references. Trials and Studies can reference Program.

The GenX RFC assertion that “BrAPI v2.1 has no place to record research programs” is therefore incorrect. The GenX schema does not presently identify a distinct concept such as a portfolio above multiple BrAPI Programs, a cross-institution programme consortium, or a governance/funding entity with a different identity/lifecycle.

**Assessment:** very high/direct semantic overlap. The current schema is not justified as an independent ResearchProgram resource.

**Potential disposition for maintainer consideration:**
- defer or withdraw the standalone resource and reference BrAPI Program;
- or, only if a distinct higher-level entity is demonstrated, rename and redefine it around that separate concept, with explicit cardinality and ownership relative to BrAPI Programs.

Do not attempt to solve missing provenance/versioning by duplicating Program. First identify the precise record that lacks those properties and determine whether they belong on the BrAPI Program, in an extension, or in a separate resource.

## 4. Cross-resource dependency model

The following is a candidate boundary graph, not a committed schema:

~~~text
BrAPI Program
    |
    +---- GenX BreedingPipeline
                |
                +---- target context(s)
                |
                +---- exact BreedingSchemeVersion(s)
                           |
                           +---- stage definitions
                           +---- permitted transitions
                           +---- task definitions
                                      |
                                      +---- BrAPI PlannedCross / CrossingProject / Cross
                                      +---- BrAPI Trial / Study / Observation
                                      +---- BrAPI Germplasm / Pedigree
                                      |
                                      +---- GenX SelectionDecision (actual verdict)
                                      +---- GenX PopulationAdvancement (actual movement)

BrAPI Germplasm / Pedigree
    +---- family/progeny relationships (already represented in BrAPI)
    +---- possible GenX immutable formation event only if a separate gap is proven

BrAPI Program / CrossingProject / PlannedCross
    +---- possible GenX scheduling record only if scheduling semantics exceed planned mating
~~~

Ownership rules:
1. BrAPI remains authoritative for BrAPI Program, Germplasm, Pedigree, CrossingProject, PlannedCross, Cross, Trial, Study, and Observation resources.
2. Pipeline and scheme describe workstream and process intent, not execution results.
3. SelectionDecision and PopulationAdvancement are candidate GenX execution records.
4. Any GenX extension record references the BrAPI source and does not silently create a second authoritative copy of the same relationship.
5. Each execution record that needs historical interpretation should retain the exact pipeline/scheme version that governed it.

## 5. Consolidated disposition recommendations

| RFC | Recommendation | Confidence | Reason |
|---|---|---|---|
| RFC-008 Selection Decisions | Retain and refine | High | Distinct actual verdict and rationale not represented as a BrAPI first-class resource |
| RFC-019 Progeny Records | Narrow or defer pending gap definition | High | Parent/progeny/family graph is already covered by BrAPI Pedigree; only generation/event semantics remain plausible differentiators |
| RFC-029 Crop Cycle | Retain, with clear naming boundary | High | Crop-production interval is distinct from breeding cycle |
| RFC-035 Population Advancement | Retain and refine | High | Actual advancement event is distinct from permitted scheme transition |
| RFC-037 Crossing Schedule | Narrow to schedule-specific semantics or defer | High | PlannedCross already models mating intent, parents, project, type, and status; schedule-specific time/resource details may remain |
| RFC-098 Research Program | Defer/withdraw standalone resource unless a different concept is proven | Very high | BrAPI Program already represents breeding programs, projects, and responsible research organizations |

These are recommendations, not accepted dispositions. RFC IDs, current operation IDs, endpoint folders, and maturity states were deliberately not altered.

## 6. Required changes to pipeline/scheme contract design

The candidate Pipeline/Scheme model should account for these findings:

- Program reference must point to BrAPI Program; do not create a GenX ResearchProgram dependency.
- Pipeline/scheme task definitions may reference BrAPI BreedingMethod, PlannedCross, CrossingProject, Cross, Trial, Study, ObservationVariable, and Germplasm where relevant.
- A SelectionDecision is an actual verdict and may cite the scheme criteria and exact version.
- A PopulationAdvancement is an actual movement event and should reference scheme stage identifiers where applicable.
- A ProgenyRecord cannot be used as a second authority for parent/offspring edges without a documented immutable-event reason.
- A CrossingSchedule cannot duplicate the same parent pair and mating intent already recorded as PlannedCross; any residual schedule record must add independent scheduling semantics.

## 7. Review outcome and next work

### Slice 3B — Cross-RFC overlap review

**Completed as assessment.** Official BrAPI v2.1 coverage and GenX draft boundaries were checked for all six RFCs in scope. RFC-008 and RFC-035 remain strong extension candidates; RFC-019 and RFC-037 need narrower semantics; RFC-098 presently duplicates BrAPI Program. No RFC or API contract changed.

### Slice 3C — Candidate logical model and fixtures

**Completed as non-normative design evidence.** The [Candidate Logical Model](./BRAPI-GENX-BREEDING-PIPELINE-LOGICAL-MODEL.md) defines relationship cardinalities and 20 design invariants. The [Candidate Fixture Corpus](./BRAPI-GENX-BREEDING-PIPELINE-CANDIDATE-FIXTURES.json) contains three positive and six negative cases for recurrent cohorts, exact version history, BrAPI execution crosswalks, dangling stages, missing scheme versions, mismatched bindings, mutation of published versions, duplicate parentage authority, and ambiguous pipeline-wide stage state. Structural and semantic checks passed. These cases remain assessment-only; they are not production conformance fixtures and are not wired into CI.

### Slice 4 — Maintainer contract decision package

**Prepared** in [the Maintainer Decision Package](./BRAPI-GENX-BREEDING-PIPELINE-MAINTAINER-DECISION-PACKAGE.md). It sets out the recommended resource boundary, scheme representation alternatives, identity/version model, BrAPI reference rules, migration consequences, and dispositions for the six related RFCs. The package identifies 13 maintainer decisions. No RFC, endpoint YAML, schema, or maturity state was changed.

## 8. References

### Breeding-domain literature

- Covarrubias-Pazaran, G. et al. (2022). *Breeding Schemes: What Are They, How to Formalize Them, and How to Improve Them?* Frontiers in Plant Science, 12:791859. https://doi.org/10.3389/fpls.2021.791859
- Bhosale, S. et al. (2025). *Onerice breeding framework: An end-to-end system to develop better varieties faster.* Crop Science, 65(3), e70087. https://doi.org/10.1002/csc2.70087

### Official BrAPI v2.1 sources inspected

Pinned source: https://github.com/plantbreeding/BrAPI/tree/0a562640f44bce7217b982ec22980b8a47561dda

- Program model: https://github.com/plantbreeding/BrAPI/blob/0a562640f44bce7217b982ec22980b8a47561dda/Specification/BrAPI-Core/Programs/Schemas/Program.yaml
- PlannedCross model: https://github.com/plantbreeding/BrAPI/blob/0a562640f44bce7217b982ec22980b8a47561dda/Specification/BrAPI-Germplasm/PlannedCrosses/Schemas/PlannedCrossNewRequest.yaml
- CrossingProject model: https://github.com/plantbreeding/BrAPI/blob/0a562640f44bce7217b982ec22980b8a47561dda/Specification/BrAPI-Germplasm/CrossingProjects/Schemas/CrossingProjectNewRequest.yaml
- Cross model: https://github.com/plantbreeding/BrAPI/blob/0a562640f44bce7217b982ec22980b8a47561dda/Specification/BrAPI-Germplasm/Crosses/Schemas/CrossNewRequest.yaml
- Pedigree node: https://github.com/plantbreeding/BrAPI/blob/0a562640f44bce7217b982ec22980b8a47561dda/Specification/BrAPI-Germplasm/Pedigree/Schemas/PedigreeNode.yaml
- Pedigree operations: https://github.com/plantbreeding/BrAPI/blob/0a562640f44bce7217b982ec22980b8a47561dda/Specification/BrAPI-Germplasm/Pedigree/Pedigree_GET_POST_PUT.yaml
- Trial model: https://github.com/plantbreeding/BrAPI/blob/0a562640f44bce7217b982ec22980b8a47561dda/Specification/BrAPI-Core/Trials/Schemas/Trial.yaml
- Study model: https://github.com/plantbreeding/BrAPI/blob/0a562640f44bce7217b982ec22980b8a47561dda/Specification/BrAPI-Core/Studies/Schemas/Study.yaml
- BreedingMethod model: https://github.com/plantbreeding/BrAPI/blob/0a562640f44bce7217b982ec22980b8a47561dda/Specification/BrAPI-Germplasm/Germplasm/Schemas/BreedingMethod.yaml
- BrAPI specification page: https://brapi.org/specification
