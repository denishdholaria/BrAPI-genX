# RFC-154 — Breeding Pipeline (D2)

- Status: approved candidate contract design; non-normative until the RFC acceptance gates are met.
- Supersedes: RFC-014 for the canonical pipeline design; RFC-014 is retained as historical evidence and is not deleted or renumbered.
- Related: RFC-001 (GenX skeleton), RFC-008 (Selection Decisions), RFC-029 (Crop Cycle), RFC-035 (Population Advancement), RFC-037 (Crossing Schedule), RFC-098 (Research Program), and the BreedingPipeline/Scheme decision package.
- Maintainer authorization: D-BP-01 through D-BP-13 approved on 18 November 2026.
- Terminology: BrAPI (Breeding Application Programming Interface); API (Application Programming Interface); RFC (Request for Comments); URI (Uniform Resource Identifier); TPE (target population of environments).

## 1. Purpose

A BreedingPipeline is a durable, goal- and target-oriented breeding workstream associated with one owning BrAPI Program. It describes why the workstream exists, its target context, and the exact breeding-scheme versions adopted or evaluated by the workstream.

A BreedingPipeline is not:
- a BrAPI Program, Trial, Study, Germplasm, Cross, or Pedigree;
- a single stage occupied by every material in the workstream;
- an execution workflow or task scheduler;
- a governmental variety approval, registration, or release record.

A pipeline may use multiple schemes and may have multiple immutable revisions over its lifetime.

## 2. BreedingPipeline and BreedingScheme boundaries

- **BreedingPipeline**: persistent breeding workstream and target context.
- **BreedingPipelineRevision**: immutable snapshot of pipeline purpose, target contexts, and exact scheme-version bindings.
- **BreedingScheme**: stable identity for a process blueprint.
- **BreedingSchemeVersion**: immutable published process definition.
- **StageDefinition**: scheme-version-local description of a breeding stage.
- **Transition**: permitted directed relationship between two stages in one scheme version. It may be forward, branching, or recurrent.
- **TaskDefinition**: design-time activity definition, not evidence that an activity occurred.
- **Execution record**: actual event or evidence, owned by its relevant BrAPI or GenX resource.

The initial public contract gives BreedingScheme a first-class logical identity and immutable version identity, but embeds the version definition in the adopting PipelineRevision. No separate BreedingScheme CRUD endpoints are introduced in this initial surface. The logical model must not preclude a later dedicated endpoint that exposes the same identity and version semantics.



#### 2.1 Embedded scheme-version definition

Each PipelineRevision `schemeBindings[]` item contains the stable `breedingSchemeDbId`, exact `breedingSchemeVersionDbId`, an optional local adoption `role`, and a required `schemeVersion` object. The embedded `schemeVersion` contains the same `breedingSchemeDbId` and `breedingSchemeVersionDbId` values plus its publication state, stages, transitions, task definitions, and provenance. The two identity pairs must match exactly. This makes a pipeline revision historically interpretable without introducing standalone BreedingScheme endpoints.

A binding is not merely a pointer to a remote mutable “current” scheme. Reuse of a scheme version across pipeline revisions is represented by embedding the same immutable definition and version identity in each adopting revision. The contract does not yet assert that a scheme may or may not be reused by different pipeline logical identities; that relationship remains constrained by the approved design boundary and future evidence.

Stage and transition task definitions are both permitted. Every stage and transition ID is unique only within its scheme version; every task ID is unique across all task definitions in that version. Transition IDs are required, transition endpoints must resolve to stages in the same version, and each transition declares an explicit type. 

## 3. Identity and immutable revisions

| Identifier | Meaning |
|---|---|
| breedingPipelineDbId | Stable logical identity of the continuing workstream |
| breedingPipelineVersionDbId | Immutable identity of one pipeline revision |
| breedingSchemeDbId | Stable logical identity of a process blueprint |
| breedingSchemeVersionDbId | Immutable identity of one scheme definition version |

