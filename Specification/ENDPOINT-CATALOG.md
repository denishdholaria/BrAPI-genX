# BrAPI-Den Master Endpoint Catalogue

> Generated from [ENDPOINT-REGISTRY.json](./ENDPOINT-REGISTRY.json) by Scripts/generateEndpointArtifacts.py on 2026-10-22. Do not edit by hand.

## Purpose and authority

This catalogue is the human-readable index for operation contracts and semantic boundaries. Source OpenAPI operations remain authoritative for wire contracts. The JSON registry is authoritative for catalogue identity, proposed crosswalk metadata, implementation-evidence status, and semantic-neighbor relationships.

A catalogue identifier does not replace a source operationId or route. Classification is a BrAPI-Den crosswalk, not an official BrAPI community reclassification. Static source declarations do not prove that an endpoint is mounted, reachable, secure, or conformant.

## Coverage

| Surface | Operations | Contract status |
|---|---:|---|
| BrAPI v2.1 official modules | 201 | Released specification; implementation availability not inferred |
| BrAPI GenX /brapi/v3 | 21 | Proposed, non-normative |
| **Total** | **222** | Existing contracts plus proposed operations |

BijMantra snapshot: 2240 records from the inventory generated 2026-10-17; see [source inventory](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md) and [crosswalk](./BIJMANTRA-CROSSWALK.md).

## Identity and review rules

1. Full identity uses API generation/base path, method, complete route template, source operationId when defined, schemas, side-effect/retry semantics, authorization boundary, and semantic neighbors.
2. The inspected BrAPI v2.1 source operations do not define OpenAPI operationId. recommendedOperationId values are advisory catalogue suggestions and do not edit the frozen v2.1 specifications.
3. Every operation should state supported uses and explicit non-goals. An HTTP route or summary alone is not enough.
4. Similar names, nearby domain classes, or shared relative routes do not prove wire equivalence or safe dual-write behavior.
5. BijMantra crosswalk entries are static source evidence; runtime availability and compatibility require separate validation.

## Semantic relationship register

| Relationship | Risk | Status | Summary |
|---|---|---|---|
| `OVERLAP-01` | medium | `versioned-contract` | Server capability discovery — Same broad discovery purpose across API generations; V2.1 ServerInfo and GenX ServerInfoV3 are not interchangeable payload contracts. |
| `SEM-01` | critical | `unresolved-semantic-overlap` | Seed-lot transactions versus ledger entries — Both can describe real-world material movement, but identity, quantity representation, ordering, atomicity and replay guarantees differ. No one-to-one event mapping or safe mirroring contract is established. |
| `SEM-02` | high | `complementary` | V2.1 search-results lifecycle versus GenX Jobs — Jobs is a general asynchronous-work lifecycle; V2.1 search operations use a search-specific lifecycle. A server may implement search through Jobs only when that behavior is explicitly advertised. |
| `SEM-03` | high | `distinct-with-possible-explicit-mapping` | Scientific observations versus telemetry samples — V2.1 observations are linked to observation variables and observation units/studies; GenX telemetry is a device/sensor time series. Mapping requires explicit variable, unit, time, quality, study/unit and provenance rules. |
| `SEM-04` | medium | `complementary-reference-not-data-replacement` | Genotyping records versus VariantMatrix references — VariantMatrix identifies and verifies an external matrix; it does not replace VariantSet, Variant, CallSet or Calls records and does not provide matrix bytes. |
| `SEM-05` | medium | `complementary-metadata-not-byte-transport` | File references versus FAIR packages — A FAIRPackage adds citation, licensing, access-rights and embargo metadata around payload references. It is not a payload-byte endpoint. The V2.1 metadata.datafiles schema is an adjacent schema-level concept. |
| `SEM-06` | medium | `distinct-schema-purpose` | Observation-variable definitions versus VariableTerm versions — V2.1 ObservationVariable and OntologyTerm contracts are not interchangeable with GenX's namespaced, versioned VariableTerm. Term equivalence and authority mapping need a separate rule. |
| `SEM-07` | medium | `distinct-resources` | Model registration versus inference execution — Model registry endpoints manage model metadata and lifecycle. Inference is submitted as a supported Job, not through a synchronous /models/{id}/infer operation. |

### OVERLAP-01 — Server capability discovery

**Risk / status:** medium / `versioned-contract`

Same broad discovery purpose across API generations; V2.1 ServerInfo and GenX ServerInfoV3 are not interchangeable payload contracts.

**BrAPI v2.1 catalogue IDs:** brapi-den.brapi-v2-1.core.get.serverinfo
**GenX catalogue IDs:** brapi-den.genx.v3.serverinfo.read
**Must not assume:**
- A V2.1 response contains GenX capability fields.
- The existence of the same relative route proves the same response schema.

### SEM-01 — Seed-lot transactions versus ledger entries

**Risk / status:** critical / `unresolved-semantic-overlap`

Both can describe real-world material movement, but identity, quantity representation, ordering, atomicity and replay guarantees differ. No one-to-one event mapping or safe mirroring contract is established.

**BrAPI v2.1 catalogue IDs:** brapi-den.brapi-v2-1.germplasm.get.seedlots.by-seedlotdbid.transactions, brapi-den.brapi-v2-1.germplasm.get.seedlots.transactions, brapi-den.brapi-v2-1.germplasm.post.seedlots.transactions
**GenX catalogue IDs:** brapi-den.genx.v3.seed-lot-ledger.list, brapi-den.genx.v3.seed-lot-ledger.append
**Decision:** `D-20`
**Must not assume:**
- Do not silently mirror one movement into both records.
- Do not double-count both streams as independent movements.
- Do not treat the GenX ledger as a drop-in replacement for V2.1 SeedLotTransaction.

### SEM-02 — V2.1 search-results lifecycle versus GenX Jobs

**Risk / status:** high / `complementary`

Jobs is a general asynchronous-work lifecycle; V2.1 search operations use a search-specific lifecycle. A server may implement search through Jobs only when that behavior is explicitly advertised.

**BrAPI v2.1 catalogue IDs:** brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid
**GenX catalogue IDs:** brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.submit, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.request-cancellation
**Must not assume:**
- Do not translate a V2.1 search-result identifier to a jobDbId.
- Do not assume a V2.1 search endpoint is replaced by Jobs.
- Do not assume a job type exists unless advertised.

### SEM-03 — Scientific observations versus telemetry samples

**Risk / status:** high / `distinct-with-possible-explicit-mapping`

V2.1 observations are linked to observation variables and observation units/studies; GenX telemetry is a device/sensor time series. Mapping requires explicit variable, unit, time, quality, study/unit and provenance rules.

**BrAPI v2.1 catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid
**GenX catalogue IDs:** brapi-den.genx.v3.telemetry.query, brapi-den.genx.v3.telemetry.append-batch
**Must not assume:**
- Do not convert telemetry to Observation records by field-name similarity.
- Do not infer an observation unit, study or observation variable from a device/sensor identifier.

### SEM-04 — Genotyping records versus VariantMatrix references

**Risk / status:** medium / `complementary-reference-not-data-replacement`

VariantMatrix identifies and verifies an external matrix; it does not replace VariantSet, Variant, CallSet or Calls records and does not provide matrix bytes.

**BrAPI v2.1 catalogue IDs:** brapi-den.brapi-v2-1.genotyping.get.allelematrix, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid, brapi-den.brapi-v2-1.genotyping.get.callsets, brapi-den.brapi-v2-1.genotyping.get.calls, brapi-den.brapi-v2-1.genotyping.put.calls, brapi-den.brapi-v2-1.genotyping.post.variantsets.extract, brapi-den.brapi-v2-1.genotyping.get.variantsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.callsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.variants, brapi-den.brapi-v2-1.genotyping.get.variants, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid
**GenX catalogue IDs:** brapi-den.genx.v3.variant-matrices.list, brapi-den.genx.v3.variant-matrices.register, brapi-den.genx.v3.variant-matrices.get
**Must not assume:**
- Do not expect matrix bytes from a VariantMatrix metadata endpoint.
- Do not treat VariantMatrix as a synonym for VariantSet or Calls.
- Do not assume GenX defines a new slicing or external-byte authorization protocol.

### SEM-05 — File references versus FAIR packages

**Risk / status:** medium / `complementary-metadata-not-byte-transport`

A FAIRPackage adds citation, licensing, access-rights and embargo metadata around payload references. It is not a payload-byte endpoint. The V2.1 metadata.datafiles schema is an adjacent schema-level concept.

**BrAPI v2.1 catalogue IDs:** —
**GenX catalogue IDs:** brapi-den.genx.v3.fair-packages.list-metadata, brapi-den.genx.v3.fair-packages.register, brapi-den.genx.v3.fair-packages.get-metadata
**Schema-level neighbors:** metadata.datafiles and external file retrieval links
**Must not assume:**
- Do not assume FAIRPackage uploads or stores payload bytes.
- Do not infer persistent-identifier minting or restricted-access approval workflows from registration.

### SEM-06 — Observation-variable definitions versus VariableTerm versions

**Risk / status:** medium / `distinct-schema-purpose`

V2.1 ObservationVariable and OntologyTerm contracts are not interchangeable with GenX's namespaced, versioned VariableTerm. Term equivalence and authority mapping need a separate rule.

**BrAPI v2.1 catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid
**GenX catalogue IDs:** brapi-den.genx.v3.variable-terms.list, brapi-den.genx.v3.variable-terms.publish-version, brapi-den.genx.v3.variable-terms.get-version
**Must not assume:**
- Do not treat VariableTerm as a replacement for V2.1 OntologyTerm.
- Do not infer term equivalence from labels.
- Do not assume full Trait/Method/Scale lifecycle or cross-authority mapping is standardized by RFC-002.

### SEM-07 — Model registration versus inference execution

**Risk / status:** medium / `distinct-resources`

Model registry endpoints manage model metadata and lifecycle. Inference is submitted as a supported Job, not through a synchronous /models/{id}/infer operation.

**BrAPI v2.1 catalogue IDs:** —
**GenX catalogue IDs:** brapi-den.genx.v3.models.list, brapi-den.genx.v3.models.register-version, brapi-den.genx.v3.models.get-version, brapi-den.genx.v3.jobs.submit, brapi-den.genx.v3.jobs.get
**Must not assume:**
- Do not infer training or inference from a model registration/read operation.
- Do not assume a revoked flag alone defines approval governance.
- Do not invent a synchronous inference route.

## BrAPI v2.1 — released official modules

### BrAPI-Core — 45 operations

### GET `/brapi/v2/commoncropnames`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.commoncropnames`
- **BrAPI-Den operation identity:** `brapiV21GetCommoncropnames` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Common Crop Names
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Crosswalk basis: unassigned; Crosswalk note: Generic reference, people, or list resource is not assigned to a proposed scientific domain without further review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the Common Crop Names
**Source contract description:**
> List the common crop names for the crops available in a database server. 
>
> This call is ** required ** for multi-crop systems where data from multiple 
> crops may be stored in the same database server. A distinct database server 
> is defined by everything in the URL before "/brapi/v2", including host 
> name and base path.
>
> This call is recommended for single crop systems to be compatible with 
> multi-crop clients. For a single crop system the response should contain 
> an array with exactly 1 element. 
>
> The common crop name can be used as a search parameter for Programs, 
> Studies, and Germplasm.
**Can be used for:**
- Get the Common Crop Names
- List the common crop names for the crops available in a database server. 
  
  This call is ** required ** for multi-crop systems where data from multiple 
  crops may be stored in the same database server. A distinct database server 
  is defined by everything in the URL before "/brapi/v2", including host 
  name and base path.
  
  This call is recommended for single crop systems to be compatible with 
  multi-crop clients. For a single crop system the response should contain 
  an array with exactly 1 element. 
  
  The common crop name can be used as a search parameter for Programs, 
  Studies, and Germplasm.
**Must not be used for / explicit non-goals:**
- Do not use this operation to create, update, or delete domain data.
- Do not assume runtime availability from the specification alone.
- **Side effects:** Read-only retrieval under the published BrAPI v2.1 contract.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Core/Common Crop Names/CommonCropNames_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Common%20Crop%20Names/CommonCropNames_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/commoncropnames.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/commoncropnames.py#L67) — `get_common_crop_names`; line 67; brapi-adapter-source-declaration.

### GET `/brapi/v2/lists`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.lists`
- **BrAPI-Den operation identity:** `brapiV21GetLists` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Lists
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Crosswalk basis: unassigned; Crosswalk note: Generic reference, people, or list resource is not assigned to a proposed scientific domain without further review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get filtered set of generic lists
**Source contract description:**
> Get filtered set of generic lists
**Can be used for:**
- Get filtered set of generic lists
- Get filtered set of generic lists
**Must not be used for / explicit non-goals:**
- Do not use this operation to create, update, or delete domain data.
- Do not assume runtime availability from the specification alone.
- **Side effects:** Read-only retrieval under the published BrAPI v2.1 contract.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** ListsListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Core/Lists/Lists_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Lists/Lists_GET_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/lists.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/lists.py#L88) — `get_lists`; line 88; brapi-adapter-source-declaration.

### POST `/brapi/v2/lists`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.post.lists`
- **BrAPI-Den operation identity:** `brapiV21PostLists` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Lists
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Crosswalk basis: unassigned; Crosswalk note: Generic reference, people, or list resource is not assigned to a proposed scientific domain without further review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Create New List Objects
**Source contract description:**
> Create new list objects in the database
**Can be used for:**
- Create New List Objects
- Create new list objects in the database
**Must not be used for / explicit non-goals:**
- Do not use this operation as a read-only list/get operation.
- Do not assume retries are idempotent unless the operation contract or server explicitly guarantees it.
- **Side effects:** State-changing submission or creation as specified by this operation; request/response schemas determine the exact effect.
- **Retry / idempotency:** The source specification does not declare an idempotency key or a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ListNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** ListsListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Core/Lists/Lists_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Lists/Lists_GET_POST.yaml)
- **BijMantra inventory row:** [line 54](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L54); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/lists.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/lists.py#L160) — `create_list`; line 160; brapi-adapter-source-declaration.

### GET `/brapi/v2/lists/{listDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.lists.by-listdbid`
- **BrAPI-Den operation identity:** `brapiV21GetListsByListDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Lists
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Crosswalk basis: unassigned; Crosswalk note: Generic reference, people, or list resource is not assigned to a proposed scientific domain without further review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the details of a specific List
**Source contract description:**
> Get a specific generic lists
**Can be used for:**
- Get the details of a specific List
- Get a specific generic lists
**Must not be used for / explicit non-goals:**
- Do not use this operation to create, update, or delete domain data.
- Do not assume runtime availability from the specification alone.
- **Side effects:** Read-only retrieval under the published BrAPI v2.1 contract.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** ListsSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Core/Lists/Lists_ListDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Lists/Lists_ListDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/lists.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/lists.py#L136) — `get_list`; line 136; brapi-adapter-source-declaration.

### PUT `/brapi/v2/lists/{listDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.put.lists.by-listdbid`
- **BrAPI-Den operation identity:** `brapiV21PutListsByListDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Lists
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Crosswalk basis: unassigned; Crosswalk note: Generic reference, people, or list resource is not assigned to a proposed scientific domain without further review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update an existing generic list
**Source contract description:**
> Update an existing generic list
**Can be used for:**
- Update an existing generic list
- Update an existing generic list
**Must not be used for / explicit non-goals:**
- Do not use this operation as a read-only list/get operation or as a generic deletion command.
- Do not infer concurrency control or field-level merge behavior unless the operation contract specifies it.
- **Side effects:** Updates or replaces the addressed resource(s) as specified by this operation.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ListNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** ListsSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Core/Lists/Lists_ListDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Lists/Lists_ListDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 31](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L31); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/lists.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/lists.py#L198) — `update_list`; line 198; brapi-adapter-source-declaration.

### POST `/brapi/v2/lists/{listDbId}/data`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.post.lists.by-listdbid.data`
- **BrAPI-Den operation identity:** `brapiV21PostListsByListDbIdData` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Lists
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Crosswalk basis: unassigned; Crosswalk note: Generic reference, people, or list resource is not assigned to a proposed scientific domain without further review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Add new data members to a specific List
**Source contract description:**
> Add new data members to a specific List
**Can be used for:**
- Add new data members to a specific List
- Add new data members to a specific List
**Must not be used for / explicit non-goals:**
- Do not use this operation as a read-only list/get operation.
- Do not assume retries are idempotent unless the operation contract or server explicitly guarantees it.
- **Side effects:** State-changing submission or creation as specified by this operation; request/response schemas determine the exact effect.
- **Retry / idempotency:** The source specification does not declare an idempotency key or a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Core/Lists/Lists_ListDbId_Data_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Lists/Lists_ListDbId_Data_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/lists.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/lists.py#L284) — `set_list_data`; line 284; brapi-adapter-source-declaration.

### POST `/brapi/v2/lists/{listDbId}/items`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.post.lists.by-listdbid.items`
- **BrAPI-Den operation identity:** `brapiV21PostListsByListDbIdItems` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Lists
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Crosswalk basis: unassigned; Crosswalk note: Generic reference, people, or list resource is not assigned to a proposed scientific domain without further review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Add Items to a specific List
**Source contract description:**
> **Deprecated in v2.1** Please use `POST /lists/{listDbId}/data`. Github issue number #444 
> <br/> Add new data to a specific generic lists
**Can be used for:**
- Add Items to a specific List
- **Deprecated in v2.1** Please use `POST /lists/{listDbId}/data`. Github issue number #444 
  <br/> Add new data to a specific generic lists
**Must not be used for / explicit non-goals:**
- Do not use this operation as a read-only list/get operation.
- Do not assume retries are idempotent unless the operation contract or server explicitly guarantees it.
- **Side effects:** State-changing submission or creation as specified by this operation; request/response schemas determine the exact effect.
- **Retry / idempotency:** The source specification does not declare an idempotency key or a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Core/Lists/Lists_ListDbId_Items_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Lists/Lists_ListDbId_Items_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/lists.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/lists.py#L249) — `add_list_items`; line 249; brapi-adapter-source-declaration.

### GET `/brapi/v2/locations`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.locations`
- **BrAPI-Den operation identity:** `brapiV21GetLocations` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Locations
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Locations commonly provide the spatial context for trials/studies; confirm in the domain crosswalk.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get a filtered list of Locations
**Source contract description:**
> Get a list of locations.
> * The `countryCode` is as per [ISO_3166-1_alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) spec.
> * `altitude` is in meters.
**Can be used for:**
- Get a filtered list of Locations
- Get a list of locations.
  * The `countryCode` is as per [ISO_3166-1_alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) spec.
  * `altitude` is in meters.
**Must not be used for / explicit non-goals:**
- Do not use this operation to create, update, or delete domain data.
- Do not assume runtime availability from the specification alone.
- **Side effects:** Read-only retrieval under the published BrAPI v2.1 contract.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** locationType
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** LocationListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Core/Locations/Locations_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Locations/Locations_GET_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/locations.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/locations.py#L49) — `list_locations`; line 49; brapi-adapter-source-declaration.

### POST `/brapi/v2/locations`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.post.locations`
- **BrAPI-Den operation identity:** `brapiV21PostLocations` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Locations
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Locations commonly provide the spatial context for trials/studies; confirm in the domain crosswalk.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Create new Locations
**Source contract description:**
> Add new locations to database
> * The `countryCode` is as per [ISO_3166-1_alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) spec.
> * `altitude` is in meters.
**Can be used for:**
- Create new Locations
- Add new locations to database
  * The `countryCode` is as per [ISO_3166-1_alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) spec.
  * `altitude` is in meters.
**Must not be used for / explicit non-goals:**
- Do not use this operation as a read-only list/get operation.
- Do not assume retries are idempotent unless the operation contract or server explicitly guarantees it.
- **Side effects:** State-changing submission or creation as specified by this operation; request/response schemas determine the exact effect.
- **Retry / idempotency:** The source specification does not declare an idempotency key or a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** LocationNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** LocationListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Core/Locations/Locations_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Locations/Locations_GET_POST.yaml)
- **BijMantra inventory row:** [line 71](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L71); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/locations.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/locations.py#L118) — `create_location`; line 118; brapi-adapter-source-declaration.

### GET `/brapi/v2/locations/{locationDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.locations.by-locationdbid`
- **BrAPI-Den operation identity:** `brapiV21GetLocationsByLocationDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Locations
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Locations commonly provide the spatial context for trials/studies; confirm in the domain crosswalk.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the details of a specific Location
**Source contract description:**
> Get details for a location.
> - The `countryCode` is as per [ISO_3166-1_alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) spec.
> - `altitude` is in meters.'
**Can be used for:**
- Get the details of a specific Location
- Get details for a location.
  - The `countryCode` is as per [ISO_3166-1_alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) spec.
  - `altitude` is in meters.'
**Must not be used for / explicit non-goals:**
- Do not use this operation to create, update, or delete domain data.
- Do not assume runtime availability from the specification alone.
- **Side effects:** Read-only retrieval under the published BrAPI v2.1 contract.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** LocationSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Core/Locations/Locations_LocationDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Locations/Locations_LocationDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/locations.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/locations.py#L85) — `get_location`; line 85; brapi-adapter-source-declaration.

### PUT `/brapi/v2/locations/{locationDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.put.locations.by-locationdbid`
- **BrAPI-Den operation identity:** `brapiV21PutLocationsByLocationDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Locations
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Locations commonly provide the spatial context for trials/studies; confirm in the domain crosswalk.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update the details for an existing Location
**Source contract description:**
> Update the details for an existing location.
> - The `countryCode` is as per [ISO_3166-1_alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) spec.
> - `altitude` is in meters.'
**Can be used for:**
- Update the details for an existing Location
- Update the details for an existing location.
  - The `countryCode` is as per [ISO_3166-1_alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) spec.
  - `altitude` is in meters.'
**Must not be used for / explicit non-goals:**
- Do not use this operation as a read-only list/get operation or as a generic deletion command.
- Do not infer concurrency control or field-level merge behavior unless the operation contract specifies it.
- **Side effects:** Updates or replaces the addressed resource(s) as specified by this operation.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** LocationNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** LocationSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Core/Locations/Locations_LocationDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Locations/Locations_LocationDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 34](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L34); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/locations.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/locations.py#L153) — `update_location`; line 153; brapi-adapter-source-declaration.

### GET `/brapi/v2/people`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.people`
- **BrAPI-Den operation identity:** `brapiV21GetPeople` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** People
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Crosswalk basis: unassigned; Crosswalk note: Generic reference, people, or list resource is not assigned to a proposed scientific domain without further review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get filtered list of People
**Source contract description:**
> Get filtered list of people
**Can be used for:**
- Get filtered list of People
- Get filtered list of people
**Must not be used for / explicit non-goals:**
- Do not use this operation to create, update, or delete domain data.
- Do not assume runtime availability from the specification alone.
- **Side effects:** Read-only retrieval under the published BrAPI v2.1 contract.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** PersonListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Core/People/People_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/People/People_GET_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/people.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/people.py#L152) — `list_people`; line 152; brapi-adapter-source-declaration.

### POST `/brapi/v2/people`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.post.people`
- **BrAPI-Den operation identity:** `brapiV21PostPeople` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** People
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Crosswalk basis: unassigned; Crosswalk note: Generic reference, people, or list resource is not assigned to a proposed scientific domain without further review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Create new People
**Source contract description:**
> Create new People entities. `personDbId` is generated and managed by the server.
**Can be used for:**
- Create new People
- Create new People entities. `personDbId` is generated and managed by the server.
**Must not be used for / explicit non-goals:**
- Do not use this operation as a read-only list/get operation.
- Do not assume retries are idempotent unless the operation contract or server explicitly guarantees it.
- **Side effects:** State-changing submission or creation as specified by this operation; request/response schemas determine the exact effect.
- **Retry / idempotency:** The source specification does not declare an idempotency key or a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** PersonNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** PersonListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Core/People/People_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/People/People_GET_POST.yaml)
- **BijMantra inventory row:** [line 54](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L54); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/people.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/people.py#L234) — `create_person`; line 234; brapi-adapter-source-declaration.

### GET `/brapi/v2/people/{personDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.people.by-persondbid`
- **BrAPI-Den operation identity:** `brapiV21GetPeopleByPersonDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** People
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Crosswalk basis: unassigned; Crosswalk note: Generic reference, people, or list resource is not assigned to a proposed scientific domain without further review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the details for a specific Person
**Source contract description:**
> Get the details for a specific Person
**Can be used for:**
- Get the details for a specific Person
- Get the details for a specific Person
**Must not be used for / explicit non-goals:**
- Do not use this operation to create, update, or delete domain data.
- Do not assume runtime availability from the specification alone.
- **Side effects:** Read-only retrieval under the published BrAPI v2.1 contract.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** PersonSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Core/People/People_PersonDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/People/People_PersonDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/people.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/people.py#L205) — `get_person`; line 205; brapi-adapter-source-declaration.

### PUT `/brapi/v2/people/{personDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.put.people.by-persondbid`
- **BrAPI-Den operation identity:** `brapiV21PutPeopleByPersonDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** People
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Crosswalk basis: unassigned; Crosswalk note: Generic reference, people, or list resource is not assigned to a proposed scientific domain without further review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update an existing Person
**Source contract description:**
> Update an existing Person
**Can be used for:**
- Update an existing Person
- Update an existing Person
**Must not be used for / explicit non-goals:**
- Do not use this operation as a read-only list/get operation or as a generic deletion command.
- Do not infer concurrency control or field-level merge behavior unless the operation contract specifies it.
- **Side effects:** Updates or replaces the addressed resource(s) as specified by this operation.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** PersonNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** PersonSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Core/People/People_PersonDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/People/People_PersonDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 31](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L31); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/people.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/people.py#L273) — `update_person`; line 273; brapi-adapter-source-declaration.

### GET `/brapi/v2/programs`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.programs`
- **BrAPI-Den operation identity:** `brapiV21GetPrograms` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Programs
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Programs, trials, studies and seasons provide breeding/experimental context.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get a filtered list of breeding Programs
**Source contract description:**
> Get a filtered list of breeding Programs. This list can be filtered by common crop name to narrow results to a specific crop.
**Can be used for:**
- Get a filtered list of breeding Programs
- Get a filtered list of breeding Programs. This list can be filtered by common crop name to narrow results to a specific crop.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** abbreviation, programType
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** ProgramListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Core/Programs/Programs_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Programs/Programs_GET_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/programs.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/programs.py#L46) — `list_programs`; line 46; brapi-adapter-source-declaration.

