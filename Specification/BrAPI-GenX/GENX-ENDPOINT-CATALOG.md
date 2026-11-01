# BrAPI-GenX Endpoint Catalogue (Focused View)

> Generated from the master registry by Scripts/generateEndpointArtifacts.py on 2026-10-22. Do not edit by hand.

This is a focused view of the 21 proposed GenX operations, not a separate source of truth. The complete catalogue covering BrAPI v2.1 and GenX is the [master endpoint catalogue](../ENDPOINT-CATALOG.md); authoritative structured records live in the [master registry](../ENDPOINT-REGISTRY.json). The [BijMantra crosswalk](../BIJMANTRA-CROSSWALK.md) records source-level implementation candidates without implying runtime availability or contract equivalence.

| Source module | Operation count | Status |
|---|---:|---|
| AnalysisMethods | 3 | proposed, non-normative |
| BreedingPipeline | 3 | proposed, non-normative |
| DoubledHaploid | 3 | proposed, non-normative |
| ExperimentalDesign | 3 | proposed, non-normative |
| FAIR | 3 | proposed, non-normative |
| GenebankStorage | 3 | proposed, non-normative |
| GenomicDatasets | 3 | proposed, non-normative |
| Genomics | 3 | proposed, non-normative |
| HarvestRecords | 3 | proposed, non-normative |
| Jobs | 4 | proposed, non-normative |
| LotLedger | 2 | proposed, non-normative |
| MeasurementMethods | 3 | proposed, non-normative |
| Models | 3 | proposed, non-normative |
| PhenotypeCapture | 3 | proposed, non-normative |
| ProgenyRecords | 3 | proposed, non-normative |
| ResearchAssets | 3 | proposed, non-normative |
| SelectionDecisions | 3 | proposed, non-normative |
| ServerInfoV3 | 1 | proposed, non-normative |
| Telemetry | 2 | proposed, non-normative |
| VariableTerms | 3 | proposed, non-normative |
| WeatherObservations | 3 | proposed, non-normative |

## Operations

### AnalysisMethods — 3 operations

### GET `/genx/v1/analysis-methods`