A PipelineRevision:
- belongs to exactly one BreedingPipeline logical identity;
- has one immutable breedingPipelineVersionDbId;
- contains the exact BrAPI Program reference;
- contains zero or more target contexts;
- contains zero or more scheme bindings, each resolving to an exact scheme version;
- carries provenance for the revision.

A scheme binding identifies the exact breedingSchemeDbId and breedingSchemeVersionDbId, and may include a locally governed role such as principal or experimental. The role does not change the referenced scheme's identity.

A new revision is registered under the existing breedingPipelineDbId by supplying a new breedingPipelineVersionDbId. Replaying the same version ID with an identical body returns the existing version. Reusing the same version ID with a different body is rejected with 409. A new version ID is required for every substantive published revision.

A published revision is immutable. Corrections preserve the original revision and are represented by a new revision with an explicit correction/supersession relationship. A mutable current-version pointer may be exposed as a convenience only; it must never be the only way to retrieve historical versions.

## 4. BrAPI authority-qualified references

BrAPI identifiers are owned by a BrAPI server. A dbId alone is not sufficient to resolve a resource across independent servers.

The candidate reference object contains:
- apiGeneration, identifying the BrAPI contract generation (wire token: `brapi-v2.1`);
- resourceType, using the exact official resource name (for example Program, Germplasm, Study, Trial, PlannedCross, Cross, Observation, or ObservationVariable);
- server, identifying the authoritative BrAPI server or authority URI;
- dbId, the identifier issued by that server.

The server/authority value must be canonical and resolvable under an explicit policy. Implementations must not infer an authority from an unqualified identifier, and must not silently resolve a reference against their own default server.

This RFC fixes the semantic shape, not a final URI serialization syntax. The contract-definition slice must settle server canonicalization, normalization, and dereference policy before schema promotion.

## 5. Target contexts

A PipelineRevision supports zero or more purpose-specific target contexts. A target context may describe:
- product concept/profile reference or immutable descriptive snapshot;
- market segment reference or description;
- target population of environments (TPE) reference or description;
- zero or more trait requirements, each with a BrAPI Trait or ObservationVariable reference and a desired direction; quantitative requirements are scale-bound as described below;
- target provenance and the source authority/version for any external profile snapshot.

Target contexts are purpose-specific. Do not require product/market fields for every pipeline purpose. Trait targets are breeding objectives, not observations or measurements.

### 5.1 Trait-only and quantitative objectives

A directional-only objective may reference an authority-qualified BrAPI `Trait`. A numeric threshold or range must reference an authority-qualified BrAPI `ObservationVariable`. Under BrAPI v2.1, an ObservationVariable is the combination of one Trait, one Method, and one Scale. The embedded Scale is therefore the authoritative source for the measurement unit, decimal-place precision, data type, and valid-value constraints.

The target requirement does not repeat a free-text unit field. Its numeric values are expressed in the Scale of the referenced ObservationVariable. Implementations must not infer or silently convert between units or scales. A different measurement scale requires a different ObservationVariable reference. The exact official BrAPI v2.1 schemas remain authoritative for Trait, Method, ObservationVariable and Scale; this RFC does not redefine them.

Numeric target representation is one of:
- `threshold`: scalar JSON number;
- `exactDecimal`: scalar base-10 decimal string, without exponent notation, when JSON number semantics are insufficient;
- `minimum` and `maximum`: inclusive numeric range bounds, both required together;
- `minimumExactDecimal` and `maximumExactDecimal`: inclusive exact-decimal range bounds, both required together.

A scalar target cannot be combined with range bounds. Numeric and exact-decimal representations cannot be mixed in one target. The `target-range` direction requires one complete lower/upper bound pair; lower must not exceed upper. Other directions do not carry range bounds. The Scale's `decimalPlaces`, `validValues`, `minimumValue`, and `maximumValue` govern admissible values; candidate schema validation can check representation and range pairing, but validation against a live ObservationVariable Scale is an interoperability/runtime acceptance gate.