### POST `/brapi/v2/programs`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.post.programs`
- **BrAPI-Den operation identity:** `brapiV21PostPrograms` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Programs
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Programs, trials, studies and seasons provide breeding/experimental context.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Add new breeding Programs to the database
**Source contract description:**
> Add new breeding Programs to the database. The `programDbId` is set by the server, all other fields are take from the request body, or a default value is used.
**Can be used for:**
- Add new breeding Programs to the database
- Add new breeding Programs to the database. The `programDbId` is set by the server, all other fields are take from the request body, or a default value is used.
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; request and response schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ProgramNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** ProgramListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Core/Programs/Programs_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Programs/Programs_GET_POST.yaml)
- **BijMantra inventory row:** [line 49](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L49); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/programs.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/programs.py#L123) — `create_program`; line 123; brapi-adapter-source-declaration.

### GET `/brapi/v2/programs/{programDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.programs.by-programdbid`
- **BrAPI-Den operation identity:** `brapiV21GetProgramsByProgramDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Programs
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Programs, trials, studies and seasons provide breeding/experimental context.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get a breeding Program by Id
**Source contract description:**
> Get a single breeding Program by Id. This can be used to quickly get the details of a Program when you have the Id from another entity.
**Can be used for:**
- Get a breeding Program by Id
- Get a single breeding Program by Id. This can be used to quickly get the details of a Program when you have the Id from another entity.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** programDbId
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** ProgramSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Core/Programs/Programs_ProgramDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Programs/Programs_ProgramDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/programs.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/programs.py#L89) — `get_program`; line 89; brapi-adapter-source-declaration.

### PUT `/brapi/v2/programs/{programDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.put.programs.by-programdbid`
- **BrAPI-Den operation identity:** `brapiV21PutProgramsByProgramDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Programs
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Programs, trials, studies and seasons provide breeding/experimental context.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update an existing Program
**Source contract description:**
> Update the details of an existing breeding Program.
**Can be used for:**
- Update an existing Program
- Update the details of an existing breeding Program.
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer field-level merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces the addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** programDbId
- **Request schema refs recorded:** ProgramNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** ProgramSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Core/Programs/Programs_ProgramDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Programs/Programs_ProgramDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 31](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L31); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/programs.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/programs.py#L166) — `update_program`; line 166; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/lists`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.post.search.lists`
- **BrAPI-Den operation identity:** `brapiV21PostSearchLists` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Lists
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Crosswalk basis: unassigned; Crosswalk note: Generic reference, people, or list resource is not assigned to a proposed scientific domain without further review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for Lists
**Source contract description:**
> Submit a search request for Lists <br/>
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/lists/{searchResultsDbId}` to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for Lists
- Submit a search request for Lists <br/>
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/lists/{searchResultsDbId}` to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat this as creating or updating the searched domain resource; it submits a search request.
- Search request replay/deduplication behavior is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results resource may be created. Domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare an idempotency key or a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ListSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** ListsListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Core/Lists/Search_Lists_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Lists/Search_Lists_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L717) — `search_lists`; line 717; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/lists/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchListsBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Lists
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Crosswalk basis: unassigned; Crosswalk note: Generic reference, people, or list resource is not assigned to a proposed scientific domain without further review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a `List` search request
**Source contract description:**
> Get the results of a `List` search request <br/>
> Clients should submit a search request using the corresponding `POST /search/lists` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Get the results of a `List` search request
- Get the results of a `List` search request <br/>
  Clients should submit a search request using the corresponding `POST /search/lists` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not use this operation to submit a new search; it retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results; no domain-resource mutation is implied.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, ListsListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Core/Lists/Search_Lists_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Lists/Search_Lists_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L765) — `get_search_lists_results`; line 765; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/locations`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.post.search.locations`
- **BrAPI-Den operation identity:** `brapiV21PostSearchLocations` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Locations
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Locations commonly provide the spatial context for trials/studies; confirm in the domain crosswalk.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for `Locations`
**Source contract description:**
> Submit a search request for `Locations`<br/>
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/locations/{searchResultsDbId}` to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for `Locations`
- Submit a search request for `Locations`<br/>
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/locations/{searchResultsDbId}` to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat this as creating or updating the searched domain resource; it submits a search request.
- Search request replay/deduplication behavior is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results resource may be created. Domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare an idempotency key or a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** LocationSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** LocationListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Core/Locations/Search_Locations_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Locations/Search_Locations_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L649) — `search_locations`; line 649; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/locations/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchLocationsBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Locations
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Locations commonly provide the spatial context for trials/studies; confirm in the domain crosswalk.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a `Locations` search request
**Source contract description:**
> Get the results of a `Locations` search request <br/>
> Clients should submit a search request using the corresponding `POST /search/location` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Get the results of a `Locations` search request
- Get the results of a `Locations` search request <br/>
  Clients should submit a search request using the corresponding `POST /search/location` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not use this operation to submit a new search; it retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results; no domain-resource mutation is implied.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, LocationListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Core/Locations/Search_Locations_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Locations/Search_Locations_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L696) — `get_search_locations_results`; line 696; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/people`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.post.search.people`
- **BrAPI-Den operation identity:** `brapiV21PostSearchPeople` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** People
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Crosswalk basis: unassigned; Crosswalk note: Generic reference, people, or list resource is not assigned to a proposed scientific domain without further review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for `People`
**Source contract description:**
> Submit a search request for `People`<br/>
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/people/{searchResultsDbId}` to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for `People`
- Submit a search request for `People`<br/>
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/people/{searchResultsDbId}` to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat this as creating or updating the searched domain resource; it submits a search request.
- Search request replay/deduplication behavior is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results resource may be created. Domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare an idempotency key or a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** PersonSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** PersonListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Core/People/Search_People_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/People/Search_People_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L786) — `search_people`; line 786; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/people/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchPeopleBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** People
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Crosswalk basis: unassigned; Crosswalk note: Generic reference, people, or list resource is not assigned to a proposed scientific domain without further review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a `People` search request
**Source contract description:**
> Get the results of a `People` search request <br/>
> Clients should submit a search request using the corresponding `POST /search/people` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Get the results of a `People` search request
- Get the results of a `People` search request <br/>
  Clients should submit a search request using the corresponding `POST /search/people` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not use this operation to submit a new search; it retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results; no domain-resource mutation is implied.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, PersonListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Core/People/Search_People_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/People/Search_People_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L827) — `get_search_people_results`; line 827; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/programs`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.post.search.programs`
- **BrAPI-Den operation identity:** `brapiV21PostSearchPrograms` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Programs
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Programs, trials, studies and seasons provide breeding/experimental context.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for `Programs`
**Source contract description:**
> Submit a search request for `Programs`<br/>
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/programs/{searchResultsDbId}` to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for `Programs`
- Submit a search request for `Programs`<br/>
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/programs/{searchResultsDbId}` to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat this as creating or updating the searched domain resource; it submits a search request.
- Search replay/deduplication is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results record may be created; domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ProgramSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** ProgramListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Core/Programs/Search_Programs_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Programs/Search_Programs_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L451) — `search_programs`; line 451; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/programs/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchProgramsBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Programs
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Programs, trials, studies and seasons provide breeding/experimental context.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a `Programs` search request
**Source contract description:**
> Get the results of a `Programs` search request <br/>
> Clients should submit a search request using the corresponding `POST /search/programs` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Get the results of a `Programs` search request
- Get the results of a `Programs` search request <br/>
  Clients should submit a search request using the corresponding `POST /search/programs` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not use to submit a new search; retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, ProgramListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Core/Programs/Search_Programs_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Programs/Search_Programs_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L491) — `get_search_programs_results`; line 491; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/studies`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.post.search.studies`
- **BrAPI-Den operation identity:** `brapiV21PostSearchStudies` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Studies
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Programs, trials, studies and seasons provide breeding/experimental context.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for `Studies`
**Source contract description:**
> Submit a search request for `Studies`<br/>
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/studies/{searchResultsDbId}` to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for `Studies`
- Submit a search request for `Studies`<br/>
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/studies/{searchResultsDbId}` to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat this as creating or updating the searched domain resource; it submits a search request.
- Search replay/deduplication is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results record may be created; domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** StudySearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** StudyListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Core/Studies/Search_Studies_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Studies/Search_Studies_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L512) — `search_studies`; line 512; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/studies/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchStudiesBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Studies
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Programs, trials, studies and seasons provide breeding/experimental context.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a `Studies` search request
**Source contract description:**
> Get the results of a `Studies` search request <br/>
> Clients should submit a search request using the corresponding `POST /search/studies` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Get the results of a `Studies` search request
- Get the results of a `Studies` search request <br/>
  Clients should submit a search request using the corresponding `POST /search/studies` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not use to submit a new search; retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, StudyListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Core/Studies/Search_Studies_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Studies/Search_Studies_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L560) — `get_search_studies_results`; line 560; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/trials`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.post.search.trials`
- **BrAPI-Den operation identity:** `brapiV21PostSearchTrials` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Trials
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Programs, trials, studies and seasons provide breeding/experimental context.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for `Trials`
**Source contract description:**
> Submit a search request for `Trials`<br/>
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/trials/{searchResultsDbId}` to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for `Trials`
- Submit a search request for `Trials`<br/>
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/trials/{searchResultsDbId}` to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat this as creating or updating the searched domain resource; it submits a search request.
- Search replay/deduplication is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results record may be created; domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** TrialSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** TrialListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Core/Trials/Search_Trials_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Trials/Search_Trials_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L581) — `search_trials`; line 581; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/trials/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchTrialsBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Trials
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Programs, trials, studies and seasons provide breeding/experimental context.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a `Trials` search request
**Source contract description:**
> Get the results of a `Trials` search request <br/>
> Clients should submit a search request using the corresponding `POST /search/trials` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Get the results of a `Trials` search request
- Get the results of a `Trials` search request <br/>
  Clients should submit a search request using the corresponding `POST /search/trials` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not use to submit a new search; retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, TrialListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Core/Trials/Search_Trials_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Trials/Search_Trials_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L628) — `get_search_trials_results`; line 628; brapi-adapter-source-declaration.

### GET `/brapi/v2/seasons`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.seasons`
- **BrAPI-Den operation identity:** `brapiV21GetSeasons` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Seasons
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Programs, trials, studies and seasons provide breeding/experimental context.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the Seasons
**Source contract description:**
> Call to retrieve all seasons in the database.
>
> A season is made of 2 parts; the primary year and a term which defines a segment of the year. 
> This could be a traditional season, like "Spring" or "Summer" or this could be a month, like 
> "May" or "June" or this could be an arbitrary season name which is meaningful to the breeding 
> program like "PlantingTime_3" or "Season E
**Can be used for:**
- Get the Seasons
- Call to retrieve all seasons in the database.
  
  A season is made of 2 parts; the primary year and a term which defines a segment of the year. 
  This could be a traditional season, like "Spring" or "Summer" or this could be a month, like 
  "May" or "June" or this could be an arbitrary season name which is meaningful to the breeding 
  program like "PlantingTime_3" or "Season E
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** SeasonListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Core/Seasons/Seasons_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Seasons/Seasons_GET_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/seasons.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/seasons.py#L37) — `list_seasons`; line 37; brapi-adapter-source-declaration.

### POST `/brapi/v2/seasons`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.post.seasons`
- **BrAPI-Den operation identity:** `brapiV21PostSeasons` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Seasons
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Programs, trials, studies and seasons provide breeding/experimental context.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> POST new Seasons
**Source contract description:**
> Add new season entries to the database
**Can be used for:**
- POST new Seasons
- Add new season entries to the database
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; request and response schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** Season
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** SeasonListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Core/Seasons/Seasons_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Seasons/Seasons_GET_POST.yaml)
- **BijMantra inventory row:** [line 59](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L59); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/seasons.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/seasons.py#L79) — `create_season`; line 79; brapi-adapter-source-declaration.

### GET `/brapi/v2/seasons/{seasonDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.seasons.by-seasondbid`
- **BrAPI-Den operation identity:** `brapiV21GetSeasonsBySeasonDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Seasons
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Programs, trials, studies and seasons provide breeding/experimental context.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the a single Season
**Source contract description:**
> Get the a single Season
**Can be used for:**
- Get the a single Season
- Get the a single Season
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** SeasonSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Core/Seasons/Seasons_SeasonDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Seasons/Seasons_SeasonDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/seasons.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/seasons.py#L58) — `get_season`; line 58; brapi-adapter-source-declaration.

### PUT `/brapi/v2/seasons/{seasonDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.put.seasons.by-seasondbid`
- **BrAPI-Den operation identity:** `brapiV21PutSeasonsBySeasonDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Seasons
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Programs, trials, studies and seasons provide breeding/experimental context.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update existing Seasons
**Source contract description:**
> Update existing Seasons
**Can be used for:**
- Update existing Seasons
- Update existing Seasons
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer field-level merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces the addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** Season
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** SeasonSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Core/Seasons/Seasons_SeasonDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Seasons/Seasons_SeasonDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 32](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L32); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/seasons.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/seasons.py#L99) — `update_season`; line 99; brapi-adapter-source-declaration.

### GET `/brapi/v2/serverinfo`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.serverinfo`
- **BrAPI-Den operation identity:** `brapiV21GetServerinfo` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Server Info
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C1 — Identity, versioning and capability discovery; Crosswalk basis: inferred-from-route; Crosswalk note: Server capability discovery is cross-cutting.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the list of implemented Calls
**Source contract description:**
> Implementation Notes
>
> Having a consistent structure for the path string of each call is very 
> important for teams to be able to connect and find errors. Read more on Github.
>
> Here are the rules for the path of each call that should be returned
>
> Every word in the call path should match the documentation exactly, both in 
> spelling and capitalization. Note that path strings are all lower case, but 
> path parameters are camel case.
>
> Each path should start relative to \"/\" and therefore should not include \"/\"
>
> No leading or trailing slashes (\"/\") 
>
> Path parameters are wrapped in curly braces (\"{}\"). The name of the path parameter 
> should be spelled exactly as it is specified in the documentation.
>
> Examples 
>
> GOOD   "call": "germplasm/{germplasmDbId}/pedigree" 
>
> BAD    "call": "germplasm/{id}/pedigree"
>
> BAD    "call": "germplasm/{germplasmDBid}/pedigree" 
>
> BAD    "call": "brapi/v2/germplasm/{germplasmDbId}/pedigree" 
>
> BAD    "call": "/germplasm/{germplasmDbId}/pedigree/" 
>
> BAD    "call": "germplasm/<germplasmDbId>/pedigree
**Can be used for:**
- Get the list of implemented Calls
- Implementation Notes
  
  Having a consistent structure for the path string of each call is very 
  important for teams to be able to connect and find errors. Read more on Github.
  
  Here are the rules for the path of each call that should be returned
  
  Every word in the call path should match the documentation exactly, both in 
  spelling and capitalization. Note that path strings are all lower case, but 
  path parameters are camel case.
  
  Each path should start relative to \"/\" and therefore should not include \"/\"
  
  No leading or trailing slashes (\"/\") 
  
  Path parameters are wrapped in curly braces (\"{}\"). The name of the path parameter 
  should be spelled exactly as it is specified in the documentation.
  
  Examples 
  
  GOOD   "call": "germplasm/{germplasmDbId}/pedigree" 
  
  BAD    "call": "germplasm/{id}/pedigree"
  
  BAD    "call": "germplasm/{germplasmDBid}/pedigree" 
  
  BAD    "call": "brapi/v2/germplasm/{germplasmDbId}/pedigree" 
  
  BAD    "call": "/germplasm/{germplasmDbId}/pedigree/" 
  
  BAD    "call": "germplasm/<germplasmDbId>/pedigree
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** OVERLAP-01
- **Related catalogue IDs:** brapi-den.genx.v3.serverinfo.read
- **Contract source:** [`Specification/BrAPI-Core/ServerInfo/ServerInfo_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/ServerInfo/ServerInfo_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/serverinfo.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/serverinfo.py#L145) — `get_server_info`; line 145; brapi-adapter-source-declaration.

### GET `/brapi/v2/studies`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.studies`
- **BrAPI-Den operation identity:** `brapiV21GetStudies` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Studies
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Programs, trials, studies and seasons provide breeding/experimental context.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get a filtered list of Studies
**Source contract description:**
> Get list of studies
>
> StartDate and endDate should be ISO-8601 format for dates
**Can be used for:**
- Get a filtered list of Studies
- Get list of studies
  
  StartDate and endDate should be ISO-8601 format for dates
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** StudyListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Core/Studies/Studies_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Studies/Studies_GET_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/studies.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/studies.py#L44) — `list_studies`; line 44; brapi-adapter-source-declaration.

### POST `/brapi/v2/studies`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.post.studies`
- **BrAPI-Den operation identity:** `brapiV21PostStudies` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Studies
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Programs, trials, studies and seasons provide breeding/experimental context.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Create new Studies.
**Source contract description:**
> Create new studies
>
> Implementation Notes
>
> StartDate and endDate should be ISO-8601 format for dates
>
> `studyDbId` is generated by the server.
**Can be used for:**
- Create new Studies.
- Create new studies
  
  Implementation Notes
  
  StartDate and endDate should be ISO-8601 format for dates
  
  `studyDbId` is generated by the server.
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; request and response schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** StudyNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** StudyListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Core/Studies/Studies_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Studies/Studies_GET_POST.yaml)
- **BijMantra inventory row:** [line 108](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L108); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/studies.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/studies.py#L110) — `create_study`; line 110; brapi-adapter-source-declaration.

### GET `/brapi/v2/studies/{studyDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.studies.by-studydbid`
- **BrAPI-Den operation identity:** `brapiV21GetStudiesByStudyDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Studies
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Programs, trials, studies and seasons provide breeding/experimental context.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the details for a specific Study
**Source contract description:**
> Retrieve the information of the study required for field data collection
>
> An additionalInfo field was added to provide a controlled vocabulary for less common data fields.
**Can be used for:**
- Get the details for a specific Study
- Retrieve the information of the study required for field data collection
  
  An additionalInfo field was added to provide a controlled vocabulary for less common data fields.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** StudySingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Core/Studies/Studies_StudyDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Studies/Studies_StudyDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/studies.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/studies.py#L79) — `get_study`; line 79; brapi-adapter-source-declaration.

### PUT `/brapi/v2/studies/{studyDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.put.studies.by-studydbid`
- **BrAPI-Den operation identity:** `brapiV21PutStudiesByStudyDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Studies
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Programs, trials, studies and seasons provide breeding/experimental context.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update an existing Study
**Source contract description:**
> Update an existing Study with new data
**Can be used for:**
- Update an existing Study
- Update an existing Study with new data
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer field-level merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces the addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** StudyNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** StudySingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Core/Studies/Studies_StudyDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Studies/Studies_StudyDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 34](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L34); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/studies.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/studies.py#L141) — `update_study`; line 141; brapi-adapter-source-declaration.

### GET `/brapi/v2/studytypes`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.studytypes`
- **BrAPI-Den operation identity:** `brapiV21GetStudytypes` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Studies
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Crosswalk basis: unassigned; Crosswalk note: Generic shared/reference resource is not assigned to a scientific domain without review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the Study Types
**Source contract description:**
> Call to retrieve the list of study types.
**Can be used for:**
- Get the Study Types
- Call to retrieve the list of study types.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Core/Studies/StudyTypes_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Studies/StudyTypes_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/studytypes.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/studytypes.py#L47) — `get_study_types`; line 47; brapi-adapter-source-declaration.

### GET `/brapi/v2/trials`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.trials`
- **BrAPI-Den operation identity:** `brapiV21GetTrials` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Trials
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Programs, trials, studies and seasons provide breeding/experimental context.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get a filtered list of Trials
**Source contract description:**
> Retrieve a filtered list of breeding Trials. A Trial is a collection of Studies
**Can be used for:**
- Get a filtered list of Trials
- Retrieve a filtered list of breeding Trials. A Trial is a collection of Studies
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** active, contactDbId, locationDbId, searchDateRangeStart, searchDateRangeEnd, trialPUI, sortBy, sortOrder
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** TrialListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Core/Trials/Trials_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Trials/Trials_GET_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/trials.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/trials.py#L52) — `list_trials`; line 52; brapi-adapter-source-declaration.

### POST `/brapi/v2/trials`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.post.trials`
- **BrAPI-Den operation identity:** `brapiV21PostTrials` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Trials
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Programs, trials, studies and seasons provide breeding/experimental context.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Create new trials
**Source contract description:**
> Create new breeding Trials. A Trial represents a collection of related Studies. `trialDbId` is generated by the server.
**Can be used for:**
- Create new trials
- Create new breeding Trials. A Trial represents a collection of related Studies. `trialDbId` is generated by the server.
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; request and response schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** TrialNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** TrialListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Core/Trials/Trials_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Trials/Trials_GET_POST.yaml)
- **BijMantra inventory row:** [line 118](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L118); static evidence only.
- **BijMantra static route crosswalk:** 2 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/trials.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/trials.py#L124) — `create_trial`; line 124; brapi-adapter-source-declaration.
  - [backend/app/modules/space/lunar/router.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/modules/space/lunar/router.py#L50) — `create_trial`; line 50; same-route-collision-other-module.

### GET `/brapi/v2/trials/{trialDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.get.trials.by-trialdbid`
- **BrAPI-Den operation identity:** `brapiV21GetTrialsByTrialDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Trials
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Programs, trials, studies and seasons provide breeding/experimental context.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the details of a specific Trial
**Source contract description:**
> Get the details of a specific Trial
**Can be used for:**
- Get the details of a specific Trial
- Get the details of a specific Trial
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** TrialSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Core/Trials/Trials_TrialDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Trials/Trials_TrialDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 3 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/trials.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/trials.py#L90) — `get_trial`; line 90; brapi-adapter-source-declaration.
  - [backend/app/modules/space/lunar/router.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/modules/space/lunar/router.py#L63) — `get_trial`; line 63; same-route-collision-other-module.
  - [backend/app/modules/space/mars/router.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/modules/space/mars/router.py#L58) — `get_trial`; line 58; same-route-collision-other-module.

### PUT `/brapi/v2/trials/{trialDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.core.put.trials.by-trialdbid`
- **BrAPI-Den operation identity:** `brapiV21PutTrialsByTrialDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Core
- **Source tag:** Trials
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Programs, trials, studies and seasons provide breeding/experimental context.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update the details of an existing Trial
**Source contract description:**
> Update the details of an existing Trial
**Can be used for:**
- Update the details of an existing Trial
- Update the details of an existing Trial
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** TrialNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** TrialSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Core/Trials/Trials_TrialDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Core/Trials/Trials_TrialDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 31](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L31); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/trials.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/trials.py#L167) — `update_trial`; line 167; brapi-adapter-source-declaration.

### BrAPI-Germplasm — 46 operations

### GET `/brapi/v2/attributes`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.attributes`
- **BrAPI-Den operation identity:** `brapiV21GetAttributes` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm Attributes
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the Germplasm Attributes
**Source contract description:**
> List available attributes.
**Can be used for:**
- Get the Germplasm Attributes
- List available attributes.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** attributeCategory, attributeDbId, attributeName, attributePUI
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** GermplasmAttributeListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm_Attributes/Attributes_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm_Attributes/Attributes_GET_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/attributes.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/attributes.py#L81) — `get_attributes`; line 81; brapi-adapter-source-declaration.

### POST `/brapi/v2/attributes`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.post.attributes`
- **BrAPI-Den operation identity:** `brapiV21PostAttributes` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm Attributes
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Create new Germplasm Attributes
**Source contract description:**
> Create new Germplasm Attributes
**Can be used for:**
- Create new Germplasm Attributes
- Create new Germplasm Attributes
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** GermplasmAttributeNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** GermplasmAttributeListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm_Attributes/Attributes_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm_Attributes/Attributes_GET_POST.yaml)
- **BijMantra inventory row:** [line 64](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L64); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/attributes.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/attributes.py#L187) — `create_attributes`; line 187; brapi-adapter-source-declaration.

### GET `/brapi/v2/attributes/categories`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.attributes.categories`
- **BrAPI-Den operation identity:** `brapiV21GetAttributesCategories` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm Attributes
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the Categories of Germplasm Attributes
**Source contract description:**
> List all available attribute categories.
**Can be used for:**
- Get the Categories of Germplasm Attributes
- List all available attribute categories.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm_Attributes/Attributes_Categories_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm_Attributes/Attributes_Categories_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/attributes.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/attributes.py#L138) — `get_attribute_categories`; line 138; brapi-adapter-source-declaration.

### GET `/brapi/v2/attributes/{attributeDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.attributes.by-attributedbid`
- **BrAPI-Den operation identity:** `brapiV21GetAttributesByAttributeDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm Attributes
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the details for a specific Germplasm Attribute
**Source contract description:**
> Get the details for a specific Germplasm Attribute
**Can be used for:**
- Get the details for a specific Germplasm Attribute
- Get the details for a specific Germplasm Attribute
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** attributeDbId
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** GermplasmAttributeSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm_Attributes/Attributes_AttributeDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm_Attributes/Attributes_AttributeDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/attributes.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/attributes.py#L164) — `get_attribute`; line 164; brapi-adapter-source-declaration.

### PUT `/brapi/v2/attributes/{attributeDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.put.attributes.by-attributedbid`
- **BrAPI-Den operation identity:** `brapiV21PutAttributesByAttributeDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm Attributes
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update an existing Germplasm Attribute
**Source contract description:**
> Update an existing Germplasm Attribute
**Can be used for:**
- Update an existing Germplasm Attribute
- Update an existing Germplasm Attribute
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** attributeDbId
- **Request schema refs recorded:** GermplasmAttributeNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** GermplasmAttributeSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm_Attributes/Attributes_AttributeDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm_Attributes/Attributes_AttributeDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 31](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L31); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/attributes.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/attributes.py#L215) — `update_attribute`; line 215; brapi-adapter-source-declaration.

### GET `/brapi/v2/attributevalues`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.attributevalues`
- **BrAPI-Den operation identity:** `brapiV21GetAttributevalues` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm Attribute Values
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the Germplasm Attribute Values
**Source contract description:**
> Get the Germplasm Attribute Values
**Can be used for:**
- Get the Germplasm Attribute Values
- Get the Germplasm Attribute Values
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** attributeValueDbId, attributeDbId, attributeName
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** GermplasmAttributeValueListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm_Attribute_Values/AttributesValues_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm_Attribute_Values/AttributesValues_GET_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/attributevalues.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/attributevalues.py#L97) — `get_attribute_values`; line 97; brapi-adapter-source-declaration.

### POST `/brapi/v2/attributevalues`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.post.attributevalues`
- **BrAPI-Den operation identity:** `brapiV21PostAttributevalues` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm Attribute Values
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Create new Germplasm Attribute Values
**Source contract description:**
> Create new Germplasm Attribute Values
**Can be used for:**
- Create new Germplasm Attribute Values
- Create new Germplasm Attribute Values
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** GermplasmAttributeValueNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** GermplasmAttributeValueListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm_Attribute_Values/AttributesValues_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm_Attribute_Values/AttributesValues_GET_POST.yaml)
- **BijMantra inventory row:** [line 49](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L49); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/attributevalues.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/attributevalues.py#L171) — `create_attribute_values`; line 171; brapi-adapter-source-declaration.

### GET `/brapi/v2/attributevalues/{attributeValueDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.attributevalues.by-attributevaluedbid`
- **BrAPI-Den operation identity:** `brapiV21GetAttributevaluesByAttributeValueDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm Attribute Values
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the details for a specific Germplasm Attribute
**Source contract description:**
> Get the details for a specific Germplasm Attribute
**Can be used for:**
- Get the details for a specific Germplasm Attribute
- Get the details for a specific Germplasm Attribute
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** attributeValueDbId
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** GermplasmAttributeValueSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm_Attribute_Values/AttributeValues_AttributeValueDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm_Attribute_Values/AttributeValues_AttributeValueDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/attributevalues.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/attributevalues.py#L149) — `get_attribute_value`; line 149; brapi-adapter-source-declaration.

### PUT `/brapi/v2/attributevalues/{attributeValueDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.put.attributevalues.by-attributevaluedbid`
- **BrAPI-Den operation identity:** `brapiV21PutAttributevaluesByAttributeValueDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm Attribute Values
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update an existing Germplasm Attribute Value
**Source contract description:**
> Update an existing Germplasm Attribute Value
**Can be used for:**
- Update an existing Germplasm Attribute Value
- Update an existing Germplasm Attribute Value
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** attributeValueDbId
- **Request schema refs recorded:** GermplasmAttributeValueNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** GermplasmAttributeValueSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm_Attribute_Values/AttributeValues_AttributeValueDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm_Attribute_Values/AttributeValues_AttributeValueDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 31](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L31); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/attributevalues.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/attributevalues.py#L235) — `update_attribute_value`; line 235; brapi-adapter-source-declaration.

### GET `/brapi/v2/breedingmethods`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.breedingmethods`
- **BrAPI-Den operation identity:** `brapiV21GetBreedingmethods` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Crossing, pedigree, progeny and breeding-method concepts relate to breeding processes.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the Breeding Methods
**Source contract description:**
> Get the list of germplasm breeding methods available in a system.
**Can be used for:**
- Get the Breeding Methods
- Get the list of germplasm breeding methods available in a system.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm/BreedingMethods_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm/BreedingMethods_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/breedingmethods.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/breedingmethods.py#L116) — `get_breeding_methods`; line 116; brapi-adapter-source-declaration.

### GET `/brapi/v2/breedingmethods/{breedingMethodDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.breedingmethods.by-breedingmethoddbid`
- **BrAPI-Den operation identity:** `brapiV21GetBreedingmethodsByBreedingMethodDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Crossing, pedigree, progeny and breeding-method concepts relate to breeding processes.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the details of a specific Breeding Method
**Source contract description:**
> Get the details of a specific Breeding Method used to produce Germplasm
**Can be used for:**
- Get the details of a specific Breeding Method
- Get the details of a specific Breeding Method used to produce Germplasm
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm/BreedingMethods_BreedingMethodDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm/BreedingMethods_BreedingMethodDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/breedingmethods.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/breedingmethods.py#L136) — `get_breeding_method`; line 136; brapi-adapter-source-declaration.

### GET `/brapi/v2/crosses`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.crosses`
- **BrAPI-Den operation identity:** `brapiV21GetCrosses` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Crosses
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Crossing, pedigree, progeny and breeding-method concepts relate to breeding processes.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get a filtered list of Cross entities
**Source contract description:**
> Get a filtered list of Cross entities.
**Can be used for:**
- Get a filtered list of Cross entities
- Get a filtered list of Cross entities.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** crossingProjectDbId, crossingProjectName, crossDbId, crossName
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** CrossesListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Germplasm/Crosses/Crosses_GET_POST_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Crosses/Crosses_GET_POST_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/crosses.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/crosses.py#L37) — `list_crosses`; line 37; brapi-adapter-source-declaration.

### POST `/brapi/v2/crosses`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.post.crosses`
- **BrAPI-Den operation identity:** `brapiV21PostCrosses` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Crosses
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Crossing, pedigree, progeny and breeding-method concepts relate to breeding processes.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Create new Cross entities on this server
**Source contract description:**
> Create new Cross entities on this server
**Can be used for:**
- Create new Cross entities on this server
- Create new Cross entities on this server
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** CrossNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** CrossesListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Germplasm/Crosses/Crosses_GET_POST_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Crosses/Crosses_GET_POST_PUT.yaml)
- **BijMantra inventory row:** [line 54](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L54); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/crosses.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/crosses.py#L67) — `create_cross`; line 67; brapi-adapter-source-declaration.

### PUT `/brapi/v2/crosses`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.put.crosses`
- **BrAPI-Den operation identity:** `brapiV21PutCrosses` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Crosses
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Crossing, pedigree, progeny and breeding-method concepts relate to breeding processes.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update existing Cross entities on this server
**Source contract description:**
> Update existing Cross entities on this server
**Can be used for:**
- Update existing Cross entities on this server
- Update existing Cross entities on this server
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** CrossNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** CrossesListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Germplasm/Crosses/Crosses_GET_POST_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Crosses/Crosses_GET_POST_PUT.yaml)
- **BijMantra inventory row:** [line 77](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L77); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/crosses.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/crosses.py#L118) — `update_crosses`; line 118; brapi-adapter-source-declaration.