- **Catalogue ID:** `brapi-genx.genx.v1.analysis-methods.list`
- **BrAPI-GenX operation identity:** `genxListAnalysisMethods` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListAnalysisMethods`
- **GenX source module:** `AnalysisMethods`
- **Source tag:** AnalysisMethods
- **Proposed BrAPI-GenX classification:** D7 — Scientific Analysis, Models and Derived Evidence; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> List registered analysis method versions and their lifecycle states.
**Source contract description:**
> Get a paged list of analysis method versions across authorities. Filters combine with AND.
**Can be used for:**
- Discover registered analysis methods and versions.
- Select a method version subject to lifecycle status and advertised support.
**Must not be used for / explicit non-goals:**
- Executing an analysis (use GenX Jobs).
- Assuming registration means scientific validation, approval, or endorsement.
- Assuming metrics or results from different methods are directly comparable.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** analysisMethodDbId, methodType, status, page, pageSize, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxRegisterAnalysisMethod, genxGetAnalysisMethod, genxSubmitAsyncJob
- **Related catalogue IDs:** brapi-genx.genx.v1.analysis-methods.register, brapi-genx.genx.v1.analysis-methods.get
- **Relevant RFC / decision references:** RFC-009
- **Contract source:** [`Specification/BrAPI-GenX/AnalysisMethods/AnalysisMethods_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/AnalysisMethods/AnalysisMethods_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/genx/v1/analysis-methods`

- **Catalogue ID:** `brapi-genx.genx.v1.analysis-methods.register`
- **BrAPI-GenX operation identity:** `genxRegisterAnalysisMethod` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxRegisterAnalysisMethod`
- **GenX source module:** `AnalysisMethods`
- **Source tag:** AnalysisMethods
- **Proposed BrAPI-GenX classification:** D7 — Scientific Analysis, Models and Derived Evidence; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Register an analysis method version with identity, version, type, input/output contracts, and lifecycle state.
**Source contract description:**
> Unknown analysisMethodDbId creates; known id with a new version appends; same (analysisMethodDbId, methodVersion) with an identical body replays the existing record; same pair with a different body is rejected with 409.
**Can be used for:**
- Publish method metadata and integrity references.
- Create a new version under an existing method identity.
- Record deprecation or revocation status as governed elsewhere.
**Must not be used for / explicit non-goals:**
- Executing an analysis.
- Assuming registration means scientific validation, approval, or endorsement.
- Assuming methods with similar types are interchangeable.
- **Side effects:** Creates a method identity or appends a new immutable version when accepted.
- **Retry / idempotency:** Same method identity/version and identical body replays; conflicting content for the same version is rejected.
- **Parameters recorded in registry:** authorizationHeader
- **Request schema refs recorded:** AnalysisMethodNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxListAnalysisMethods, genxGetAnalysisMethod, genxSubmitAsyncJob
- **Related catalogue IDs:** brapi-genx.genx.v1.analysis-methods.list, brapi-genx.genx.v1.analysis-methods.get
- **Relevant RFC / decision references:** RFC-009
- **Contract source:** [`Specification/BrAPI-GenX/AnalysisMethods/AnalysisMethods_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/AnalysisMethods/AnalysisMethods_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/genx/v1/analysis-methods/{analysisMethodDbId}`

- **Catalogue ID:** `brapi-genx.genx.v1.analysis-methods.get`
- **BrAPI-GenX operation identity:** `genxGetAnalysisMethod` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetAnalysisMethod`
- **GenX source module:** `AnalysisMethods`
- **Source tag:** AnalysisMethods
- **Proposed BrAPI-GenX classification:** D7 — Scientific Analysis, Models and Derived Evidence; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Retrieve one registered analysis method version.
**Source contract description:**
> Returns the requested version, or the most recently created version when `version` is omitted.
**Can be used for:**
- Inspect method identity, version, type, contracts, and lifecycle status before selecting an analysis.
**Must not be used for / explicit non-goals:**
- Executing an analysis.
- Assuming method metadata alone proves scientific fitness for a particular task.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** analysisMethodDbId, version, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** genxRegisterAnalysisMethod, genxListAnalysisMethods, genxSubmitAsyncJob
- **Related catalogue IDs:** brapi-genx.genx.v1.analysis-methods.list, brapi-genx.genx.v1.analysis-methods.register
- **Relevant RFC / decision references:** RFC-009
- **Contract source:** [`Specification/BrAPI-GenX/AnalysisMethods/AnalysisMethods_AnalysisMethodDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/AnalysisMethods/AnalysisMethods_AnalysisMethodDbId_GET.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### BreedingPipeline — 3 operations

### GET `/genx/v1/breeding-pipelines`

- **Catalogue ID:** `brapi-genx.genx.v1.breeding-pipelines.list`
- **BrAPI-GenX operation identity:** `genxListBreedingPipelines` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListBreedingPipelines`
- **GenX source module:** `BreedingPipeline`
- **Source tag:** BreedingPipeline
- **Proposed BrAPI-GenX classification:** D2 — Breeding Programs and Experimental Design; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> List breeding pipeline definitions, optionally filtered by program or status.
**Source contract description:**
> Get a paged list of breeding pipelines across authorities. Filters combine with AND.
**Can be used for:**
- Discover breeding pipelines and their stage gates.
- Support breeding program planning and auditing.
**Must not be used for / explicit non-goals:**
- Creating or changing a pipeline (use the POST endpoint).
- Assuming a pipeline is a BrAPI Program or Study.
- Treating the list as a complete breeding program record.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** programDbId, status, page, pageSize, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxRegisterBreedingPipeline, genxGetBreedingPipeline
- **Related catalogue IDs:** brapi-genx.genx.v1.breeding-pipelines.register, brapi-genx.genx.v1.breeding-pipelines.get
- **Relevant RFC / decision references:** RFC-014
- **Contract source:** [`Specification/BrAPI-GenX/BreedingPipeline/BreedingPipeline_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/BreedingPipeline/BreedingPipeline_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/genx/v1/breeding-pipelines`

- **Catalogue ID:** `brapi-genx.genx.v1.breeding-pipelines.register`
- **BrAPI-GenX operation identity:** `genxRegisterBreedingPipeline` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxRegisterBreedingPipeline`
- **GenX source module:** `BreedingPipeline`
- **Source tag:** BreedingPipeline
- **Proposed BrAPI-GenX classification:** D2 — Breeding Programs and Experimental Design; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Register a breeding pipeline with stages, entry/exit criteria, and provenance.
**Source contract description:**
> Unknown breedingPipelineDbId creates; same id with an identical body replays the existing record; same id with a different body is rejected with 409.
**Can be used for:**
- Publish pipeline stage-gate definitions.
- Create a new version under an existing pipeline identity.
**Must not be used for / explicit non-goals:**
- Updating or deleting an existing pipeline; corrections require a new record that supersedes.
- Assuming the pipeline is a BrAPI Program or Study.
- Treating the pipeline as an approved breeding plan.
- **Side effects:** Creates a pipeline identity or appends a new immutable version when accepted.
- **Retry / idempotency:** Same pipeline identity and identical body replays; conflicting content for the same identity is rejected.
- **Parameters recorded in registry:** authorizationHeader
- **Request schema refs recorded:** BreedingPipelineNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxListBreedingPipelines, genxGetBreedingPipeline
- **Related catalogue IDs:** brapi-genx.genx.v1.breeding-pipelines.list, brapi-genx.genx.v1.breeding-pipelines.get
- **Relevant RFC / decision references:** RFC-014
- **Contract source:** [`Specification/BrAPI-GenX/BreedingPipeline/BreedingPipeline_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/BreedingPipeline/BreedingPipeline_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/genx/v1/breeding-pipelines/{breedingPipelineDbId}`

- **Catalogue ID:** `brapi-genx.genx.v1.breeding-pipelines.get`
- **BrAPI-GenX operation identity:** `genxGetBreedingPipeline` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetBreedingPipeline`
- **GenX source module:** `BreedingPipeline`
- **Source tag:** BreedingPipeline
- **Proposed BrAPI-GenX classification:** D2 — Breeding Programs and Experimental Design; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Retrieve one registered breeding pipeline.
**Source contract description:**
> Returns the registered pipeline, or 404.
**Can be used for:**
- Inspect pipeline stages, criteria, and provenance.
**Must not be used for / explicit non-goals:**
- Assuming the pipeline is a BrAPI Program or Study.
- Treating a superseded pipeline as current.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** breedingPipelineDbId, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** genxRegisterBreedingPipeline, genxListBreedingPipelines
- **Related catalogue IDs:** brapi-genx.genx.v1.breeding-pipelines.list, brapi-genx.genx.v1.breeding-pipelines.register
- **Relevant RFC / decision references:** RFC-014
- **Contract source:** [`Specification/BrAPI-GenX/BreedingPipeline/BreedingPipeline_BreedingPipelineDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/BreedingPipeline/BreedingPipeline_BreedingPipelineDbId_GET.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### DoubledHaploid — 3 operations

### GET `/genx/v1/doubled-haploid-programs`

- **Catalogue ID:** `brapi-genx.genx.v1.doubled-haploid-programs.list`
- **BrAPI-GenX operation identity:** `genxListDoubledHaploidPrograms` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListDoubledHaploidPrograms`
- **GenX source module:** `DoubledHaploid`
- **Source tag:** DoubledHaploid
- **Proposed BrAPI-GenX classification:** D2 — Breeding Programs and Experimental Design; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> List doubled haploid programs, optionally filtered by program or status.
**Source contract description:**
> Get a paged list of doubled haploid programs across authorities. Filters combine with AND.
**Can be used for:**
- Discover doubled haploid programs and their counts.
- Support breeding program planning and auditing.
**Must not be used for / explicit non-goals:**
- Creating or changing a program (use the POST endpoint).
- Assuming a program is a BrAPI Program.
- Treating the list as a complete breeding program record.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** programDbId, status, page, pageSize, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxRegisterDoubledHaploidProgram, genxGetDoubledHaploidProgram
- **Related catalogue IDs:** brapi-genx.genx.v1.doubled-haploid-programs.register, brapi-genx.genx.v1.doubled-haploid-programs.get
- **Relevant RFC / decision references:** RFC-020
- **Contract source:** [`Specification/BrAPI-GenX/DoubledHaploid/DoubledHaploid_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/DoubledHaploid/DoubledHaploid_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/genx/v1/doubled-haploid-programs`

- **Catalogue ID:** `brapi-genx.genx.v1.doubled-haploid-programs.register`
- **BrAPI-GenX operation identity:** `genxRegisterDoubledHaploidProgram` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxRegisterDoubledHaploidProgram`
- **GenX source module:** `DoubledHaploid`
- **Source tag:** DoubledHaploid
- **Proposed BrAPI-GenX classification:** D2 — Breeding Programs and Experimental Design; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Register a doubled haploid program with method, donor, counts, and provenance.
**Source contract description:**
> Unknown doubledHaploidProgramDbId creates; same id with an identical body replays the existing record; same id with a different body is rejected with 409.
**Can be used for:**
- Publish doubled haploid program metadata.
- Create a new version under an existing program identity.
**Must not be used for / explicit non-goals:**
- Updating or deleting an existing program; corrections require a new record that supersedes.
- Assuming the program is a BrAPI Program.
- Treating the program as an approved breeding plan.
- **Side effects:** Creates a program identity or appends a new immutable version when accepted.
- **Retry / idempotency:** Same program identity and identical body replays; conflicting content for the same identity is rejected.
- **Parameters recorded in registry:** authorizationHeader
- **Request schema refs recorded:** DoubledHaploidProgramNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxListDoubledHaploidPrograms, genxGetDoubledHaploidProgram
- **Related catalogue IDs:** brapi-genx.genx.v1.doubled-haploid-programs.list, brapi-genx.genx.v1.doubled-haploid-programs.get
- **Relevant RFC / decision references:** RFC-020
- **Contract source:** [`Specification/BrAPI-GenX/DoubledHaploid/DoubledHaploid_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/DoubledHaploid/DoubledHaploid_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/genx/v1/doubled-haploid-programs/{doubledHaploidProgramDbId}`

- **Catalogue ID:** `brapi-genx.genx.v1.doubled-haploid-programs.get`
- **BrAPI-GenX operation identity:** `genxGetDoubledHaploidProgram` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetDoubledHaploidProgram`
- **GenX source module:** `DoubledHaploid`
- **Source tag:** DoubledHaploid
- **Proposed BrAPI-GenX classification:** D2 — Breeding Programs and Experimental Design; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Retrieve one doubled haploid program.
**Source contract description:**
> Returns the registered program, or 404.
**Can be used for:**
- Inspect method, donor, counts, and provenance.
**Must not be used for / explicit non-goals:**
- Assuming the program is a BrAPI Program.
- Treating a superseded program as current.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** doubledHaploidProgramDbId, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** genxRegisterDoubledHaploidProgram, genxListDoubledHaploidPrograms
- **Related catalogue IDs:** brapi-genx.genx.v1.doubled-haploid-programs.list, brapi-genx.genx.v1.doubled-haploid-programs.register
- **Relevant RFC / decision references:** RFC-020
- **Contract source:** [`Specification/BrAPI-GenX/DoubledHaploid/DoubledHaploid_DoubledHaploidProgramDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/DoubledHaploid/DoubledHaploid_DoubledHaploidProgramDbId_GET.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### ExperimentalDesign — 3 operations

### GET `/genx/v1/experimental-designs`

- **Catalogue ID:** `brapi-genx.genx.v1.experimental-designs.list`
- **BrAPI-GenX operation identity:** `genxListExperimentalDesigns` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListExperimentalDesigns`
- **GenX source module:** `ExperimentalDesign`
- **Source tag:** ExperimentalDesign
- **Proposed BrAPI-GenX classification:** D2 — Breeding Programs and Experimental Design; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> List experimental design records, optionally filtered by study or design type.
**Source contract description:**
> Get a paged list of experimental designs across authorities. Filters combine with AND.
**Can be used for:**
- Discover trial layouts, replication, and randomization.
- Support experimental planning and auditing.
**Must not be used for / explicit non-goals:**
- Creating or changing a design (use the POST endpoint).
- Assuming a design is a BrAPI Study or Observation Unit.
- Treating the list as a complete trial record.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** studyDbId, designType, page, pageSize, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxRegisterExperimentalDesign, genxGetExperimentalDesign
- **Related catalogue IDs:** brapi-genx.genx.v1.experimental-designs.register, brapi-genx.genx.v1.experimental-designs.get
- **Relevant RFC / decision references:** RFC-018
- **Contract source:** [`Specification/BrAPI-GenX/ExperimentalDesign/ExperimentalDesign_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/ExperimentalDesign/ExperimentalDesign_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/genx/v1/experimental-designs`

- **Catalogue ID:** `brapi-genx.genx.v1.experimental-designs.register`
- **BrAPI-GenX operation identity:** `genxRegisterExperimentalDesign` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxRegisterExperimentalDesign`
- **GenX source module:** `ExperimentalDesign`
- **Source tag:** ExperimentalDesign
- **Proposed BrAPI-GenX classification:** D2 — Breeding Programs and Experimental Design; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Register an experimental design with layout, replication, randomization, and provenance.
**Source contract description:**
> Unknown experimentalDesignDbId creates; same id with an identical body replays the existing record; same id with a different body is rejected with 409.
**Can be used for:**
- Publish trial layout and treatment assignment.
- Create a new version under an existing design identity.
**Must not be used for / explicit non-goals:**
- Updating or deleting an existing design; corrections require a new record that supersedes.
- Assuming the design is a BrAPI Study.
- Treating the design as an approved protocol.
- **Side effects:** Creates a design identity or appends a new immutable version when accepted.
- **Retry / idempotency:** Same design identity and identical body replays; conflicting content for the same identity is rejected.
- **Parameters recorded in registry:** authorizationHeader
- **Request schema refs recorded:** ExperimentalDesignNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxListExperimentalDesigns, genxGetExperimentalDesign
- **Related catalogue IDs:** brapi-genx.genx.v1.experimental-designs.list, brapi-genx.genx.v1.experimental-designs.get
- **Relevant RFC / decision references:** RFC-018
- **Contract source:** [`Specification/BrAPI-GenX/ExperimentalDesign/ExperimentalDesign_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/ExperimentalDesign/ExperimentalDesign_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/genx/v1/experimental-designs/{experimentalDesignDbId}`

- **Catalogue ID:** `brapi-genx.genx.v1.experimental-designs.get`
- **BrAPI-GenX operation identity:** `genxGetExperimentalDesign` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetExperimentalDesign`
- **GenX source module:** `ExperimentalDesign`
- **Source tag:** ExperimentalDesign
- **Proposed BrAPI-GenX classification:** D2 — Breeding Programs and Experimental Design; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Retrieve one registered experimental design.
**Source contract description:**
> Returns the registered design, or 404.
**Can be used for:**
- Inspect design type, replication, randomization, and provenance.
**Must not be used for / explicit non-goals:**
- Assuming the design is a BrAPI Study.
- Treating a superseded design as current.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** experimentalDesignDbId, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** genxRegisterExperimentalDesign, genxListExperimentalDesigns
- **Related catalogue IDs:** brapi-genx.genx.v1.experimental-designs.list, brapi-genx.genx.v1.experimental-designs.register
- **Relevant RFC / decision references:** RFC-018
- **Contract source:** [`Specification/BrAPI-GenX/ExperimentalDesign/ExperimentalDesign_ExperimentalDesignDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/ExperimentalDesign/ExperimentalDesign_ExperimentalDesignDbId_GET.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### FAIR — 3 operations

### GET `/genx/v1/fair-packages`

- **Catalogue ID:** `brapi-genx.genx.v1.fair-packages.list-metadata`
- **BrAPI-GenX operation identity:** `genxListFairPackageMetadata` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListFairPackageMetadata`
- **GenX source module:** `FAIR`
- **Source tag:** FAIR Packages
- **Proposed BrAPI-GenX classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C5 — Data exchange, publication and access, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> List FAIR package metadata with optional access-rights and license filters; the endpoint does not serve payload bytes.
**Source contract description:**
> Get a paged list of package metadata across authorities. Filters combine with AND. Payload bytes are never served here.
**Can be used for:**
- Discover package citation, licensing, access-rights, embargo, and payload-reference metadata.
- Find packages by supported metadata filters.
**Must not be used for / explicit non-goals:**
- Downloading payload bytes or assuming the package service stores them.
- Minting Digital Object Identifiers (DOIs) or approving restricted-access requests.
- Assuming all embargo policies or metadata-visibility rules have been finalized.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** accessRights, license
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** FAIRPackageListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-05
- **Related catalogue IDs:** brapi-genx.genx.v1.fair-packages.get-metadata, brapi-genx.genx.v1.fair-packages.register
- **Relevant RFC / decision references:** RFC-006, D-13, D-14, D-15
- **Contract source:** [`Specification/BrAPI-GenX/FAIR/FairPackages_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/FAIR/FairPackages_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/genx/v1/fair-packages`

- **Catalogue ID:** `brapi-genx.genx.v1.fair-packages.register`
- **BrAPI-GenX operation identity:** `genxRegisterFairPackage` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxRegisterFairPackage`
- **GenX source module:** `FAIR`
- **Source tag:** FAIR Packages
- **Proposed BrAPI-GenX classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C5 — Data exchange, publication and access, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Register an identified, licensed, access-controlled package envelope that binds one or more payload references into a citable metadata record.
**Source contract description:**
> Unknown packageDbId creates; known id with an identical body replays
> the existing record; known id with a different body is rejected with
> 409.
**Can be used for:**
- Record a package title, identifiers, license, access rights, embargo, creators, and payload references.
- Publish a stable metadata envelope around data owned by another service.
**Must not be used for / explicit non-goals:**
- Uploading or storing the payload bytes.
- Minting persistent identifiers or running license negotiation.
- Implementing restricted-access approval workflows.
- **Side effects:** Creates package metadata if accepted.
- **Retry / idempotency:** Identical registration replays; conflicting content under the same package identity is rejected.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** FAIRPackageNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-05
- **Related catalogue IDs:** brapi-genx.genx.v1.fair-packages.get-metadata, brapi-genx.genx.v1.fair-packages.list-metadata
- **Relevant RFC / decision references:** RFC-006, D-13, D-14, D-15
- **Contract source:** [`Specification/BrAPI-GenX/FAIR/FairPackages_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/FAIR/FairPackages_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/genx/v1/fair-packages/{packageDbId}`

- **Catalogue ID:** `brapi-genx.genx.v1.fair-packages.get-metadata`
- **BrAPI-GenX operation identity:** `genxGetFairPackageMetadata` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetFairPackageMetadata`
- **GenX source module:** `FAIR`
- **Source tag:** FAIR Packages
- **Proposed BrAPI-GenX classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C5 — Data exchange, publication and access, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Retrieve the metadata envelope for one FAIR package subject to the currently specified embargo gate.
**Source contract description:**
> Returns the package metadata, or 404. While payloads are embargoed (embargoUntil in the future) the record is denied with 403 to prove the gate exists; the gentler metadata-visible alternative is requires-decision (see RFC-006 §5).
**Can be used for:**
- Read package metadata when the access contract permits the request.
**Must not be used for / explicit non-goals:**
- Retrieving payload bytes.
- Assuming embargoed metadata remains visible: the current reference behavior denies the whole record with 403, while the preferred metadata-visible policy remains unresolved.
- Treating this endpoint as an access-request approval workflow.
- **Side effects:** Read-only; may deny the record while its payload is embargoed under the current proposal behavior.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** packageDbId
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-05
- **Related catalogue IDs:** brapi-genx.genx.v1.fair-packages.list-metadata, brapi-genx.genx.v1.fair-packages.register
- **Relevant RFC / decision references:** RFC-006, D-15
- **Contract source:** [`Specification/BrAPI-GenX/FAIR/FairPackages_PackageDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/FAIR/FairPackages_PackageDbId_GET.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GenebankStorage — 3 operations

### GET `/genx/v1/genebank-storage`

- **Catalogue ID:** `brapi-genx.genx.v1.genebank-storage.list`
- **BrAPI-GenX operation identity:** `genxListStorageLocations` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListStorageLocations`
- **GenX source module:** `GenebankStorage`
- **Source tag:** GenebankStorage
- **Proposed BrAPI-GenX classification:** D1 — Germplasm and Biological Resources; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> List genebank storage locations, optionally filtered by facility, vault, or status.
**Source contract description:**
> Get a paged list of genebank storage locations across authorities. Filters combine with AND.
**Can be used for:**
- Discover storage locations and their capacity.
- Support conservation planning and auditing.
**Must not be used for / explicit non-goals:**
- Creating or changing a location (use the POST endpoint).
- Assuming a location implies a BrAPI SeedLot transaction.
- Treating the list as a complete conservation record.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** facilityName, vaultName, status, page, pageSize, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxRegisterStorageLocation, genxGetStorageLocation
- **Related catalogue IDs:** brapi-genx.genx.v1.genebank-storage.register, brapi-genx.genx.v1.genebank-storage.get
- **Relevant RFC / decision references:** RFC-015
- **Contract source:** [`Specification/BrAPI-GenX/GenebankStorage/GenebankStorage_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/GenebankStorage/GenebankStorage_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/genx/v1/genebank-storage`

- **Catalogue ID:** `brapi-genx.genx.v1.genebank-storage.register`
- **BrAPI-GenX operation identity:** `genxRegisterStorageLocation` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxRegisterStorageLocation`
- **GenX source module:** `GenebankStorage`
- **Source tag:** GenebankStorage
- **Proposed BrAPI-GenX classification:** D1 — Germplasm and Biological Resources; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Register a genebank storage location with capacity, environment, and provenance.
**Source contract description:**
> Unknown storageLocationDbId creates; same id with an identical body replays the existing record; same id with a different body is rejected with 409.
**Can be used for:**
- Publish storage location metadata.
- Create a new version under an existing location identity.
**Must not be used for / explicit non-goals:**
- Updating or deleting an existing location; corrections require a new record that supersedes.
- Assuming the location is a BrAPI SeedLot.
- Treating the location as a complete conservation record.
- **Side effects:** Creates a storage location identity or appends a new immutable version when accepted.
- **Retry / idempotency:** Same location identity and identical body replays; conflicting content for the same identity is rejected.
- **Parameters recorded in registry:** authorizationHeader
- **Request schema refs recorded:** StorageLocationNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxListStorageLocations, genxGetStorageLocation
- **Related catalogue IDs:** brapi-genx.genx.v1.genebank-storage.list, brapi-genx.genx.v1.genebank-storage.get
- **Relevant RFC / decision references:** RFC-015
- **Contract source:** [`Specification/BrAPI-GenX/GenebankStorage/GenebankStorage_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/GenebankStorage/GenebankStorage_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/genx/v1/genebank-storage/{storageLocationDbId}`

- **Catalogue ID:** `brapi-genx.genx.v1.genebank-storage.get`
- **BrAPI-GenX operation identity:** `genxGetStorageLocation` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetStorageLocation`
- **GenX source module:** `GenebankStorage`
- **Source tag:** GenebankStorage
- **Proposed BrAPI-GenX classification:** D1 — Germplasm and Biological Resources; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Retrieve one genebank storage location.
**Source contract description:**
> Returns the registered location, or 404.
**Can be used for:**
- Inspect storage capacity, environment, and provenance.
**Must not be used for / explicit non-goals:**
- Assuming the location is a BrAPI SeedLot.
- Treating a decommissioned location as active.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** storageLocationDbId, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** genxRegisterStorageLocation, genxListStorageLocations
- **Related catalogue IDs:** brapi-genx.genx.v1.genebank-storage.list, brapi-genx.genx.v1.genebank-storage.register
- **Relevant RFC / decision references:** RFC-015
- **Contract source:** [`Specification/BrAPI-GenX/GenebankStorage/GenebankStorage_StorageLocationDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/GenebankStorage/GenebankStorage_StorageLocationDbId_GET.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GenomicDatasets — 3 operations

### GET `/genx/v1/genomic-datasets`

- **Catalogue ID:** `brapi-genx.genx.v1.genomic-datasets.list`
- **BrAPI-GenX operation identity:** `genxListGenomicDatasets` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListGenomicDatasets`
- **GenX source module:** `GenomicDatasets`
- **Source tag:** GenomicDatasets
- **Proposed BrAPI-GenX classification:** D3 — Genotyping and Molecular Genomics; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C5 — Data exchange, publication and access, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> List prepared genomic datasets, optionally filtered by type, reference assembly, or release status.
**Source contract description:**
> Get a paged list of genomic datasets across authorities. Filters combine with AND.
**Can be used for:**
- Discover genomic datasets and their provenance.
- Select a dataset subject to access policy and release status.
**Must not be used for / explicit non-goals:**
- Creating or changing a dataset (use the POST endpoint).
- Assuming a dataset is a BrAPI VariantSet or VariantMatrix.
- Treating the list as a complete genomic repository.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** genomicDatasetDbId, datasetType, referenceAssembly, releaseStatus, page, pageSize, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxRegisterGenomicDataset, genxGetGenomicDataset, genxRegisterVariantMatrixReference
- **Related catalogue IDs:** brapi-genx.genx.v1.genomic-datasets.register, brapi-genx.genx.v1.genomic-datasets.get
- **Relevant RFC / decision references:** RFC-013
- **Contract source:** [`Specification/BrAPI-GenX/GenomicDatasets/GenomicDatasets_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/GenomicDatasets/GenomicDatasets_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/genx/v1/genomic-datasets`

- **Catalogue ID:** `brapi-genx.genx.v1.genomic-datasets.register`
- **BrAPI-GenX operation identity:** `genxRegisterGenomicDataset` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxRegisterGenomicDataset`
- **GenX source module:** `GenomicDatasets`
- **Source tag:** GenomicDatasets
- **Proposed BrAPI-GenX classification:** D3 — Genotyping and Molecular Genomics; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C5 — Data exchange, publication and access, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Register a prepared genomic dataset with reference assembly, pipeline provenance, and access policy.
**Source contract description:**
> Unknown genomicDatasetDbId creates; same id with an identical body replays the existing record; same id with a different body is rejected with 409.
**Can be used for:**
- Publish dataset metadata and integrity references.
- Create a new version under an existing dataset identity.
- Record release or withdrawal status as governed elsewhere.
**Must not be used for / explicit non-goals:**
- Uploading dataset bytes through this endpoint.
- Assuming registration means scientific validation or approval.
- Treating the dataset as a BrAPI VariantSet or VariantMatrix.
- **Side effects:** Creates a dataset identity or appends a new immutable version when accepted.
- **Retry / idempotency:** Same dataset identity/version and identical body replays; conflicting content for the same identity is rejected.
- **Parameters recorded in registry:** authorizationHeader
- **Request schema refs recorded:** GenomicDatasetNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxListGenomicDatasets, genxGetGenomicDataset, genxRegisterVariantMatrixReference
- **Related catalogue IDs:** brapi-genx.genx.v1.genomic-datasets.list, brapi-genx.genx.v1.genomic-datasets.get
- **Relevant RFC / decision references:** RFC-013
- **Contract source:** [`Specification/BrAPI-GenX/GenomicDatasets/GenomicDatasets_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/GenomicDatasets/GenomicDatasets_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/genx/v1/genomic-datasets/{genomicDatasetDbId}`

- **Catalogue ID:** `brapi-genx.genx.v1.genomic-datasets.get`
- **BrAPI-GenX operation identity:** `genxGetGenomicDataset` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetGenomicDataset`
- **GenX source module:** `GenomicDatasets`
- **Source tag:** GenomicDatasets
- **Proposed BrAPI-GenX classification:** D3 — Genotyping and Molecular Genomics; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C5 — Data exchange, publication and access, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Retrieve one registered genomic dataset.
**Source contract description:**
> Returns the registered dataset, or 404.
**Can be used for:**
- Inspect dataset identity, reference assembly, pipeline provenance, and access policy.
**Must not be used for / explicit non-goals:**
- Assuming the dataset is a BrAPI VariantSet or VariantMatrix.
- Treating a withdrawn dataset as current.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** genomicDatasetDbId, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** genxRegisterGenomicDataset, genxListGenomicDatasets, genxRegisterVariantMatrixReference
- **Related catalogue IDs:** brapi-genx.genx.v1.genomic-datasets.list, brapi-genx.genx.v1.genomic-datasets.register
- **Relevant RFC / decision references:** RFC-013
- **Contract source:** [`Specification/BrAPI-GenX/GenomicDatasets/GenomicDatasets_GenomicDatasetDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/GenomicDatasets/GenomicDatasets_GenomicDatasetDbId_GET.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### Genomics — 3 operations

### GET `/genx/v1/variantmatrices`

- **Catalogue ID:** `brapi-genx.genx.v1.variant-matrices.list`
- **BrAPI-GenX operation identity:** `genxListVariantMatrixReferences` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListVariantMatrixReferences`
- **GenX source module:** `Genomics`
- **Source tag:** Variant Matrices
- **Proposed BrAPI-GenX classification:** D3 — Genotyping and Molecular Genomics; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C5 — Data exchange, publication and access, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> List registered references to external variant matrices, optionally filtered by VariantSet identity and format.
**Source contract description:**
> Get a paged list of matrix references across authorities. Filters combine with AND.
**Can be used for:**
- Discover matrix metadata, file digests, counts, formats, and retrieval service references.
- Plan external retrieval or subsetting through the declared retrieval service.
**Must not be used for / explicit non-goals:**
- Expecting genotype matrix bytes in the response.
- Treating VariantMatrix as an alias for VariantSet, CallSet, or Calls.
- Assuming the endpoint itself implements matrix slicing or access control for external bytes.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** variantSetDbId, format
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** VariantMatrixListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-04
- **Related catalogue IDs:** brapi-genx.brapi-v2-1.genotyping.get.allelematrix, brapi-genx.brapi-v2-1.genotyping.get.calls, brapi-genx.brapi-v2-1.genotyping.get.callsets, brapi-genx.brapi-v2-1.genotyping.get.callsets.by-callsetdbid, brapi-genx.brapi-v2-1.genotyping.get.callsets.by-callsetdbid.calls, brapi-genx.brapi-v2-1.genotyping.get.variants, brapi-genx.brapi-v2-1.genotyping.get.variants.by-variantdbid, brapi-genx.brapi-v2-1.genotyping.get.variants.by-variantdbid.calls, brapi-genx.brapi-v2-1.genotyping.get.variantsets, brapi-genx.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid, brapi-genx.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.calls, brapi-genx.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.callsets, brapi-genx.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.variants, brapi-genx.brapi-v2-1.genotyping.post.variantsets.extract, brapi-genx.brapi-v2-1.genotyping.put.calls, brapi-genx.genx.v1.variant-matrices.get, brapi-genx.genx.v1.variant-matrices.register
- **Relevant RFC / decision references:** RFC-005, D-11, D-12, D-19
- **Contract source:** [`Specification/BrAPI-GenX/Genomics/VariantMatrices_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Genomics/VariantMatrices_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/genx/v1/variantmatrices`

- **Catalogue ID:** `brapi-genx.genx.v1.variant-matrices.register`
- **BrAPI-GenX operation identity:** `genxRegisterVariantMatrixReference` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxRegisterVariantMatrixReference`
- **GenX source module:** `Genomics`
- **Source tag:** Variant Matrices
- **Proposed BrAPI-GenX classification:** D3 — Genotyping and Molecular Genomics; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C5 — Data exchange, publication and access, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Register a content-addressed reference to an externally stored genomic variant matrix, including format, location, digest, and optional dimensions and retrieval-service metadata.
**Source contract description:**
> Unknown matrixDbId creates; known id with an identical body replays
> the existing record; known id with different bytes is rejected with
> 409. New bytes get a new id.
**Can be used for:**
- Publish a resolvable reference to VCF, BCF, VCF Zarr, PLINK, or another declared matrix format.
- Bind a matrix identity to immutable content metadata.
**Must not be used for / explicit non-goals:**
- Uploading or returning matrix bytes through this endpoint.
- Replacing V2.1 variant/call resources or claiming drop-in equivalence.
- Assuming a custom matrix slicing protocol or access-authorization scheme is defined here.
- **Side effects:** Creates a matrix reference if accepted.
- **Retry / idempotency:** Identical registration replays; a different body under the same matrix identity is rejected; changed bytes require a new identity.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** VariantMatrixNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-04
- **Related catalogue IDs:** brapi-genx.brapi-v2-1.genotyping.get.allelematrix, brapi-genx.brapi-v2-1.genotyping.get.calls, brapi-genx.brapi-v2-1.genotyping.get.callsets, brapi-genx.brapi-v2-1.genotyping.get.callsets.by-callsetdbid, brapi-genx.brapi-v2-1.genotyping.get.callsets.by-callsetdbid.calls, brapi-genx.brapi-v2-1.genotyping.get.variants, brapi-genx.brapi-v2-1.genotyping.get.variants.by-variantdbid, brapi-genx.brapi-v2-1.genotyping.get.variants.by-variantdbid.calls, brapi-genx.brapi-v2-1.genotyping.get.variantsets, brapi-genx.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid, brapi-genx.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.calls, brapi-genx.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.callsets, brapi-genx.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.variants, brapi-genx.brapi-v2-1.genotyping.post.variantsets.extract, brapi-genx.brapi-v2-1.genotyping.put.calls, brapi-genx.genx.v1.variant-matrices.get, brapi-genx.genx.v1.variant-matrices.list
- **Relevant RFC / decision references:** RFC-005, D-11, D-12, D-19
- **Contract source:** [`Specification/BrAPI-GenX/Genomics/VariantMatrices_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Genomics/VariantMatrices_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/genx/v1/variantmatrices/{matrixDbId}`

- **Catalogue ID:** `brapi-genx.genx.v1.variant-matrices.get`
- **BrAPI-GenX operation identity:** `genxGetVariantMatrixReference` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetVariantMatrixReference`
- **GenX source module:** `Genomics`
- **Source tag:** Variant Matrices
- **Proposed BrAPI-GenX classification:** D3 — Genotyping and Molecular Genomics; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C5 — Data exchange, publication and access, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Retrieve one registered variant-matrix reference and its integrity and retrieval metadata.
**Source contract description:**
> Returns the registered record, or 404. Bytes are retrieved out of band via fileURL or accessService.
**Can be used for:**
- Resolve the metadata needed to retrieve and verify external matrix bytes.
**Must not be used for / explicit non-goals:**
- Expecting the matrix file or selected variants to be streamed in the response.
- Treating the matrix reference as a VariantSet or CallSet.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** matrixDbId
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-04
- **Related catalogue IDs:** brapi-genx.brapi-v2-1.genotyping.get.allelematrix, brapi-genx.brapi-v2-1.genotyping.get.calls, brapi-genx.brapi-v2-1.genotyping.get.callsets, brapi-genx.brapi-v2-1.genotyping.get.callsets.by-callsetdbid, brapi-genx.brapi-v2-1.genotyping.get.callsets.by-callsetdbid.calls, brapi-genx.brapi-v2-1.genotyping.get.variants, brapi-genx.brapi-v2-1.genotyping.get.variants.by-variantdbid, brapi-genx.brapi-v2-1.genotyping.get.variants.by-variantdbid.calls, brapi-genx.brapi-v2-1.genotyping.get.variantsets, brapi-genx.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid, brapi-genx.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.calls, brapi-genx.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.callsets, brapi-genx.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.variants, brapi-genx.brapi-v2-1.genotyping.post.variantsets.extract, brapi-genx.brapi-v2-1.genotyping.put.calls, brapi-genx.genx.v1.variant-matrices.list, brapi-genx.genx.v1.variant-matrices.register
- **Relevant RFC / decision references:** RFC-005, D-11, D-12, D-19
- **Contract source:** [`Specification/BrAPI-GenX/Genomics/VariantMatrices_MatrixDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Genomics/VariantMatrices_MatrixDbId_GET.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### HarvestRecords — 3 operations

### GET `/genx/v1/harvest-records`

- **Catalogue ID:** `brapi-genx.genx.v1.harvest-records.list`
- **BrAPI-GenX operation identity:** `genxListHarvestRecords` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListHarvestRecords`
- **GenX source module:** `HarvestRecords`
- **Source tag:** HarvestRecords
- **Proposed BrAPI-GenX classification:** D6 — Crop Production and Material Operations; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> List harvest-event records, optionally filtered by study, location, germplasm, or date range.
**Source contract description:**
> Get a paged list of harvest records across authorities. Filters combine with AND.
**Can be used for:**
- Discover harvest outcomes for a study or location.
- Support yield tracking and seed-lot linkage.
**Must not be used for / explicit non-goals:**
- Creating or changing a record (use the POST endpoint).
- Assuming a harvest record is a BrAPI SeedLot transaction.
- Treating the list as a complete yield forecast.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** studyDbId, locationDbId, germplasmDbId, harvestedFrom, harvestedTo, page, pageSize, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxRecordHarvest, genxGetHarvestRecord
- **Related catalogue IDs:** brapi-genx.genx.v1.harvest-records.record, brapi-genx.genx.v1.harvest-records.get
- **Relevant RFC / decision references:** RFC-011
- **Contract source:** [`Specification/BrAPI-GenX/HarvestRecords/HarvestRecords_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/HarvestRecords/HarvestRecords_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/genx/v1/harvest-records`

- **Catalogue ID:** `brapi-genx.genx.v1.harvest-records.record`
- **BrAPI-GenX operation identity:** `genxRecordHarvest` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxRecordHarvest`
- **GenX source module:** `HarvestRecords`
- **Source tag:** HarvestRecords
- **Proposed BrAPI-GenX classification:** D6 — Crop Production and Material Operations; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Record one harvest event with quantity, quality, and provenance.
**Source contract description:**
> Unknown harvestRecordDbId creates; same id with an identical body replays the existing record; same id with a different body is rejected with 409.
**Can be used for:**
- Record a harvest event for a study, location, and germplasm.
- Retry an identical record safely using the same harvestRecordDbId.
**Must not be used for / explicit non-goals:**
- Updating or deleting an existing record; corrections require a new record that supersedes.
- Assuming the record is a BrAPI SeedLot transaction.
- Treating the record as a yield forecast or prediction.
- **Side effects:** Creates a harvest record when accepted.
- **Retry / idempotency:** Same harvestRecordDbId and identical body replays the existing record; same id with a different body is rejected with 409.
- **Parameters recorded in registry:** authorizationHeader
- **Request schema refs recorded:** HarvestRecordNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxListHarvestRecords, genxGetHarvestRecord
- **Related catalogue IDs:** brapi-genx.genx.v1.harvest-records.list, brapi-genx.genx.v1.harvest-records.get
- **Relevant RFC / decision references:** RFC-011
- **Contract source:** [`Specification/BrAPI-GenX/HarvestRecords/HarvestRecords_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/HarvestRecords/HarvestRecords_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/genx/v1/harvest-records/{harvestRecordDbId}`

- **Catalogue ID:** `brapi-genx.genx.v1.harvest-records.get`
- **BrAPI-GenX operation identity:** `genxGetHarvestRecord` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetHarvestRecord`
- **GenX source module:** `HarvestRecords`
- **Source tag:** HarvestRecords
- **Proposed BrAPI-GenX classification:** D6 — Crop Production and Material Operations; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Retrieve one recorded harvest event.
**Source contract description:**
> Returns the recorded harvest, or 404.
**Can be used for:**
- Inspect harvest quantity, quality, and provenance.
**Must not be used for / explicit non-goals:**
- Assuming the record is a BrAPI SeedLot transaction.
- Treating a superseded record as current.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** harvestRecordDbId, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** genxRecordHarvest, genxListHarvestRecords
- **Related catalogue IDs:** brapi-genx.genx.v1.harvest-records.list, brapi-genx.genx.v1.harvest-records.record
- **Relevant RFC / decision references:** RFC-011
- **Contract source:** [`Specification/BrAPI-GenX/HarvestRecords/HarvestRecords_HarvestRecordDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/HarvestRecords/HarvestRecords_HarvestRecordDbId_GET.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### Jobs — 4 operations

### GET `/genx/v1/jobs`

- **Catalogue ID:** `brapi-genx.genx.v1.jobs.list`
- **BrAPI-GenX operation identity:** `genxListJobs` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListJobs`
- **GenX source module:** `Jobs`
- **Source tag:** Jobs
- **Proposed BrAPI-GenX classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery, C3 — Asynchronous execution and idempotency, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Return a paginated list of caller-visible asynchronous jobs, optionally filtered by job type and lifecycle status.
**Source contract description:**
> Get a paged list of jobs submitted by the caller. Follows standard pagination.
**Can be used for:**
- Show a caller the jobs they submitted and their current lifecycle states.
- Filter jobs by an advertised job type or status.
**Must not be used for / explicit non-goals:**
- List scientific resources such as models, observations, or seed lots.
- Assume V2.1 search-result records are jobs.
- Assume a job type exists unless capability negotiation advertises it.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** jobType, status
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** JobListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-genx.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.post.search.lists, brapi-genx.brapi-v2-1.core.post.search.locations, brapi-genx.brapi-v2-1.core.post.search.people, brapi-genx.brapi-v2-1.core.post.search.programs, brapi-genx.brapi-v2-1.core.post.search.studies, brapi-genx.brapi-v2-1.core.post.search.trials, brapi-genx.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.post.search.allelematrix, brapi-genx.brapi-v2-1.genotyping.post.search.calls, brapi-genx.brapi-v2-1.genotyping.post.search.callsets, brapi-genx.brapi-v2-1.genotyping.post.search.markerpositions, brapi-genx.brapi-v2-1.genotyping.post.search.plates, brapi-genx.brapi-v2-1.genotyping.post.search.references, brapi-genx.brapi-v2-1.genotyping.post.search.referencesets, brapi-genx.brapi-v2-1.genotyping.post.search.samples, brapi-genx.brapi-v2-1.genotyping.post.search.variants, brapi-genx.brapi-v2-1.genotyping.post.search.variantsets, brapi-genx.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-genx.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-genx.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-genx.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-genx.brapi-v2-1.germplasm.post.search.attributes, brapi-genx.brapi-v2-1.germplasm.post.search.attributevalues, brapi-genx.brapi-v2-1.germplasm.post.search.germplasm, brapi-genx.brapi-v2-1.germplasm.post.search.pedigree, brapi-genx.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-genx.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-genx.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-genx.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-genx.brapi-v2-1.phenotyping.post.search.images, brapi-genx.brapi-v2-1.phenotyping.post.search.observations, brapi-genx.brapi-v2-1.phenotyping.post.search.observationunits, brapi-genx.brapi-v2-1.phenotyping.post.search.variables, brapi-genx.genx.v1.jobs.get, brapi-genx.genx.v1.jobs.request-cancellation, brapi-genx.genx.v1.jobs.submit
- **Relevant RFC / decision references:** RFC-001
- **Contract source:** [`Specification/BrAPI-GenX/Jobs/Jobs_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Jobs/Jobs_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/genx/v1/jobs`

- **Catalogue ID:** `brapi-genx.genx.v1.jobs.submit`
- **BrAPI-GenX operation identity:** `genxSubmitAsyncJob` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxSubmitAsyncJob`
- **GenX source module:** `Jobs`
- **Source tag:** Jobs
- **Proposed BrAPI-GenX classification:** No primary domain assigned; cross-cutting or review required; Facets: C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Submit one advertised unit of asynchronous work and receive a Job resource for polling and, when eligible, cancellation.
**Source contract description:**
> Submit work and receive a Job with HTTP 202. When `idempotencyKey` is
> supplied and was already accepted with a byte-identical body, the
> server returns the existing Job with zero new effects.
**Can be used for:**
- Long-running analysis, model inference, and other explicitly advertised job types.
- Replay-safe submission when the same idempotency key and identical request body are retried.
**Must not be used for / explicit non-goals:**
- Expecting synchronous completion in the submit response.
- Submitting an unadvertised or undefined jobType.
- Using one idempotency key for materially different request bodies.
- Using it as an implicit replacement for every V2.1 search endpoint.
- **Side effects:** May create one Job and dispatch work; identical replay must not create a second effect.
- **Retry / idempotency:** Same key plus identical body replays the existing Job; same key plus different body is a conflict, not an overwrite.
- **Parameters recorded in registry:** Idempotency-Key
- **Request schema refs recorded:** JobNewRequest
- **Response status codes recorded:** 202, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02, SEM-07
- **Related catalogue IDs:** brapi-genx.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.post.search.lists, brapi-genx.brapi-v2-1.core.post.search.locations, brapi-genx.brapi-v2-1.core.post.search.people, brapi-genx.brapi-v2-1.core.post.search.programs, brapi-genx.brapi-v2-1.core.post.search.studies, brapi-genx.brapi-v2-1.core.post.search.trials, brapi-genx.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.post.search.allelematrix, brapi-genx.brapi-v2-1.genotyping.post.search.calls, brapi-genx.brapi-v2-1.genotyping.post.search.callsets, brapi-genx.brapi-v2-1.genotyping.post.search.markerpositions, brapi-genx.brapi-v2-1.genotyping.post.search.plates, brapi-genx.brapi-v2-1.genotyping.post.search.references, brapi-genx.brapi-v2-1.genotyping.post.search.referencesets, brapi-genx.brapi-v2-1.genotyping.post.search.samples, brapi-genx.brapi-v2-1.genotyping.post.search.variants, brapi-genx.brapi-v2-1.genotyping.post.search.variantsets, brapi-genx.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-genx.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-genx.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-genx.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-genx.brapi-v2-1.germplasm.post.search.attributes, brapi-genx.brapi-v2-1.germplasm.post.search.attributevalues, brapi-genx.brapi-v2-1.germplasm.post.search.germplasm, brapi-genx.brapi-v2-1.germplasm.post.search.pedigree, brapi-genx.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-genx.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-genx.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-genx.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-genx.brapi-v2-1.phenotyping.post.search.images, brapi-genx.brapi-v2-1.phenotyping.post.search.observations, brapi-genx.brapi-v2-1.phenotyping.post.search.observationunits, brapi-genx.brapi-v2-1.phenotyping.post.search.variables, brapi-genx.genx.v1.jobs.get, brapi-genx.genx.v1.jobs.list, brapi-genx.genx.v1.jobs.request-cancellation, brapi-genx.genx.v1.models.get-version, brapi-genx.genx.v1.models.list, brapi-genx.genx.v1.models.register-version
- **Relevant RFC / decision references:** RFC-001, A-04, A-07
- **Contract source:** [`Specification/BrAPI-GenX/Jobs/Jobs_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Jobs/Jobs_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### DELETE `/genx/v1/jobs/{jobDbId}`

- **Catalogue ID:** `brapi-genx.genx.v1.jobs.request-cancellation`
- **BrAPI-GenX operation identity:** `genxRequestAsyncJobCancellation` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxRequestAsyncJobCancellation`
- **GenX source module:** `Jobs`
- **Source tag:** Jobs
- **Proposed BrAPI-GenX classification:** No primary domain assigned; cross-cutting or review required; Facets: C3 — Asynchronous execution and idempotency, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Request cancellation of a non-terminal asynchronous Job while preserving the Job record and its auditability.
**Source contract description:**
> Requests cancellation. Terminal states (COMPLETED, FAILED, CANCELLED, EXPIRED) are immutable and their cancellation is rejected.
**Can be used for:**
- Request that queued or running work stop, subject to implementation and execution state.
**Must not be used for / explicit non-goals:**
- Deleting a Job resource or erasing its history.
- Assuming a cancellation request guarantees immediate interruption.
- Changing terminal states such as COMPLETED, FAILED, CANCELLED, or EXPIRED.
- **Side effects:** May request a lifecycle transition for a non-terminal Job; terminal-state cancellation is rejected.
- **Retry / idempotency:** The effect is a cancellation request, not resource deletion; clients must re-read the Job state after the request.
- **Parameters recorded in registry:** jobDbId
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** genxGetAsyncJobById, SEM-02
- **Related catalogue IDs:** brapi-genx.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.post.search.lists, brapi-genx.brapi-v2-1.core.post.search.locations, brapi-genx.brapi-v2-1.core.post.search.people, brapi-genx.brapi-v2-1.core.post.search.programs, brapi-genx.brapi-v2-1.core.post.search.studies, brapi-genx.brapi-v2-1.core.post.search.trials, brapi-genx.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.post.search.allelematrix, brapi-genx.brapi-v2-1.genotyping.post.search.calls, brapi-genx.brapi-v2-1.genotyping.post.search.callsets, brapi-genx.brapi-v2-1.genotyping.post.search.markerpositions, brapi-genx.brapi-v2-1.genotyping.post.search.plates, brapi-genx.brapi-v2-1.genotyping.post.search.references, brapi-genx.brapi-v2-1.genotyping.post.search.referencesets, brapi-genx.brapi-v2-1.genotyping.post.search.samples, brapi-genx.brapi-v2-1.genotyping.post.search.variants, brapi-genx.brapi-v2-1.genotyping.post.search.variantsets, brapi-genx.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-genx.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-genx.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-genx.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-genx.brapi-v2-1.germplasm.post.search.attributes, brapi-genx.brapi-v2-1.germplasm.post.search.attributevalues, brapi-genx.brapi-v2-1.germplasm.post.search.germplasm, brapi-genx.brapi-v2-1.germplasm.post.search.pedigree, brapi-genx.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-genx.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-genx.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-genx.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-genx.brapi-v2-1.phenotyping.post.search.images, brapi-genx.brapi-v2-1.phenotyping.post.search.observations, brapi-genx.brapi-v2-1.phenotyping.post.search.observationunits, brapi-genx.brapi-v2-1.phenotyping.post.search.variables, brapi-genx.genx.v1.jobs.get, brapi-genx.genx.v1.jobs.list, brapi-genx.genx.v1.jobs.submit
- **Relevant RFC / decision references:** RFC-001
- **Contract source:** [`Specification/BrAPI-GenX/Jobs/Jobs_JobDbId_GET_DELETE.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Jobs/Jobs_JobDbId_GET_DELETE.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/genx/v1/jobs/{jobDbId}`

- **Catalogue ID:** `brapi-genx.genx.v1.jobs.get`
- **BrAPI-GenX operation identity:** `genxGetAsyncJobById` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetAsyncJobById`
- **GenX source module:** `Jobs`
- **Source tag:** Jobs
- **Proposed BrAPI-GenX classification:** No primary domain assigned; cross-cutting or review required; Facets: C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Read the current state and available result of one asynchronous Job.
**Source contract description:**
> Returns the Job. Past expiry the server reports status EXPIRED and refuses retrieval of the result.
**Can be used for:**
- Poll a submitted job until it reaches a terminal state.
- Read the result while it remains available under its expiry policy.
**Must not be used for / explicit non-goals:**
- Assuming completed results are retained indefinitely.
- Treating an expired job as a failed job or expecting its expired result to be served.
- Fetching a model artifact or a domain object directly.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** jobDbId
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** genxSubmitAsyncJob, genxRequestAsyncJobCancellation, SEM-02, SEM-07
- **Related catalogue IDs:** brapi-genx.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-genx.brapi-v2-1.core.post.search.lists, brapi-genx.brapi-v2-1.core.post.search.locations, brapi-genx.brapi-v2-1.core.post.search.people, brapi-genx.brapi-v2-1.core.post.search.programs, brapi-genx.brapi-v2-1.core.post.search.studies, brapi-genx.brapi-v2-1.core.post.search.trials, brapi-genx.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-genx.brapi-v2-1.genotyping.post.search.allelematrix, brapi-genx.brapi-v2-1.genotyping.post.search.calls, brapi-genx.brapi-v2-1.genotyping.post.search.callsets, brapi-genx.brapi-v2-1.genotyping.post.search.markerpositions, brapi-genx.brapi-v2-1.genotyping.post.search.plates, brapi-genx.brapi-v2-1.genotyping.post.search.references, brapi-genx.brapi-v2-1.genotyping.post.search.referencesets, brapi-genx.brapi-v2-1.genotyping.post.search.samples, brapi-genx.brapi-v2-1.genotyping.post.search.variants, brapi-genx.brapi-v2-1.genotyping.post.search.variantsets, brapi-genx.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-genx.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-genx.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-genx.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-genx.brapi-v2-1.germplasm.post.search.attributes, brapi-genx.brapi-v2-1.germplasm.post.search.attributevalues, brapi-genx.brapi-v2-1.germplasm.post.search.germplasm, brapi-genx.brapi-v2-1.germplasm.post.search.pedigree, brapi-genx.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-genx.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-genx.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-genx.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-genx.brapi-v2-1.phenotyping.post.search.images, brapi-genx.brapi-v2-1.phenotyping.post.search.observations, brapi-genx.brapi-v2-1.phenotyping.post.search.observationunits, brapi-genx.brapi-v2-1.phenotyping.post.search.variables, brapi-genx.genx.v1.jobs.list, brapi-genx.genx.v1.jobs.request-cancellation, brapi-genx.genx.v1.jobs.submit, brapi-genx.genx.v1.models.get-version, brapi-genx.genx.v1.models.list, brapi-genx.genx.v1.models.register-version
- **Relevant RFC / decision references:** RFC-001
- **Contract source:** [`Specification/BrAPI-GenX/Jobs/Jobs_JobDbId_GET_DELETE.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Jobs/Jobs_JobDbId_GET_DELETE.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### LotLedger — 2 operations

### GET `/genx/v1/seedlots/{seedLotDbId}/ledger`

- **Catalogue ID:** `brapi-genx.genx.v1.seed-lot-ledger.list`
- **BrAPI-GenX operation identity:** `genxListSeedLotLedgerEntries` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListSeedLotLedgerEntries`
- **GenX source module:** `LotLedger`
- **Source tag:** Seed Lots
- **Proposed BrAPI-GenX classification:** D6 — Crop Production and Material Operations; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Read a seed lot's append-only movement ledger in position order, with an optional movement-type filter.
**Source contract description:**
> Entries are returned in per-lot position order. Positions are source-local cursors; no global ordering is claimed. Unknown lots follow documented server behavior (reference server returns an empty list).
**Can be used for:**
- Inspect the entry stream for one lot.
- Reconstruct or audit that lot's history when entries and quantity semantics are valid.
**Must not be used for / explicit non-goals:**
- Assuming a globally comparable order across lots, servers, or independent streams.
- Treating the ledger as a complete atomic multi-lot transfer transaction.
- Combining with V2.1 SeedLotTransaction records as independent movements or assuming automatic equivalence.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** seedLotDbId, entryType
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** LotLedgerEntryListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-01
- **Related catalogue IDs:** brapi-genx.brapi-v2-1.germplasm.get.seedlots.by-seedlotdbid.transactions, brapi-genx.brapi-v2-1.germplasm.get.seedlots.transactions, brapi-genx.brapi-v2-1.germplasm.post.seedlots.transactions, brapi-genx.genx.v1.seed-lot-ledger.append
- **Relevant RFC / decision references:** RFC-003, D-07, D-08, D-20
- **Contract source:** [`Specification/BrAPI-GenX/LotLedger/Ledger_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/LotLedger/Ledger_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/genx/v1/seedlots/{seedLotDbId}/ledger`

- **Catalogue ID:** `brapi-genx.genx.v1.seed-lot-ledger.append`
- **BrAPI-GenX operation identity:** `genxAppendSeedLotLedgerEntry` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxAppendSeedLotLedgerEntry`
- **GenX source module:** `LotLedger`
- **Source tag:** Seed Lots
- **Proposed BrAPI-GenX classification:** D6 — Crop Production and Material Operations; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Append one immutable movement entry to one seed lot's ledger with replay and conflict protection.
**Source contract description:**
> Unknown idempotencyKey appends; known key with an identical body
> replays the existing entry with zero new effects; known key with a
> different body is rejected with 409.
**Can be used for:**
- Record a single-lot adjustment, movement, handoff, production, planting, or trade entry.
- Retry an identical entry safely using the same idempotency key.
**Must not be used for / explicit non-goals:**
- Updating or deleting an existing ledger entry; corrections require an additional record.
- Assuming multi-lot transfer atomicity.
- Automatically mirroring a movement to V2.1 SeedLotTransaction or double-counting both streams.
- **Side effects:** Appends one ledger entry when accepted.
- **Retry / idempotency:** Same key and identical body replays existing entry; same key and different body is rejected as a conflict.
- **Parameters recorded in registry:** seedLotDbId, Idempotency-Key
- **Request schema refs recorded:** LotLedgerEntryNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-01
- **Related catalogue IDs:** brapi-genx.brapi-v2-1.germplasm.get.seedlots.by-seedlotdbid.transactions, brapi-genx.brapi-v2-1.germplasm.get.seedlots.transactions, brapi-genx.brapi-v2-1.germplasm.post.seedlots.transactions, brapi-genx.genx.v1.seed-lot-ledger.list
- **Relevant RFC / decision references:** RFC-003, D-07, D-08, D-20, A-05, A-06
- **Contract source:** [`Specification/BrAPI-GenX/LotLedger/Ledger_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/LotLedger/Ledger_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### MeasurementMethods — 3 operations

### GET `/genx/v1/measurement-methods`

- **Catalogue ID:** `brapi-genx.genx.v1.measurement-methods.list`
- **BrAPI-GenX operation identity:** `genxListMeasurementMethods` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListMeasurementMethods`
- **GenX source module:** `MeasurementMethods`
- **Source tag:** MeasurementMethods
- **Proposed BrAPI-GenX classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C4 — Scientific terminology governance, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> List measurement method definitions, optionally filtered by type or status.
**Source contract description:**
> Get a paged list of measurement methods across authorities. Filters combine with AND.
**Can be used for:**
- Discover measurement methods and their procedures.
- Support terminology and method governance.
**Must not be used for / explicit non-goals:**
- Creating or changing a method (use the POST endpoint).
- Assuming a method is a BrAPI Method or Scale.
- Treating the list as a complete method catalogue.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** methodType, status, page, pageSize, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxRegisterMeasurementMethod, genxGetMeasurementMethod
- **Related catalogue IDs:** brapi-genx.genx.v1.measurement-methods.register, brapi-genx.genx.v1.measurement-methods.get
- **Relevant RFC / decision references:** RFC-017
- **Contract source:** [`Specification/BrAPI-GenX/MeasurementMethods/MeasurementMethods_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/MeasurementMethods/MeasurementMethods_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/genx/v1/measurement-methods`

- **Catalogue ID:** `brapi-genx.genx.v1.measurement-methods.register`
- **BrAPI-GenX operation identity:** `genxRegisterMeasurementMethod` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxRegisterMeasurementMethod`
- **GenX source module:** `MeasurementMethods`
- **Source tag:** MeasurementMethods
- **Proposed BrAPI-GenX classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C4 — Scientific terminology governance, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Register a measurement method with procedure, equipment, precision, and provenance.
**Source contract description:**
> Unknown measurementMethodDbId creates; same id with an identical body replays the existing record; same id with a different body is rejected with 409.
**Can be used for:**
- Publish measurement method definitions.
- Create a new version under an existing method identity.
**Must not be used for / explicit non-goals:**
- Updating or deleting an existing method; corrections require a new record that supersedes.
- Assuming the method is a BrAPI Method.
- Treating the method as an approved protocol.
- **Side effects:** Creates a method identity or appends a new immutable version when accepted.
- **Retry / idempotency:** Same method identity and identical body replays; conflicting content for the same identity is rejected.
- **Parameters recorded in registry:** authorizationHeader
- **Request schema refs recorded:** MeasurementMethodNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxListMeasurementMethods, genxGetMeasurementMethod
- **Related catalogue IDs:** brapi-genx.genx.v1.measurement-methods.list, brapi-genx.genx.v1.measurement-methods.get
- **Relevant RFC / decision references:** RFC-017
- **Contract source:** [`Specification/BrAPI-GenX/MeasurementMethods/MeasurementMethods_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/MeasurementMethods/MeasurementMethods_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/genx/v1/measurement-methods/{measurementMethodDbId}`

- **Catalogue ID:** `brapi-genx.genx.v1.measurement-methods.get`
- **BrAPI-GenX operation identity:** `genxGetMeasurementMethod` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetMeasurementMethod`
- **GenX source module:** `MeasurementMethods`
- **Source tag:** MeasurementMethods
- **Proposed BrAPI-GenX classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C4 — Scientific terminology governance, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Retrieve one registered measurement method.
**Source contract description:**
> Returns the registered method, or 404.
**Can be used for:**
- Inspect method procedure, equipment, precision, and provenance.
**Must not be used for / explicit non-goals:**
- Assuming the method is a BrAPI Method.
- Treating a superseded method as current.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** measurementMethodDbId, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** genxRegisterMeasurementMethod, genxListMeasurementMethods
- **Related catalogue IDs:** brapi-genx.genx.v1.measurement-methods.list, brapi-genx.genx.v1.measurement-methods.register
- **Relevant RFC / decision references:** RFC-017
- **Contract source:** [`Specification/BrAPI-GenX/MeasurementMethods/MeasurementMethods_MeasurementMethodDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/MeasurementMethods/MeasurementMethods_MeasurementMethodDbId_GET.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### Models — 3 operations

### GET `/genx/v1/models`

- **Catalogue ID:** `brapi-genx.genx.v1.models.list`
- **BrAPI-GenX operation identity:** `genxListModelVersions` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListModelVersions`
- **GenX source module:** `Models`
- **Source tag:** Models
- **Proposed BrAPI-GenX classification:** D7 — Scientific Analysis, Models and Derived Evidence; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> List registered model artifact versions and their lifecycle states, including active, deprecated, and revoked.
**Source contract description:**
> Get a paged list of model versions across authorities. Filters combine with AND.
**Can be used for:**
- Discover registered model identities and versions.
- Select a model version subject to lifecycle status and advertised inference support.
**Must not be used for / explicit non-goals:**
- Running inference or training a model.
- Assuming registration means scientific validation, approval, or endorsement.
- Assuming metrics from different models are directly comparable without defined metric semantics.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** modelDbId, status
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** ModelArtifactListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxRegisterModelVersion, genxGetModelVersion, genxSubmitAsyncJob, SEM-07
- **Related catalogue IDs:** brapi-genx.genx.v1.jobs.get, brapi-genx.genx.v1.jobs.submit, brapi-genx.genx.v1.models.get-version, brapi-genx.genx.v1.models.register-version
- **Relevant RFC / decision references:** RFC-004, D-09
- **Contract source:** [`Specification/BrAPI-GenX/Models/Models_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Models/Models_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/genx/v1/models`

- **Catalogue ID:** `brapi-genx.genx.v1.models.register-version`
- **BrAPI-GenX operation identity:** `genxRegisterModelVersion` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxRegisterModelVersion`
- **GenX source module:** `Models`
- **Source tag:** Models
- **Proposed BrAPI-GenX classification:** D7 — Scientific Analysis, Models and Derived Evidence; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Register a model artifact version with a namespaced identity, immutable artifact digest, training provenance, metrics, framework, and lifecycle state.
**Source contract description:**
> Unknown modelDbId creates; known id with a new version appends;
> same (modelDbId, modelVersion) with an identical body replays the
> existing record; same pair with a different body is rejected with 409.
**Can be used for:**
- Publish model metadata and integrity references.
- Create a new version under an existing model identity.
- Record deprecation or revocation status as governed elsewhere.
**Must not be used for / explicit non-goals:**
- Training a model or executing inference.
- Assuming the endpoint uploads model bytes; artifact transport is a separate unresolved contract.
- Treating the revoked flag as an approval or governance workflow.
- **Side effects:** Creates a model identity or appends a new immutable version when accepted.
- **Retry / idempotency:** Same model identity/version and identical body replays; conflicting content for the same version is rejected.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ModelArtifactNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxListModelVersions, genxGetModelVersion, genxSubmitAsyncJob, SEM-07
- **Related catalogue IDs:** brapi-genx.genx.v1.jobs.get, brapi-genx.genx.v1.jobs.submit, brapi-genx.genx.v1.models.get-version, brapi-genx.genx.v1.models.list
- **Relevant RFC / decision references:** RFC-004, D-09, D-10
- **Contract source:** [`Specification/BrAPI-GenX/Models/Models_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Models/Models_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/genx/v1/models/{modelDbId}`

- **Catalogue ID:** `brapi-genx.genx.v1.models.get-version`
- **BrAPI-GenX operation identity:** `genxGetModelVersion` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetModelVersion`
- **GenX source module:** `Models`
- **Source tag:** Models
- **Proposed BrAPI-GenX classification:** D7 — Scientific Analysis, Models and Derived Evidence; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Retrieve the registered metadata for one model identity/version.
**Source contract description:**
> Returns the requested version, or the most recently created version when `version` is omitted.
**Can be used for:**
- Inspect artifact digest, training provenance, version, and lifecycle status before selecting an inference model.
**Must not be used for / explicit non-goals:**
- Executing inference or training.
- Assuming model bytes are served by this endpoint.
- Assuming metadata status alone proves scientific fitness for a particular task.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** modelDbId, version
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** genxRegisterModelVersion, genxSubmitAsyncJob, SEM-07
- **Related catalogue IDs:** brapi-genx.genx.v1.jobs.get, brapi-genx.genx.v1.jobs.submit, brapi-genx.genx.v1.models.list, brapi-genx.genx.v1.models.register-version
- **Relevant RFC / decision references:** RFC-004, D-09, D-10
- **Contract source:** [`Specification/BrAPI-GenX/Models/Models_ModelDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Models/Models_ModelDbId_GET.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### PhenotypeCapture — 3 operations

### GET `/genx/v1/phenotype-captures`

- **Catalogue ID:** `brapi-genx.genx.v1.phenotype-captures.list`
- **BrAPI-GenX operation identity:** `genxListPhenotypeCaptures` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListPhenotypeCaptures`
- **GenX source module:** `PhenotypeCapture`
- **Source tag:** PhenotypeCapture
- **Proposed BrAPI-GenX classification:** D4 — Phenotyping and Plant Observations; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> List phenotype capture records, optionally filtered by study, observation unit, or capture method.
**Source contract description:**
> Get a paged list of phenotype capture records across authorities. Filters combine with AND.
**Can be used for:**
- Discover phenotype capture events for a study or observation unit.
- Audit capture workflow, quality flags, and corrections.
**Must not be used for / explicit non-goals:**
- Creating or changing a capture (use the POST endpoint).
- Assuming a capture is a BrAPI Observation.
- Treating the list as a complete phenotype dataset.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** studyDbId, observationUnitDbId, captureMethod, page, pageSize, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxRecordPhenotypeCapture, genxGetPhenotypeCapture
- **Related catalogue IDs:** brapi-genx.genx.v1.phenotype-captures.record, brapi-genx.genx.v1.phenotype-captures.get
- **Relevant RFC / decision references:** RFC-012
- **Contract source:** [`Specification/BrAPI-GenX/PhenotypeCapture/PhenotypeCapture_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/PhenotypeCapture/PhenotypeCapture_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/genx/v1/phenotype-captures`

- **Catalogue ID:** `brapi-genx.genx.v1.phenotype-captures.record`
- **BrAPI-GenX operation identity:** `genxRecordPhenotypeCapture` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxRecordPhenotypeCapture`
- **GenX source module:** `PhenotypeCapture`
- **Source tag:** PhenotypeCapture
- **Proposed BrAPI-GenX classification:** D4 — Phenotyping and Plant Observations; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Record one phenotype capture event with entries, quality flags, missingness, and provenance.
**Source contract description:**
> Unknown phenotypeCaptureDbId creates; same id with an identical body replays the existing record; same id with a different body is rejected with 409.
**Can be used for:**
- Record a capture event for an observation unit.
- Retry an identical capture safely using the same phenotypeCaptureDbId.
**Must not be used for / explicit non-goals:**
- Updating or deleting an existing capture; corrections require a new record that supersedes.
- Assuming the capture is a BrAPI Observation.
- Treating the capture as a complete phenotype dataset.
- **Side effects:** Creates a phenotype capture when accepted.
- **Retry / idempotency:** Same phenotypeCaptureDbId and identical body replays the existing record; same id with a different body is rejected with 409.
- **Parameters recorded in registry:** authorizationHeader
- **Request schema refs recorded:** PhenotypeCaptureNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxListPhenotypeCaptures, genxGetPhenotypeCapture
- **Related catalogue IDs:** brapi-genx.genx.v1.phenotype-captures.list, brapi-genx.genx.v1.phenotype-captures.get
- **Relevant RFC / decision references:** RFC-012
- **Contract source:** [`Specification/BrAPI-GenX/PhenotypeCapture/PhenotypeCapture_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/PhenotypeCapture/PhenotypeCapture_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/genx/v1/phenotype-captures/{phenotypeCaptureDbId}`

- **Catalogue ID:** `brapi-genx.genx.v1.phenotype-captures.get`
- **BrAPI-GenX operation identity:** `genxGetPhenotypeCapture` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetPhenotypeCapture`
- **GenX source module:** `PhenotypeCapture`
- **Source tag:** PhenotypeCapture
- **Proposed BrAPI-GenX classification:** D4 — Phenotyping and Plant Observations; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Retrieve one recorded phenotype capture event.
**Source contract description:**
> Returns the recorded capture, or 404.
**Can be used for:**
- Inspect capture entries, quality flags, and provenance.
**Must not be used for / explicit non-goals:**
- Assuming the capture is a BrAPI Observation.
- Treating a superseded capture as current.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** phenotypeCaptureDbId, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** genxRecordPhenotypeCapture, genxListPhenotypeCaptures
- **Related catalogue IDs:** brapi-genx.genx.v1.phenotype-captures.list, brapi-genx.genx.v1.phenotype-captures.record
- **Relevant RFC / decision references:** RFC-012
- **Contract source:** [`Specification/BrAPI-GenX/PhenotypeCapture/PhenotypeCapture_PhenotypeCaptureDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/PhenotypeCapture/PhenotypeCapture_PhenotypeCaptureDbId_GET.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### ProgenyRecords — 3 operations

### GET `/genx/v1/progeny-records`

- **Catalogue ID:** `brapi-genx.genx.v1.progeny-records.list`
- **BrAPI-GenX operation identity:** `genxListProgenyRecords` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListProgenyRecords`
- **GenX source module:** `ProgenyRecords`
- **Source tag:** ProgenyRecords
- **Proposed BrAPI-GenX classification:** D2 — Breeding Programs and Experimental Design; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> List progeny/family records, optionally filtered by program, parent, or generation.
**Source contract description:**
> Get a paged list of progeny records across authorities. Filters combine with AND.
**Can be used for:**
- Discover progeny and family links within a breeding program.
- Support pedigree and lineage auditing.
**Must not be used for / explicit non-goals:**
- Creating or changing a record (use the POST endpoint).
- Assuming a record is a BrAPI Pedigree or Cross.
- Treating the list as a complete breeding program record.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** programDbId, parentDbId, generation, page, pageSize, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxRecordProgeny, genxGetProgenyRecord
- **Related catalogue IDs:** brapi-genx.genx.v1.progeny-records.record, brapi-genx.genx.v1.progeny-records.get
- **Relevant RFC / decision references:** RFC-019
- **Contract source:** [`Specification/BrAPI-GenX/ProgenyRecords/ProgenyRecords_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/ProgenyRecords/ProgenyRecords_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/genx/v1/progeny-records`

- **Catalogue ID:** `brapi-genx.genx.v1.progeny-records.record`
- **BrAPI-GenX operation identity:** `genxRecordProgeny` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxRecordProgeny`
- **GenX source module:** `ProgenyRecords`
- **Source tag:** ProgenyRecords
- **Proposed BrAPI-GenX classification:** D2 — Breeding Programs and Experimental Design; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Record one progeny/family link with parents, generation, and provenance.
**Source contract description:**
> Unknown progenyRecordDbId creates; same id with an identical body replays the existing record; same id with a different body is rejected with 409.
**Can be used for:**
- Record a progeny/family link within a breeding program.
- Retry an identical record safely using the same progenyRecordDbId.
**Must not be used for / explicit non-goals:**
- Updating or deleting an existing record; corrections require a new record that supersedes.
- Assuming the record is a BrAPI Pedigree or Cross.
- Treating the record as a complete breeding program record.
- **Side effects:** Creates a progeny record when accepted.
- **Retry / idempotency:** Same progenyRecordDbId and identical body replays the existing record; same id with a different body is rejected with 409.
- **Parameters recorded in registry:** authorizationHeader
- **Request schema refs recorded:** ProgenyRecordNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxListProgenyRecords, genxGetProgenyRecord
- **Related catalogue IDs:** brapi-genx.genx.v1.progeny-records.list, brapi-genx.genx.v1.progeny-records.get
- **Relevant RFC / decision references:** RFC-019
- **Contract source:** [`Specification/BrAPI-GenX/ProgenyRecords/ProgenyRecords_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/ProgenyRecords/ProgenyRecords_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/genx/v1/progeny-records/{progenyRecordDbId}`

- **Catalogue ID:** `brapi-genx.genx.v1.progeny-records.get`
- **BrAPI-GenX operation identity:** `genxGetProgenyRecord` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetProgenyRecord`
- **GenX source module:** `ProgenyRecords`
- **Source tag:** ProgenyRecords
- **Proposed BrAPI-GenX classification:** D2 — Breeding Programs and Experimental Design; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Retrieve one recorded progeny/family link.
**Source contract description:**
> Returns the recorded progeny, or 404.
**Can be used for:**
- Inspect progeny, parents, generation, and provenance.
**Must not be used for / explicit non-goals:**
- Assuming the record is a BrAPI Pedigree or Cross.
- Treating a superseded record as current.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** progenyRecordDbId, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** genxRecordProgeny, genxListProgenyRecords
- **Related catalogue IDs:** brapi-genx.genx.v1.progeny-records.list, brapi-genx.genx.v1.progeny-records.record
- **Relevant RFC / decision references:** RFC-019
- **Contract source:** [`Specification/BrAPI-GenX/ProgenyRecords/ProgenyRecords_ProgenyRecordDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/ProgenyRecords/ProgenyRecords_ProgenyRecordDbId_GET.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### ResearchAssets — 3 operations

### GET `/genx/v1/research-assets`

- **Catalogue ID:** `brapi-genx.genx.v1.research-assets.list`
- **BrAPI-GenX operation identity:** `genxListResearchAssets` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListResearchAssets`
- **GenX source module:** `ResearchAssets`
- **Source tag:** ResearchAssets
- **Proposed BrAPI-GenX classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C5 — Data exchange, publication and access, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> List research asset records, optionally filtered by type, license, or access policy.
**Source contract description:**
> Get a paged list of research assets across authorities. Filters combine with AND.
**Can be used for:**
- Discover research assets and their metadata.
- Support publication and citation workflows.
**Must not be used for / explicit non-goals:**
- Creating or changing an asset (use the POST endpoint).
- Assuming an asset is a BrAPI data resource.
- Treating the list as a complete repository.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** assetType, license, accessPolicy, page, pageSize, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxRegisterResearchAsset, genxGetResearchAsset, genxRegisterFairPackage
- **Related catalogue IDs:** brapi-genx.genx.v1.research-assets.register, brapi-genx.genx.v1.research-assets.get
- **Relevant RFC / decision references:** RFC-016
- **Contract source:** [`Specification/BrAPI-GenX/ResearchAssets/ResearchAssets_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/ResearchAssets/ResearchAssets_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/genx/v1/research-assets`

- **Catalogue ID:** `brapi-genx.genx.v1.research-assets.register`
- **BrAPI-GenX operation identity:** `genxRegisterResearchAsset` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxRegisterResearchAsset`
- **GenX source module:** `ResearchAssets`
- **Source tag:** ResearchAssets
- **Proposed BrAPI-GenX classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C5 — Data exchange, publication and access, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Register a research asset with type, title, license, access policy, and persistent identifier.
**Source contract description:**
> Unknown researchAssetDbId creates; same id with an identical body replays the existing record; same id with a different body is rejected with 409.
**Can be used for:**
- Publish research asset metadata.
- Create a new version under an existing asset identity.
**Must not be used for / explicit non-goals:**
- Uploading payload bytes through this endpoint.
- Assuming registration mints a persistent identifier.
- Treating the asset as a BrAPI data resource.
- **Side effects:** Creates a research asset identity or appends a new immutable version when accepted.
- **Retry / idempotency:** Same asset identity and identical body replays; conflicting content for the same identity is rejected.
- **Parameters recorded in registry:** authorizationHeader
- **Request schema refs recorded:** ResearchAssetNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxListResearchAssets, genxGetResearchAsset, genxRegisterFairPackage
- **Related catalogue IDs:** brapi-genx.genx.v1.research-assets.list, brapi-genx.genx.v1.research-assets.get
- **Relevant RFC / decision references:** RFC-016
- **Contract source:** [`Specification/BrAPI-GenX/ResearchAssets/ResearchAssets_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/ResearchAssets/ResearchAssets_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/genx/v1/research-assets/{researchAssetDbId}`

- **Catalogue ID:** `brapi-genx.genx.v1.research-assets.get`
- **BrAPI-GenX operation identity:** `genxGetResearchAsset` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetResearchAsset`
- **GenX source module:** `ResearchAssets`
- **Source tag:** ResearchAssets
- **Proposed BrAPI-GenX classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C5 — Data exchange, publication and access, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Retrieve one registered research asset.
**Source contract description:**
> Returns the registered asset, or 404.
**Can be used for:**
- Inspect asset metadata, license, access policy, and provenance.
**Must not be used for / explicit non-goals:**
- Assuming the asset is a BrAPI data resource.
- Treating a withdrawn asset as current.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** researchAssetDbId, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** genxRegisterResearchAsset, genxListResearchAssets, genxRegisterFairPackage
- **Related catalogue IDs:** brapi-genx.genx.v1.research-assets.list, brapi-genx.genx.v1.research-assets.register
- **Relevant RFC / decision references:** RFC-016
- **Contract source:** [`Specification/BrAPI-GenX/ResearchAssets/ResearchAssets_ResearchAssetDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/ResearchAssets/ResearchAssets_ResearchAssetDbId_GET.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### SelectionDecisions — 3 operations

### GET `/genx/v1/selection-decisions`

- **Catalogue ID:** `brapi-genx.genx.v1.selection-decisions.list`
- **BrAPI-GenX operation identity:** `genxListSelectionDecisions` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListSelectionDecisions`
- **GenX source module:** `SelectionDecisions`
- **Source tag:** SelectionDecisions
- **Proposed BrAPI-GenX classification:** D2 — Breeding Programs and Experimental Design; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> List recorded breeding selection decisions, optionally filtered by program, study, candidate, or verdict.
**Source contract description:**
> Get a paged list of selection decisions across authorities. Filters combine with AND.
**Can be used for:**
- Discover selection verdicts for a breeding program or trial.
- Audit breeding history and candidate advancement.
**Must not be used for / explicit non-goals:**
- Creating or changing a verdict (use the POST endpoint).
- Assuming a decision implies release or commercial approval.
- Treating the list as a complete breeding program record.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** programDbId, studyDbId, candidateGermplasmDbId, decision, page, pageSize, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxRecordSelectionDecision, genxGetSelectionDecision
- **Related catalogue IDs:** brapi-genx.genx.v1.selection-decisions.record, brapi-genx.genx.v1.selection-decisions.get
- **Relevant RFC / decision references:** RFC-008
- **Contract source:** [`Specification/BrAPI-GenX/SelectionDecisions/SelectionDecisions_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/SelectionDecisions/SelectionDecisions_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/genx/v1/selection-decisions`

- **Catalogue ID:** `brapi-genx.genx.v1.selection-decisions.record`
- **BrAPI-GenX operation identity:** `genxRecordSelectionDecision` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxRecordSelectionDecision`
- **GenX source module:** `SelectionDecisions`
- **Source tag:** SelectionDecisions
- **Proposed BrAPI-GenX classification:** D2 — Breeding Programs and Experimental Design; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Record one breeding selection verdict with candidate, criterion, evidence inputs, and provenance.
**Source contract description:**
> Unknown selectionDecisionDbId creates; same id with an identical body replays the existing record; same id with a different body is rejected with 409.
**Can be used for:**
- Record a selected/rejected/deferred/advanced verdict for a candidate.
- Retry an identical decision safely using the same selectionDecisionDbId.
**Must not be used for / explicit non-goals:**
- Updating or deleting an existing decision; corrections require a new record that supersedes.
- Assuming the decision grants release, registration, or commercial approval.
- Treating the verdict as an automated breeding recommendation.
- **Side effects:** Creates a selection decision when accepted.
- **Retry / idempotency:** Same selectionDecisionDbId and identical body replays the existing record; same id with a different body is rejected with 409.
- **Parameters recorded in registry:** authorizationHeader
- **Request schema refs recorded:** SelectionDecisionNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxListSelectionDecisions, genxGetSelectionDecision
- **Related catalogue IDs:** brapi-genx.genx.v1.selection-decisions.list, brapi-genx.genx.v1.selection-decisions.get
- **Relevant RFC / decision references:** RFC-008
- **Contract source:** [`Specification/BrAPI-GenX/SelectionDecisions/SelectionDecisions_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/SelectionDecisions/SelectionDecisions_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/genx/v1/selection-decisions/{selectionDecisionDbId}`

- **Catalogue ID:** `brapi-genx.genx.v1.selection-decisions.get`
- **BrAPI-GenX operation identity:** `genxGetSelectionDecision` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetSelectionDecision`
- **GenX source module:** `SelectionDecisions`
- **Source tag:** SelectionDecisions
- **Proposed BrAPI-GenX classification:** D2 — Breeding Programs and Experimental Design; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Retrieve one recorded breeding selection decision.
**Source contract description:**
> Returns the recorded decision, or 404.
**Can be used for:**
- Inspect a verdict, its candidate, criterion, and provenance.
**Must not be used for / explicit non-goals:**
- Assuming the decision is the only or final authority for release.
- Treating a superseded decision as current.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** selectionDecisionDbId, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** genxRecordSelectionDecision, genxListSelectionDecisions
- **Related catalogue IDs:** brapi-genx.genx.v1.selection-decisions.list, brapi-genx.genx.v1.selection-decisions.record
- **Relevant RFC / decision references:** RFC-008
- **Contract source:** [`Specification/BrAPI-GenX/SelectionDecisions/SelectionDecisions_SelectionDecisionDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/SelectionDecisions/SelectionDecisions_SelectionDecisionDbId_GET.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### ServerInfoV3 — 1 operations

### GET `/genx/v1/serverinfo`

- **Catalogue ID:** `brapi-genx.genx.v1.serverinfo.read`
- **BrAPI-GenX operation identity:** `genxGetServerInfoV3` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetServerInfoV3`
- **GenX source module:** `ServerInfoV3`
- **Source tag:** Server Info
- **Proposed BrAPI-GenX classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery, C8 — Contract conformance and governance, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Advertise supported API generations, capabilities, and authentication profiles so clients can negotiate behavior before using optional GenX features.
**Source contract description:**
> GenX capability negotiation. Served under `/genx/v1/`.
>
> Returns the V2.1 ServerInfo fields plus `brapiVersions`,
> `capabilities`, and `authProfiles` so clients negotiate instead of
> probing endpoints. V2.1 `GET /serverinfo` under `/brapi/v2/` is
> unchanged. A GenX client against a V2.1-only server falls back to the
> V2.1 `calls` array.
**Can be used for:**
- Discover whether a server advertises GenX and which capabilities/job types it supports.
- Choose a documented V2.1 fallback when GenX is not advertised.
**Must not be used for / explicit non-goals:**
- Proving that every advertised operation is healthy at this instant.
- Calling unadvertised endpoints as feature probes.
- Treating the V2.1 ServerInfo payload and ServerInfoV3 as interchangeable.
- **Side effects:** Read-only; no domain records are created or changed.
- **Retry / idempotency:** Read-only; repeated calls have no intended state-changing effects.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** V2.1 GET /brapi/v2/serverinfo, OVERLAP-01
- **Related catalogue IDs:** brapi-genx.brapi-v2-1.core.get.serverinfo
- **Relevant RFC / decision references:** RFC-001, A-01
- **Contract source:** [`Specification/BrAPI-GenX/ServerInfoV3/ServerInfoV3_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/ServerInfoV3/ServerInfoV3_GET.yaml)
- **BijMantra relative-route candidates:** 1. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - [backend/app/api/brapi/v2/core/serverinfo.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/serverinfo.py#L145) — `get_server_info`; brapi-adapter-source-declaration.
  - Interpretation: Same relative method/path appears in BijMantra's static inventory. Do not infer V3 wiring, contract equivalence, or runtime mounting.

### Telemetry — 2 operations

### GET `/genx/v1/telemetry`

- **Catalogue ID:** `brapi-genx.genx.v1.telemetry.query`
- **BrAPI-GenX operation identity:** `genxQueryTelemetrySamplesOrAggregates` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxQueryTelemetrySamplesOrAggregates`
- **GenX source module:** `Telemetry`
- **Source tag:** Telemetry
- **Proposed BrAPI-GenX classification:** No primary domain assigned; cross-cutting or review required; Context-dependent: D4 — Phenotyping and Plant Observations, D5 — Environment, Agroecology and Field Context; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C7 — Streaming and temporal aggregation, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Read device/sensor samples in timestamp order or calculate deterministic aggregates over a requested time range.
**Source contract description:**
> Points are returned in timestamp order. With aggregation set,
> TelemetryBucket rows are returned instead, computed deterministically
> over windowSeconds buckets (default: one bucket over the whole
> range). Empty ranges yield empty data, never an error.
**Can be used for:**
- Retrieve raw telemetry for a device and optional sensor over a time interval.
- Calculate mean, minimum, maximum, or count aggregates in defined windows.
- Use an inclusive from timestamp and exclusive to timestamp.
**Must not be used for / explicit non-goals:**
- Automatically converting every telemetry sample into a BrAPI Observation.
- Assuming implicit links to a study, observation unit, or observation variable.
- Assuming unspecified gap-filling, resampling, or timezone-of-record behavior.
- **Side effects:** Read-only; aggregates are calculated from stored samples.
- **Retry / idempotency:** Read-only for an unchanged stored dataset and query; deterministic aggregation rules apply to the same sample set and range.
- **Parameters recorded in registry:** deviceDbId, sensorDbId, from, to, aggregation, windowSeconds
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-03
- **Related catalogue IDs:** brapi-genx.brapi-v2-1.phenotyping.get.observations, brapi-genx.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-genx.brapi-v2-1.phenotyping.get.observations.table, brapi-genx.brapi-v2-1.phenotyping.get.observationunits, brapi-genx.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-genx.brapi-v2-1.phenotyping.get.observationunits.table, brapi-genx.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-genx.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-genx.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-genx.brapi-v2-1.phenotyping.get.variables, brapi-genx.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-genx.brapi-v2-1.phenotyping.post.delete.observations, brapi-genx.brapi-v2-1.phenotyping.post.observations, brapi-genx.brapi-v2-1.phenotyping.post.observationunits, brapi-genx.brapi-v2-1.phenotyping.post.search.observations, brapi-genx.brapi-v2-1.phenotyping.post.search.observationunits, brapi-genx.brapi-v2-1.phenotyping.post.search.variables, brapi-genx.brapi-v2-1.phenotyping.post.variables, brapi-genx.brapi-v2-1.phenotyping.put.observations, brapi-genx.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-genx.brapi-v2-1.phenotyping.put.observationunits, brapi-genx.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-genx.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-genx.genx.v1.telemetry.append-batch
- **Relevant RFC / decision references:** RFC-007, D-16, D-17, D-18
- **Contract source:** [`Specification/BrAPI-GenX/Telemetry/Telemetry_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Telemetry/Telemetry_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/genx/v1/telemetry`

- **Catalogue ID:** `brapi-genx.genx.v1.telemetry.append-batch`
- **BrAPI-GenX operation identity:** `genxAppendTelemetryBatch` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxAppendTelemetryBatch`
- **GenX source module:** `Telemetry`
- **Source tag:** Telemetry
- **Proposed BrAPI-GenX classification:** No primary domain assigned; cross-cutting or review required; Context-dependent: D4 — Phenotyping and Plant Observations, D5 — Environment, Agroecology and Field Context; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C7 — Streaming and temporal aggregation, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Append a batch of timestamped device/sensor samples while reporting newly appended, replayed, and conflicting elements.
**Source contract description:**
> Takes an array of TelemetryPoint (V2.1 batch style). Reports
> appended, replayed, and conflicts counts with the conflicting keys.
> Conflicting elements reject the element, never the batch.
**Can be used for:**
- Ingest sample batches from field or laboratory sensors.
- Retry identical samples without duplicating stored points.
- Reject conflicting values for an already-used device/sensor/timestamp key without discarding unrelated valid batch elements.
**Must not be used for / explicit non-goals:**
- Replacing existing samples silently.
- Assuming the batch is all-or-nothing; conflicts are handled element-wise.
- Treating telemetry as a complete observation record or assuming all samples are environmental.
- **Side effects:** Appends non-conflicting new points; reports duplicate replays and per-element conflicts.
- **Retry / idempotency:** Natural key is deviceDbId + sensorDbId + timestamp. Same key and value replays; same key with a different value conflicts.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** TelemetryPoint
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-03
- **Related catalogue IDs:** brapi-genx.brapi-v2-1.phenotyping.get.observations, brapi-genx.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-genx.brapi-v2-1.phenotyping.get.observations.table, brapi-genx.brapi-v2-1.phenotyping.get.observationunits, brapi-genx.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-genx.brapi-v2-1.phenotyping.get.observationunits.table, brapi-genx.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-genx.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-genx.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-genx.brapi-v2-1.phenotyping.get.variables, brapi-genx.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-genx.brapi-v2-1.phenotyping.post.delete.observations, brapi-genx.brapi-v2-1.phenotyping.post.observations, brapi-genx.brapi-v2-1.phenotyping.post.observationunits, brapi-genx.brapi-v2-1.phenotyping.post.search.observations, brapi-genx.brapi-v2-1.phenotyping.post.search.observationunits, brapi-genx.brapi-v2-1.phenotyping.post.search.variables, brapi-genx.brapi-v2-1.phenotyping.post.variables, brapi-genx.brapi-v2-1.phenotyping.put.observations, brapi-genx.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-genx.brapi-v2-1.phenotyping.put.observationunits, brapi-genx.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-genx.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-genx.genx.v1.telemetry.query
- **Relevant RFC / decision references:** RFC-007, D-16, D-17, D-18
- **Contract source:** [`Specification/BrAPI-GenX/Telemetry/Telemetry_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Telemetry/Telemetry_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### VariableTerms — 3 operations

### GET `/genx/v1/variable-terms`

- **Catalogue ID:** `brapi-genx.genx.v1.variable-terms.list`
- **BrAPI-GenX operation identity:** `genxListVariableTermVersions` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListVariableTermVersions`
- **GenX source module:** `VariableTerms`
- **Source tag:** VariableTerms
- **Proposed BrAPI-GenX classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C4 — Scientific terminology governance
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> List paginated, namespaced versions of observation-variable term definitions, with optional authority, ontology, and lifecycle filters.
**Source contract description:**
> Return a paged list of namespaced observation-variable term versions across authorities. All supplied filters combine with AND.
**Can be used for:**
- Discover published VariableTerm versions and filter the term registry.
- Resolve which namespaced term definitions are available.
**Must not be used for / explicit non-goals:**
- Treating results as measured observations or trait values.
- Assuming this endpoint implements full Trait, Method, Scale, or ontology-merging lifecycles.
- Assuming terms with similar labels are semantically equivalent.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** variableDbId, ontologyDbId, status
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** VariableTermListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** V2.1 /brapi/v2/variables, V2.1 OntologyTerm schema, SEM-06
- **Related catalogue IDs:** brapi-genx.brapi-v2-1.phenotyping.get.methods, brapi-genx.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-genx.brapi-v2-1.phenotyping.get.ontologies, brapi-genx.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-genx.brapi-v2-1.phenotyping.get.scales, brapi-genx.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-genx.brapi-v2-1.phenotyping.get.traits, brapi-genx.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-genx.brapi-v2-1.phenotyping.get.variables, brapi-genx.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-genx.brapi-v2-1.phenotyping.post.methods, brapi-genx.brapi-v2-1.phenotyping.post.ontologies, brapi-genx.brapi-v2-1.phenotyping.post.scales, brapi-genx.brapi-v2-1.phenotyping.post.traits, brapi-genx.brapi-v2-1.phenotyping.post.variables, brapi-genx.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-genx.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-genx.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-genx.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-genx.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-genx.genx.v1.variable-terms.get-version, brapi-genx.genx.v1.variable-terms.publish-version
- **Relevant RFC / decision references:** RFC-002, A-03
- **Contract source:** [`Specification/BrAPI-GenX/VariableTerms/VariableTerms_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/VariableTerms/VariableTerms_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/genx/v1/variable-terms`

- **Catalogue ID:** `brapi-genx.genx.v1.variable-terms.publish-version`
- **BrAPI-GenX operation identity:** `genxPublishVariableTermVersion` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxPublishVariableTermVersion`
- **GenX source module:** `VariableTerms`
- **Source tag:** VariableTerms
- **Proposed BrAPI-GenX classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C4 — Scientific terminology governance
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Publish a namespaced VariableTerm definition as a new immutable version, creating the term identity when new or appending a version when known.
**Source contract description:**
> Unknown variableDbId creates; known id with a new version appends;
> same (variableDbId, version) with an identical body replays the
> existing record; same pair with a different body is rejected with 409.
**Can be used for:**
- Publish a term definition with explicit version and provenance.
- Retry the same publication idempotently.
- Reject conflicting definitions for the same term identity and version.
**Must not be used for / explicit non-goals:**
- Silently editing a published version.
- Deleting a term used by historical observations.
- Merging cross-authority terms or asserting equivalence without a separate mapping contract.
- **Side effects:** Creates a term or a new immutable term version when valid.
- **Retry / idempotency:** Same identity/version plus identical body replays; same pair plus different body is a conflict.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** VariableTermNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxListVariableTermVersions, genxGetVariableTermVersion, V2.1 /brapi/v2/variables, SEM-06
- **Related catalogue IDs:** brapi-genx.brapi-v2-1.phenotyping.get.methods, brapi-genx.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-genx.brapi-v2-1.phenotyping.get.ontologies, brapi-genx.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-genx.brapi-v2-1.phenotyping.get.scales, brapi-genx.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-genx.brapi-v2-1.phenotyping.get.traits, brapi-genx.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-genx.brapi-v2-1.phenotyping.get.variables, brapi-genx.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-genx.brapi-v2-1.phenotyping.post.methods, brapi-genx.brapi-v2-1.phenotyping.post.ontologies, brapi-genx.brapi-v2-1.phenotyping.post.scales, brapi-genx.brapi-v2-1.phenotyping.post.traits, brapi-genx.brapi-v2-1.phenotyping.post.variables, brapi-genx.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-genx.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-genx.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-genx.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-genx.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-genx.genx.v1.variable-terms.get-version, brapi-genx.genx.v1.variable-terms.list
- **Relevant RFC / decision references:** RFC-002, A-03
- **Contract source:** [`Specification/BrAPI-GenX/VariableTerms/VariableTerms_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/VariableTerms/VariableTerms_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/genx/v1/variable-terms/{variableDbId}`

- **Catalogue ID:** `brapi-genx.genx.v1.variable-terms.get-version`
- **BrAPI-GenX operation identity:** `genxGetVariableTermVersion` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetVariableTermVersion`
- **GenX source module:** `VariableTerms`
- **Source tag:** VariableTerms
- **Proposed BrAPI-GenX classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C4 — Scientific terminology governance
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Retrieve a specific VariableTerm version, or the most recently created version when the version query parameter is omitted.
**Source contract description:**
> Returns the requested version, or the most recently created version when `version` is omitted. Version ordering semantics are requires-decision (see RFC-002 §5).
**Can be used for:**
- Resolve the exact term version referenced by a reproducible analysis when version is supplied.
- Read the latest-created version when no version is supplied.
**Must not be used for / explicit non-goals:**
- Assuming omitted-version lookup returns the highest semantic-version number; ordering semantics remain unresolved.
- Treating VariableTerm as the V2.1 OntologyTerm schema.
- Inferring cross-authority equivalence from a matching name.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** variableDbId, version
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** genxPublishVariableTermVersion, V2.1 OntologyTerm schema, SEM-06
- **Related catalogue IDs:** brapi-genx.brapi-v2-1.phenotyping.get.methods, brapi-genx.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-genx.brapi-v2-1.phenotyping.get.ontologies, brapi-genx.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-genx.brapi-v2-1.phenotyping.get.scales, brapi-genx.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-genx.brapi-v2-1.phenotyping.get.traits, brapi-genx.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-genx.brapi-v2-1.phenotyping.get.variables, brapi-genx.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-genx.brapi-v2-1.phenotyping.post.methods, brapi-genx.brapi-v2-1.phenotyping.post.ontologies, brapi-genx.brapi-v2-1.phenotyping.post.scales, brapi-genx.brapi-v2-1.phenotyping.post.traits, brapi-genx.brapi-v2-1.phenotyping.post.variables, brapi-genx.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-genx.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-genx.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-genx.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-genx.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-genx.genx.v1.variable-terms.list, brapi-genx.genx.v1.variable-terms.publish-version
- **Relevant RFC / decision references:** RFC-002, D-05, D-06, A-03
- **Contract source:** [`Specification/BrAPI-GenX/VariableTerms/VariableTerms_VariableDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/VariableTerms/VariableTerms_VariableDbId_GET.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### WeatherObservations — 3 operations

### GET `/genx/v1/weather-observations`

- **Catalogue ID:** `brapi-genx.genx.v1.weather-observations.list`
- **BrAPI-GenX operation identity:** `genxListWeatherObservations` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListWeatherObservations`
- **GenX source module:** `WeatherObservations`
- **Source tag:** WeatherObservations
- **Proposed BrAPI-GenX classification:** D5 — Environment, Agroecology and Field Context; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C7 — Streaming and temporal aggregation, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> List recorded weather/environmental observations, optionally filtered by station, location, variable, or time range.
**Source contract description:**
> Get a paged list of weather/environmental observations across authorities. Filters combine with AND.
**Can be used for:**
- Discover environmental conditions for a location or station.
- Provide environmental context for trials, studies, and crop models.
**Must not be used for / explicit non-goals:**
- Creating or changing an observation (use the POST endpoint).
- Assuming an observation is a BrAPI scientific Observation.
- Treating the list as a complete climate record.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** stationDbId, locationDbId, variableDbId, observedFrom, observedTo, page, pageSize, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxRecordWeatherObservation, genxGetWeatherObservation, genxQueryTelemetrySamplesOrAggregates
- **Related catalogue IDs:** brapi-genx.genx.v1.weather-observations.record, brapi-genx.genx.v1.weather-observations.get
- **Relevant RFC / decision references:** RFC-010
- **Contract source:** [`Specification/BrAPI-GenX/WeatherObservations/WeatherObservations_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/WeatherObservations/WeatherObservations_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/genx/v1/weather-observations`

- **Catalogue ID:** `brapi-genx.genx.v1.weather-observations.record`
- **BrAPI-GenX operation identity:** `genxRecordWeatherObservation` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxRecordWeatherObservation`
- **GenX source module:** `WeatherObservations`
- **Source tag:** WeatherObservations
- **Proposed BrAPI-GenX classification:** D5 — Environment, Agroecology and Field Context; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C6 — Artifact integrity and external references, C7 — Streaming and temporal aggregation, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Record one weather/environmental observation with measurements, quality flag, and provenance.
**Source contract description:**
> Unknown weatherObservationDbId creates; same id with an identical body replays the existing record; same id with a different body is rejected with 409.
**Can be used for:**
- Record measured environmental conditions at a station or location.
- Retry an identical observation safely using the same weatherObservationDbId.
**Must not be used for / explicit non-goals:**
- Updating or deleting an existing observation; corrections require a new record that supersedes.
- Assuming the observation is a BrAPI scientific Observation.
- Treating the record as a complete climate or forecast product.
- **Side effects:** Creates a weather observation when accepted.
- **Retry / idempotency:** Same weatherObservationDbId and identical body replays the existing record; same id with a different body is rejected with 409.
- **Parameters recorded in registry:** authorizationHeader
- **Request schema refs recorded:** WeatherObservationNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** genxListWeatherObservations, genxGetWeatherObservation, genxAppendTelemetryBatch
- **Related catalogue IDs:** brapi-genx.genx.v1.weather-observations.list, brapi-genx.genx.v1.weather-observations.get
- **Relevant RFC / decision references:** RFC-010
- **Contract source:** [`Specification/BrAPI-GenX/WeatherObservations/WeatherObservations_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/WeatherObservations/WeatherObservations_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/genx/v1/weather-observations/{weatherObservationDbId}`

- **Catalogue ID:** `brapi-genx.genx.v1.weather-observations.get`
- **BrAPI-GenX operation identity:** `genxGetWeatherObservation` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetWeatherObservation`
- **GenX source module:** `WeatherObservations`
- **Source tag:** WeatherObservations
- **Proposed BrAPI-GenX classification:** D5 — Environment, Agroecology and Field Context; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C7 — Streaming and temporal aggregation, C9 — Security, authority and tenancy
- **Classification review / confidence:** `defined-in-genx-proposal-community-review-pending` / `medium`
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Retrieve one recorded weather/environmental observation.
**Source contract description:**
> Returns the recorded observation, or 404.
**Can be used for:**
- Inspect measured environmental conditions and their provenance.
**Must not be used for / explicit non-goals:**
- Assuming the observation is a BrAPI scientific Observation.
- Treating a superseded observation as current.
- **Side effects:** Read-only.
- **Retry / idempotency:** Read-only.
- **Parameters recorded in registry:** weatherObservationDbId, authorizationHeader
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** genxRecordWeatherObservation, genxListWeatherObservations, genxQueryTelemetrySamplesOrAggregates
- **Related catalogue IDs:** brapi-genx.genx.v1.weather-observations.list, brapi-genx.genx.v1.weather-observations.record
- **Relevant RFC / decision references:** RFC-010
- **Contract source:** [`Specification/BrAPI-GenX/WeatherObservations/WeatherObservations_WeatherObservationDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-GenX/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/WeatherObservations/WeatherObservations_WeatherObservationDbId_GET.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.


## Non-normative status

Every operation in this view remains a proposal. This focused catalogue is generated from operation-level x-brapi-genx metadata and must not be edited independently. Change the OpenAPI operation metadata and master registry inputs, then regenerate this document and the all-generation catalogue.
