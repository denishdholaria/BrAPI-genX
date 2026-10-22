# BrAPI-GenX Endpoint Catalogue (Focused View)

> Generated from the master registry by Scripts/generateEndpointArtifacts.py on 2026-10-22. Do not edit by hand.

This is a focused view of the 21 proposed GenX operations, not a separate source of truth. The complete catalogue covering BrAPI v2.1 and GenX is the [master endpoint catalogue](../ENDPOINT-CATALOG.md); authoritative structured records live in the [master registry](../ENDPOINT-REGISTRY.json). The [BijMantra crosswalk](../BIJMANTRA-CROSSWALK.md) records source-level implementation candidates without implying runtime availability or contract equivalence.

| Source module | Operation count | Status |
|---|---:|---|
| FAIR | 3 | proposed, non-normative |
| Genomics | 3 | proposed, non-normative |
| Jobs | 4 | proposed, non-normative |
| LotLedger | 2 | proposed, non-normative |
| Models | 3 | proposed, non-normative |
| ServerInfoV3 | 1 | proposed, non-normative |
| Telemetry | 2 | proposed, non-normative |
| VariableTerms | 3 | proposed, non-normative |

## Operations

### FAIR — 3 operations

### GET `/brapi/v3/fair-packages`

- **Catalogue ID:** `brapi-den.genx.v3.fair-packages.list-metadata`
- **BrAPI-Den operation identity:** `genxListFairPackageMetadata` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListFairPackageMetadata`
- **GenX source module:** `FAIR`
- **Source tag:** FAIR Packages
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C5 — Data exchange, publication and access, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
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
- **Related catalogue IDs:** brapi-den.genx.v3.fair-packages.get-metadata, brapi-den.genx.v3.fair-packages.register
- **Relevant RFC / decision references:** RFC-006, D-13, D-14, D-15
- **Contract source:** [`Specification/BrAPI-GenX/FAIR/FairPackages_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/FAIR/FairPackages_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/brapi/v3/fair-packages`

- **Catalogue ID:** `brapi-den.genx.v3.fair-packages.register`
- **BrAPI-Den operation identity:** `genxRegisterFairPackage` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxRegisterFairPackage`
- **GenX source module:** `FAIR`
- **Source tag:** FAIR Packages
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C5 — Data exchange, publication and access, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
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
- **Related catalogue IDs:** brapi-den.genx.v3.fair-packages.get-metadata, brapi-den.genx.v3.fair-packages.list-metadata
- **Relevant RFC / decision references:** RFC-006, D-13, D-14, D-15
- **Contract source:** [`Specification/BrAPI-GenX/FAIR/FairPackages_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/FAIR/FairPackages_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/brapi/v3/fair-packages/{packageDbId}`

- **Catalogue ID:** `brapi-den.genx.v3.fair-packages.get-metadata`
- **BrAPI-Den operation identity:** `genxGetFairPackageMetadata` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetFairPackageMetadata`
- **GenX source module:** `FAIR`
- **Source tag:** FAIR Packages
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C5 — Data exchange, publication and access, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
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
- **Related catalogue IDs:** brapi-den.genx.v3.fair-packages.list-metadata, brapi-den.genx.v3.fair-packages.register
- **Relevant RFC / decision references:** RFC-006, D-15
- **Contract source:** [`Specification/BrAPI-GenX/FAIR/FairPackages_PackageDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/FAIR/FairPackages_PackageDbId_GET.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### Genomics — 3 operations

### GET `/brapi/v3/variantmatrices`

- **Catalogue ID:** `brapi-den.genx.v3.variant-matrices.list`
- **BrAPI-Den operation identity:** `genxListVariantMatrixReferences` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListVariantMatrixReferences`
- **GenX source module:** `Genomics`
- **Source tag:** Variant Matrices
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C5 — Data exchange, publication and access, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
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
- **Related catalogue IDs:** brapi-den.brapi-v2-1.genotyping.get.allelematrix, brapi-den.brapi-v2-1.genotyping.get.calls, brapi-den.brapi-v2-1.genotyping.get.callsets, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variants, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.callsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.variants, brapi-den.brapi-v2-1.genotyping.post.variantsets.extract, brapi-den.brapi-v2-1.genotyping.put.calls, brapi-den.genx.v3.variant-matrices.get, brapi-den.genx.v3.variant-matrices.register
- **Relevant RFC / decision references:** RFC-005, D-11, D-12, D-19
- **Contract source:** [`Specification/BrAPI-GenX/Genomics/VariantMatrices_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Genomics/VariantMatrices_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/brapi/v3/variantmatrices`

- **Catalogue ID:** `brapi-den.genx.v3.variant-matrices.register`
- **BrAPI-Den operation identity:** `genxRegisterVariantMatrixReference` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxRegisterVariantMatrixReference`
- **GenX source module:** `Genomics`
- **Source tag:** Variant Matrices
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C5 — Data exchange, publication and access, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
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
- **Related catalogue IDs:** brapi-den.brapi-v2-1.genotyping.get.allelematrix, brapi-den.brapi-v2-1.genotyping.get.calls, brapi-den.brapi-v2-1.genotyping.get.callsets, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variants, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.callsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.variants, brapi-den.brapi-v2-1.genotyping.post.variantsets.extract, brapi-den.brapi-v2-1.genotyping.put.calls, brapi-den.genx.v3.variant-matrices.get, brapi-den.genx.v3.variant-matrices.list
- **Relevant RFC / decision references:** RFC-005, D-11, D-12, D-19
- **Contract source:** [`Specification/BrAPI-GenX/Genomics/VariantMatrices_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Genomics/VariantMatrices_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/brapi/v3/variantmatrices/{matrixDbId}`

- **Catalogue ID:** `brapi-den.genx.v3.variant-matrices.get`
- **BrAPI-Den operation identity:** `genxGetVariantMatrixReference` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetVariantMatrixReference`
- **GenX source module:** `Genomics`
- **Source tag:** Variant Matrices
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C5 — Data exchange, publication and access, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
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
- **Related catalogue IDs:** brapi-den.brapi-v2-1.genotyping.get.allelematrix, brapi-den.brapi-v2-1.genotyping.get.calls, brapi-den.brapi-v2-1.genotyping.get.callsets, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variants, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.callsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.variants, brapi-den.brapi-v2-1.genotyping.post.variantsets.extract, brapi-den.brapi-v2-1.genotyping.put.calls, brapi-den.genx.v3.variant-matrices.list, brapi-den.genx.v3.variant-matrices.register
- **Relevant RFC / decision references:** RFC-005, D-11, D-12, D-19
- **Contract source:** [`Specification/BrAPI-GenX/Genomics/VariantMatrices_MatrixDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Genomics/VariantMatrices_MatrixDbId_GET.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### Jobs — 4 operations

### GET `/brapi/v3/jobs`

- **Catalogue ID:** `brapi-den.genx.v3.jobs.list`
- **BrAPI-Den operation identity:** `genxListJobs` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListJobs`
- **GenX source module:** `Jobs`
- **Source tag:** Jobs
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery, C3 — Asynchronous execution and idempotency, C9 — Security, authority and tenancy
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
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Relevant RFC / decision references:** RFC-001
- **Contract source:** [`Specification/BrAPI-GenX/Jobs/Jobs_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Jobs/Jobs_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/brapi/v3/jobs`

- **Catalogue ID:** `brapi-den.genx.v3.jobs.submit`
- **BrAPI-Den operation identity:** `genxSubmitAsyncJob` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxSubmitAsyncJob`
- **GenX source module:** `Jobs`
- **Source tag:** Jobs
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C9 — Security, authority and tenancy
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
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.models.get-version, brapi-den.genx.v3.models.list, brapi-den.genx.v3.models.register-version
- **Relevant RFC / decision references:** RFC-001, A-04, A-07
- **Contract source:** [`Specification/BrAPI-GenX/Jobs/Jobs_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Jobs/Jobs_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### DELETE `/brapi/v3/jobs/{jobDbId}`

- **Catalogue ID:** `brapi-den.genx.v3.jobs.request-cancellation`
- **BrAPI-Den operation identity:** `genxRequestAsyncJobCancellation` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxRequestAsyncJobCancellation`
- **GenX source module:** `Jobs`
- **Source tag:** Jobs
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C3 — Asynchronous execution and idempotency, C9 — Security, authority and tenancy
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
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.submit
- **Relevant RFC / decision references:** RFC-001
- **Contract source:** [`Specification/BrAPI-GenX/Jobs/Jobs_JobDbId_GET_DELETE.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Jobs/Jobs_JobDbId_GET_DELETE.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/brapi/v3/jobs/{jobDbId}`

- **Catalogue ID:** `brapi-den.genx.v3.jobs.get`
- **BrAPI-Den operation identity:** `genxGetAsyncJobById` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetAsyncJobById`
- **GenX source module:** `Jobs`
- **Source tag:** Jobs
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C9 — Security, authority and tenancy
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
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit, brapi-den.genx.v3.models.get-version, brapi-den.genx.v3.models.list, brapi-den.genx.v3.models.register-version
- **Relevant RFC / decision references:** RFC-001
- **Contract source:** [`Specification/BrAPI-GenX/Jobs/Jobs_JobDbId_GET_DELETE.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Jobs/Jobs_JobDbId_GET_DELETE.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### LotLedger — 2 operations

### GET `/brapi/v3/seedlots/{seedLotDbId}/ledger`

- **Catalogue ID:** `brapi-den.genx.v3.seed-lot-ledger.list`
- **BrAPI-Den operation identity:** `genxListSeedLotLedgerEntries` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListSeedLotLedgerEntries`
- **GenX source module:** `LotLedger`
- **Source tag:** Seed Lots
- **Proposed BrAPI-Den classification:** D6 — Crop Production and Material Operations; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
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
- **Related catalogue IDs:** brapi-den.brapi-v2-1.germplasm.get.seedlots.by-seedlotdbid.transactions, brapi-den.brapi-v2-1.germplasm.get.seedlots.transactions, brapi-den.brapi-v2-1.germplasm.post.seedlots.transactions, brapi-den.genx.v3.seed-lot-ledger.append
- **Relevant RFC / decision references:** RFC-003, D-07, D-08, D-20
- **Contract source:** [`Specification/BrAPI-GenX/LotLedger/Ledger_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/LotLedger/Ledger_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/brapi/v3/seedlots/{seedLotDbId}/ledger`

- **Catalogue ID:** `brapi-den.genx.v3.seed-lot-ledger.append`
- **BrAPI-Den operation identity:** `genxAppendSeedLotLedgerEntry` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxAppendSeedLotLedgerEntry`
- **GenX source module:** `LotLedger`
- **Source tag:** Seed Lots
- **Proposed BrAPI-Den classification:** D6 — Crop Production and Material Operations; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
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
- **Related catalogue IDs:** brapi-den.brapi-v2-1.germplasm.get.seedlots.by-seedlotdbid.transactions, brapi-den.brapi-v2-1.germplasm.get.seedlots.transactions, brapi-den.brapi-v2-1.germplasm.post.seedlots.transactions, brapi-den.genx.v3.seed-lot-ledger.list
- **Relevant RFC / decision references:** RFC-003, D-07, D-08, D-20, A-05, A-06
- **Contract source:** [`Specification/BrAPI-GenX/LotLedger/Ledger_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/LotLedger/Ledger_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### Models — 3 operations

### GET `/brapi/v3/models`

- **Catalogue ID:** `brapi-den.genx.v3.models.list`
- **BrAPI-Den operation identity:** `genxListModelVersions` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListModelVersions`
- **GenX source module:** `Models`
- **Source tag:** Models
- **Proposed BrAPI-Den classification:** D7 — Scientific Analysis, Models and Derived Evidence; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
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
- **Related catalogue IDs:** brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.submit, brapi-den.genx.v3.models.get-version, brapi-den.genx.v3.models.register-version
- **Relevant RFC / decision references:** RFC-004, D-09
- **Contract source:** [`Specification/BrAPI-GenX/Models/Models_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Models/Models_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/brapi/v3/models`

- **Catalogue ID:** `brapi-den.genx.v3.models.register-version`
- **BrAPI-Den operation identity:** `genxRegisterModelVersion` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxRegisterModelVersion`
- **GenX source module:** `Models`
- **Source tag:** Models
- **Proposed BrAPI-Den classification:** D7 — Scientific Analysis, Models and Derived Evidence; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
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
- **Related catalogue IDs:** brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.submit, brapi-den.genx.v3.models.get-version, brapi-den.genx.v3.models.list
- **Relevant RFC / decision references:** RFC-004, D-09, D-10
- **Contract source:** [`Specification/BrAPI-GenX/Models/Models_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Models/Models_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/brapi/v3/models/{modelDbId}`

- **Catalogue ID:** `brapi-den.genx.v3.models.get-version`
- **BrAPI-Den operation identity:** `genxGetModelVersion` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetModelVersion`
- **GenX source module:** `Models`
- **Source tag:** Models
- **Proposed BrAPI-Den classification:** D7 — Scientific Analysis, Models and Derived Evidence; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C6 — Artifact integrity and external references, C9 — Security, authority and tenancy
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
- **Related catalogue IDs:** brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.submit, brapi-den.genx.v3.models.list, brapi-den.genx.v3.models.register-version
- **Relevant RFC / decision references:** RFC-004, D-09, D-10
- **Contract source:** [`Specification/BrAPI-GenX/Models/Models_ModelDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Models/Models_ModelDbId_GET.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### ServerInfoV3 — 1 operations

### GET `/brapi/v3/serverinfo`

- **Catalogue ID:** `brapi-den.genx.v3.serverinfo.read`
- **BrAPI-Den operation identity:** `genxGetServerInfoV3` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetServerInfoV3`
- **GenX source module:** `ServerInfoV3`
- **Source tag:** Server Info
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery, C8 — Contract conformance and governance, C9 — Security, authority and tenancy
- **Standard / proposal status:** `proposal-non-normative`
- **Implementation status:** `reference-test-server-evidence-only`
**Purpose:**
> Advertise supported API generations, capabilities, and authentication profiles so clients can negotiate behavior before using optional GenX features.
**Source contract description:**
> GenX capability negotiation. Served under `/brapi/v3/`.
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
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.serverinfo
- **Relevant RFC / decision references:** RFC-001, A-01
- **Contract source:** [`Specification/BrAPI-GenX/ServerInfoV3/ServerInfoV3_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/ServerInfoV3/ServerInfoV3_GET.yaml)
- **BijMantra relative-route candidates:** 1. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - [backend/app/api/brapi/v2/core/serverinfo.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/serverinfo.py#L145) — `get_server_info`; brapi-adapter-source-declaration.
  - Interpretation: Same relative method/path appears in BijMantra's static inventory. Do not infer V3 wiring, contract equivalence, or runtime mounting.

### Telemetry — 2 operations

### GET `/brapi/v3/telemetry`

- **Catalogue ID:** `brapi-den.genx.v3.telemetry.query`
- **BrAPI-Den operation identity:** `genxQueryTelemetrySamplesOrAggregates` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxQueryTelemetrySamplesOrAggregates`
- **GenX source module:** `Telemetry`
- **Source tag:** Telemetry
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Context-dependent: D4 — Phenotyping and Plant Observations, D5 — Environment, Agroecology and Field Context; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C7 — Streaming and temporal aggregation, C9 — Security, authority and tenancy
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
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.telemetry.append-batch
- **Relevant RFC / decision references:** RFC-007, D-16, D-17, D-18
- **Contract source:** [`Specification/BrAPI-GenX/Telemetry/Telemetry_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Telemetry/Telemetry_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/brapi/v3/telemetry`

- **Catalogue ID:** `brapi-den.genx.v3.telemetry.append-batch`
- **BrAPI-Den operation identity:** `genxAppendTelemetryBatch` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxAppendTelemetryBatch`
- **GenX source module:** `Telemetry`
- **Source tag:** Telemetry
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Context-dependent: D4 — Phenotyping and Plant Observations, D5 — Environment, Agroecology and Field Context; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C3 — Asynchronous execution and idempotency, C7 — Streaming and temporal aggregation, C9 — Security, authority and tenancy
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
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.telemetry.query
- **Relevant RFC / decision references:** RFC-007, D-16, D-17, D-18
- **Contract source:** [`Specification/BrAPI-GenX/Telemetry/Telemetry_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/Telemetry/Telemetry_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### VariableTerms — 3 operations

### GET `/brapi/v3/variable-terms`

- **Catalogue ID:** `brapi-den.genx.v3.variable-terms.list`
- **BrAPI-Den operation identity:** `genxListVariableTermVersions` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxListVariableTermVersions`
- **GenX source module:** `VariableTerms`
- **Source tag:** VariableTerms
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C4 — Scientific terminology governance
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
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.variable-terms.get-version, brapi-den.genx.v3.variable-terms.publish-version
- **Relevant RFC / decision references:** RFC-002, A-03
- **Contract source:** [`Specification/BrAPI-GenX/VariableTerms/VariableTerms_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/VariableTerms/VariableTerms_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### POST `/brapi/v3/variable-terms`

- **Catalogue ID:** `brapi-den.genx.v3.variable-terms.publish-version`
- **BrAPI-Den operation identity:** `genxPublishVariableTermVersion` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxPublishVariableTermVersion`
- **GenX source module:** `VariableTerms`
- **Source tag:** VariableTerms
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C4 — Scientific terminology governance
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
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.variable-terms.get-version, brapi-den.genx.v3.variable-terms.list
- **Relevant RFC / decision references:** RFC-002, A-03
- **Contract source:** [`Specification/BrAPI-GenX/VariableTerms/VariableTerms_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/VariableTerms/VariableTerms_GET_POST.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.

### GET `/brapi/v3/variable-terms/{variableDbId}`

- **Catalogue ID:** `brapi-den.genx.v3.variable-terms.get-version`
- **BrAPI-Den operation identity:** `genxGetVariableTermVersion` (advisory where absent from source)
- **Source OpenAPI operationId:** `genxGetVariableTermVersion`
- **GenX source module:** `VariableTerms`
- **Source tag:** VariableTerms
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery, C2 — Provenance, evidence and uncertainty, C4 — Scientific terminology governance
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
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.variable-terms.list, brapi-den.genx.v3.variable-terms.publish-version
- **Relevant RFC / decision references:** RFC-002, D-05, D-06, A-03
- **Contract source:** [`Specification/BrAPI-GenX/VariableTerms/VariableTerms_VariableDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/proposal/scientific-domain-classification/Specification/BrAPI-GenX/VariableTerms/VariableTerms_VariableDbId_GET.yaml)
- **BijMantra relative-route candidates:** 0. Matching relative paths do not prove GenX v3 mounting or contract equivalence.
  - Interpretation: No exact relative method/path candidate was found in the supplied static inventory; this is not proof of runtime absence.


## Non-normative status

Every operation in this view remains a proposal. This focused catalogue is generated from operation-level x-brapi-den metadata and must not be edited independently. Change the OpenAPI operation metadata and master registry inputs, then regenerate this document and the all-generation catalogue.
