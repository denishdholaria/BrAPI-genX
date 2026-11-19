# BrAPI-GenX — BreedingPipeline

**Canonical design:** [RFC-154 — Breeding Pipeline](../RFC-154-BreedingPipeline.md)  
**Historical predecessor:** [RFC-014 — Breeding Pipeline (Stage Gates)](../RFC-014-Breeding-Pipeline.md)  
**Maintainer decisions:** [D-BP-01 through D-BP-14](../../../docs/assessment/BRAPI-GENX-BREEDING-PIPELINE-DECISIONS-APPROVED.md)

## Resource boundary

A BreedingPipeline is a stable, goal- and target-oriented workstream associated with one authority-qualified BrAPI Program reference. Its changing configuration is represented by immutable BreedingPipelineRevision records.

BreedingScheme has a distinct logical identity and immutable version identity. In the initial API surface its version definition is embedded in the adopting PipelineRevision; separate Scheme endpoints are deferred. Scheme versions contain stage definitions, directed transitions, and design-time task definitions. They do not represent actual execution.

Actual crosses, germplasm and pedigree, trials, studies, and observations remain owned by official BrAPI resources. SelectionDecision and PopulationAdvancement remain separate GenX execution records and may reference the exact pipeline revision, scheme version, and scheme-local stage when applicable.

## Target-context semantics

A PipelineRevision may include multiple purpose-specific target contexts. A directional-only objective may refer to an authority-qualified BrAPI Trait. A quantitative target must refer to a BrAPI ObservationVariable, because BrAPI v2.1 defines an ObservationVariable as the combination of a Trait, Method and Scale.

The embedded BrAPI Scale is authoritative for measurement units, decimal-place precision, data type and valid values. The GenX target requirement therefore does not repeat a free-text unit property and does not imply unit conversion. A target on another measurement scale uses the corresponding ObservationVariable reference.

Candidate numeric representations are:
- scalar: `threshold` or exact base-10 `exactDecimal`;
- numeric range: inclusive `minimum` and `maximum`;
- exact-decimal range: inclusive `minimumExactDecimal` and `maximumExactDecimal`.

Use a complete lower/upper pair for `target-range`. Do not combine scalar values with ranges or mix JSON number and exact-decimal bound representations. The candidate checker verifies shape and range consistency; validation against the live BrAPI Scale remains an interoperability gate.

## Execution-context semantics

PopulationAdvancement and SelectionDecision carry optional nested contexts rather than loose version/stage identifiers:
- `pipelineContext` identifies the stable pipeline and exact immutable revision;
- `schemeContext` identifies the stable scheme and exact immutable scheme version and contains any stage IDs.

A stage ID is never valid at the event root. When both contexts are present, the exact scheme version must be embedded in the referenced pipeline revision. Events not governed by a registered strategy may omit both contexts.

## Provisional operations

The existing list, register, and retrieve operations remain provisional. Before normative promotion, the contract must define:
- list behavior for logical pipelines versus revisions, including default current-only behavior and an explicit all-revisions mode;
- registration under a stable pipeline ID with a required new immutable version ID for every new revision;
- replay keyed by the immutable version ID;
- exact historical revision retrieval;
- authority-qualified BrAPI reference resolution.

No published revision may be changed in place. A substantive change requires a new version identity.


## Ratified candidate current-revision concurrency profile (D-BP-14)

The draft registration envelope now carries `expectedCurrentBreedingPipelineVersionDbId` separately from the immutable `breedingPipelineVersion` payload. For an existing workstream, a new version must compare the expected pointer with the current published pointer atomically. Explicit null means no published version; omission is reserved for first creation or an identical same-version replay.

The candidate profile is:
- identical version ID plus identical JSON Canonicalization Scheme (JCS, RFC 8785) revision content replays before the current-pointer check;
- the same version ID with different revision content conflicts;
- a new draft is appended without moving the current published pointer;
- a new published revision advances the pointer only when its expected pointer matches and its revision relationship identifies the prior current version;
- a withdrawal appends a new immutable withdrawn revision and clears the pointer only when it identifies the exact current published version;
- a stale or omitted expected pointer on an append returns HTTP 409 Conflict without changing revision history or current state.

**Status:** Option A (optimistic compare-and-set) is ratified as the candidate concurrency model under D-BP-14. The profile remains non-normative pending deterministic concurrent-service and transaction-level conformance. Publish/withdraw authorization and audit requirements remain separate maintainer gates. The fixture checker is not production conformance.

## Deliberate exclusions

This module does not introduce a pipeline-wide current stage, a generic workflow engine, standalone MarketSegment/ProductConcept/TPE APIs, or duplicate BrAPI Program, Cross, Germplasm, Pedigree, Trial, or Study resources.

All operations remain non-normative until the RFC-154 acceptance gates pass.