### GET `/brapi/v2/crossingprojects`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.crossingprojects`
- **BrAPI-Den operation identity:** `brapiV21GetCrossingprojects` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Crossing Projects
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Crossing, pedigree, progeny and breeding-method concepts relate to breeding processes.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get a filtered list of Crossing Projects
**Source contract description:**
> Get a filtered list of Crossing Projects.
**Can be used for:**
- Get a filtered list of Crossing Projects
- Get a filtered list of Crossing Projects.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** crossingProjectDbId, crossingProjectName, includePotentialParents
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** CrossingProjectsListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Germplasm/CrossingProjects/CrossingProjects_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/CrossingProjects/CrossingProjects_GET_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/crossingprojects.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/crossingprojects.py#L83) — `get_crossing_projects`; line 83; brapi-adapter-source-declaration.

### POST `/brapi/v2/crossingprojects`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.post.crossingprojects`
- **BrAPI-Den operation identity:** `brapiV21PostCrossingprojects` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Crossing Projects
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Crossing, pedigree, progeny and breeding-method concepts relate to breeding processes.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Create new Crossing Project entities on this server
**Source contract description:**
> Create new Crossing Project entities on this server
**Can be used for:**
- Create new Crossing Project entities on this server
- Create new Crossing Project entities on this server
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** CrossingProjectNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** CrossingProjectsListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Germplasm/CrossingProjects/CrossingProjects_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/CrossingProjects/CrossingProjects_GET_POST.yaml)
- **BijMantra inventory row:** [line 48](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L48); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/crossingprojects.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/crossingprojects.py#L177) — `create_crossing_projects`; line 177; brapi-adapter-source-declaration.

### GET `/brapi/v2/crossingprojects/{crossingProjectDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.crossingprojects.by-crossingprojectdbid`
- **BrAPI-Den operation identity:** `brapiV21GetCrossingprojectsByCrossingProjectDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Crossing Projects
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Crossing, pedigree, progeny and breeding-method concepts relate to breeding processes.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get a filtered list of Crossing Projects
**Source contract description:**
> Get a filtered list of Crossing Projects.
**Can be used for:**
- Get a filtered list of Crossing Projects
- Get a filtered list of Crossing Projects.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** crossingProjectDbId
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** CrossingProjectsSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Germplasm/CrossingProjects/CrossingProjects_CrossingProjectDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/CrossingProjects/CrossingProjects_CrossingProjectDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/crossingprojects.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/crossingprojects.py#L145) — `get_crossing_project`; line 145; brapi-adapter-source-declaration.

### PUT `/brapi/v2/crossingprojects/{crossingProjectDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.put.crossingprojects.by-crossingprojectdbid`
- **BrAPI-Den operation identity:** `brapiV21PutCrossingprojectsByCrossingProjectDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Crossing Projects
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Crossing, pedigree, progeny and breeding-method concepts relate to breeding processes.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update an existing Crossing Project
**Source contract description:**
> Update an existing Crossing Project entity on this server
**Can be used for:**
- Update an existing Crossing Project
- Update an existing Crossing Project entity on this server
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** crossingProjectDbId
- **Request schema refs recorded:** CrossingProjectNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** CrossingProjectsSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Germplasm/CrossingProjects/CrossingProjects_CrossingProjectDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/CrossingProjects/CrossingProjects_CrossingProjectDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 31](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L31); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/crossingprojects.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/crossingprojects.py#L228) — `update_crossing_project`; line 228; brapi-adapter-source-declaration.

### GET `/brapi/v2/germplasm`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.germplasm`
- **BrAPI-Den operation identity:** `brapiV21GetGermplasm` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get a filtered list of Germplasm
**Source contract description:**
> Addresses these needs
>
> - General germplasm search mechanism that accepts POST for complex queries 
>
> - Possibility to search germplasm by more parameters than those allowed by the existing germplasm search 
>
> - Possibility to get MCPD details by PUID rather than dbId
**Can be used for:**
- Get a filtered list of Germplasm
- Addresses these needs
  
  - General germplasm search mechanism that accepts POST for complex queries 
  
  - Possibility to search germplasm by more parameters than those allowed by the existing germplasm search 
  
  - Possibility to get MCPD details by PUID rather than dbId
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** accessionNumber, collection, binomialName, genus, species, synonym, parentDbId, progenyDbId
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** GermplasmListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm/Germplasm_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm/Germplasm_GET_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/domains/germplasm/capabilities/accession_passport/adapters/api/brapi_germplasm.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/domains/germplasm/capabilities/accession_passport/adapters/api/brapi_germplasm.py#L63) — `list_germplasm`; line 63; brapi-adapter-source-declaration.

### POST `/brapi/v2/germplasm`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.post.germplasm`
- **BrAPI-Den operation identity:** `brapiV21PostGermplasm` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Create new Germplasm entities on this server
**Source contract description:**
> Create new Germplasm entities on this server
**Can be used for:**
- Create new Germplasm entities on this server
- Create new Germplasm entities on this server
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** GermplasmNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** GermplasmListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm/Germplasm_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm/Germplasm_GET_POST.yaml)
- **BijMantra inventory row:** [line 93](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L93); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/domains/germplasm/capabilities/accession_passport/adapters/api/brapi_germplasm.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/domains/germplasm/capabilities/accession_passport/adapters/api/brapi_germplasm.py#L105) — `create_germplasm`; line 105; brapi-adapter-source-declaration.

### GET `/brapi/v2/germplasm/{germplasmDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.germplasm.by-germplasmdbid`
- **BrAPI-Den operation identity:** `brapiV21GetGermplasmByGermplasmDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the details of a specific Germplasm
**Source contract description:**
> Germplasm Details by germplasmDbId was merged with Germplasm Multi Crop Passport Data. The MCPD fields are optional and marked with the prefix [MCPD].
**Can be used for:**
- Get the details of a specific Germplasm
- Germplasm Details by germplasmDbId was merged with Germplasm Multi Crop Passport Data. The MCPD fields are optional and marked with the prefix [MCPD].
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** GermplasmSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm/Germplasm_GermplasmDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm/Germplasm_GermplasmDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/domains/germplasm/capabilities/accession_passport/adapters/api/brapi_germplasm.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/domains/germplasm/capabilities/accession_passport/adapters/api/brapi_germplasm.py#L133) — `get_germplasm`; line 133; brapi-adapter-source-declaration.

### PUT `/brapi/v2/germplasm/{germplasmDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.put.germplasm.by-germplasmdbid`
- **BrAPI-Den operation identity:** `brapiV21PutGermplasmByGermplasmDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update the details of an existing Germplasm
**Source contract description:**
> Germplasm Details by germplasmDbId was merged with Germplasm Multi Crop Passport Data. The MCPD fields are optional and marked with the prefix [MCPD].
**Can be used for:**
- Update the details of an existing Germplasm
- Germplasm Details by germplasmDbId was merged with Germplasm Multi Crop Passport Data. The MCPD fields are optional and marked with the prefix [MCPD].
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** GermplasmNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** GermplasmSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm/Germplasm_GermplasmDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm/Germplasm_GermplasmDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 31](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L31); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/domains/germplasm/capabilities/accession_passport/adapters/api/brapi_germplasm.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/domains/germplasm/capabilities/accession_passport/adapters/api/brapi_germplasm.py#L165) — `update_germplasm`; line 165; brapi-adapter-source-declaration.

### GET `/brapi/v2/germplasm/{germplasmDbId}/mcpd`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.germplasm.by-germplasmdbid.mcpd`
- **BrAPI-Den operation identity:** `brapiV21GetGermplasmByGermplasmDbIdMcpd` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the details of a specific Germplasm in MCPD format
**Source contract description:**
> Get all MCPD details of a germplasm
>
> <a target="_blank" href="https://www.bioversityInternational.org/fileadmin/user_upload/online_library/publications/pdfs/FAOBIOVERSITY_MULTI-CROP_PASSPORT_DESCRIPTORS_V.2.1_2015_2020.pdf"> MCPD v2.1 spec can be found here </a>
>
> Implementation Notes
>
> - When the MCPD spec identifies a field which can have multiple values returned, the JSON response should be an array instead of a semi-colon separated string.
**Can be used for:**
- Get the details of a specific Germplasm in MCPD format
- Get all MCPD details of a germplasm
  
  <a target="_blank" href="https://www.bioversityInternational.org/fileadmin/user_upload/online_library/publications/pdfs/FAOBIOVERSITY_MULTI-CROP_PASSPORT_DESCRIPTORS_V.2.1_2015_2020.pdf"> MCPD v2.1 spec can be found here </a>
  
  Implementation Notes
  
  - When the MCPD spec identifies a field which can have multiple values returned, the JSON response should be an array instead of a semi-colon separated string.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm/Germplasm_GermplasmDbId_MCPD_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm/Germplasm_GermplasmDbId_MCPD_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/domains/germplasm/capabilities/accession_passport/adapters/api/brapi_germplasm.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/domains/germplasm/capabilities/accession_passport/adapters/api/brapi_germplasm.py#L326) — `get_germplasm_mcpd`; line 326; brapi-adapter-source-declaration.

### GET `/brapi/v2/germplasm/{germplasmDbId}/pedigree`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.germplasm.by-germplasmdbid.pedigree`
- **BrAPI-Den operation identity:** `brapiV21GetGermplasmByGermplasmDbIdPedigree` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Crossing, pedigree, progeny and breeding-method concepts relate to breeding processes.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> **Deprecated in v2.1** Please use `GET /pedigree?germplasmDbId={germplasmDbId}`. Github issue number #481 
> <br/> Get the pedigree details of a specific Germplasm
**Source contract description:**
> **Deprecated in v2.1** Please use `GET /pedigree?germplasmDbId={germplasmDbId}`. Github issue number #481 
> <br/> Get the parentage information of a specific Germplasm
**Can be used for:**
- **Deprecated in v2.1** Please use `GET /pedigree?germplasmDbId={germplasmDbId}`. Github issue number #481 
  <br/> Get the pedigree details of a specific Germplasm
- **Deprecated in v2.1** Please use `GET /pedigree?germplasmDbId={germplasmDbId}`. Github issue number #481 
  <br/> Get the parentage information of a specific Germplasm
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm/Germplasm_GermplasmDbId_Pedigree_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm/Germplasm_GermplasmDbId_Pedigree_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/domains/germplasm/capabilities/accession_passport/adapters/api/brapi_germplasm.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/domains/germplasm/capabilities/accession_passport/adapters/api/brapi_germplasm.py#L250) — `get_germplasm_pedigree`; line 250; brapi-adapter-source-declaration.

### GET `/brapi/v2/germplasm/{germplasmDbId}/progeny`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.germplasm.by-germplasmdbid.progeny`
- **BrAPI-Den operation identity:** `brapiV21GetGermplasmByGermplasmDbIdProgeny` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Crossing, pedigree, progeny and breeding-method concepts relate to breeding processes.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> **Deprecated in v2.1** Please use `GET /pedigree?germplasmDbId={germplasmDbId}`. Github issue number #481 
> <br/> Get the progeny details of a specific Germplasm
**Source contract description:**
> **Deprecated in v2.1** Please use `GET /pedigree?germplasmDbId={germplasmDbId}`. Github issue number #481 
> <br/> Get the germplasmDbIds for all the Progeny of a particular germplasm.
> <br/> Implementation Notes
> <br/> - Regarding the ''parentType'' field in the progeny object. Given a germplasm A having a progeny B and C, ''parentType'' for progeny B refers to the ''parentType'' of A toward B.
**Can be used for:**
- **Deprecated in v2.1** Please use `GET /pedigree?germplasmDbId={germplasmDbId}`. Github issue number #481 
  <br/> Get the progeny details of a specific Germplasm
- **Deprecated in v2.1** Please use `GET /pedigree?germplasmDbId={germplasmDbId}`. Github issue number #481 
  <br/> Get the germplasmDbIds for all the Progeny of a particular germplasm.
  <br/> Implementation Notes
  <br/> - Regarding the ''parentType'' field in the progeny object. Given a germplasm A having a progeny B and C, ''parentType'' for progeny B refers to the ''parentType'' of A toward B.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm/Germplasm_GermplasmDbId_Progeny_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm/Germplasm_GermplasmDbId_Progeny_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/domains/germplasm/capabilities/accession_passport/adapters/api/brapi_germplasm.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/domains/germplasm/capabilities/accession_passport/adapters/api/brapi_germplasm.py#L288) — `get_germplasm_progeny`; line 288; brapi-adapter-source-declaration.

### GET `/brapi/v2/pedigree`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.pedigree`
- **BrAPI-Den operation identity:** `brapiV21GetPedigree` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Pedigree
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Crossing, pedigree, progeny and breeding-method concepts relate to breeding processes.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get a filtered list of pedigree nodes which represent a subset of a pedigree tree
**Source contract description:**
> Get a filtered list of pedigree nodes which represent a subset of a pedigree tree
**Can be used for:**
- Get a filtered list of pedigree nodes which represent a subset of a pedigree tree
- Get a filtered list of pedigree nodes which represent a subset of a pedigree tree
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** accessionNumber, collection, familyCode, binomialName, genus, species, synonym
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** PedigreeListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Germplasm/Pedigree/Pedigree_GET_POST_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Pedigree/Pedigree_GET_POST_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/pedigree.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/pedigree.py#L256) — `get_pedigree_brapi`; line 256; brapi-adapter-source-declaration.

### POST `/brapi/v2/pedigree`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.post.pedigree`
- **BrAPI-Den operation identity:** `brapiV21PostPedigree` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Pedigree
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Crossing, pedigree, progeny and breeding-method concepts relate to breeding processes.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Send a list of new pedigree nodes to a server
**Source contract description:**
> Send a list of new pedigree nodes to a server
**Can be used for:**
- Send a list of new pedigree nodes to a server
- Send a list of new pedigree nodes to a server
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** PedigreeNode
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** PedigreeListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Germplasm/Pedigree/Pedigree_GET_POST_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Pedigree/Pedigree_GET_POST_PUT.yaml)
- **BijMantra inventory row:** [line 118](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L118); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/core/pedigree.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/core/pedigree.py#L293) — `create_pedigree_brapi`; line 293; brapi-adapter-source-declaration.

### PUT `/brapi/v2/pedigree`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.put.pedigree`
- **BrAPI-Den operation identity:** `brapiV21PutPedigree` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Pedigree
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Crossing, pedigree, progeny and breeding-method concepts relate to breeding processes.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Send a list of pedigree nodes to update existing information on a server
**Source contract description:**
> Send a list of pedigree nodes to update existing information on a server
**Can be used for:**
- Send a list of pedigree nodes to update existing information on a server
- Send a list of pedigree nodes to update existing information on a server
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** PedigreeNode
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** PedigreeListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Germplasm/Pedigree/Pedigree_GET_POST_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Pedigree/Pedigree_GET_POST_PUT.yaml)
- **BijMantra inventory row:** [line 143](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L143); static evidence only.
- **BijMantra static route crosswalk:** 0 exact normalized method/path candidate(s); 0 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - No exact normalized source declaration was found. This is not proof of runtime absence.

### GET `/brapi/v2/plannedcrosses`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.plannedcrosses`
- **BrAPI-Den operation identity:** `brapiV21GetPlannedcrosses` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Crosses
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Crossing, pedigree, progeny and breeding-method concepts relate to breeding processes.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get a filtered list of Planned Cross entities
**Source contract description:**
> Get a filtered list of Planned Cross entities.
**Can be used for:**
- Get a filtered list of Planned Cross entities
- Get a filtered list of Planned Cross entities.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** crossingProjectDbId, crossingProjectName, plannedCrossDbId, plannedCrossName, status
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** PlannedCrossesListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Germplasm/PlannedCrosses/PlannedCrosses_GET_POST_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/PlannedCrosses/PlannedCrosses_GET_POST_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/plannedcrosses.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/plannedcrosses.py#L116) — `get_planned_crosses`; line 116; brapi-adapter-source-declaration.

### POST `/brapi/v2/plannedcrosses`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.post.plannedcrosses`
- **BrAPI-Den operation identity:** `brapiV21PostPlannedcrosses` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Crosses
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Crossing, pedigree, progeny and breeding-method concepts relate to breeding processes.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Create new Planned Cross entities on this server
**Source contract description:**
> Create new Planned Cross entities on this server
**Can be used for:**
- Create new Planned Cross entities on this server
- Create new Planned Cross entities on this server
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** PlannedCrossNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** PlannedCrossesListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Germplasm/PlannedCrosses/PlannedCrosses_GET_POST_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/PlannedCrosses/PlannedCrosses_GET_POST_PUT.yaml)
- **BijMantra inventory row:** [line 64](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L64); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/plannedcrosses.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/plannedcrosses.py#L225) — `create_planned_crosses`; line 225; brapi-adapter-source-declaration.

### PUT `/brapi/v2/plannedcrosses`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.put.plannedcrosses`
- **BrAPI-Den operation identity:** `brapiV21PutPlannedcrosses` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Crosses
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Crossing, pedigree, progeny and breeding-method concepts relate to breeding processes.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update existing Planned Cross entities on this server
**Source contract description:**
> Update existing Planned Cross entities on this server
**Can be used for:**
- Update existing Planned Cross entities on this server
- Update existing Planned Cross entities on this server
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** PlannedCrossNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** PlannedCrossesListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Germplasm/PlannedCrosses/PlannedCrosses_GET_POST_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/PlannedCrosses/PlannedCrosses_GET_POST_PUT.yaml)
- **BijMantra inventory row:** [line 87](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L87); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/plannedcrosses.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/plannedcrosses.py#L314) — `update_planned_crosses`; line 314; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/attributes`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.post.search.attributes`
- **BrAPI-Den operation identity:** `brapiV21PostSearchAttributes` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm Attributes
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for Germplasm `Attributes`
**Source contract description:**
> Submit a search request for Germplasm `Attributes`<br/>
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/attributes/{searchResultsDbId}` to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for Germplasm `Attributes`
- Submit a search request for Germplasm `Attributes`<br/>
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/attributes/{searchResultsDbId}` to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat as create/update of searched domain resource; it submits a search request.
- Search replay/deduplication is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results record may be created; domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** GermplasmAttributeSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** GermplasmAttributeListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm_Attributes/Search_Attributes_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm_Attributes/Search_Attributes_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L927) — `search_attributes`; line 927; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/attributes/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchAttributesBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm Attributes
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a Germplasm `Attributes` search request
**Source contract description:**
> Get the results of a Germplasm `Attributes` search request <br/>
> Clients should submit a search request using the corresponding `POST /search/attributes` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Get the results of a Germplasm `Attributes` search request
- Get the results of a Germplasm `Attributes` search request <br/>
  Clients should submit a search request using the corresponding `POST /search/attributes` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not use to submit a new search; retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, GermplasmAttributeListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm_Attributes/Search_Attributes_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm_Attributes/Search_Attributes_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L967) — `get_search_attributes_results`; line 967; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/attributevalues`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.post.search.attributevalues`