This initial contract does not create independent public APIs for MarketSegment, ProductConcept, or TPE. Their independent identity, authority, reuse, and lifecycle have not been demonstrated.

## 6. Scheme version contents

A SchemeVersion contains:
- one or more StageDefinitions;
- zero or more directed Transitions;
- zero or more TaskDefinitions assigned to stages or transition/gate contexts;
- provenance and version/lifecycle metadata.

Stage IDs are unique only within their exact scheme version. Labels and codes may be crop- and organization-specific. Display order is presentation metadata only and does not define process semantics.

Initial task categories are crossing, generation advancement, multiplication, evaluation, and selection.

The initial model does not include executable gate scripts, generic workflow gateways, orchestration, scheduling, dispatch, retries, event routing, or live cohort state. Category-specific detail must be typed and introduced only for validated interoperability needs; opaque parameter bags are not a substitute for domain modelling.

## 7. Execution and evidence ownership

Actual execution remains with the authoritative resource:
- BrAPI Program owns program context.
- BrAPI BreedingMethod owns breeding-method identity.
- BrAPI CrossingProject, PlannedCross, and Cross own crossing project, mating intent, and actual cross facts.
- BrAPI Germplasm and Pedigree own biological material and parentage.
- BrAPI Trial, Study, ObservationUnit, Observation, and ObservationVariable own experiment and observation evidence.
- GenX SelectionDecision may own an actual selection verdict.
- GenX PopulationAdvancement may own an actual material-progression event.

A scheme TaskDefinition is not proof of execution. A Transition is not an actual advancement event. An execution event may cite pipeline and scheme version context when it was governed by a registered strategy. If it includes a stage ID, it must include the exact scheme version that defines that stage. If it includes both a pipeline revision and scheme version, the revision must bind that exact scheme version.


### 7.1 Execution-context envelopes

Execution resources use two optional nested context objects rather than independent scalar identifiers:
- `pipelineContext` contains both `breedingPipelineDbId` and exact `breedingPipelineVersionDbId`;
- `schemeContext` contains both `breedingSchemeDbId` and exact `breedingSchemeVersionDbId`, with optional `stageId`, `fromStageId`, or `toStageId` inside that object.

Because stage identifiers are nested inside `schemeContext`, an event cannot express a scheme-local stage without also expressing the scheme logical and version identities. Either context may be omitted when the activity was not governed by a registered GenX pipeline or scheme. If both are present, the exact scheme version must be included in the referenced pipeline revision's embedded scheme bindings. A scheme context without pipeline context remains valid.

## 8. Lifecycle dimensions

Do not overload a single status field to express draft versus published, adopted/active versus no longer used, current versus superseded, governance approval, and governmental variety registration or release.

Published pipeline and scheme versions are immutable. Substantive changes create new version identities. The final public contract must define permitted lifecycle transitions and actor authority. No GenX lifecycle status implies regulatory approval.

## 9. Initial endpoint surface

The initial BreedingPipeline endpoint surface remains:
- GET /genx/v1/breeding-pipelines — list logical pipelines, with explicitly defined current/all revision semantics;
- POST /genx/v1/breeding-pipelines — register a logical pipeline and immutable revision, or append a revision using a new version ID;
- GET /genx/v1/breeding-pipelines/{breedingPipelineDbId} — retrieve the logical pipeline view with a defined current-revision selector;
- exact historical revision retrieval must be supported by a version-aware lookup contract before normative promotion.

The route shape for exact revision retrieval, whether nested or a query parameter, remains to be finalized in the contract-definition slice. The initial design does not add separate BreedingScheme endpoints.

The list and retrieval operations must not imply that a logical pipeline is a single immutable version. Mutation of published content is prohibited; corrections create new versions.