- **BrAPI-Den operation identity:** `brapiV21PostSearchAttributevalues` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm Attribute Values
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for Germplasm `AttributeValues`
**Source contract description:**
> Submit a search request for Germplasm `AttributeValues`<br/>
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/attributevalues/{searchResultsDbId}` to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for Germplasm `AttributeValues`
- Submit a search request for Germplasm `AttributeValues`<br/>
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/attributevalues/{searchResultsDbId}` to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat as create/update of searched domain resource; it submits a search request.
- Search replay/deduplication is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results record may be created; domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** GermplasmAttributeValueSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** GermplasmAttributeValueListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm_Attribute_Values/Search_AttributeValues_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm_Attribute_Values/Search_AttributeValues_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L988) — `search_attributevalues`; line 988; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/attributevalues/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchAttributevaluesBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm Attribute Values
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a Germplasm `AttributeValues` search request
**Source contract description:**
> Get the results of a Germplasm `AttributeValues` search request <br/>
> Clients should submit a search request using the corresponding `POST /search/attributevalues` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Get the results of a Germplasm `AttributeValues` search request
- Get the results of a Germplasm `AttributeValues` search request <br/>
  Clients should submit a search request using the corresponding `POST /search/attributevalues` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not use to submit a new search; retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, GermplasmAttributeValueListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm_Attribute_Values/Search_AttributeValues_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm_Attribute_Values/Search_AttributeValues_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1037) — `get_search_attributevalues_results`; line 1037; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/germplasm`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.post.search.germplasm`
- **BrAPI-Den operation identity:** `brapiV21PostSearchGermplasm` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for `Germplasm`
**Source contract description:**
> Submit a search request for `Germplasm`<br/>
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/germplasm/{searchResultsDbId}` to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for `Germplasm`
- Submit a search request for `Germplasm`<br/>
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/germplasm/{searchResultsDbId}` to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat as create/update of searched domain resource; it submits a search request.
- Search replay/deduplication is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results record may be created; domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** GermplasmSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** GermplasmListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm/Search_Germplasm_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm/Search_Germplasm_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L850) — `search_germplasm`; line 850; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/germplasm/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchGermplasmBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Germplasm
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a `Germplasm` search request
**Source contract description:**
> Get the results of a `Germplasm` search request <br/>
> Clients should submit a search request using the corresponding `POST /search/germplasm` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Get the results of a `Germplasm` search request
- Get the results of a `Germplasm` search request <br/>
  Clients should submit a search request using the corresponding `POST /search/germplasm` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not use to submit a new search; retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, GermplasmListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Germplasm/Germplasm/Search_Germplasm_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Germplasm/Search_Germplasm_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L906) — `get_search_germplasm_results`; line 906; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/pedigree`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.post.search.pedigree`
- **BrAPI-Den operation identity:** `brapiV21PostSearchPedigree` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Pedigree
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Crossing, pedigree, progeny and breeding-method concepts relate to breeding processes.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for `Pedigree`
**Source contract description:**
> Submit a search request for `Pedigree`<br/>
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/germplasm/{searchResultsDbId}` to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for `Pedigree`
- Submit a search request for `Pedigree`<br/>
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/germplasm/{searchResultsDbId}` to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat as create/update of searched domain resource; it submits a search request.
- Search replay/deduplication is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results record may be created; domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** PedigreeSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** PedigreeListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Germplasm/Pedigree/Search_Pedigree_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Pedigree/Search_Pedigree_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1058) — `search_pedigree`; line 1058; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/pedigree/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchPedigreeBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Pedigree
- **Proposed BrAPI-Den classification:** D2 — Breeding Programs and Experimental Design; Crosswalk basis: inferred-from-route; Crosswalk note: Crossing, pedigree, progeny and breeding-method concepts relate to breeding processes.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a `Pedigree` search request
**Source contract description:**
> Get the results of a `Pedigree` search request <br/>
> Clients should submit a search request using the corresponding `POST /search/germplasm` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Get the results of a `Pedigree` search request
- Get the results of a `Pedigree` search request <br/>
  Clients should submit a search request using the corresponding `POST /search/germplasm` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not use to submit a new search; retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, PedigreeListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Germplasm/Pedigree/Search_Pedigree_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/Pedigree/Search_Pedigree_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1116) — `get_search_pedigree_results`; line 1116; brapi-adapter-source-declaration.

### GET `/brapi/v2/seedlots`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.seedlots`
- **BrAPI-Den operation identity:** `brapiV21GetSeedlots` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Seed Lots
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get a filtered list of Seed Lot descriptions
**Source contract description:**
> Get a filtered list of Seed Lot descriptions available in a system.
**Can be used for:**
- Get a filtered list of Seed Lot descriptions
- Get a filtered list of Seed Lot descriptions available in a system.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** seedLotDbId, crossDbId, crossName
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** SeedLotListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Germplasm/SeedLots/SeedLots_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/SeedLots/SeedLots_GET_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/seedlots.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/seedlots.py#L76) — `list_seedlots`; line 76; brapi-adapter-source-declaration.

### POST `/brapi/v2/seedlots`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.post.seedlots`
- **BrAPI-Den operation identity:** `brapiV21PostSeedlots` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Seed Lots
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Add new Seed Lot descriptions to a server
**Source contract description:**
> Add new Seed Lot descriptions to a server
**Can be used for:**
- Add new Seed Lot descriptions to a server
- Add new Seed Lot descriptions to a server
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** SeedLotNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** SeedLotListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Germplasm/SeedLots/SeedLots_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/SeedLots/SeedLots_GET_POST.yaml)
- **BijMantra inventory row:** [line 50](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L50); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/seedlots.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/seedlots.py#L153) — `create_seedlot`; line 153; brapi-adapter-source-declaration.

### GET `/brapi/v2/seedlots/transactions`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.seedlots.transactions`
- **BrAPI-Den operation identity:** `brapiV21GetSeedlotsTransactions` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Seed Lots
- **Proposed BrAPI-Den classification:** D6 — Crop Production and Material Operations; Crosswalk basis: inferred-from-route; Crosswalk note: Seed-lot transactions represent material movement.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get a filtered list of Seed Lot Transactions
**Source contract description:**
> Get a filtered list of Seed Lot Transactions
**Can be used for:**
- Get a filtered list of Seed Lot Transactions
- Get a filtered list of Seed Lot Transactions
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** transactionDbId, seedLotDbId, crossDbId, crossName
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** SeedLotTransactionListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-01
- **Related catalogue IDs:** brapi-den.brapi-v2-1.germplasm.get.seedlots.by-seedlotdbid.transactions, brapi-den.brapi-v2-1.germplasm.post.seedlots.transactions, brapi-den.genx.v3.seed-lot-ledger.append, brapi-den.genx.v3.seed-lot-ledger.list
- **Contract source:** [`Specification/BrAPI-Germplasm/SeedLots/SeedLots_Transactions_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/SeedLots/SeedLots_Transactions_GET_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/seedlots.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/seedlots.py#L370) — `list_all_transactions`; line 370; brapi-adapter-source-declaration.

### POST `/brapi/v2/seedlots/transactions`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.post.seedlots.transactions`
- **BrAPI-Den operation identity:** `brapiV21PostSeedlotsTransactions` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Seed Lots
- **Proposed BrAPI-Den classification:** D6 — Crop Production and Material Operations; Crosswalk basis: inferred-from-route; Crosswalk note: Seed-lot transactions represent material movement.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Add new Seed Lot Transaction to be recorded
**Source contract description:**
> Add new Seed Lot Transaction to be recorded
**Can be used for:**
- Add new Seed Lot Transaction to be recorded
- Add new Seed Lot Transaction to be recorded
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** SeedLotTransactionNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** SeedLotTransactionListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-01
- **Related catalogue IDs:** brapi-den.brapi-v2-1.germplasm.get.seedlots.by-seedlotdbid.transactions, brapi-den.brapi-v2-1.germplasm.get.seedlots.transactions, brapi-den.genx.v3.seed-lot-ledger.append, brapi-den.genx.v3.seed-lot-ledger.list
- **Contract source:** [`Specification/BrAPI-Germplasm/SeedLots/SeedLots_Transactions_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/SeedLots/SeedLots_Transactions_GET_POST.yaml)
- **BijMantra inventory row:** [line 56](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L56); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/seedlots.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/seedlots.py#L489) — `create_transaction`; line 489; brapi-adapter-source-declaration.

### GET `/brapi/v2/seedlots/{seedLotDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.seedlots.by-seedlotdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSeedlotsBySeedLotDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Seed Lots
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get a specific Seed Lot
**Source contract description:**
> Get a specific Seed Lot by seedLotDbId
**Can be used for:**
- Get a specific Seed Lot
- Get a specific Seed Lot by seedLotDbId
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** seedLotDbId
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** SeedLotSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Germplasm/SeedLots/SeedLots_SeedLotDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/SeedLots/SeedLots_SeedLotDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/seedlots.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/seedlots.py#L224) — `get_seedlot`; line 224; brapi-adapter-source-declaration.

### PUT `/brapi/v2/seedlots/{seedLotDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.put.seedlots.by-seedlotdbid`
- **BrAPI-Den operation identity:** `brapiV21PutSeedlotsBySeedLotDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Seed Lots
- **Proposed BrAPI-Den classification:** D1 — Germplasm and Biological Resources; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Germplasm module; no stronger route-level crosswalk identified.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update an existing Seed Lot
**Source contract description:**
> Update an existing Seed Lot
**Can be used for:**
- Update an existing Seed Lot
- Update an existing Seed Lot
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** seedLotDbId
- **Request schema refs recorded:** SeedLotNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** SeedLotSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Germplasm/SeedLots/SeedLots_SeedLotDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/SeedLots/SeedLots_SeedLotDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 31](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L31); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/seedlots.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/seedlots.py#L267) — `update_seedlot`; line 267; brapi-adapter-source-declaration.

### GET `/brapi/v2/seedlots/{seedLotDbId}/transactions`

- **Catalogue ID:** `brapi-den.brapi-v2-1.germplasm.get.seedlots.by-seedlotdbid.transactions`
- **BrAPI-Den operation identity:** `brapiV21GetSeedlotsBySeedLotDbIdTransactions` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Germplasm
- **Source tag:** Seed Lots
- **Proposed BrAPI-Den classification:** D6 — Crop Production and Material Operations; Crosswalk basis: inferred-from-route; Crosswalk note: Seed-lot transactions represent material movement.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get all Transactions related to a specific Seed Lot
**Source contract description:**
> Get all Transactions related to a specific Seed Lot
**Can be used for:**
- Get all Transactions related to a specific Seed Lot
- Get all Transactions related to a specific Seed Lot
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** seedLotDbId, transactionDbId, transactionDirection
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** SeedLotTransactionListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-01
- **Related catalogue IDs:** brapi-den.brapi-v2-1.germplasm.get.seedlots.transactions, brapi-den.brapi-v2-1.germplasm.post.seedlots.transactions, brapi-den.genx.v3.seed-lot-ledger.append, brapi-den.genx.v3.seed-lot-ledger.list
- **Contract source:** [`Specification/BrAPI-Germplasm/SeedLots/SeedLots_SeedLotDbId_Transactions_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Germplasm/SeedLots/SeedLots_SeedLotDbId_Transactions_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/seedlots.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/seedlots.py#L425) — `list_seedlot_transactions`; line 425; brapi-adapter-source-declaration.

### BrAPI-Genotyping — 61 operations

### GET `/brapi/v2/allelematrix`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.allelematrix`
- **BrAPI-Den operation identity:** `brapiV21GetAllelematrix` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Use this endpoint to retrieve a two dimensional matrix of genotype data
**Source contract description:**
> Use this endpoint to retrieve a two dimensional matrix of genotype data. The response structure is based on the VCF file format, 
> but the search and filter parameters give the ability to slice and merge data sets. This allows the user to return the subset of data they are interested in, 
> without having to download the entire genotype file.
> <br/>Each row of data (outer array) corresponds to a variant definition, and each column (inner array) corresponds to a callSet.
**Can be used for:**
- Use this endpoint to retrieve a two dimensional matrix of genotype data
- Use this endpoint to retrieve a two dimensional matrix of genotype data. The response structure is based on the VCF file format, 
  but the search and filter parameters give the ability to slice and merge data sets. This allows the user to return the subset of data they are interested in, 
  without having to download the entire genotype file.
  <br/>Each row of data (outer array) corresponds to a variant definition, and each column (inner array) corresponds to a callSet.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** AlleleMatrixResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-04
- **Related catalogue IDs:** brapi-den.brapi-v2-1.genotyping.get.calls, brapi-den.brapi-v2-1.genotyping.get.callsets, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variants, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.callsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.variants, brapi-den.brapi-v2-1.genotyping.post.variantsets.extract, brapi-den.brapi-v2-1.genotyping.put.calls, brapi-den.genx.v3.variant-matrices.get, brapi-den.genx.v3.variant-matrices.list, brapi-den.genx.v3.variant-matrices.register
- **Contract source:** [`Specification/BrAPI-Genotyping/AlleleMatrix/AlleleMatrix_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/AlleleMatrix/AlleleMatrix_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/allelematrix.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/allelematrix.py#L45) — `get_allele_matrix`; line 45; brapi-adapter-source-declaration.

### GET `/brapi/v2/calls`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.calls`
- **BrAPI-Den operation identity:** `brapiV21GetCalls` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Gets a filtered list of `Calls`
**Source contract description:**
> Gets a filtered list of `Call` JSON objects.
**Can be used for:**
- Gets a filtered list of `Calls`
- Gets a filtered list of `Call` JSON objects.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** CallsListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-04
- **Related catalogue IDs:** brapi-den.brapi-v2-1.genotyping.get.allelematrix, brapi-den.brapi-v2-1.genotyping.get.callsets, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variants, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.callsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.variants, brapi-den.brapi-v2-1.genotyping.post.variantsets.extract, brapi-den.brapi-v2-1.genotyping.put.calls, brapi-den.genx.v3.variant-matrices.get, brapi-den.genx.v3.variant-matrices.list, brapi-den.genx.v3.variant-matrices.register
- **Contract source:** [`Specification/BrAPI-Genotyping/Calls/Calls_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/Calls/Calls_GET_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/calls.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/calls.py#L66) — `get_calls`; line 66; brapi-adapter-source-declaration.

### PUT `/brapi/v2/calls`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.put.calls`
- **BrAPI-Den operation identity:** `brapiV21PutCalls` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update existing `Calls` with new genotype value or metadata
**Source contract description:**
> Update existing `Calls` with new genotype value or metadata
> <br/>Implementation Note - 
> <br/>A `Call` object does not have a DbId of its own. It is defined by the unique combination of 
> `callSetDbId`, `variantDbId`, and `variantSetDbId`. These three fields MUST be present for every 
> `call` update request. This endpoint should not allow these fields to be modified for a given 
> `call`. Modifying these fields in the database is effectively moving a cell to a different location
> in the genotype matrix. This action is dangerous and can cause data collisions.
**Can be used for:**
- Update existing `Calls` with new genotype value or metadata
- Update existing `Calls` with new genotype value or metadata
  <br/>Implementation Note - 
  <br/>A `Call` object does not have a DbId of its own. It is defined by the unique combination of 
  `callSetDbId`, `variantDbId`, and `variantSetDbId`. These three fields MUST be present for every 
  `call` update request. This endpoint should not allow these fields to be modified for a given 
  `call`. Modifying these fields in the database is effectively moving a cell to a different location
  in the genotype matrix. This action is dangerous and can cause data collisions.
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** Call
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** CallsListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-04
- **Related catalogue IDs:** brapi-den.brapi-v2-1.genotyping.get.allelematrix, brapi-den.brapi-v2-1.genotyping.get.calls, brapi-den.brapi-v2-1.genotyping.get.callsets, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variants, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.callsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.variants, brapi-den.brapi-v2-1.genotyping.post.variantsets.extract, brapi-den.genx.v3.variant-matrices.get, brapi-den.genx.v3.variant-matrices.list, brapi-den.genx.v3.variant-matrices.register
- **Contract source:** [`Specification/BrAPI-Genotyping/Calls/Calls_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/Calls/Calls_GET_PUT.yaml)
- **BijMantra inventory row:** [line 69](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L69); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/calls.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/calls.py#L95) — `update_calls`; line 95; brapi-adapter-source-declaration.

### GET `/brapi/v2/callsets`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.callsets`
- **BrAPI-Den operation identity:** `brapiV21GetCallsets` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Gets a filtered list of `CallSet` JSON objects.
**Source contract description:**
> Gets a filtered list of `CallSet` JSON objects.
**Can be used for:**
- Gets a filtered list of `CallSet` JSON objects.
- Gets a filtered list of `CallSet` JSON objects.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** callSetDbId, callSetName, variantSetDbId, sampleDbId
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** CallSetsListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-04
- **Related catalogue IDs:** brapi-den.brapi-v2-1.genotyping.get.allelematrix, brapi-den.brapi-v2-1.genotyping.get.calls, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variants, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.callsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.variants, brapi-den.brapi-v2-1.genotyping.post.variantsets.extract, brapi-den.brapi-v2-1.genotyping.put.calls, brapi-den.genx.v3.variant-matrices.get, brapi-den.genx.v3.variant-matrices.list, brapi-den.genx.v3.variant-matrices.register
- **Contract source:** [`Specification/BrAPI-Genotyping/CallSets/CallSets_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/CallSets/CallSets_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/callsets.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/callsets.py#L80) — `get_callsets`; line 80; brapi-adapter-source-declaration.

### GET `/brapi/v2/callsets/{callSetDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid`
- **BrAPI-Den operation identity:** `brapiV21GetCallsetsByCallSetDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Gets a `CallSet` by ID.
**Source contract description:**
> Gets a `CallSet` by ID.
**Can be used for:**
- Gets a `CallSet` by ID.
- Gets a `CallSet` by ID.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-04
- **Related catalogue IDs:** brapi-den.brapi-v2-1.genotyping.get.allelematrix, brapi-den.brapi-v2-1.genotyping.get.calls, brapi-den.brapi-v2-1.genotyping.get.callsets, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variants, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.callsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.variants, brapi-den.brapi-v2-1.genotyping.post.variantsets.extract, brapi-den.brapi-v2-1.genotyping.put.calls, brapi-den.genx.v3.variant-matrices.get, brapi-den.genx.v3.variant-matrices.list, brapi-den.genx.v3.variant-matrices.register
- **Contract source:** [`Specification/BrAPI-Genotyping/CallSets/CallSets_CallSetId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/CallSets/CallSets_CallSetId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/callsets.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/callsets.py#L137) — `get_callset`; line 137; brapi-adapter-source-declaration.

### GET `/brapi/v2/callsets/{callSetDbId}/calls`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid.calls`
- **BrAPI-Den operation identity:** `brapiV21GetCallsetsByCallSetDbIdCalls` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Gets a list of `Calls` associated with a `CallSet`.
**Source contract description:**
> Gets a list of `Calls` associated with a `CallSet`.
**Can be used for:**
- Gets a list of `Calls` associated with a `CallSet`.
- Gets a list of `Calls` associated with a `CallSet`.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** CallsListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-04
- **Related catalogue IDs:** brapi-den.brapi-v2-1.genotyping.get.allelematrix, brapi-den.brapi-v2-1.genotyping.get.calls, brapi-den.brapi-v2-1.genotyping.get.callsets, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid, brapi-den.brapi-v2-1.genotyping.get.variants, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.callsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.variants, brapi-den.brapi-v2-1.genotyping.post.variantsets.extract, brapi-den.brapi-v2-1.genotyping.put.calls, brapi-den.genx.v3.variant-matrices.get, brapi-den.genx.v3.variant-matrices.list, brapi-den.genx.v3.variant-matrices.register
- **Contract source:** [`Specification/BrAPI-Genotyping/CallSets/CallSets_CallSetId_Calls_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/CallSets/CallSets_CallSetId_Calls_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/callsets.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/callsets.py#L173) — `get_callset_calls`; line 173; brapi-adapter-source-declaration.

### GET `/brapi/v2/maps`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.maps`
- **BrAPI-Den operation identity:** `brapiV21GetMaps` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Genome Maps
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the Genomic Maps
**Source contract description:**
> Get list of maps
**Can be used for:**
- Get the Genomic Maps
- Get list of maps
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** mapDbId, mapPUI, scientificName, type
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Genotyping/GenomeMaps/Maps_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/GenomeMaps/Maps_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 2 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/maps.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/maps.py#L73) — `get_maps`; line 73; brapi-adapter-source-declaration.
  - [backend/app/modules/soil/router.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/modules/soil/router.py#L50) — `read_soil_maps`; line 50; same-route-collision-other-module.

### GET `/brapi/v2/maps/{mapDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.maps.by-mapdbid`
- **BrAPI-Den operation identity:** `brapiV21GetMapsByMapDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Genome Maps
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the details of a specific Genomic Map
**Source contract description:**
> Provides the number of markers on each linkageGroup and the max position on the linkageGroup
**Can be used for:**
- Get the details of a specific Genomic Map
- Provides the number of markers on each linkageGroup and the max position on the linkageGroup
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Genotyping/GenomeMaps/Maps_MapDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/GenomeMaps/Maps_MapDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/maps.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/maps.py#L103) — `get_map`; line 103; brapi-adapter-source-declaration.

### GET `/brapi/v2/maps/{mapDbId}/linkagegroups`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.maps.by-mapdbid.linkagegroups`
- **BrAPI-Den operation identity:** `brapiV21GetMapsByMapDbIdLinkagegroups` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Genome Maps
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the Linkage Groups of a specific Genomic Map
**Source contract description:**
> Get the Linkage Groups of a specific Genomic Map. A Linkage Group is the BrAPI generic term for a named section of a map. A Linkage Group can represent a Chromosome, Scaffold, or Linkage Group.
**Can be used for:**
- Get the Linkage Groups of a specific Genomic Map
- Get the Linkage Groups of a specific Genomic Map. A Linkage Group is the BrAPI generic term for a named section of a map. A Linkage Group can represent a Chromosome, Scaffold, or Linkage Group.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Genotyping/GenomeMaps/Maps_MapDbId_LinkageGroups_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/GenomeMaps/Maps_MapDbId_LinkageGroups_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/maps.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/maps.py#L168) — `get_map_linkage_groups`; line 168; brapi-adapter-source-declaration.

### GET `/brapi/v2/markerpositions`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.markerpositions`
- **BrAPI-Den operation identity:** `brapiV21GetMarkerpositions` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Genome Maps
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get marker position info
**Source contract description:**
> Get marker position information, based on Map, Linkage Group, and Marker ID
**Can be used for:**
- Get marker position info
- Get marker position information, based on Map, Linkage Group, and Marker ID
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** mapDbId, linkageGroupName, variantDbId, minPosition, maxPosition
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** MarkerPositionListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Genotyping/GenomeMaps/MarkerPositions_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/GenomeMaps/MarkerPositions_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/markerpositions.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/markerpositions.py#L82) — `get_marker_positions`; line 82; brapi-adapter-source-declaration.

### GET `/brapi/v2/plates`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.plates`
- **BrAPI-Den operation identity:** `brapiV21GetPlates` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Plates
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get a filtered list of Plates.
**Source contract description:**
> Get a filtered list of `Plates`. Each `Plate` is a collection of `Samples` that are physically grouped together.
**Can be used for:**
- Get a filtered list of Plates.
- Get a filtered list of `Plates`. Each `Plate` is a collection of `Samples` that are physically grouped together.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** sampleDbId, sampleName, sampleGroupDbId, observationUnitDbId, plateDbId, plateName
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** PlateListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Genotyping/Plates/Plates_GET_POST_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/Plates/Plates_GET_POST_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/plates.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/plates.py#L101) — `get_plates`; line 101; brapi-adapter-source-declaration.

### POST `/brapi/v2/plates`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.post.plates`
- **BrAPI-Den operation identity:** `brapiV21PostPlates` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Plates
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit new Plate entities to the server
**Source contract description:**
> Submit new Plate entities to the server
**Can be used for:**
- Submit new Plate entities to the server
- Submit new Plate entities to the server
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** PlateNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** PlateListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Genotyping/Plates/Plates_GET_POST_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/Plates/Plates_GET_POST_PUT.yaml)
- **BijMantra inventory row:** [line 69](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L69); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/plates.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/plates.py#L237) — `create_plates`; line 237; brapi-adapter-source-declaration.

### PUT `/brapi/v2/plates`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.put.plates`
- **BrAPI-Den operation identity:** `brapiV21PutPlates` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Plates
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update the details of existing Plates
**Source contract description:**
> Update the details of existing Plates
**Can be used for:**
- Update the details of existing Plates
- Update the details of existing Plates
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** PlateNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** PlateListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Genotyping/Plates/Plates_GET_POST_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/Plates/Plates_GET_POST_PUT.yaml)
- **BijMantra inventory row:** [line 92](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L92); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/plates.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/plates.py#L277) — `update_plates`; line 277; brapi-adapter-source-declaration.

### GET `/brapi/v2/plates/{plateDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.plates.by-platedbid`
- **BrAPI-Den operation identity:** `brapiV21GetPlatesByPlateDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Plates
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the details of a specific Plate.
**Source contract description:**
> Get the details of a specific `Plate`. Each `Plate` is a collection of `Samples` that are physically grouped together.
**Can be used for:**
- Get the details of a specific Plate.
- Get the details of a specific `Plate`. Each `Plate` is a collection of `Samples` that are physically grouped together.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** PlateSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Genotyping/Plates/Plates_PlateDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/Plates/Plates_PlateDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/plates.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/plates.py#L196) — `get_plate`; line 196; brapi-adapter-source-declaration.

### GET `/brapi/v2/references`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.references`
- **BrAPI-Den operation identity:** `brapiV21GetReferences` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Gets a filtered list of `Reference` objects.
**Source contract description:**
> `GET /references` will return a filtered list of `Reference` JSON objects.
**Can be used for:**
- Gets a filtered list of `Reference` objects.
- `GET /references` will return a filtered list of `Reference` JSON objects.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** ReferencesListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Genotyping/References/References_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/References/References_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/references.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/references.py#L85) — `get_references`; line 85; brapi-adapter-source-declaration.

### GET `/brapi/v2/references/{referenceDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.references.by-referencedbid`
- **BrAPI-Den operation identity:** `brapiV21GetReferencesByReferenceDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Gets a `Reference` by ID.
**Source contract description:**
> `GET /references/{reference_id}` will return a JSON version of
> `Reference`.
**Can be used for:**
- Gets a `Reference` by ID.
- `GET /references/{reference_id}` will return a JSON version of
  `Reference`.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Genotyping/References/References_ReferenceId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/References/References_ReferenceId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/references.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/references.py#L151) — `get_reference`; line 151; brapi-adapter-source-declaration.

### GET `/brapi/v2/references/{referenceDbId}/bases`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.references.by-referencedbid.bases`
- **BrAPI-Den operation identity:** `brapiV21GetReferencesByReferenceDbIdBases` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Lists `Reference` bases by ID and optional range.
**Source contract description:**
> Lists `Reference` bases by ID and optional range.
**Can be used for:**
- Lists `Reference` bases by ID and optional range.
- Lists `Reference` bases by ID and optional range.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Genotyping/References/References_ReferenceId_Bases_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/References/References_ReferenceId_Bases_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/references.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/references.py#L184) — `get_reference_bases`; line 184; brapi-adapter-source-declaration.

### GET `/brapi/v2/referencesets`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.referencesets`
- **BrAPI-Den operation identity:** `brapiV21GetReferencesets` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Gets a list of `ReferenceSets`.
**Source contract description:**
> Gets a filtered list of `ReferenceSets`.
**Can be used for:**
- Gets a list of `ReferenceSets`.
- Gets a filtered list of `ReferenceSets`.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** ReferenceSetsListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Genotyping/ReferenceSets/ReferenceSets_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/ReferenceSets/ReferenceSets_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/referencesets.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/referencesets.py#L83) — `get_referencesets`; line 83; brapi-adapter-source-declaration.

### GET `/brapi/v2/referencesets/{referenceSetDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.referencesets.by-referencesetdbid`
- **BrAPI-Den operation identity:** `brapiV21GetReferencesetsByReferenceSetDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Gets a `ReferenceSet` by ID.
**Source contract description:**
> Gets a `ReferenceSet` by ID.
**Can be used for:**
- Gets a `ReferenceSet` by ID.
- Gets a `ReferenceSet` by ID.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Genotyping/ReferenceSets/ReferenceSets_RefernceSetId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/ReferenceSets/ReferenceSets_RefernceSetId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/referencesets.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/referencesets.py#L136) — `get_referenceset`; line 136; brapi-adapter-source-declaration.

### GET `/brapi/v2/samples`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.samples`
- **BrAPI-Den operation identity:** `brapiV21GetSamples` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Samples
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the Samples
**Source contract description:**
> Used to retrieve list of Samples from a Sample Tracking system based on some search criteria.
**Can be used for:**
- Get the Samples
- Used to retrieve list of Samples from a Sample Tracking system based on some search criteria.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** sampleDbId, sampleName, sampleGroupDbId, observationUnitDbId, plateDbId, plateName
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** SampleListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Genotyping/Samples/Samples_GET_POST_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/Samples/Samples_GET_POST_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/samples.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/samples.py#L97) — `list_samples`; line 97; brapi-adapter-source-declaration.

### POST `/brapi/v2/samples`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.post.samples`
- **BrAPI-Den operation identity:** `brapiV21PostSamples` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Samples
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Add new Samples
**Source contract description:**
> Call to register the event of a sample being taken. Sample ID is assigned as a result of the operation and returned in response.
**Can be used for:**
- Add new Samples
- Call to register the event of a sample being taken. Sample ID is assigned as a result of the operation and returned in response.
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** SampleNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** SampleListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Genotyping/Samples/Samples_GET_POST_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/Samples/Samples_GET_POST_PUT.yaml)
- **BijMantra inventory row:** [line 69](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L69); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/samples.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/samples.py#L182) — `create_sample`; line 182; brapi-adapter-source-declaration.

### PUT `/brapi/v2/samples`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.put.samples`
- **BrAPI-Den operation identity:** `brapiV21PutSamples` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Samples
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update the details of existing Samples
**Source contract description:**
> Update the details of existing Samples
**Can be used for:**
- Update the details of existing Samples
- Update the details of existing Samples
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** SampleNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** SampleListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Genotyping/Samples/Samples_GET_POST_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/Samples/Samples_GET_POST_PUT.yaml)
- **BijMantra inventory row:** [line 92](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L92); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/samples.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/samples.py#L287) — `update_samples_bulk`; line 287; brapi-adapter-source-declaration.

### GET `/brapi/v2/samples/{sampleDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.samples.by-sampledbid`
- **BrAPI-Den operation identity:** `brapiV21GetSamplesBySampleDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Samples
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the details of a specific Sample
**Source contract description:**
> Used to retrieve the details of a single Sample from a Sample Tracking system.
**Can be used for:**
- Get the details of a specific Sample
- Used to retrieve the details of a single Sample from a Sample Tracking system.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** SampleSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Genotyping/Samples/Samples_SampleDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/Samples/Samples_SampleDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/samples.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/samples.py#L249) — `get_sample`; line 249; brapi-adapter-source-declaration.

### PUT `/brapi/v2/samples/{sampleDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.put.samples.by-sampledbid`
- **BrAPI-Den operation identity:** `brapiV21PutSamplesBySampleDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Samples
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update the details of an existing Sample
**Source contract description:**
> **Deprecated in v2.1** Please use `PUT /samples`. Github issue number #462 
> <br/>Update the details of an existing Sample
**Can be used for:**
- Update the details of an existing Sample
- **Deprecated in v2.1** Please use `PUT /samples`. Github issue number #462 
  <br/>Update the details of an existing Sample
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** SampleNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** SampleSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Genotyping/Samples/Samples_SampleDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/Samples/Samples_SampleDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 31](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L31); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/samples.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/samples.py#L350) — `update_sample`; line 350; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/allelematrix`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.post.search.allelematrix`
- **BrAPI-Den operation identity:** `brapiV21PostSearchAllelematrix` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Allele Matrix
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for a Allele Matrix
**Source contract description:**
> Use this endpoint to retrieve a two dimensional matrix of genotype data. The response structure is based on the VCF format, but the search and filter parameters give the ability to slice and merge data sets. This allows the user to return the subset of data they are interested in, without having to download the entire genotype file.
> <br/>Each row of data (outer array) corresponds to a variant definition, and each column (inner array) corresponds to a callSet. 
> <br/>Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. If a server needs more time to process the request, it might respond with a `searchResultsDbId`. Use the corresponding `GET /search/allelematrix/{searchResultsDbId}` to retrieve the results of the search. 
> <br/>Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for a Allele Matrix
- Use this endpoint to retrieve a two dimensional matrix of genotype data. The response structure is based on the VCF format, but the search and filter parameters give the ability to slice and merge data sets. This allows the user to return the subset of data they are interested in, without having to download the entire genotype file.
  <br/>Each row of data (outer array) corresponds to a variant definition, and each column (inner array) corresponds to a callSet. 
  <br/>Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. If a server needs more time to process the request, it might respond with a `searchResultsDbId`. Use the corresponding `GET /search/allelematrix/{searchResultsDbId}` to retrieve the results of the search. 
  <br/>Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat as create/update of searched domain resource; it submits a search request.
- Search replay/deduplication is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results record may be created; domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** AlleleMatrixSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** AlleleMatrixResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Genotyping/AlleleMatrix/Search_AlleleMatrix_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/AlleleMatrix/Search_AlleleMatrix_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L2097) — `search_allelematrix`; line 2097; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/allelematrix/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchAllelematrixBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a Allele Matrix search request
**Source contract description:**
> Use this endpoint to retrieve a two dimensional matrix of genotype data. The response structure is based on the VCF format, but the search and filter parameters give the ability to slice and merge data sets. This allows the user to return the subset of data they are interested in, without having to download the entire genotype file.
> <br/>Each row of data (outer array) corresponds to a variant definition, and each column (inner array) corresponds to a callSet. 
> <br/>Clients should submit a search request using the corresponding `POST /search/allelematrix` endpoint. Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. If a server needs more time to process the request, it might respond with a `searchResultsDbId`. Use this endpoint to retrieve the results of the search. 
> <br/>Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Get the results of a Allele Matrix search request
- Use this endpoint to retrieve a two dimensional matrix of genotype data. The response structure is based on the VCF format, but the search and filter parameters give the ability to slice and merge data sets. This allows the user to return the subset of data they are interested in, without having to download the entire genotype file.
  <br/>Each row of data (outer array) corresponds to a variant definition, and each column (inner array) corresponds to a callSet. 
  <br/>Clients should submit a search request using the corresponding `POST /search/allelematrix` endpoint. Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. If a server needs more time to process the request, it might respond with a `searchResultsDbId`. Use this endpoint to retrieve the results of the search. 
  <br/>Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not use to submit a new search; retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, AlleleMatrixResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Genotyping/AlleleMatrix/Search_AlleleMatrix_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/AlleleMatrix/Search_AlleleMatrix_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L2190) — `get_search_allelematrix_results`; line 2190; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/calls`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.post.search.calls`
- **BrAPI-Den operation identity:** `brapiV21PostSearchCalls` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Calls
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for `Calls`
**Source contract description:**
> Submit a search request for `Calls`<br/>
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/calls/{searchResultsDbId}` to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details. 
> <br/>
> <br/>
> <strong>NOTE:</strong> This endpoint uses Token based pagination. Please Review the 
> <a target="_blank" href="https://wiki.brapi.org/index.php/Pagination">Pagination documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for `Calls`
- Submit a search request for `Calls`<br/>
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/calls/{searchResultsDbId}` to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details. 
  <br/>
  <br/>
  <strong>NOTE:</strong> This endpoint uses Token based pagination. Please Review the 
  <a target="_blank" href="https://wiki.brapi.org/index.php/Pagination">Pagination documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat as create/update of searched domain resource; it submits a search request.
- Search replay/deduplication is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results record may be created; domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** CallsSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** CallsListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Genotyping/Calls/Search_Calls_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/Calls/Search_Calls_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1542) — `search_calls`; line 1542; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/calls/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchCallsBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a `Calls` search request
**Source contract description:**
> Get the results of a `Calls` search request <br/>
> Clients should submit a search request using the corresponding `POST /search/calls` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
> <br/>
**Can be used for:**
- Get the results of a `Calls` search request
- Get the results of a `Calls` search request <br/>
  Clients should submit a search request using the corresponding `POST /search/calls` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
  <br/>
**Must not be used for / explicit non-goals:**
- Do not use to submit a new search; retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, CallsListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Genotyping/Calls/Search_Calls_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/Calls/Search_Calls_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1589) — `get_search_calls_results`; line 1589; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/callsets`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.post.search.callsets`
- **BrAPI-Den operation identity:** `brapiV21PostSearchCallsets` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Call Sets
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for `CallSets`
**Source contract description:**
> Submit a search request for `CallSets` 
> <br> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/callsets/{searchResultsDbId}` to retrieve the results of the search. 
> <br> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for `CallSets`
- Submit a search request for `CallSets` 
  <br> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/callsets/{searchResultsDbId}` to retrieve the results of the search. 
  <br> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat as create/update of searched domain resource; it submits a search request.
- Search replay/deduplication is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results record may be created; domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** CallSetsSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** CallSetsListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Genotyping/CallSets/Search_CallSets_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/CallSets/Search_CallSets_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1610) — `search_callsets`; line 1610; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/callsets/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchCallsetsBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Call Sets
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a `CallSets` search request
**Source contract description:**
> Get the results of a `CallSets` search request 
> <br> Clients should submit a search request using the corresponding `POST /search/callsets` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. 
> <br>Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Get the results of a `CallSets` search request
- Get the results of a `CallSets` search request 
  <br> Clients should submit a search request using the corresponding `POST /search/callsets` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. 
  <br>Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not use to submit a new search; retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, CallSetsListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Genotyping/CallSets/Search_CallSets_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/CallSets/Search_CallSets_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1654) — `get_search_callsets_results`; line 1654; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/markerpositions`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.post.search.markerpositions`
- **BrAPI-Den operation identity:** `brapiV21PostSearchMarkerpositions` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Genome Maps
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for `MarkerPositions`
**Source contract description:**
> Submit a search request for `MarkerPositions`<br/>
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/markerpositions/{searchResultsDbId}` to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for `MarkerPositions`
- Submit a search request for `MarkerPositions`<br/>
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/markerpositions/{searchResultsDbId}` to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat as create/update of searched domain resource; it submits a search request.
- Search replay/deduplication is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results record may be created; domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** MarkerPositionSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** MarkerPositionListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Genotyping/GenomeMaps/Search_MarkerPositions_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/GenomeMaps/Search_MarkerPositions_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L2028) — `search_markerpositions`; line 2028; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/markerpositions/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchMarkerpositionsBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Genome Maps
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a `MarkerPositions` search request
**Source contract description:**
> Get the results of a `MarkerPositions` search request <br/>
> Clients should submit a search request using the corresponding `POST /search/markerpositions` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Get the results of a `MarkerPositions` search request
- Get the results of a `MarkerPositions` search request <br/>
  Clients should submit a search request using the corresponding `POST /search/markerpositions` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not use to submit a new search; retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, MarkerPositionListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Genotyping/GenomeMaps/Search_MarkerPositions_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/GenomeMaps/Search_MarkerPositions_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L2076) — `get_search_markerpositions_results`; line 2076; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/plates`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.post.search.plates`