## 10. Related RFC disposition

| RFC | Disposition |
|---|---|
| RFC-014 | Historical predecessor. Preserve file and number; canonical design is consolidated here. |
| RFC-008 SelectionDecision | Retain and refine as an actual verdict; add exact pipeline/scheme version context where applicable. |
| RFC-019 ProgenyRecords | Defer the current broad resource. BrAPI Pedigree remains authoritative for parentage. Reopen only for a distinct immutable formation/family event with a proven gap. |
| RFC-029 CropCycle | Retain as crop planting-to-harvest cycle; never reuse as a breeding cycle. |
| RFC-035 PopulationAdvancement | Retain and refine as an actual population progression event; qualify stage IDs with an exact scheme version. |
| RFC-037 CrossingSchedule | Defer the broad current resource. Reopen only for scheduling/booking semantics that add value beyond PlannedCross and CrossingProject. |
| RFC-098 ResearchProgram | Defer the duplicate resource. BrAPI Program remains authoritative. Reopen only if a distinct portfolio/network/governance concept is demonstrated. |

No historical RFC is deleted or renumbered.

## 11. Compatibility and conformance

The GenX surface is additive and optional. It must not alter official BrAPI v2.1 paths, schemas, or operation identifiers.

Before this RFC is promoted:
1. settle the exact version-retrieval route and current/all list semantics;
2. settle BrAPI server canonicalization and typed reference schema;
3. validate target-context profile variants and typed units/precision;
4. implement and behaviorally validate the maintainer-ratified candidate current-revision compare-and-set profile in §12.7, including concurrent publication and failure-atomicity tests; validate lifecycle/actor authorization separately;
5. validate embedded scheme-version identity equality and nested execution-context envelopes;
6. synchronize OpenAPI, registry, generated catalogue, crosswalk, and conformance probes;
7. test positive and negative revision/replay/version-binding cases;
8. retain all official BrAPI source contracts unchanged.

The current maintainer choices, recommendations, alternatives, and implementation consequences are consolidated in [Breeding Pipeline Open Maintainer Decisions](../../docs/assessment/BRAPI-GENX-BREEDING-PIPELINE-OPEN-DECISIONS.md). That note is advisory and does not change the approval record.

Until these gates pass, this document is an approved candidate design, not a normative released specification.

## 12. Candidate request and response semantics

This section makes the provisional operation behavior explicit enough for schema and registry reconciliation. It does not waive the acceptance gates in §11.

### 12.1 Registration request

The registration request contains:
- `breedingPipelineDbId`: stable logical workstream identity;
- `breedingPipelineVersion`: the immutable revision payload, including `breedingPipelineVersionDbId`.

The first successful registration creates the logical identity and its first revision. A subsequent registration under the same `breedingPipelineDbId` appends a revision only when `breedingPipelineVersionDbId` is new. The idempotency key is the immutable version identity, not the logical workstream identity.

The request body must not allow a client to mutate an already published revision by sending changed content under the same version identifier. Servers must compare the canonical request representation under the GenX idempotency rules and reject a same-version/different-payload conflict with HTTP 409.

### 12.2 List behavior

`GET /breeding-pipelines` returns logical workstream summaries. By default, each workstream is represented by its current published revision summary. `includeRevisions=true` includes the known revision summaries for each logical workstream. This flag does not inline the full historical revision payloads and does not replace exact revision retrieval.

The list response's `BreedingPipeline` item represents the stable logical identity and may include the convenience `currentBreedingPipelineVersionDbId` and a `currentRevisionSummary`. When `includeRevisions=true`, the `revisionSummaries` array contains lightweight metadata for all known revisions. These summaries include the immutable version identifier and publication state but not full scheme definitions, target contexts, or other historical payload content. Exact historical revision retrieval remains a separate operation. It must not imply that the workstream itself is an immutable revision.

### 12.3 Single-resource retrieval