- **BrAPI-Den operation identity:** `brapiV21PostSearchPlates` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Plates
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for `Plates`
**Source contract description:**
> Submit a search request for `Plates`<br/>
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/plates/{searchResultsDbId}` to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for `Plates`
- Submit a search request for `Plates`<br/>
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/plates/{searchResultsDbId}` to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat as create/update of searched domain resource; it submits a search request.
- Search replay/deduplication is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results record may be created; domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** PlateSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** PlateListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Genotyping/Plates/Search_Plates_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/Plates/Search_Plates_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1815) — `search_plates`; line 1815; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/plates/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchPlatesBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Plates
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a `Plates` search request
**Source contract description:**
> Get the results of a `Plates` search request <br/>
> Clients should submit a search request using the corresponding `POST /search/plates` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Get the results of a `Plates` search request
- Get the results of a `Plates` search request <br/>
  Clients should submit a search request using the corresponding `POST /search/plates` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not use to submit a new search; retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, PlateListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Genotyping/Plates/Search_Plates_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/Plates/Search_Plates_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1866) — `get_search_plates_results`; line 1866; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/references`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.post.search.references`
- **BrAPI-Den operation identity:** `brapiV21PostSearchReferences` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for `References`
**Source contract description:**
> Submit a search request for `References`<br/>
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/references/{searchResultsDbId}` to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for `References`
- Submit a search request for `References`<br/>
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/references/{searchResultsDbId}` to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat as create/update of searched domain resource; it submits a search request.
- Search replay/deduplication is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results record may be created; domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ReferencesSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** ReferencesListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Genotyping/References/Search_References_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/References/Search_References_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1887) — `search_references`; line 1887; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/references/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchReferencesBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a `References` search request
**Source contract description:**
> Get the results of a `References` search request <br/>
> Clients should submit a search request using the corresponding `POST /search/references` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Get the results of a `References` search request
- Get the results of a `References` search request <br/>
  Clients should submit a search request using the corresponding `POST /search/references` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not use to submit a new search; retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, ReferencesListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Genotyping/References/Search_References_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/References/Search_References_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1939) — `get_search_references_results`; line 1939; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/referencesets`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.post.search.referencesets`
- **BrAPI-Den operation identity:** `brapiV21PostSearchReferencesets` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for `ReferenceSets`
**Source contract description:**
> Submit a search request for `ReferenceSets`<br/>
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/referencesets/{searchResultsDbId}` to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for `ReferenceSets`
- Submit a search request for `ReferenceSets`<br/>
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/referencesets/{searchResultsDbId}` to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat as create/update of searched domain resource; it submits a search request.
- Search replay/deduplication is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results record may be created; domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ReferenceSetsSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** ReferenceSetsListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Genotyping/ReferenceSets/Search_ReferenceSets_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/ReferenceSets/Search_ReferenceSets_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1960) — `search_referencesets`; line 1960; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/referencesets/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchReferencesetsBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a `ReferenceSets` search request
**Source contract description:**
> Get the results of a `ReferenceSets` search request <br/>
> Clients should submit a search request using the corresponding `POST /search/referencesets` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Get the results of a `ReferenceSets` search request
- Get the results of a `ReferenceSets` search request <br/>
  Clients should submit a search request using the corresponding `POST /search/referencesets` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not use to submit a new search; retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, ReferenceSetsListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Genotyping/ReferenceSets/Search_ReferenceSets_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/ReferenceSets/Search_ReferenceSets_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L2007) — `get_search_referencesets_results`; line 2007; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/samples`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.post.search.samples`
- **BrAPI-Den operation identity:** `brapiV21PostSearchSamples` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Samples
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for `Samples`
**Source contract description:**
> Submit a search request for `Samples`<br/>
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/samples/{searchResultsDbId}` to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for `Samples`
- Submit a search request for `Samples`<br/>
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/samples/{searchResultsDbId}` to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat as create/update of searched domain resource; it submits a search request.
- Search replay/deduplication is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results record may be created; domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** SampleSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** SampleListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Genotyping/Samples/Search_Samples_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/Samples/Search_Samples_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1456) — `search_samples`; line 1456; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/samples/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchSamplesBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Samples
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a `Samples` search request
**Source contract description:**
> Get the results of a `Samples` search request <br/>
> Clients should submit a search request using the corresponding `POST /search/samples` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Get the results of a `Samples` search request
- Get the results of a `Samples` search request <br/>
  Clients should submit a search request using the corresponding `POST /search/samples` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not use to submit a new search; retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, SampleListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Genotyping/Samples/Search_Samples_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/Samples/Search_Samples_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1519) — `get_search_samples_results`; line 1519; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/variants`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.post.search.variants`
- **BrAPI-Den operation identity:** `brapiV21PostSearchVariants` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Variants
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for `Variants`
**Source contract description:**
> Submit a search request for `Variants`<br/>
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/variants/{searchResultsDbId}` to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
> <br/>
> <br/>
> <strong>NOTE:</strong> This endpoint uses Token based pagination. Please Review the 
> <a target="_blank" href="https://wiki.brapi.org/index.php/Pagination">Pagination documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for `Variants`
- Submit a search request for `Variants`<br/>
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/variants/{searchResultsDbId}` to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
  <br/>
  <br/>
  <strong>NOTE:</strong> This endpoint uses Token based pagination. Please Review the 
  <a target="_blank" href="https://wiki.brapi.org/index.php/Pagination">Pagination documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat as create/update of searched domain resource; it submits a search request.
- Search replay/deduplication is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results record may be created; domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** VariantsSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** VariantsListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Genotyping/Variants/Search_Variants_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/Variants/Search_Variants_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1675) — `search_variants`; line 1675; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/variants/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchVariantsBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Variants
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a `Variants` search request
**Source contract description:**
> Get the results of a `Variants` search request <br/>
> Clients should submit a search request using the corresponding `POST /search/variants` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
> <br/>
**Can be used for:**
- Get the results of a `Variants` search request
- Get the results of a `Variants` search request <br/>
  Clients should submit a search request using the corresponding `POST /search/variants` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
  <br/>
**Must not be used for / explicit non-goals:**
- Do not use to submit a new search; retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, VariantsListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Genotyping/Variants/Search_Variants_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/Variants/Search_Variants_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1728) — `get_search_variants_results`; line 1728; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/variantsets`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.post.search.variantsets`
- **BrAPI-Den operation identity:** `brapiV21PostSearchVariantsets` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Variant Sets
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for `VariantSets`
**Source contract description:**
> Submit a search request for `VariantSets`<br/>
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/variantsets/{searchResultsDbId}` to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for `VariantSets`
- Submit a search request for `VariantSets`<br/>
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/variantsets/{searchResultsDbId}` to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat as create/update of searched domain resource; it submits a search request.
- Search replay/deduplication is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results record may be created; domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** VariantSetsSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** VariantSetsListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Genotyping/VariantSets/Search_VariantSets_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/VariantSets/Search_VariantSets_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1749) — `search_variantsets`; line 1749; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/variantsets/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchVariantsetsBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Variant Sets
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a `VariantSets` search request
**Source contract description:**
> Get the results of a `VariantSets` search request <br/>
> Clients should submit a search request using the corresponding `POST /search/variantsets` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Get the results of a `VariantSets` search request
- Get the results of a `VariantSets` search request <br/>
  Clients should submit a search request using the corresponding `POST /search/variantsets` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not use to submit a new search; retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, VariantSetsListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Genotyping/VariantSets/Search_VariantSets_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/VariantSets/Search_VariantSets_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1794) — `get_search_variantsets_results`; line 1794; brapi-adapter-source-declaration.