`GET /breeding-pipelines/{breedingPipelineDbId}` without a version selector returns the logical identity and current published revision view. Supplying `breedingPipelineVersionDbId` selects that exact immutable revision. The response result is the `BreedingPipelineRevision` for both default and exact-version lookups; the stable logical identifier is retained within the revision object.

A missing logical identity returns 404. An unknown version under an existing logical identity also returns 404 and must not fall back silently to the current revision.

### 12.4 Lifecycle and revision relationships

`publicationState` distinguishes draft, published, and withdrawn definitions. It does not describe adoption, currentness, governance approval, or regulatory variety release. `revisionRelationship.relationshipType` may identify `supersedes` or `corrects`; `priorBreedingPipelineVersionDbId` identifies the exact prior revision. A revision with no prior relationship leaves this object absent.

### 12.5 Explicitly unresolved wire-level details

The following remain gates rather than guessed defaults:
- whether exact version selection remains a query parameter or becomes a nested version route;
- final authorization policy for publishing, withdrawing, and resolving a current-revision precondition;
- canonical BrAPI server URI normalization and authority dereferencing;
- runtime dereference of ObservationVariable to its Trait/Method/Scale, and validation of target values against the referenced Scale's units, decimalPlaces, and validValues;
- whether lifecycle transitions need a separate governance event/audit resource.

The current query-selector and list flag are candidate semantics to test in the implementation-independent OpenAPI build, not a promise that the final public path is immutable.

### 12.6 Authority-qualified execution filters

List filters that accept BrAPI identifiers must preserve the owning server authority rather than resolve a bare `dbId` against an inferred local/default server. The current candidate filter pairs are:

| Resource filter | Required authority context when the identifier filter is used |
|---|---|
| Program | `programDbId` + `programServer` |
| Study | `studyDbId` + `studyServer` |
| Germplasm candidate | `candidateGermplasmDbId` + `candidateGermplasmServer` |
| Population/family | `populationDbId` + `populationServer` + `populationResourceType` |

The source server is the authoritative BrAPI v2.1 base URI. The exact `populationResourceType` is supplied because the candidate model has not approved one universal mapping from a population/family concept to a single BrAPI resource type. A server must not guess that resource type from an identifier or silently substitute Germplasm. API generation is fixed to BrAPI v2.1 for this initial filter profile; resource types use exact official resource names.

These paired parameters are candidate wire semantics. Before normative promotion, conformance cases must prove that omitted authority/type pairs fail closed when an identifier filter is supplied, valid pairs resolve only against the identified server/resource type, and same-valued dbIds from different authorities remain distinct.


### 12.7 Candidate current-revision compare-and-set profile — pending maintainer ratification

The following is the maintainer-ratified candidate concurrency profile for a single current published revision per stable BreedingPipeline identity. The maintainer selected Option A (optimistic compare-and-set) on 19 November 2026. This ratification adds a technical decision beyond D-BP-01 through D-BP-13; it does not promote RFC-154 to normative status.

The registration envelope carries `expectedCurrentBreedingPipelineVersionDbId` alongside `breedingPipelineVersion`. This precondition is outside the immutable revision payload and is excluded from that revision's canonical replay fingerprint.