### GET `/brapi/v2/variants`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.variants`
- **BrAPI-Den operation identity:** `brapiV21GetVariants` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Gets a filtered list of `Variants`.
**Source contract description:**
> Gets a filtered list of `Variants`.
**Can be used for:**
- Gets a filtered list of `Variants`.
- Gets a filtered list of `Variants`.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** VariantsListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-04
- **Related catalogue IDs:** brapi-den.brapi-v2-1.genotyping.get.allelematrix, brapi-den.brapi-v2-1.genotyping.get.calls, brapi-den.brapi-v2-1.genotyping.get.callsets, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.callsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.variants, brapi-den.brapi-v2-1.genotyping.post.variantsets.extract, brapi-den.brapi-v2-1.genotyping.put.calls, brapi-den.genx.v3.variant-matrices.get, brapi-den.genx.v3.variant-matrices.list, brapi-den.genx.v3.variant-matrices.register
- **Contract source:** [`Specification/BrAPI-Genotyping/Variants/Variants_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/Variants/Variants_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/variants.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/variants.py#L76) — `get_variants`; line 76; brapi-adapter-source-declaration.

### GET `/brapi/v2/variants/{variantDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid`
- **BrAPI-Den operation identity:** `brapiV21GetVariantsByVariantDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Gets a `Variant` by ID.
**Source contract description:**
> The endpoint `GET /variants/{id}` will return a JSON version of `Variant`.
**Can be used for:**
- Gets a `Variant` by ID.
- The endpoint `GET /variants/{id}` will return a JSON version of `Variant`.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-04
- **Related catalogue IDs:** brapi-den.brapi-v2-1.genotyping.get.allelematrix, brapi-den.brapi-v2-1.genotyping.get.calls, brapi-den.brapi-v2-1.genotyping.get.callsets, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variants, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.callsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.variants, brapi-den.brapi-v2-1.genotyping.post.variantsets.extract, brapi-den.brapi-v2-1.genotyping.put.calls, brapi-den.genx.v3.variant-matrices.get, brapi-den.genx.v3.variant-matrices.list, brapi-den.genx.v3.variant-matrices.register
- **Contract source:** [`Specification/BrAPI-Genotyping/Variants/Variants_VariantId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/Variants/Variants_VariantId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/variants.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/variants.py#L107) — `get_variant`; line 107; brapi-adapter-source-declaration.

### GET `/brapi/v2/variants/{variantDbId}/calls`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid.calls`
- **BrAPI-Den operation identity:** `brapiV21GetVariantsByVariantDbIdCalls` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Gets a list of `Calls` associated with a `Variant`.
**Source contract description:**
> The variant calls for this particular variant. Each one represents the determination of genotype with respect to this variant. `Calls` in this array are implicitly associated with this `Variant`.
**Can be used for:**
- Gets a list of `Calls` associated with a `Variant`.
- The variant calls for this particular variant. Each one represents the determination of genotype with respect to this variant. `Calls` in this array are implicitly associated with this `Variant`.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** CallsListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-04
- **Related catalogue IDs:** brapi-den.brapi-v2-1.genotyping.get.allelematrix, brapi-den.brapi-v2-1.genotyping.get.calls, brapi-den.brapi-v2-1.genotyping.get.callsets, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variants, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid, brapi-den.brapi-v2-1.genotyping.get.variantsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.callsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.variants, brapi-den.brapi-v2-1.genotyping.post.variantsets.extract, brapi-den.brapi-v2-1.genotyping.put.calls, brapi-den.genx.v3.variant-matrices.get, brapi-den.genx.v3.variant-matrices.list, brapi-den.genx.v3.variant-matrices.register
- **Contract source:** [`Specification/BrAPI-Genotyping/Variants/Variants_VariantId_Calls_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/Variants/Variants_VariantId_Calls_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/variants.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/variants.py#L172) — `get_variant_calls`; line 172; brapi-adapter-source-declaration.

### GET `/brapi/v2/variantsets`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.variantsets`
- **BrAPI-Den operation identity:** `brapiV21GetVariantsets` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Gets a filtered list of `VariantSets`.
**Source contract description:**
> Will return a filtered list of `VariantSet`.
**Can be used for:**
- Gets a filtered list of `VariantSets`.
- Will return a filtered list of `VariantSet`.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** VariantSetsListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-04
- **Related catalogue IDs:** brapi-den.brapi-v2-1.genotyping.get.allelematrix, brapi-den.brapi-v2-1.genotyping.get.calls, brapi-den.brapi-v2-1.genotyping.get.callsets, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variants, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.callsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.variants, brapi-den.brapi-v2-1.genotyping.post.variantsets.extract, brapi-den.brapi-v2-1.genotyping.put.calls, brapi-den.genx.v3.variant-matrices.get, brapi-den.genx.v3.variant-matrices.list, brapi-den.genx.v3.variant-matrices.register
- **Contract source:** [`Specification/BrAPI-Genotyping/VariantSets/VariantSets_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/VariantSets/VariantSets_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/variantsets.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/variantsets.py#L68) — `get_variantsets`; line 68; brapi-adapter-source-declaration.

### POST `/brapi/v2/variantsets/extract`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.post.variantsets.extract`
- **BrAPI-Den operation identity:** `brapiV21PostVariantsetsExtract` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Variant Sets
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Create new `VariantSet` based on search results
**Source contract description:**
> Will perform a search for `Calls` which match the search criteria in `variantSetsExtractRequest`. The results of the search will be used to create a new `VariantSet` on the server. The new `VariantSet` will be returned.
**Can be used for:**
- Create new `VariantSet` based on search results
- Will perform a search for `Calls` which match the search criteria in `variantSetsExtractRequest`. The results of the search will be used to create a new `VariantSet` on the server. The new `VariantSet` will be returned.
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** VariantSetsExtractRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-04
- **Related catalogue IDs:** brapi-den.brapi-v2-1.genotyping.get.allelematrix, brapi-den.brapi-v2-1.genotyping.get.calls, brapi-den.brapi-v2-1.genotyping.get.callsets, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variants, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.callsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.variants, brapi-den.brapi-v2-1.genotyping.put.calls, brapi-den.genx.v3.variant-matrices.get, brapi-den.genx.v3.variant-matrices.list, brapi-den.genx.v3.variant-matrices.register
- **Contract source:** [`Specification/BrAPI-Genotyping/VariantSets/VariantSets_Extract_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/VariantSets/VariantSets_Extract_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/variantsets.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/variantsets.py#L292) — `extract_variantset`; line 292; brapi-adapter-source-declaration.

### GET `/brapi/v2/variantsets/{variantSetDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid`
- **BrAPI-Den operation identity:** `brapiV21GetVariantsetsByVariantSetDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Gets a `VariantSet` by ID.
**Source contract description:**
> This call will return a JSON version of a `VariantSet`.
**Can be used for:**
- Gets a `VariantSet` by ID.
- This call will return a JSON version of a `VariantSet`.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-04
- **Related catalogue IDs:** brapi-den.brapi-v2-1.genotyping.get.allelematrix, brapi-den.brapi-v2-1.genotyping.get.calls, brapi-den.brapi-v2-1.genotyping.get.callsets, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variants, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.callsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.variants, brapi-den.brapi-v2-1.genotyping.post.variantsets.extract, brapi-den.brapi-v2-1.genotyping.put.calls, brapi-den.genx.v3.variant-matrices.get, brapi-den.genx.v3.variant-matrices.list, brapi-den.genx.v3.variant-matrices.register
- **Contract source:** [`Specification/BrAPI-Genotyping/VariantSets/VariantSets_VariantSetId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/VariantSets/VariantSets_VariantSetId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/variantsets.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/variantsets.py#L94) — `get_variantset`; line 94; brapi-adapter-source-declaration.

### GET `/brapi/v2/variantsets/{variantSetDbId}/calls`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.calls`
- **BrAPI-Den operation identity:** `brapiV21GetVariantsetsByVariantSetDbIdCalls` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Gets a list of `Calls` associated with a `VariantSet`.
**Source contract description:**
> Gets a list of `Calls` associated with a `VariantSet`.
**Can be used for:**
- Gets a list of `Calls` associated with a `VariantSet`.
- Gets a list of `Calls` associated with a `VariantSet`.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** CallsListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-04
- **Related catalogue IDs:** brapi-den.brapi-v2-1.genotyping.get.allelematrix, brapi-den.brapi-v2-1.genotyping.get.calls, brapi-den.brapi-v2-1.genotyping.get.callsets, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variants, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.callsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.variants, brapi-den.brapi-v2-1.genotyping.post.variantsets.extract, brapi-den.brapi-v2-1.genotyping.put.calls, brapi-den.genx.v3.variant-matrices.get, brapi-den.genx.v3.variant-matrices.list, brapi-den.genx.v3.variant-matrices.register
- **Contract source:** [`Specification/BrAPI-Genotyping/VariantSets/VariantSets_VariantSetId_Calls_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/VariantSets/VariantSets_VariantSetId_Calls_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/variantsets.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/variantsets.py#L159) — `get_variantset_calls`; line 159; brapi-adapter-source-declaration.

### GET `/brapi/v2/variantsets/{variantSetDbId}/callsets`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.callsets`
- **BrAPI-Den operation identity:** `brapiV21GetVariantsetsByVariantSetDbIdCallsets` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Gets a list of `CallSets` associated with a `VariantSet`.
**Source contract description:**
> Gets a list of `CallSets` associated with a `VariantSet`.
**Can be used for:**
- Gets a list of `CallSets` associated with a `VariantSet`.
- Gets a list of `CallSets` associated with a `VariantSet`.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** CallSetsListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-04
- **Related catalogue IDs:** brapi-den.brapi-v2-1.genotyping.get.allelematrix, brapi-den.brapi-v2-1.genotyping.get.calls, brapi-den.brapi-v2-1.genotyping.get.callsets, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variants, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.variants, brapi-den.brapi-v2-1.genotyping.post.variantsets.extract, brapi-den.brapi-v2-1.genotyping.put.calls, brapi-den.genx.v3.variant-matrices.get, brapi-den.genx.v3.variant-matrices.list, brapi-den.genx.v3.variant-matrices.register
- **Contract source:** [`Specification/BrAPI-Genotyping/VariantSets/VariantSets_VariantSetId_CallSets_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/VariantSets/VariantSets_VariantSetId_CallSets_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/variantsets.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/variantsets.py#L203) — `get_variantset_callsets`; line 203; brapi-adapter-source-declaration.

### GET `/brapi/v2/variantsets/{variantSetDbId}/variants`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.variants`
- **BrAPI-Den operation identity:** `brapiV21GetVariantsetsByVariantSetDbIdVariants` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Gets a `Variants` for a given `VariantSet`.
**Source contract description:**
> This call will return an array of `Variants`.
**Can be used for:**
- Gets a `Variants` for a given `VariantSet`.
- This call will return an array of `Variants`.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** VariantsListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-04
- **Related catalogue IDs:** brapi-den.brapi-v2-1.genotyping.get.allelematrix, brapi-den.brapi-v2-1.genotyping.get.calls, brapi-den.brapi-v2-1.genotyping.get.callsets, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid, brapi-den.brapi-v2-1.genotyping.get.callsets.by-callsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variants, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid, brapi-den.brapi-v2-1.genotyping.get.variants.by-variantdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.calls, brapi-den.brapi-v2-1.genotyping.get.variantsets.by-variantsetdbid.callsets, brapi-den.brapi-v2-1.genotyping.post.variantsets.extract, brapi-den.brapi-v2-1.genotyping.put.calls, brapi-den.genx.v3.variant-matrices.get, brapi-den.genx.v3.variant-matrices.list, brapi-den.genx.v3.variant-matrices.register
- **Contract source:** [`Specification/BrAPI-Genotyping/VariantSets/VariantSets_VariantSetId_Variants_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/VariantSets/VariantSets_VariantSetId_Variants_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/variantsets.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/variantsets.py#L253) — `get_variantset_variants`; line 253; brapi-adapter-source-declaration.

### GET `/brapi/v2/vendor/orders`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.vendor.orders`
- **BrAPI-Den operation identity:** `brapiV21GetVendorOrders` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Vendor
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> List current available orders
**Source contract description:**
> List current available orders
**Can be used for:**
- List current available orders
- List current available orders
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Genotyping/VendorSamples/Vendor_Orders_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/VendorSamples/Vendor_Orders_GET_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/vendor.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/vendor.py#L138) — `list_vendor_orders`; line 138; brapi-adapter-source-declaration.

### POST `/brapi/v2/vendor/orders`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.post.vendor.orders`
- **BrAPI-Den operation identity:** `brapiV21PostVendorOrders` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Vendor
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit New Order
**Source contract description:**
> Submit a new order to a vendor
**Can be used for:**
- Submit New Order
- Submit a new order to a vendor
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** VendorOrderSubmissionRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Genotyping/VendorSamples/Vendor_Orders_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/VendorSamples/Vendor_Orders_GET_POST.yaml)
- **BijMantra inventory row:** [line 58](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L58); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/vendor.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/vendor.py#L176) — `create_vendor_order`; line 176; brapi-adapter-source-declaration.

### GET `/brapi/v2/vendor/orders/{orderId}/plates`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.vendor.orders.by-orderid.plates`
- **BrAPI-Den operation identity:** `brapiV21GetVendorOrdersByOrderIdPlates` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Vendor
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the Plates for a specific Order
**Source contract description:**
> Retrieve the plate and sample details of an order being processed
**Can be used for:**
- Get the Plates for a specific Order
- Retrieve the plate and sample details of an order being processed
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Genotyping/VendorSamples/Vendor_Orders_OrderId_Plates_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/VendorSamples/Vendor_Orders_OrderId_Plates_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/vendor.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/vendor.py#L208) — `get_vendor_order_plates`; line 208; brapi-adapter-source-declaration.

### GET `/brapi/v2/vendor/orders/{orderId}/results`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.vendor.orders.by-orderid.results`
- **BrAPI-Den operation identity:** `brapiV21GetVendorOrdersByOrderIdResults` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Vendor
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a specific Order
**Source contract description:**
> Retrieve the data files generated by the vendors analysis
**Can be used for:**
- Get the results of a specific Order
- Retrieve the data files generated by the vendors analysis
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Genotyping/VendorSamples/Vendor_Orders_OrderId_Results_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/VendorSamples/Vendor_Orders_OrderId_Results_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/vendor.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/vendor.py#L282) — `get_vendor_order_results`; line 282; brapi-adapter-source-declaration.

### GET `/brapi/v2/vendor/orders/{orderId}/status`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.vendor.orders.by-orderid.status`
- **BrAPI-Den operation identity:** `brapiV21GetVendorOrdersByOrderIdStatus` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Vendor
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the status of a specific Order
**Source contract description:**
> Retrieve the current status of an order being processed
**Can be used for:**
- Get the status of a specific Order
- Retrieve the current status of an order being processed
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Genotyping/VendorSamples/Vendor_Orders_OrderId_Status_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/VendorSamples/Vendor_Orders_OrderId_Status_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/vendor.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/vendor.py#L339) — `get_vendor_order_status`; line 339; brapi-adapter-source-declaration.

### POST `/brapi/v2/vendor/plates`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.post.vendor.plates`
- **BrAPI-Den operation identity:** `brapiV21PostVendorPlates` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Vendor
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a new set of Sample data
**Source contract description:**
> Submit a new set of Sample data
**Can be used for:**
- Submit a new set of Sample data
- Submit a new set of Sample data
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** VendorPlateSubmissionRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Genotyping/VendorSamples/Vendor_Plates_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/VendorSamples/Vendor_Plates_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/vendor.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/vendor.py#L384) — `submit_vendor_plates`; line 384; brapi-adapter-source-declaration.

### GET `/brapi/v2/vendor/plates/{submissionId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.vendor.plates.by-submissionid`
- **BrAPI-Den operation identity:** `brapiV21GetVendorPlatesBySubmissionId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Vendor
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the data for a submitted set of plates
**Source contract description:**
> Get data for a submitted set of plates
**Can be used for:**
- Get the data for a submitted set of plates
- Get data for a submitted set of plates
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Genotyping/VendorSamples/Vendor_Plates_SubmissionId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/VendorSamples/Vendor_Plates_SubmissionId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/vendor.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/vendor.py#L426) — `get_vendor_plate_submission`; line 426; brapi-adapter-source-declaration.

### GET `/brapi/v2/vendor/specifications`

- **Catalogue ID:** `brapi-den.brapi-v2-1.genotyping.get.vendor.specifications`
- **BrAPI-Den operation identity:** `brapiV21GetVendorSpecifications` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Genotyping
- **Source tag:** Vendor
- **Proposed BrAPI-Den classification:** D3 — Genotyping and Molecular Genomics; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official BrAPI Genotyping module; proposed crosswalk to molecular genomics.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the Vendor Specifications
**Source contract description:**
> Defines the plate format specification for the vendor.
**Can be used for:**
- Get the Vendor Specifications
- Defines the plate format specification for the vendor.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200
- **Response component refs recorded:** —
- **Contract source:** [`Specification/BrAPI-Genotyping/VendorSamples/Vendor_Specifications_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Genotyping/VendorSamples/Vendor_Specifications_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/vendor.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/vendor.py#L76) — `get_vendor_specifications`; line 76; brapi-adapter-source-declaration.

### BrAPI-Phenotyping — 49 operations

### POST `/brapi/v2/delete/images`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.post.delete.images`
- **BrAPI-Den operation identity:** `brapiV21PostDeleteImages` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Images
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a delete request for `Images`
**Source contract description:**
> Submit a delete request for `Images`
**Can be used for:**
- Submit a delete request for `Images`
- Submit a delete request for `Images`
**Must not be used for / explicit non-goals:**
- Do not treat as read/create/general update; this is a deletion command.
- Deletion scope and retry behavior must follow the operation-specific contract.
- **Side effects:** Destructive deletion command; exact scope follows the request contract.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ImageSearchRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** ImageDeleteResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Phenotyping/Images/Delete_Images_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Images/Delete_Images_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 0 exact normalized method/path candidate(s); 0 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - No exact normalized source declaration was found. This is not proof of runtime absence.

### POST `/brapi/v2/delete/observations`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.post.delete.observations`
- **BrAPI-Den operation identity:** `brapiV21PostDeleteObservations` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observations
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a delete request for `Observations`
**Source contract description:**
> Submit a delete request for `Observations`
**Can be used for:**
- Submit a delete request for `Observations`
- Submit a delete request for `Observations`
**Must not be used for / explicit non-goals:**
- Do not treat as read/create/general update; this is a deletion command.
- Deletion scope and retry behavior must follow the operation-specific contract.
- **Side effects:** Destructive deletion command; exact scope follows the request contract.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ObservationSearchRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** ObservationDeleteResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-03
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query
- **Contract source:** [`Specification/BrAPI-Phenotyping/Observations/Delete_Observations_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Observations/Delete_Observations_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/observations.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/observations.py#L478) — `delete_observations_bulk`; line 478; brapi-adapter-source-declaration.

### GET `/brapi/v2/events`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.events`
- **BrAPI-Den operation identity:** `brapiV21GetEvents` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Events
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the Events
**Source contract description:**
> Get list of events
**Can be used for:**
- Get the Events
- Get list of events
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Phenotyping/Events/Events_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Events/Events_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/events.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/events.py#L63) — `list_events`; line 63; brapi-adapter-source-declaration.

### GET `/brapi/v2/images`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.images`
- **BrAPI-Den operation identity:** `brapiV21GetImages` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Images
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the image metadata summaries
**Source contract description:**
> Get filtered set of image metadata
>
> Implementation Notes
>
> - ''imageURL'' should be a complete URL describing the location of the image. There is no BrAPI call for 
> retrieving the image content, so it could be on a different path, or a different host.
>
> - ''descriptiveOntologyTerm'' can be thought of as Tags for the image. These could be simple descriptive 
> words, or ontology references, or full ontology URI''s.
**Can be used for:**
- Get the image metadata summaries
- Get filtered set of image metadata
  
  Implementation Notes
  
  - ''imageURL'' should be a complete URL describing the location of the image. There is no BrAPI call for 
  retrieving the image content, so it could be on a different path, or a different host.
  
  - ''descriptiveOntologyTerm'' can be thought of as Tags for the image. These could be simple descriptive 
  words, or ontology references, or full ontology URI''s.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** ImageListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Phenotyping/Images/Images_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Images/Images_GET_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/images.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/images.py#L82) — `list_images`; line 82; brapi-adapter-source-declaration.

### POST `/brapi/v2/images`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.post.images`
- **BrAPI-Den operation identity:** `brapiV21PostImages` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Images
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Create new image metadata records
**Source contract description:**
> Create new image metadata records
>
> Implementation Notes
>
> - This endpoint should be implemented with 'PUT /images/{imageDbId}/imagecontent' for full image upload capability
>
> - ''imageURL'' should be a complete URL describing the location of the image. There is no BrAPI call for retrieving 
> the image content, so it could be on a different path, or a different host.
>
> - ''descriptiveOntologyTerm'' can be thought of as Tags for the image. These could be simple descriptive words, or 
> ontology references, or full ontology URI's.
>
> - The '/images' calls support a GeoJSON object structure for describing their location. The BrAPI spec for GeoJSON 
> only supports two of the possible geometries; Points and Polygons.
>
> - With most images, the Point geometry should be used, and it should indicate the longitude and latitude of the camera.
>
> - For top down images (ie from drones, cranes, etc), the Point geometry may be used to indicate the longitude and 
> latitude of the centroid of the image content, and the Polygon geometry may be used to indicate the border of the 
> image content.
>
> An example use case is available on the BrAPI Wiki -> https://wiki.brapi.org/index.php/Image_Upload
**Can be used for:**
- Create new image metadata records
- Create new image metadata records
  
  Implementation Notes
  
  - This endpoint should be implemented with 'PUT /images/{imageDbId}/imagecontent' for full image upload capability
  
  - ''imageURL'' should be a complete URL describing the location of the image. There is no BrAPI call for retrieving 
  the image content, so it could be on a different path, or a different host.
  
  - ''descriptiveOntologyTerm'' can be thought of as Tags for the image. These could be simple descriptive words, or 
  ontology references, or full ontology URI's.
  
  - The '/images' calls support a GeoJSON object structure for describing their location. The BrAPI spec for GeoJSON 
  only supports two of the possible geometries; Points and Polygons.
  
  - With most images, the Point geometry should be used, and it should indicate the longitude and latitude of the camera.
  
  - For top down images (ie from drones, cranes, etc), the Point geometry may be used to indicate the longitude and 
  latitude of the centroid of the image content, and the Polygon geometry may be used to indicate the border of the 
  image content.
  
  An example use case is available on the BrAPI Wiki -> https://wiki.brapi.org/index.php/Image_Upload
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ImageNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** ImageListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Phenotyping/Images/Images_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Images/Images_GET_POST.yaml)
- **BijMantra inventory row:** [line 69](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L69); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/images.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/images.py#L111) — `create_image`; line 111; brapi-adapter-source-declaration.

### GET `/brapi/v2/images/{imageDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.images.by-imagedbid`
- **BrAPI-Den operation identity:** `brapiV21GetImagesByImageDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Images
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the an image metadata summary
**Source contract description:**
> Get one image metadata object
>
> Implementation Notes
>
> - ''imageURL'' should be a complete URL describing the location of the image. There is no BrAPI call for 
> retrieving the image content, so it could be on a different path, or a different host.
>
> - ''descriptiveOntologyTerm'' can be thought of as Tags for the image. These could be simple descriptive 
> words, or ontology references, or full ontology URI''s.
**Can be used for:**
- Get the an image metadata summary
- Get one image metadata object
  
  Implementation Notes
  
  - ''imageURL'' should be a complete URL describing the location of the image. There is no BrAPI call for 
  retrieving the image content, so it could be on a different path, or a different host.
  
  - ''descriptiveOntologyTerm'' can be thought of as Tags for the image. These could be simple descriptive 
  words, or ontology references, or full ontology URI''s.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** ImageSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Phenotyping/Images/Images_ImageDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Images/Images_ImageDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/images.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/images.py#L128) — `get_image`; line 128; brapi-adapter-source-declaration.

### PUT `/brapi/v2/images/{imageDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.put.images.by-imagedbid`
- **BrAPI-Den operation identity:** `brapiV21PutImagesByImageDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Images
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update an existing image metadata record
**Source contract description:**
> Update an existing image metadata record
>
> Implementation Notes
>
> - This endpoint should be implemented with 'PUT /images/{imageDbId}/imagecontent' for full image update capability
>
> - A server may choose to modify the image metadata object based on the actually image which has been uploaded. 
>
> - Image data may be stored in a database or file system. Servers should generate and provide the "imageURL" as an 
> absolute path for retrieving the image, wherever it happens to live. 
>
> - 'descriptiveOntologyTerm' can be thought of as Tags for the image. These could be simple descriptive words, or 
> ontology references, or full ontology URI's. 
>
> - The '/images' calls support a GeoJSON object structure for describing their location. The BrAPI spec for GeoJSON 
> only supports two of the possible geometries; Points and Polygons. 
>
> - With most images, the Point geometry should be used, and it should indicate the longitude and latitude of the camera. 
>
> - For top down images (ie from drones, cranes, etc), the Point geometry may be used to indicate the longitude and 
> latitude of the centroid of the image content, and the Polygon geometry may be used to indicate the border of the 
> image content.
>
> An example use case is available on the BrAPI Wiki -> https://wiki.brapi.org/index.php/Image_Upload
**Can be used for:**
- Update an existing image metadata record
- Update an existing image metadata record
  
  Implementation Notes
  
  - This endpoint should be implemented with 'PUT /images/{imageDbId}/imagecontent' for full image update capability
  
  - A server may choose to modify the image metadata object based on the actually image which has been uploaded. 
  
  - Image data may be stored in a database or file system. Servers should generate and provide the "imageURL" as an 
  absolute path for retrieving the image, wherever it happens to live. 
  
  - 'descriptiveOntologyTerm' can be thought of as Tags for the image. These could be simple descriptive words, or 
  ontology references, or full ontology URI's. 
  
  - The '/images' calls support a GeoJSON object structure for describing their location. The BrAPI spec for GeoJSON 
  only supports two of the possible geometries; Points and Polygons. 
  
  - With most images, the Point geometry should be used, and it should indicate the longitude and latitude of the camera. 
  
  - For top down images (ie from drones, cranes, etc), the Point geometry may be used to indicate the longitude and 
  latitude of the centroid of the image content, and the Polygon geometry may be used to indicate the border of the 
  image content.
  
  An example use case is available on the BrAPI Wiki -> https://wiki.brapi.org/index.php/Image_Upload
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ImageNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** ImageSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Phenotyping/Images/Images_ImageDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Images/Images_ImageDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 40](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L40); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/images.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/images.py#L142) — `update_image`; line 142; brapi-adapter-source-declaration.

### PUT `/brapi/v2/images/{imageDbId}/imagecontent`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.put.images.by-imagedbid.imagecontent`
- **BrAPI-Den operation identity:** `brapiV21PutImagesByImageDbIdImagecontent` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Images
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Attach an image binary file to an existing image metadata record
**Source contract description:**
> This endpoint is used to attach an image binary file to an existing image metadata record. All of the other Images endpoints 
> deal with the JSON for image metadata, but 'PUT /images/{imageDbId}/imagecontent' allows you to send any binary file with a Content 
> Type (MIME) of image/*. When the real image is uploaded, the server may choose to update some of the metadata to reflect the 
> reality of the image that was uploaded, and should respond with the updated JSON.
>
> Implementation Notes
>
> - This endpoint should be implemented with 'POST /images' for full image upload capability
>
> - This endpoint should be implemented with 'PUT /images/{imageDbId}' for full image update capability
>
> - A server may choose to modify the image metadata object based on the actually image which has been uploaded by this endpoint. 
>
> - Image data may be stored in a database or file system. Servers should generate and provide the "imageURL" for retrieving the 
>   image binary file. 
>
> An example use case is available on the BrAPI Wiki -> https://wiki.brapi.org/index.php/Image_Upload
**Can be used for:**
- Attach an image binary file to an existing image metadata record
- This endpoint is used to attach an image binary file to an existing image metadata record. All of the other Images endpoints 
  deal with the JSON for image metadata, but 'PUT /images/{imageDbId}/imagecontent' allows you to send any binary file with a Content 
  Type (MIME) of image/*. When the real image is uploaded, the server may choose to update some of the metadata to reflect the 
  reality of the image that was uploaded, and should respond with the updated JSON.
  
  Implementation Notes
  
  - This endpoint should be implemented with 'POST /images' for full image upload capability
  
  - This endpoint should be implemented with 'PUT /images/{imageDbId}' for full image update capability
  
  - A server may choose to modify the image metadata object based on the actually image which has been uploaded by this endpoint. 
  
  - Image data may be stored in a database or file system. Servers should generate and provide the "imageURL" for retrieving the 
    image binary file. 
  
  An example use case is available on the BrAPI Wiki -> https://wiki.brapi.org/index.php/Image_Upload
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** ImageSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Contract source:** [`Specification/BrAPI-Phenotyping/Images/Images_ImageDbId_ImageContent_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Images/Images_ImageDbId_ImageContent_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 0 exact normalized method/path candidate(s); 0 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - No exact normalized source declaration was found. This is not proof of runtime absence.

### GET `/brapi/v2/methods`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.methods`
- **BrAPI-Den operation identity:** `brapiV21GetMethods` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Methods
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C4 — Scientific terminology governance; Crosswalk basis: inferred-from-route; Crosswalk note: Scientific term definitions are shared semantics, not measured observations.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the Methods
**Source contract description:**
> Returns a list of Methods available on a server.
>
> An Observation Variable has 3 critical parts; A Trait being observed, a Method for making the observation, and a Scale on which the observation can be measured and compared with other observations.
**Can be used for:**
- Get the Methods
- Returns a list of Methods available on a server.
  
  An Observation Variable has 3 critical parts; A Trait being observed, a Method for making the observation, and a Scale on which the observation can be measured and compared with other observations.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** MethodListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-06
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.variable-terms.get-version, brapi-den.genx.v3.variable-terms.list, brapi-den.genx.v3.variable-terms.publish-version
- **Contract source:** [`Specification/BrAPI-Phenotyping/Methods/Methods_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Methods/Methods_GET_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/methods.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/methods.py#L95) — `get_methods`; line 95; brapi-adapter-source-declaration.

### POST `/brapi/v2/methods`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.post.methods`
- **BrAPI-Den operation identity:** `brapiV21PostMethods` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Methods
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C4 — Scientific terminology governance; Crosswalk basis: inferred-from-route; Crosswalk note: Scientific term definitions are shared semantics, not measured observations.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Add new Methods
**Source contract description:**
> Create new method objects in the database
**Can be used for:**
- Add new Methods
- Create new method objects in the database
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** MethodNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** MethodListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-06
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.variable-terms.get-version, brapi-den.genx.v3.variable-terms.list, brapi-den.genx.v3.variable-terms.publish-version
- **Contract source:** [`Specification/BrAPI-Phenotyping/Methods/Methods_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Methods/Methods_GET_POST.yaml)
- **BijMantra inventory row:** [line 46](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L46); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/methods.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/methods.py#L200) — `create_methods`; line 200; brapi-adapter-source-declaration.

### GET `/brapi/v2/methods/{methodDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid`
- **BrAPI-Den operation identity:** `brapiV21GetMethodsByMethodDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Methods
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C4 — Scientific terminology governance; Crosswalk basis: inferred-from-route; Crosswalk note: Scientific term definitions are shared semantics, not measured observations.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the details for a specific Method
**Source contract description:**
> Retrieve details about a specific method
>
> An Observation Variable has 3 critical parts; A Trait being observed, a Method for making the observation, and a Scale on which the observation can be measured and compared with other observations.
**Can be used for:**
- Get the details for a specific Method
- Retrieve details about a specific method
  
  An Observation Variable has 3 critical parts; A Trait being observed, a Method for making the observation, and a Scale on which the observation can be measured and compared with other observations.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** MethodSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-06
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.variable-terms.get-version, brapi-den.genx.v3.variable-terms.list, brapi-den.genx.v3.variable-terms.publish-version
- **Contract source:** [`Specification/BrAPI-Phenotyping/Methods/Methods_MethodDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Methods/Methods_MethodDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/methods.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/methods.py#L156) — `get_method`; line 156; brapi-adapter-source-declaration.

### PUT `/brapi/v2/methods/{methodDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid`
- **BrAPI-Den operation identity:** `brapiV21PutMethodsByMethodDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Methods
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C4 — Scientific terminology governance; Crosswalk basis: inferred-from-route; Crosswalk note: Scientific term definitions are shared semantics, not measured observations.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update an existing Method
**Source contract description:**
> Update the details of an existing method
**Can be used for:**
- Update an existing Method
- Update the details of an existing method
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** MethodNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** MethodSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-06
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.variable-terms.get-version, brapi-den.genx.v3.variable-terms.list, brapi-den.genx.v3.variable-terms.publish-version
- **Contract source:** [`Specification/BrAPI-Phenotyping/Methods/Methods_MethodDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Methods/Methods_MethodDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 34](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L34); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/methods.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/methods.py#L255) — `update_method`; line 255; brapi-adapter-source-declaration.

### GET `/brapi/v2/observationlevels`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.observationlevels`
- **BrAPI-Den operation identity:** `brapiV21GetObservationlevels` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observation Units
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the Observation Levels
**Source contract description:**
> Call to retrieve the list of supported observation levels. 
>
> Observation levels indicate the granularity level at which the measurements are taken. `levelName` defines the level, `levelOrder` defines where that level exists in the hierarchy of levels. `levelOrder`s lower numbers are at the top of the hierarchy (ie field > 0) and higher numbers are at the bottom of the hierarchy (ie plant > 6). 
>
> The values are used to supply the `observationLevel` parameter in the observation unit details call.
>       
> For more information on Observation Levels, please review the <a target="_blank" href="https://wiki.brapi.org/index.php/Observation_Levels">Observation Levels documentation</a>.
**Can be used for:**
- Get the Observation Levels
- Call to retrieve the list of supported observation levels. 
  
  Observation levels indicate the granularity level at which the measurements are taken. `levelName` defines the level, `levelOrder` defines where that level exists in the hierarchy of levels. `levelOrder`s lower numbers are at the top of the hierarchy (ie field > 0) and higher numbers are at the bottom of the hierarchy (ie plant > 6). 
  
  The values are used to supply the `observationLevel` parameter in the observation unit details call.
        
  For more information on Observation Levels, please review the <a target="_blank" href="https://wiki.brapi.org/index.php/Observation_Levels">Observation Levels documentation</a>.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** 400BadRequest, 401Unauthorized, 403Forbidden
- **Contract source:** [`Specification/BrAPI-Phenotyping/ObservationUnits/ObservationLevels_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/ObservationUnits/ObservationLevels_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/observationlevels.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/observationlevels.py#L61) — `get_observation_levels`; line 61; brapi-adapter-source-declaration.

### GET `/brapi/v2/observations`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.observations`
- **BrAPI-Den operation identity:** `brapiV21GetObservations` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observations
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get a filtered set of Observations
**Source contract description:**
> Retrieve all observations where there are measurements for the given observation variables. 
>
> observationTimestamp should be ISO8601 format with timezone -> YYYY-MM-DDThh:mm:ss+hhmm
**Can be used for:**
- Get a filtered set of Observations
- Retrieve all observations where there are measurements for the given observation variables. 
  
  observationTimestamp should be ISO8601 format with timezone -> YYYY-MM-DDThh:mm:ss+hhmm
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** ObservationListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-03
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query
- **Contract source:** [`Specification/BrAPI-Phenotyping/Observations/Observations_GET_POST_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Observations/Observations_GET_POST_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/observations.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/observations.py#L73) — `list_observations`; line 73; brapi-adapter-source-declaration.

### POST `/brapi/v2/observations`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.post.observations`
- **BrAPI-Den operation identity:** `brapiV21PostObservations` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observations
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Add new Observation entities
**Source contract description:**
> Add new Observation entities
**Can be used for:**
- Add new Observation entities
- Add new Observation entities
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ObservationNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** ObservationListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-03
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query
- **Contract source:** [`Specification/BrAPI-Phenotyping/Observations/Observations_GET_POST_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Observations/Observations_GET_POST_PUT.yaml)
- **BijMantra inventory row:** [line 87](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L87); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/observations.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/observations.py#L155) — `create_observation`; line 155; brapi-adapter-source-declaration.

### PUT `/brapi/v2/observations`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.put.observations`
- **BrAPI-Den operation identity:** `brapiV21PutObservations` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observations
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update multiple Observation entities
**Source contract description:**
> Update multiple Observation entities simultaneously with a single call 
>
> Include as many `observationDbIds` in the request as needed. 
>
> Note - In strictly typed languages, this structure can be represented as a Map or Dictionary of objects and parsed directly from JSON.
**Can be used for:**
- Update multiple Observation entities
- Update multiple Observation entities simultaneously with a single call 
  
  Include as many `observationDbIds` in the request as needed. 
  
  Note - In strictly typed languages, this structure can be represented as a Map or Dictionary of objects and parsed directly from JSON.
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ObservationNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** ObservationListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-03
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query
- **Contract source:** [`Specification/BrAPI-Phenotyping/Observations/Observations_GET_POST_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Observations/Observations_GET_POST_PUT.yaml)
- **BijMantra inventory row:** [line 113](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L113); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/observations.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/observations.py#L274) — `update_observations`; line 274; brapi-adapter-source-declaration.

### GET `/brapi/v2/observations/table`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.observations.table`
- **BrAPI-Den operation identity:** `brapiV21GetObservationsTable` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observations
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get a list of Observations in a table format
**Source contract description:**
> <p>This service is designed to retrieve a table of time dependant observation values as a matrix of Observation Units and Observation Variables.
> This is also sometimes called a Time Series. This service takes the "Sparse Table" approach for representing this time dependant data.</p>
> <p>The table may be represented by JSON, CSV, or TSV. The "Accept" HTTP header is used for the client to request different return formats. 
> By default, if the "Accept" header is not included in the request, the server should return JSON as described below.</p>
> <p>The table is REQUIRED to have the following columns</p>
> <ul>
>   <li>observationUnitDbId - Each row is related to one Observation Unit</li>
>   <li>observationTimeStamp - Each row is has a time stamp for when the observation was taken</li>
>   <li>At least one column with an observationVariableDbId</li>
> </ul>
> <p>The table may have any or all of the following OPTIONAL columns. Included columns are decided by the server developer</p>
> <ul>
>   <li>observationUnitName</li>
>   <li>studyDbId</li>
>   <li>studyName</li>
>   <li>germplasmDbId</li>
>   <li>germplasmName</li>
>   <li>positionCoordinateX</li>
>   <li>positionCoordinateY</li>
>   <li>year</li>
> </ul>
> <p>The table also may have any number of Observation Unit Hierarchy Level columns. For example:</p>
> <ul>
>   <li>field</li>
>   <li>plot</li>
>   <li>sub-plot</li>
>   <li>plant</li>
>   <li>pot</li>
>   <li>block</li>
>   <li>entry</li>
>   <li>rep</li>
> </ul>
> <p>The JSON representation provides a pair of extra arrays for defining the headers of the table. 
> The first array "headerRow" will always contain "observationUnitDbId" and any or all of the OPTIONAL column header names. 
> The second array "observationVariables" contains the names and DbIds for the Observation Variables represented in the table. 
> By appending the two arrays, you can construct the complete header row of the table. </p>
> <p>For CSV and TSV representations of the table, an extra header row is needed to describe both the Observation Variable DbId and the Observation Variable Name for each data column. 
> See the example responses below</p>
**Can be used for:**
- Get a list of Observations in a table format
- <p>This service is designed to retrieve a table of time dependant observation values as a matrix of Observation Units and Observation Variables.
  This is also sometimes called a Time Series. This service takes the "Sparse Table" approach for representing this time dependant data.</p>
  <p>The table may be represented by JSON, CSV, or TSV. The "Accept" HTTP header is used for the client to request different return formats. 
  By default, if the "Accept" header is not included in the request, the server should return JSON as described below.</p>
  <p>The table is REQUIRED to have the following columns</p>
  <ul>
    <li>observationUnitDbId - Each row is related to one Observation Unit</li>
    <li>observationTimeStamp - Each row is has a time stamp for when the observation was taken</li>
    <li>At least one column with an observationVariableDbId</li>
  </ul>
  <p>The table may have any or all of the following OPTIONAL columns. Included columns are decided by the server developer</p>
  <ul>
    <li>observationUnitName</li>
    <li>studyDbId</li>
    <li>studyName</li>
    <li>germplasmDbId</li>
    <li>germplasmName</li>
    <li>positionCoordinateX</li>
    <li>positionCoordinateY</li>
    <li>year</li>
  </ul>
  <p>The table also may have any number of Observation Unit Hierarchy Level columns. For example:</p>
  <ul>
    <li>field</li>
    <li>plot</li>
    <li>sub-plot</li>
    <li>plant</li>
    <li>pot</li>
    <li>block</li>
    <li>entry</li>
    <li>rep</li>
  </ul>
  <p>The JSON representation provides a pair of extra arrays for defining the headers of the table. 
  The first array "headerRow" will always contain "observationUnitDbId" and any or all of the OPTIONAL column header names. 
  The second array "observationVariables" contains the names and DbIds for the Observation Variables represented in the table. 
  By appending the two arrays, you can construct the complete header row of the table. </p>
  <p>For CSV and TSV representations of the table, an extra header row is needed to describe both the Observation Variable DbId and the Observation Variable Name for each data column. 
  See the example responses below</p>
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** ObservationTableResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-03
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query
- **Contract source:** [`Specification/BrAPI-Phenotyping/Observations/Observations_Table_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Observations/Observations_Table_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/observations.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/observations.py#L384) — `get_observations_table`; line 384; brapi-adapter-source-declaration.

### GET `/brapi/v2/observations/{observationDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid`
- **BrAPI-Den operation identity:** `brapiV21GetObservationsByObservationDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observations
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the details of a specific Observations
**Source contract description:**
> Get the details of a specific Observations
>
> observationTimestamp should be ISO8601 format with timezone -> YYYY-MM-DDThh:mm:ss+hhmm
**Can be used for:**
- Get the details of a specific Observations
- Get the details of a specific Observations
  
  observationTimestamp should be ISO8601 format with timezone -> YYYY-MM-DDThh:mm:ss+hhmm
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** ObservationSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-03
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query
- **Contract source:** [`Specification/BrAPI-Phenotyping/Observations/Observations_ObservationDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Observations/Observations_ObservationDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/observations.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/observations.py#L233) — `get_observation`; line 233; brapi-adapter-source-declaration.

### PUT `/brapi/v2/observations/{observationDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid`
- **BrAPI-Den operation identity:** `brapiV21PutObservationsByObservationDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observations
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update an existing Observation
**Source contract description:**
> Update an existing Observation
**Can be used for:**
- Update an existing Observation
- Update an existing Observation
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ObservationNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** ObservationSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-03
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query
- **Contract source:** [`Specification/BrAPI-Phenotyping/Observations/Observations_ObservationDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Observations/Observations_ObservationDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 34](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L34); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/observations.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/observations.py#L329) — `update_observation`; line 329; brapi-adapter-source-declaration.

### GET `/brapi/v2/observationunits`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.observationunits`
- **BrAPI-Den operation identity:** `brapiV21GetObservationunits` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observation Units
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get a filtered set of Observation Units
**Source contract description:**
> Get a filtered set of Observation Units
**Can be used for:**
- Get a filtered set of Observation Units
- Get a filtered set of Observation Units
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** ObservationUnitListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-03
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query
- **Contract source:** [`Specification/BrAPI-Phenotyping/ObservationUnits/ObservationUnits_GET_POST_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/ObservationUnits/ObservationUnits_GET_POST_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/observationunits.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/observationunits.py#L58) — `list_observation_units`; line 58; brapi-adapter-source-declaration.

### POST `/brapi/v2/observationunits`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.post.observationunits`
- **BrAPI-Den operation identity:** `brapiV21PostObservationunits` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observation Units
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Add new Observation Units
**Source contract description:**
> Add new Observation Units
**Can be used for:**
- Add new Observation Units
- Add new Observation Units
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ObservationUnitNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** ObservationUnitListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-03
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query
- **Contract source:** [`Specification/BrAPI-Phenotyping/ObservationUnits/ObservationUnits_GET_POST_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/ObservationUnits/ObservationUnits_GET_POST_PUT.yaml)
- **BijMantra inventory row:** [line 73](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L73); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/observationunits.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/observationunits.py#L100) — `create_observation_unit`; line 100; brapi-adapter-source-declaration.

### PUT `/brapi/v2/observationunits`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.put.observationunits`
- **BrAPI-Den operation identity:** `brapiV21PutObservationunits` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observation Units
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update a set of Observation Units
**Source contract description:**
> Update a set of Observation Units 
>
> Note - In strictly typed languages, this structure can be represented as a Map or Dictionary of objects and parsed directly to JSON.
**Can be used for:**
- Update a set of Observation Units
- Update a set of Observation Units 
  
  Note - In strictly typed languages, this structure can be represented as a Map or Dictionary of objects and parsed directly to JSON.
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ObservationUnitNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** ObservationUnitListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-03
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query
- **Contract source:** [`Specification/BrAPI-Phenotyping/ObservationUnits/ObservationUnits_GET_POST_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/ObservationUnits/ObservationUnits_GET_POST_PUT.yaml)
- **BijMantra inventory row:** [line 96](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L96); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/observationunits.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/observationunits.py#L147) — `update_observation_units_bulk`; line 147; brapi-adapter-source-declaration.

### GET `/brapi/v2/observationunits/table`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.observationunits.table`
- **BrAPI-Den operation identity:** `brapiV21GetObservationunitsTable` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observation Units
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get a list of Observations in a table format
**Source contract description:**
> <p>This service is designed to retrieve a table for observation values as a matrix of Observation Units and Observation Variables.</p>
> <p>The table may be represented by JSON, CSV, or TSV. The "Accept" HTTP header is used for the client to request different return formats. 
> By default, if the "Accept" header is not included in the request, the server should return JSON as described below.</p>
> <p>The table is REQUIRED to have the following columns</p>
> <ul>
>   <li>observationUnitDbId - Each row is related to one Observation Unit</li>
>   <li>At least one column with an observationVariableDbId</li>
> </ul>
> <p>The table may have any or all of the following OPTIONAL columns. Included columns are decided by the server developer</p>
> <ul>
>   <li>observationUnitName</li>
>   <li>studyDbId</li>
>   <li>studyName</li>
>   <li>germplasmDbId</li>
>   <li>germplasmName</li>
>   <li>positionCoordinateX</li>
>   <li>positionCoordinateY</li>
>   <li>year</li>
> </ul>
> <p>The table also may have any number of Observation Unit Hierarchy Level columns. For example:</p>
> <ul>
>   <li>field</li>
>   <li>plot</li>
>   <li>sub-plot</li>
>   <li>plant</li>
>   <li>pot</li>
>   <li>block</li>
>   <li>entry</li>
>   <li>rep</li>
> </ul>
> <p>The JSON representation provides a pair of extra arrays for defining the headers of the table. 
> The first array "headerRow" will always contain "observationUnitDbId" and any or all of the OPTIONAL column header names. 
> The second array "observationVariables" contains the names and DbIds for the Observation Variables represented in the table. 
> By appending the two arrays, you can construct the complete header row of the table. </p>
> <p>For CSV and TSV representations of the table, an extra header row is needed to describe both the Observation Variable DbId and the Observation Variable Name for each data column. 
> See the example responses below</p>
**Can be used for:**
- Get a list of Observations in a table format
- <p>This service is designed to retrieve a table for observation values as a matrix of Observation Units and Observation Variables.</p>
  <p>The table may be represented by JSON, CSV, or TSV. The "Accept" HTTP header is used for the client to request different return formats. 
  By default, if the "Accept" header is not included in the request, the server should return JSON as described below.</p>
  <p>The table is REQUIRED to have the following columns</p>
  <ul>
    <li>observationUnitDbId - Each row is related to one Observation Unit</li>
    <li>At least one column with an observationVariableDbId</li>
  </ul>
  <p>The table may have any or all of the following OPTIONAL columns. Included columns are decided by the server developer</p>
  <ul>
    <li>observationUnitName</li>
    <li>studyDbId</li>
    <li>studyName</li>
    <li>germplasmDbId</li>
    <li>germplasmName</li>
    <li>positionCoordinateX</li>
    <li>positionCoordinateY</li>
    <li>year</li>
  </ul>
  <p>The table also may have any number of Observation Unit Hierarchy Level columns. For example:</p>
  <ul>
    <li>field</li>
    <li>plot</li>
    <li>sub-plot</li>
    <li>plant</li>
    <li>pot</li>
    <li>block</li>
    <li>entry</li>
    <li>rep</li>
  </ul>
  <p>The JSON representation provides a pair of extra arrays for defining the headers of the table. 
  The first array "headerRow" will always contain "observationUnitDbId" and any or all of the OPTIONAL column header names. 
  The second array "observationVariables" contains the names and DbIds for the Observation Variables represented in the table. 
  By appending the two arrays, you can construct the complete header row of the table. </p>
  <p>For CSV and TSV representations of the table, an extra header row is needed to describe both the Observation Variable DbId and the Observation Variable Name for each data column. 
  See the example responses below</p>
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** ObservationUnitTableResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-03
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query
- **Contract source:** [`Specification/BrAPI-Phenotyping/ObservationUnits/ObservationUnits_Table_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/ObservationUnits/ObservationUnits_Table_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/observationunits.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/observationunits.py#L189) — `get_observation_units_table`; line 189; brapi-adapter-source-declaration.

### GET `/brapi/v2/observationunits/{observationUnitDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid`
- **BrAPI-Den operation identity:** `brapiV21GetObservationunitsByObservationUnitDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observation Units
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the details of a specific Observation Unit
**Source contract description:**
> Get the details of a specific Observation Unit
**Can be used for:**
- Get the details of a specific Observation Unit
- Get the details of a specific Observation Unit
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** ObservationUnitSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-03
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query
- **Contract source:** [`Specification/BrAPI-Phenotyping/ObservationUnits/ObservationUnits_ObservationUnitDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/ObservationUnits/ObservationUnits_ObservationUnitDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/observationunits.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/observationunits.py#L125) — `get_observation_unit`; line 125; brapi-adapter-source-declaration.

### PUT `/brapi/v2/observationunits/{observationUnitDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid`
- **BrAPI-Den operation identity:** `brapiV21PutObservationunitsByObservationUnitDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observation Units
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update an existing Observation Units
**Source contract description:**
> Update an existing Observation Units
**Can be used for:**
- Update an existing Observation Units
- Update an existing Observation Units
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ObservationUnitNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** ObservationUnitSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-03
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query
- **Contract source:** [`Specification/BrAPI-Phenotyping/ObservationUnits/ObservationUnits_ObservationUnitDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/ObservationUnits/ObservationUnits_ObservationUnitDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 31](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L31); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/observationunits.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/observationunits.py#L166) — `update_observation_unit`; line 166; brapi-adapter-source-declaration.

### GET `/brapi/v2/ontologies`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.ontologies`
- **BrAPI-Den operation identity:** `brapiV21GetOntologies` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Ontologies
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C4 — Scientific terminology governance; Crosswalk basis: inferred-from-route; Crosswalk note: Scientific term definitions are shared semantics, not measured observations.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get a filtered list of Ontologies
**Source contract description:**
> Retrieve a list of ontologies available in the system. 
> Each Ontology record describes the metadata of an existing ontology, it does not include all the terms that are part of that ontology.
**Can be used for:**
- Get a filtered list of Ontologies
- Retrieve a list of ontologies available in the system. 
  Each Ontology record describes the metadata of an existing ontology, it does not include all the terms that are part of that ontology.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** OntologyListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-06
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.variable-terms.get-version, brapi-den.genx.v3.variable-terms.list, brapi-den.genx.v3.variable-terms.publish-version
- **Contract source:** [`Specification/BrAPI-Phenotyping/Ontologies/Ontologies_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Ontologies/Ontologies_GET_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/ontologies.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/ontologies.py#L86) — `get_ontologies`; line 86; brapi-adapter-source-declaration.

### POST `/brapi/v2/ontologies`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.post.ontologies`
- **BrAPI-Den operation identity:** `brapiV21PostOntologies` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Ontologies
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C4 — Scientific terminology governance; Crosswalk basis: inferred-from-route; Crosswalk note: Scientific term definitions are shared semantics, not measured observations.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Create a new Ontology record in the database
**Source contract description:**
> Use this endpoint to create a new Ontology record in the database
> Each Ontology record describes the metadata of an existing ontology, it does not include all the terms that are part of that ontology.
**Can be used for:**
- Create a new Ontology record in the database
- Use this endpoint to create a new Ontology record in the database
  Each Ontology record describes the metadata of an existing ontology, it does not include all the terms that are part of that ontology.
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** OntologyNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** OntologyListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-06
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.variable-terms.get-version, brapi-den.genx.v3.variable-terms.list, brapi-den.genx.v3.variable-terms.publish-version
- **Contract source:** [`Specification/BrAPI-Phenotyping/Ontologies/Ontologies_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Ontologies/Ontologies_GET_POST.yaml)
- **BijMantra inventory row:** [line 34](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L34); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/ontologies.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/ontologies.py#L173) — `create_ontologies`; line 173; brapi-adapter-source-declaration.

### GET `/brapi/v2/ontologies/{ontologyDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid`
- **BrAPI-Den operation identity:** `brapiV21GetOntologiesByOntologyDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Ontologies
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C4 — Scientific terminology governance; Crosswalk basis: inferred-from-route; Crosswalk note: Scientific term definitions are shared semantics, not measured observations.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get a specific Ontology record by its ontologyDbId
**Source contract description:**
> Use this endpoint to retrieve a specific Ontology record by its ontologyDbId. 
> Each Ontology record describes the metadata of an existing ontology, it does not include all the terms that are part of that ontology.
**Can be used for:**
- Get a specific Ontology record by its ontologyDbId
- Use this endpoint to retrieve a specific Ontology record by its ontologyDbId. 
  Each Ontology record describes the metadata of an existing ontology, it does not include all the terms that are part of that ontology.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** OntologySingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-06
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.variable-terms.get-version, brapi-den.genx.v3.variable-terms.list, brapi-den.genx.v3.variable-terms.publish-version
- **Contract source:** [`Specification/BrAPI-Phenotyping/Ontologies/Ontologies_OntologyDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Ontologies/Ontologies_OntologyDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/ontologies.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/ontologies.py#L135) — `get_ontology`; line 135; brapi-adapter-source-declaration.

### PUT `/brapi/v2/ontologies/{ontologyDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid`
- **BrAPI-Den operation identity:** `brapiV21PutOntologiesByOntologyDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Ontologies
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C4 — Scientific terminology governance; Crosswalk basis: inferred-from-route; Crosswalk note: Scientific term definitions are shared semantics, not measured observations.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update a specific Ontology record
**Source contract description:**
> Use this endpoint to update a specific Ontology record. 
> Each Ontology record describes the metadata of an existing ontology, it does not include all the terms that are part of that ontology.
**Can be used for:**
- Update a specific Ontology record
- Use this endpoint to update a specific Ontology record. 
  Each Ontology record describes the metadata of an existing ontology, it does not include all the terms that are part of that ontology.
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** OntologyNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** OntologySingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-06
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.variable-terms.get-version, brapi-den.genx.v3.variable-terms.list, brapi-den.genx.v3.variable-terms.publish-version
- **Contract source:** [`Specification/BrAPI-Phenotyping/Ontologies/Ontologies_OntologyDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Ontologies/Ontologies_OntologyDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 36](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L36); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/ontologies.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/ontologies.py#L218) — `update_ontology`; line 218; brapi-adapter-source-declaration.

### GET `/brapi/v2/scales`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.scales`
- **BrAPI-Den operation identity:** `brapiV21GetScales` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Scales
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C4 — Scientific terminology governance; Crosswalk basis: inferred-from-route; Crosswalk note: Scientific term definitions are shared semantics, not measured observations.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the Scales
**Source contract description:**
> Returns a list of Scales available on a server.
>
> An Observation Variable has 3 critical parts; A Trait being observed, a Method for making the observation, and a Scale on which the observation can be measured and compared with other observations.
**Can be used for:**
- Get the Scales
- Returns a list of Scales available on a server.
  
  An Observation Variable has 3 critical parts; A Trait being observed, a Method for making the observation, and a Scale on which the observation can be measured and compared with other observations.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** ScaleListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-06
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.variable-terms.get-version, brapi-den.genx.v3.variable-terms.list, brapi-den.genx.v3.variable-terms.publish-version
- **Contract source:** [`Specification/BrAPI-Phenotyping/Scales/Scales_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Scales/Scales_GET_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/scales.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/scales.py#L224) — `get_scales`; line 224; brapi-adapter-source-declaration.

### POST `/brapi/v2/scales`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.post.scales`
- **BrAPI-Den operation identity:** `brapiV21PostScales` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Scales
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C4 — Scientific terminology governance; Crosswalk basis: inferred-from-route; Crosswalk note: Scientific term definitions are shared semantics, not measured observations.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Add new Scales
**Source contract description:**
> Create new scale objects in the database
**Can be used for:**
- Add new Scales
- Create new scale objects in the database
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ScaleNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** ScaleListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-06
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.variable-terms.get-version, brapi-den.genx.v3.variable-terms.list, brapi-den.genx.v3.variable-terms.publish-version
- **Contract source:** [`Specification/BrAPI-Phenotyping/Scales/Scales_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Scales/Scales_GET_POST.yaml)
- **BijMantra inventory row:** [line 46](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L46); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/scales.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/scales.py#L301) — `create_scales`; line 301; brapi-adapter-source-declaration.

### GET `/brapi/v2/scales/{scaleDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid`
- **BrAPI-Den operation identity:** `brapiV21GetScalesByScaleDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Scales
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C4 — Scientific terminology governance; Crosswalk basis: inferred-from-route; Crosswalk note: Scientific term definitions are shared semantics, not measured observations.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the details of a specific Scale
**Source contract description:**
> Retrieve details about a specific scale
**Can be used for:**
- Get the details of a specific Scale
- Retrieve details about a specific scale
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** ScaleSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-06
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.variable-terms.get-version, brapi-den.genx.v3.variable-terms.list, brapi-den.genx.v3.variable-terms.publish-version
- **Contract source:** [`Specification/BrAPI-Phenotyping/Scales/Scales_ScaleDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Scales/Scales_ScaleDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/scales.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/scales.py#L270) — `get_scale`; line 270; brapi-adapter-source-declaration.

### PUT `/brapi/v2/scales/{scaleDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid`
- **BrAPI-Den operation identity:** `brapiV21PutScalesByScaleDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Scales
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C4 — Scientific terminology governance; Crosswalk basis: inferred-from-route; Crosswalk note: Scientific term definitions are shared semantics, not measured observations.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update an existing Scale
**Source contract description:**
> Update the details of an existing scale
**Can be used for:**
- Update an existing Scale
- Update the details of an existing scale
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ScaleNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** ScaleSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-06
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.variable-terms.get-version, brapi-den.genx.v3.variable-terms.list, brapi-den.genx.v3.variable-terms.publish-version
- **Contract source:** [`Specification/BrAPI-Phenotyping/Scales/Scales_ScaleDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Scales/Scales_ScaleDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 34](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L34); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/scales.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/scales.py#L327) — `update_scale`; line 327; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/images`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.post.search.images`
- **BrAPI-Den operation identity:** `brapiV21PostSearchImages` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Images
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for `XXEntitiesXX`
**Source contract description:**
> Submit a search request for `XXEntitiesXX`<br/>
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/XXEntitiesXX/{searchResultsDbId}` to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
> <br/>
> <br/>
> Image Implementation Notes<br/>
> - `imageURL` should be a complete URL describing the location of the image. There is no BrAPI call for retrieving the image content, so it could be on a different path, or a different host.<br/>
> - `descriptiveOntologyTerm` can be thought of as Tags for the image. These could be simple descriptive words, or ontology references, or full ontology URI's.<br/>
**Can be used for:**
- Submit a search request for `XXEntitiesXX`
- Submit a search request for `XXEntitiesXX`<br/>
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/XXEntitiesXX/{searchResultsDbId}` to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
  <br/>
  <br/>
  Image Implementation Notes<br/>
  - `imageURL` should be a complete URL describing the location of the image. There is no BrAPI call for retrieving the image content, so it could be on a different path, or a different host.<br/>
  - `descriptiveOntologyTerm` can be thought of as Tags for the image. These could be simple descriptive words, or ontology references, or full ontology URI's.<br/>
**Must not be used for / explicit non-goals:**
- Do not treat as create/update of searched domain resource; it submits a search request.
- Search replay/deduplication is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results record may be created; domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** SearchRequestParametersPaging, ImageSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** ImageListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Phenotyping/Images/Search_Images_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Images/Search_Images_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1376) — `search_images`; line 1376; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/images/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchImagesBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Images
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a `Images` search request
**Source contract description:**
> Get the results of a `Images` search request <br/>
> Clients should submit a search request using the corresponding `POST /search/images` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
> <br/>
> <br/>
> Image Implementation Notes<br/>
> - `imageURL` should be a complete URL describing the location of the image. There is no BrAPI call for retrieving the image content, so it could be on a different path, or a different host.<br/>
> - `descriptiveOntologyTerm` can be thought of as Tags for the image. These could be simple descriptive words, or ontology references, or full ontology URI's.<br/>
**Can be used for:**
- Get the results of a `Images` search request
- Get the results of a `Images` search request <br/>
  Clients should submit a search request using the corresponding `POST /search/images` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
  <br/>
  <br/>
  Image Implementation Notes<br/>
  - `imageURL` should be a complete URL describing the location of the image. There is no BrAPI call for retrieving the image content, so it could be on a different path, or a different host.<br/>
  - `descriptiveOntologyTerm` can be thought of as Tags for the image. These could be simple descriptive words, or ontology references, or full ontology URI's.<br/>
**Must not be used for / explicit non-goals:**
- Do not use to submit a new search; retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, ImageListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit
- **Contract source:** [`Specification/BrAPI-Phenotyping/Images/Search_Images_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Images/Search_Images_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1435) — `get_search_images_results`; line 1435; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/observations`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.post.search.observations`
- **BrAPI-Den operation identity:** `brapiV21PostSearchObservations` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observations
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for `Observations`
**Source contract description:**
> Submit a search request for `Observations`<br/>
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/observations/{searchResultsDbId}` to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for `Observations`
- Submit a search request for `Observations`<br/>
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/observations/{searchResultsDbId}` to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat as create/update of searched domain resource; it submits a search request.
- Search replay/deduplication is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results record may be created; domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** SearchRequestParametersPaging, ObservationSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** ObservationListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02, SEM-03
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query
- **Contract source:** [`Specification/BrAPI-Phenotyping/Observations/Search_Observations_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Observations/Search_Observations_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1139) — `search_observations`; line 1139; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/observations/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchObservationsBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observations
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a `Observations` search request
**Source contract description:**
> Get the results of a `Observations` search request <br/>
> Clients should submit a search request using the corresponding `POST /search/observations` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Get the results of a `Observations` search request
- Get the results of a `Observations` search request <br/>
  Clients should submit a search request using the corresponding `POST /search/observations` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not use to submit a new search; retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, ObservationListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02, SEM-03
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query
- **Contract source:** [`Specification/BrAPI-Phenotyping/Observations/Search_Observations_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Observations/Search_Observations_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1184) — `get_search_observations_results`; line 1184; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/observationunits`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.post.search.observationunits`
- **BrAPI-Den operation identity:** `brapiV21PostSearchObservationunits` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observation Units
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for `ObservationUnits`
**Source contract description:**
> Submit a search request for `ObservationUnits`<br/>
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/observationunits/{searchResultsDbId}` to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for `ObservationUnits`
- Submit a search request for `ObservationUnits`<br/>
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/observationunits/{searchResultsDbId}` to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat as create/update of searched domain resource; it submits a search request.
- Search replay/deduplication is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results record may be created; domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ObservationUnitSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** ObservationUnitListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02, SEM-03
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query
- **Contract source:** [`Specification/BrAPI-Phenotyping/ObservationUnits/Search_ObservationUnits_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/ObservationUnits/Search_ObservationUnits_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1205) — `search_observationunits`; line 1205; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/observationunits/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchObservationunitsBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observation Units
- **Proposed BrAPI-Den classification:** D4 — Phenotyping and Plant Observations; Crosswalk basis: inferred-from-official-module; Crosswalk note: Official Phenotyping module; resource-specific exceptions may require review.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a `ObservationUnits` search request
**Source contract description:**
> Get the results of a `ObservationUnits` search request <br/>
> Clients should submit a search request using the corresponding `POST /search/observationunits` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Get the results of a `ObservationUnits` search request
- Get the results of a `ObservationUnits` search request <br/>
  Clients should submit a search request using the corresponding `POST /search/observationunits` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not use to submit a new search; retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, ObservationUnitListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02, SEM-03
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query
- **Contract source:** [`Specification/BrAPI-Phenotyping/ObservationUnits/Search_ObservationUnits_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/ObservationUnits/Search_ObservationUnits_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1259) — `get_search_observationunits_results`; line 1259; brapi-adapter-source-declaration.

### POST `/brapi/v2/search/variables`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.post.search.variables`
- **BrAPI-Den operation identity:** `brapiV21PostSearchVariables` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observation Variables
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C4 — Scientific terminology governance; Crosswalk basis: inferred-from-route; Crosswalk note: Scientific term definitions are shared semantics, not measured observations.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Submit a search request for Observation `Variables`
**Source contract description:**
> Submit a search request for Observation `Variables`<br/>
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use the corresponding `GET /search/variables/{searchResultsDbId}` to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Submit a search request for Observation `Variables`
- Submit a search request for Observation `Variables`<br/>
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use the corresponding `GET /search/variables/{searchResultsDbId}` to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not treat as create/update of searched domain resource; it submits a search request.
- Search replay/deduplication is not asserted unless separately documented.
- **Side effects:** Submits a search query; a search-results record may be created; domain-resource creation is not implied.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ObservationVariableSearchRequest
- **Response status codes recorded:** 200, 202, 400, 401, 403
- **Response component refs recorded:** ObservationVariableListResponse, 202AcceptedSearchResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-02, SEM-03
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query
- **Contract source:** [`Specification/BrAPI-Phenotyping/ObservationVariables/Search_Variables_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/ObservationVariables/Search_Variables_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1280) — `search_variables`; line 1280; brapi-adapter-source-declaration.

### GET `/brapi/v2/search/variables/{searchResultsDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid`
- **BrAPI-Den operation identity:** `brapiV21GetSearchVariablesBySearchResultsDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observation Variables
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C4 — Scientific terminology governance; Crosswalk basis: inferred-from-route; Crosswalk note: Scientific term definitions are shared semantics, not measured observations.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the results of a Observation `variables` search request
**Source contract description:**
> Get the results of a Observation `variables` search request <br/>
> Clients should submit a search request using the corresponding `POST /search/variables` endpoint.
> Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
> If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
> Use this endpoint to retrieve the results of the search. <br/> 
> Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Can be used for:**
- Get the results of a Observation `variables` search request
- Get the results of a Observation `variables` search request <br/>
  Clients should submit a search request using the corresponding `POST /search/variables` endpoint.
  Search requests allow a client to send a complex query for data. However, the server may not respond with the search results immediately. 
  If a server needs more time to process the request, it might respond with a `searchResultsDbId`. 
  Use this endpoint to retrieve the results of the search. <br/> 
  Review the <a target="_blank" href="https://wiki.brapi.org/index.php/Search_Services#POST_Search_Entity">Search Services documentation</a> for additional implementation details.
**Must not be used for / explicit non-goals:**
- Do not use to submit a new search; retrieves results for an existing search-results identifier.
- **Side effects:** Reads previously submitted search results.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 202, 200, 400, 401, 403, 404
- **Response component refs recorded:** 202AcceptedSearchResponse, ObservationVariableListResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-02, SEM-03
- **Related catalogue IDs:** brapi-den.brapi-v2-1.core.get.search.lists.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.locations.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.people.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.programs.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.studies.by-searchresultsdbid, brapi-den.brapi-v2-1.core.get.search.trials.by-searchresultsdbid, brapi-den.brapi-v2-1.core.post.search.lists, brapi-den.brapi-v2-1.core.post.search.locations, brapi-den.brapi-v2-1.core.post.search.people, brapi-den.brapi-v2-1.core.post.search.programs, brapi-den.brapi-v2-1.core.post.search.studies, brapi-den.brapi-v2-1.core.post.search.trials, brapi-den.brapi-v2-1.genotyping.get.search.allelematrix.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.calls.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.callsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.markerpositions.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.plates.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.references.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.referencesets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.samples.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variants.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.get.search.variantsets.by-searchresultsdbid, brapi-den.brapi-v2-1.genotyping.post.search.allelematrix, brapi-den.brapi-v2-1.genotyping.post.search.calls, brapi-den.brapi-v2-1.genotyping.post.search.callsets, brapi-den.brapi-v2-1.genotyping.post.search.markerpositions, brapi-den.brapi-v2-1.genotyping.post.search.plates, brapi-den.brapi-v2-1.genotyping.post.search.references, brapi-den.brapi-v2-1.genotyping.post.search.referencesets, brapi-den.brapi-v2-1.genotyping.post.search.samples, brapi-den.brapi-v2-1.genotyping.post.search.variants, brapi-den.brapi-v2-1.genotyping.post.search.variantsets, brapi-den.brapi-v2-1.germplasm.get.search.attributes.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.attributevalues.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.germplasm.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.get.search.pedigree.by-searchresultsdbid, brapi-den.brapi-v2-1.germplasm.post.search.attributes, brapi-den.brapi-v2-1.germplasm.post.search.attributevalues, brapi-den.brapi-v2-1.germplasm.post.search.germplasm, brapi-den.brapi-v2-1.germplasm.post.search.pedigree, brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.search.images.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.images, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.jobs.get, brapi-den.genx.v3.jobs.list, brapi-den.genx.v3.jobs.request-cancellation, brapi-den.genx.v3.jobs.submit, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query
- **Contract source:** [`Specification/BrAPI-Phenotyping/ObservationVariables/Search_Variables_SearchResultsDbId_GET.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/ObservationVariables/Search_Variables_SearchResultsDbId_GET.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/search.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/search.py#L1355) — `get_search_variables_results`; line 1355; brapi-adapter-source-declaration.

### GET `/brapi/v2/traits`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.traits`
- **BrAPI-Den operation identity:** `brapiV21GetTraits` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Traits
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C4 — Scientific terminology governance; Crosswalk basis: inferred-from-route; Crosswalk note: Scientific term definitions are shared semantics, not measured observations.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the Traits
**Source contract description:**
> Call to retrieve a list of traits available in the system and their associated variables.
>
> An Observation Variable has 3 critical parts; A Trait being observed, a Method for making the observation, and a Scale on which the observation can be measured and compared with other observations.
**Can be used for:**
- Get the Traits
- Call to retrieve a list of traits available in the system and their associated variables.
  
  An Observation Variable has 3 critical parts; A Trait being observed, a Method for making the observation, and a Scale on which the observation can be measured and compared with other observations.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** TraitListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-06
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.variable-terms.get-version, brapi-den.genx.v3.variable-terms.list, brapi-den.genx.v3.variable-terms.publish-version
- **Contract source:** [`Specification/BrAPI-Phenotyping/Traits/Traits_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Traits/Traits_GET_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/traits.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/traits.py#L85) — `list_traits`; line 85; brapi-adapter-source-declaration.

### POST `/brapi/v2/traits`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.post.traits`
- **BrAPI-Den operation identity:** `brapiV21PostTraits` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Traits
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C4 — Scientific terminology governance; Crosswalk basis: inferred-from-route; Crosswalk note: Scientific term definitions are shared semantics, not measured observations.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Add new Traits
**Source contract description:**
> Create new trait objects in the database
**Can be used for:**
- Add new Traits
- Create new trait objects in the database
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** TraitNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** TraitListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-06
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.variable-terms.get-version, brapi-den.genx.v3.variable-terms.list, brapi-den.genx.v3.variable-terms.publish-version
- **Contract source:** [`Specification/BrAPI-Phenotyping/Traits/Traits_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Traits/Traits_GET_POST.yaml)
- **BijMantra inventory row:** [line 46](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L46); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/traits.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/traits.py#L154) — `create_trait`; line 154; brapi-adapter-source-declaration.

### GET `/brapi/v2/traits/{traitDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid`
- **BrAPI-Den operation identity:** `brapiV21GetTraitsByTraitDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Traits
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C4 — Scientific terminology governance; Crosswalk basis: inferred-from-route; Crosswalk note: Scientific term definitions are shared semantics, not measured observations.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the details of a specific Trait
**Source contract description:**
> Retrieve the details of a single trait
>
> An Observation Variable has 3 critical parts: A Trait being observed, a Method for making the observation, and a Scale on which the observation can be measured and compared with other observations.
**Can be used for:**
- Get the details of a specific Trait
- Retrieve the details of a single trait
  
  An Observation Variable has 3 critical parts: A Trait being observed, a Method for making the observation, and a Scale on which the observation can be measured and compared with other observations.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** TraitSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-06
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.variable-terms.get-version, brapi-den.genx.v3.variable-terms.list, brapi-den.genx.v3.variable-terms.publish-version
- **Contract source:** [`Specification/BrAPI-Phenotyping/Traits/Traits_TraitDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Traits/Traits_TraitDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/traits.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/traits.py#L218) — `get_trait`; line 218; brapi-adapter-source-declaration.

### PUT `/brapi/v2/traits/{traitDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid`
- **BrAPI-Den operation identity:** `brapiV21PutTraitsByTraitDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Traits
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C4 — Scientific terminology governance; Crosswalk basis: inferred-from-route; Crosswalk note: Scientific term definitions are shared semantics, not measured observations.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update an existing Trait
**Source contract description:**
> Update an existing trait
**Can be used for:**
- Update an existing Trait
- Update an existing trait
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** TraitNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** TraitSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-06
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.variable-terms.get-version, brapi-den.genx.v3.variable-terms.list, brapi-den.genx.v3.variable-terms.publish-version
- **Contract source:** [`Specification/BrAPI-Phenotyping/Traits/Traits_TraitDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/Traits/Traits_TraitDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 34](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L34); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/traits.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/traits.py#L258) — `update_trait`; line 258; brapi-adapter-source-declaration.

### GET `/brapi/v2/variables`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.variables`
- **BrAPI-Den operation identity:** `brapiV21GetVariables` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observation Variables
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C4 — Scientific terminology governance; Crosswalk basis: inferred-from-route; Crosswalk note: Scientific term definitions are shared semantics, not measured observations.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the Observation Variables
**Source contract description:**
> Call to retrieve a list of observationVariables available in the system.
**Can be used for:**
- Get the Observation Variables
- Call to retrieve a list of observationVariables available in the system.
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** ObservationVariableListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-03, SEM-06
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query, brapi-den.genx.v3.variable-terms.get-version, brapi-den.genx.v3.variable-terms.list, brapi-den.genx.v3.variable-terms.publish-version
- **Contract source:** [`Specification/BrAPI-Phenotyping/ObservationVariables/Variables_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/ObservationVariables/Variables_GET_POST.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/variables.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/variables.py#L131) — `list_variables`; line 131; brapi-adapter-source-declaration.

### POST `/brapi/v2/variables`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.post.variables`
- **BrAPI-Den operation identity:** `brapiV21PostVariables` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observation Variables
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C4 — Scientific terminology governance; Crosswalk basis: inferred-from-route; Crosswalk note: Scientific term definitions are shared semantics, not measured observations.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Add new Observation Variables
**Source contract description:**
> Add new Observation Variables to the system.
**Can be used for:**
- Add new Observation Variables
- Add new Observation Variables to the system.
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get operation.
- Do not assume retries are idempotent unless explicitly guaranteed.
- **Side effects:** State-changing submission or creation as specified; schemas determine exact effect.
- **Retry / idempotency:** The source specification does not declare a universal replay guarantee; do not blindly retry after an unknown outcome.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ObservationVariableNewRequest
- **Response status codes recorded:** 200, 400, 401, 403
- **Response component refs recorded:** ObservationVariableListResponse, 400BadRequest, 401Unauthorized, 403Forbidden
- **Semantic relationship IDs / labels:** SEM-03, SEM-06
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query, brapi-den.genx.v3.variable-terms.get-version, brapi-den.genx.v3.variable-terms.list, brapi-den.genx.v3.variable-terms.publish-version
- **Contract source:** [`Specification/BrAPI-Phenotyping/ObservationVariables/Variables_GET_POST.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/ObservationVariables/Variables_GET_POST.yaml)
- **BijMantra inventory row:** [line 66](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L66); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/variables.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/variables.py#L216) — `create_variable`; line 216; brapi-adapter-source-declaration.

### GET `/brapi/v2/variables/{observationVariableDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid`
- **BrAPI-Den operation identity:** `brapiV21GetVariablesByObservationVariableDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observation Variables
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C4 — Scientific terminology governance; Crosswalk basis: inferred-from-route; Crosswalk note: Scientific term definitions are shared semantics, not measured observations.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Get the details for a specific Observation Variable
**Source contract description:**
> Retrieve variable details
**Can be used for:**
- Get the details for a specific Observation Variable
- Retrieve variable details
**Must not be used for / explicit non-goals:**
- Do not use to create, update, or delete domain data.
- Specification presence does not prove runtime availability.
- **Side effects:** Read-only retrieval under the released specification.
- **Retry / idempotency:** Read-only retrieval is safe to repeat without changing domain state.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** —
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** ObservationVariableSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-03, SEM-06
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query, brapi-den.genx.v3.variable-terms.get-version, brapi-den.genx.v3.variable-terms.list, brapi-den.genx.v3.variable-terms.publish-version
- **Contract source:** [`Specification/BrAPI-Phenotyping/ObservationVariables/Variables_ObservationVariableDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/ObservationVariables/Variables_ObservationVariableDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 7](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L7); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/variables.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/variables.py#L290) — `get_variable`; line 290; brapi-adapter-source-declaration.

### PUT `/brapi/v2/variables/{observationVariableDbId}`

- **Catalogue ID:** `brapi-den.brapi-v2-1.phenotyping.put.variables.by-observationvariabledbid`
- **BrAPI-Den operation identity:** `brapiV21PutVariablesByObservationVariableDbId` (advisory where absent from source)
- **Source OpenAPI operationId:** not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract.
- **Official BrAPI module:** BrAPI-Phenotyping
- **Source tag:** Observation Variables
- **Proposed BrAPI-Den classification:** No primary domain assigned; cross-cutting or review required; Facets: C4 — Scientific terminology governance; Crosswalk basis: inferred-from-route; Crosswalk note: Scientific term definitions are shared semantics, not measured observations.
- **Standard / proposal status:** `released-specification`
- **Implementation status:** `not-verified`
**Purpose:**
> Update an existing Observation Variable
**Source contract description:**
> Update an existing Observation Variable
**Can be used for:**
- Update an existing Observation Variable
- Update an existing Observation Variable
**Must not be used for / explicit non-goals:**
- Do not use as a read-only list/get or generic deletion operation.
- Do not infer merge or concurrency semantics unless specified.
- **Side effects:** Updates or replaces addressed resource(s) as specified.
- **Retry / idempotency:** HTTP PUT has idempotent method semantics; exact business effects remain defined by the operation contract.
- **Parameters recorded in registry:** —
- **Request schema refs recorded:** ObservationVariableNewRequest
- **Response status codes recorded:** 200, 400, 401, 403, 404
- **Response component refs recorded:** ObservationVariableSingleResponse, 400BadRequest, 401Unauthorized, 403Forbidden, 404NotFound
- **Semantic relationship IDs / labels:** SEM-03, SEM-06
- **Related catalogue IDs:** brapi-den.brapi-v2-1.phenotyping.get.methods, brapi-den.brapi-v2-1.phenotyping.get.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.get.observations, brapi-den.brapi-v2-1.phenotyping.get.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.get.observations.table, brapi-den.brapi-v2-1.phenotyping.get.observationunits, brapi-den.brapi-v2-1.phenotyping.get.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.get.observationunits.table, brapi-den.brapi-v2-1.phenotyping.get.ontologies, brapi-den.brapi-v2-1.phenotyping.get.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.get.scales, brapi-den.brapi-v2-1.phenotyping.get.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.get.search.observations.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.observationunits.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.search.variables.by-searchresultsdbid, brapi-den.brapi-v2-1.phenotyping.get.traits, brapi-den.brapi-v2-1.phenotyping.get.traits.by-traitdbid, brapi-den.brapi-v2-1.phenotyping.get.variables, brapi-den.brapi-v2-1.phenotyping.get.variables.by-observationvariabledbid, brapi-den.brapi-v2-1.phenotyping.post.delete.observations, brapi-den.brapi-v2-1.phenotyping.post.methods, brapi-den.brapi-v2-1.phenotyping.post.observations, brapi-den.brapi-v2-1.phenotyping.post.observationunits, brapi-den.brapi-v2-1.phenotyping.post.ontologies, brapi-den.brapi-v2-1.phenotyping.post.scales, brapi-den.brapi-v2-1.phenotyping.post.search.observations, brapi-den.brapi-v2-1.phenotyping.post.search.observationunits, brapi-den.brapi-v2-1.phenotyping.post.search.variables, brapi-den.brapi-v2-1.phenotyping.post.traits, brapi-den.brapi-v2-1.phenotyping.post.variables, brapi-den.brapi-v2-1.phenotyping.put.methods.by-methoddbid, brapi-den.brapi-v2-1.phenotyping.put.observations, brapi-den.brapi-v2-1.phenotyping.put.observations.by-observationdbid, brapi-den.brapi-v2-1.phenotyping.put.observationunits, brapi-den.brapi-v2-1.phenotyping.put.observationunits.by-observationunitdbid, brapi-den.brapi-v2-1.phenotyping.put.ontologies.by-ontologydbid, brapi-den.brapi-v2-1.phenotyping.put.scales.by-scaledbid, brapi-den.brapi-v2-1.phenotyping.put.traits.by-traitdbid, brapi-den.genx.v3.telemetry.append-batch, brapi-den.genx.v3.telemetry.query, brapi-den.genx.v3.variable-terms.get-version, brapi-den.genx.v3.variable-terms.list, brapi-den.genx.v3.variable-terms.publish-version
- **Contract source:** [`Specification/BrAPI-Phenotyping/ObservationVariables/Variables_ObservationVariableDbId_GET_PUT.yaml`](https://github.com/denishdholaria/BrAPI-Den/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/ObservationVariables/Variables_ObservationVariableDbId_GET_PUT.yaml)
- **BijMantra inventory row:** [line 31](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L31); static evidence only.
- **BijMantra static route crosswalk:** 1 exact normalized method/path candidate(s); 1 BrAPI-specific source declaration(s). Runtime and conformance are unverified.
  - [backend/app/api/brapi/v2/variables.py](https://github.com/denishdholaria/bijmantraorg/blob/main/backend/app/api/brapi/v2/variables.py#L330) — `update_variable`; line 330; brapi-adapter-source-declaration.

## BrAPI GenX — proposed /brapi/v3 operations

Every operation below is proposal-only. Reference-test-server evidence is not community acceptance or production deployment.

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


## Registry quality summary

- Unique catalogue identifiers: `true`.
- Unique full-base-path/method/route keys: `true`.
- Unique source/advisory operation identifiers where present: `true`.
- BrAPI v2.1 inventory rows resolved to source YAML operations: 201 / 201.
- GenX operations documented: 21.

See [BIJMANTRA-CROSSWALK.md](./BIJMANTRA-CROSSWALK.md) for inventory evidence and semantic boundaries.