1. **First registration:** omit the precondition because no logical pipeline exists yet. The first revision may be draft or published. A first published revision initializes the current pointer; a first draft leaves it unset. Creation of the logical identity and first revision must be atomic, and a concurrent attempt to create the same logical identity must resolve as a single winner; the losing request must not overwrite or silently append to the winner's workstream.
2. **Existing workstream:** every new immutable version must include the expected current pointer observed by the client. Supply the exact current `breedingPipelineVersionDbId`, or explicit JSON `null` when the workstream has no published revision. Omission is not equivalent to null.
3. **Replay precedence:** first evaluate whether the incoming `breedingPipelineVersionDbId` already exists. If the revision payload is canonically identical under JCS (RFC 8785), return the prior result without re-evaluating the now possibly stale pointer precondition. If the same version ID has different canonical revision content, return a version-content conflict. The expected-current field is not part of this equality comparison. Replay lookup must be scoped to the owning logical pipeline identity; a version ID collision across different logical pipelines must never return or disclose another pipeline's revision.
4. **New draft:** compare the supplied expected pointer atomically with the current pointer. On a match, append the immutable draft but do not change the current pointer. Multiple drafts may therefore coexist against the same published baseline. A draft's prior relationship records its declared baseline; it does not imply that the draft has superseded the published revision.
5. **New published revision:** compare the supplied expected pointer atomically with the current pointer. On a match, append the immutable published revision and advance the pointer in the same transaction. If a current pointer exists, `revisionRelationship.priorBreedingPipelineVersionDbId` must identify that exact version using `supersedes` or `corrects`. If the current pointer is null, this is the first published revision.
6. **Withdrawal:** compare the supplied expected pointer atomically with the current pointer. A new immutable withdrawn revision must identify the exact current version it withdraws; append it and clear the pointer in the same transaction. A workstream with no current published version cannot withdraw a current version. Withdrawal must not delete or mutate the historical published revision.
7. **Lost race and linearization:** the publication or withdrawal linearization point is the successful atomic commit that both appends the immutable revision and advances or clears the current pointer after the expected-pointer comparison. For a draft append, it is the atomic commit that appends the draft after checking the expected pointer. If the expected pointer does not equal the current pointer at the transaction's serialization/commit decision, return HTTP 409 Conflict and make no append or pointer mutation. Concurrent requests using the same baseline therefore have at most one successful published-pointer transition; the loser must retrieve current state and, if its intent remains valid, submit a new revision with a new version ID. A server must not report success before the atomic commit is durable.
8. **Persistence independence:** implementations may use row locking, serializable transactions, conditional updates, or another persistence-specific mechanism, but externally observable behavior must be equivalent to the atomic rules above. The read/compare/write sequence must not permit a time-of-check/time-of-use race. The complete revision append, pointer transition, and any required outbox/audit record must commit or roll back together where those records are part of the operation's defined side effects.

The current pointer is a convenience for discovery, not the identity or history of the workstream. It must never be advanced independently of the immutable revision append.

The current draft fixture corpus exercises replay, append, stale-precondition rejection, published successor relationships, and withdrawal relationships at the design-validation layer. It does not yet prove concurrent execution, durable commit behavior, or production transaction isolation. The acceptance suite must add deterministic two-writer race cases demonstrating one winner and one HTTP 409 loser, no partial history/pointer mutation, safe retries, and first-creation collision handling.

**Decision record:** Option A (optimistic compare-and-set) is ratified as the candidate concurrency model. Publication/withdrawal actor scopes, authorization enforcement, audit-resource shape, and the other open decisions remain separate gates. RFC-154 remains an approved candidate design, not a normative released specification.
### 12.8 BrAPI v2.1 authority and target-scale profile (candidate)

The reference and target-value model is based on the official BrAPI v2.1 source contracts, not on GenX-defined copies of BrAPI measurement metadata:

- [ObservationVariable schema](https://github.com/plantbreeding/BrAPI/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/ObservationVariables/Schemas/ObservationVariable.yaml) defines an ObservationVariable as a unique combination of Trait, Method, and Scale.
- [VariableBaseClass schema](https://github.com/plantbreeding/BrAPI/blob/brapi-V2.1/Specification/Components/Schemas/VariableBaseClass.yaml) requires Trait, Method, and Scale and embeds the Scale definition in an ObservationVariable.
- [ScaleBaseClass schema](https://github.com/plantbreeding/BrAPI/blob/brapi-V2.1/Specification/Components/Schemas/ScaleBaseClass.yaml) defines the scale's data type, decimalPlaces, units, and validValues. The v2.1 profile uses minimumValue and maximumValue; the older min and max properties are explicitly deprecated.
- [TraitDataType schema](https://github.com/plantbreeding/BrAPI/blob/brapi-V2.1/Specification/BrAPI-Schema/BrAPI-Common/TraitDataType.json) defines Code, Date, Duration, Nominal, Numerical, Ordinal, and Text.

Candidate semantic constraints:

1. A direction-only breeding objective may refer to a BrAPI Trait or ObservationVariable.
2. A quantitative target must refer to an authority-qualified ObservationVariable, not a Trait-only reference. The referenced ObservationVariable's Scale is the measurement contract.
3. The resolved Scale must have `dataType: Numerical` before a numeric threshold or range is considered semantically valid. A non-numerical Scale must not be coerced into a numeric target.
4. The Scale's `units` is authoritative. GenX must not add a second free-text unit that could conflict with the referenced Scale.
5. Where supplied, `validValues.minimumValue` and `validValues.maximumValue` bound the admissible numeric range. The v2.1 values are strings and should be parsed as decimal quantities, not binary floating-point text.
6. Where supplied, `decimalPlaces` describes the number of decimal places to be reported. Candidate validation should reject a target whose requested precision exceeds an explicitly defined scale precision rather than silently rounding or truncating it. A null or absent decimalPlaces value means that precision is not specified by the Scale; it must not be guessed.
7. If `validValues.categories` is the governing representation, values must be checked against the allowed categories rather than treated as unrestricted numerical values.

These are target-profile constraints, not a new GenX measurement-scale resource. The immutable pipeline revision preserves the authority-qualified ObservationVariable reference; it does not snapshot a conflicting copy of Trait, Method, Scale, or units.

**Open implementation gate:** decide whether registration must synchronously dereference the authority-qualified ObservationVariable and validate against its Scale, or whether unresolved references may be accepted with an explicit unverified state and later validation. Silent fallback, local-server guessing, unit substitution, and implicit rounding are prohibited under either profile. Behavior-level tests must cover stale or unavailable authority servers, wrong resource types, non-numerical scales, configured minimum/maximum values, and configured decimalPlaces.

### 12.9 BrAPI server URI canonicalization profile (candidate)

The `server` component identifies a BrAPI server base URI, including its configured BrAPI base path (for example `/brapi/v2`). It is not a per-resource URL and must not be reconstructed from a host name or an unqualified dbId.

The candidate canonicalization profile follows the syntax-based normalization rules in [RFC 3986 §§6.2.2–6.2.3](https://www.rfc-editor.org/rfc/rfc3986.html):

- Require an absolute hierarchical HTTP or HTTPS URI with an authority and no user information, query, or fragment.
- Lowercase the scheme and DNS host; normalize percent-encoding hex digits to uppercase and decode percent-encoded unreserved characters only.
- Remove dot segments and the default port for the selected scheme. Normalize an empty HTTP(S) path to `/`.
- Preserve path case, reserved percent-encoded octets, and a non-empty trailing slash because these can be part of a deployment's base-path identity. Do not treat `/brapi/v2` and `/brapi/v2/` as equivalent without an explicit deployment rule.
- Do not resolve redirects during identity canonicalization. A redirect target is not silently substituted for the declared authority.

A canonical server identifier is used consistently in reference equality, filter pairing, and cache keys. URI canonicalization is distinct from permission to make a network request to that server. Dereferencing must use an explicit server/authority policy with outbound-request protections; a user-supplied URI must not become an unrestricted server-side fetch target.

The allowed deployment scheme policy (HTTPS-only versus explicitly configured HTTP for private/test servers), internationalized DNS name profile, proxy/redirect policy, DNS rebinding defenses, and authority onboarding/trust model remain gates. RFC 3986 defines generic normalization, but it does not decide which external authorities an implementation trusts or is permitted to contact.

