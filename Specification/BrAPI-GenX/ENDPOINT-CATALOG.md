# BrAPI-GenX Endpoint Catalogue

- Status: proposal; non-normative; not accepted by the BrAPI community.
- Scope: all 21 HTTP operations currently defined under the BrAPI-GenX proposal's `/brapi/v3` base path.
- Compatibility: no BrAPI V2.1 operation is replaced or changed by this catalogue.

## How to use this catalogue

This is the human-facing semantic index. The matching endpoint YAML operation remains authoritative for its exact route template, parameter schema, request/response schema, status codes, and OpenAPI `operationId`. Each GenX operation now carries an `x-brapi-den` block in that same operation definition; this block records catalog identity, domain/cross-cutting classification, purpose, supported uses, non-goals, side effects, idempotency, and semantic neighbors. Keep both views aligned in one change.

The complete identity of an operation is **API generation/base path + HTTP method + full route template + stable `operationId` + request/response contract + action and side-effect semantics + identity/version and idempotency rules + authorization boundary + semantic-neighbor relationship**. Never identify an operation by a short path fragment such as “the model endpoint.”

### Uniqueness rule

- Every GenX operation has a stable `catalogId` under the `x-brapi-den` extension and a stable `operationId` beginning with `genx`.
- `operationId` and `catalogId` must be unique across the complete BrAPI-Den API surface, not merely inside one source YAML file. A major-version path does not make a semantic collision safe.
- Resource paths identify resources; HTTP methods describe standard actions. Use action-like subresources only where they model a real domain command or workflow.
- A classification is not proof of equivalence, implementation availability, or safe dual-write behavior.
- The 21 operations below are the current GenX proposal surface. Existing V2.1 operations stay defined by their original BrAPI specifications and are referenced only where necessary to prevent confusion.

## Classification key

| Code | Meaning |
|---|---|
| D3 | Genotyping and Molecular Genomics |
| D6 | Crop Production and Material Operations |
| D7 | Scientific Analysis, Models and Derived Evidence |
| C1 | Identity, versioning and capability discovery |
| C2 | Provenance, evidence and uncertainty |
| C3 | Asynchronous execution and idempotency |
| C4 | Scientific terminology governance |
| C5 | Data exchange, publication and access |
| C6 | Artifact integrity and external references |
| C7 | Streaming and temporal aggregation |
| C8 | Contract conformance and governance |
| C9 | Security, authority and tenancy |

A `null` primary domain means the operation is a cross-cutting capability rather than a scientific domain resource. Telemetry is context-dependent: classify environmental measurements as D5 and plant/phenotyping measurements as D4, even though the transport endpoint is shared.

## 1. Capability discovery and asynchronous execution

### 1.1 Get GenX capability document
- **Identity:** `GET /brapi/v3/serverinfo`
- **operationId:** `genxGetServerInfoV3`
- **Catalogue ID:** `brapi-den.genx.v3.serverinfo.read`
- **Classification:** Cross-cutting C1, C8, C9.
- **Purpose:** Advertise supported API generations, capabilities, and authentication profiles so clients negotiate before using optional features.
- **Use it for:** Discover whether GenX is advertised and which capabilities or job types a server claims to support; select a documented V2.1 fallback when GenX is absent.
- **Do not use it for:** Proving every advertised operation is healthy at that instant; probing unadvertised endpoints; treating V2.1 `ServerInfo` and GenX `ServerInfoV3` as interchangeable.
- **Side effects / retry:** Read-only.
- **Neighbor:** V2.1 `GET /brapi/v2/serverinfo` has the same broad discovery purpose but a different response contract.

### 1.2 List caller-visible jobs
- **Identity:** `GET /brapi/v3/jobs`
- **operationId:** `genxListJobs`
- **Catalogue ID:** `brapi-den.genx.v3.jobs.list`
- **Classification:** Cross-cutting C1, C3, C9.
- **Purpose:** Return a paginated list of asynchronous jobs visible to the caller, with optional job-type and lifecycle-state filters.
- **Use it for:** Presenting jobs submitted by the caller and filtering them by supported job type or status.
- **Do not use it for:** Listing scientific resources such as models, observations, or seed lots; assuming V2.1 search results are jobs; assuming an unadvertised job type exists.
- **Side effects / retry:** Read-only.

### 1.3 Submit asynchronous work
- **Identity:** `POST /brapi/v3/jobs`
- **operationId:** `genxSubmitAsyncJob`
- **Catalogue ID:** `brapi-den.genx.v3.jobs.submit`
- **Classification:** Cross-cutting C2, C3, C9.
- **Purpose:** Submit one advertised unit of asynchronous work and receive a Job resource for polling and eligible cancellation.
- **Use it for:** Long-running analysis, model inference, and other expressly advertised job types; safe retries using the same idempotency key and identical request body.
- **Do not use it for:** Expecting synchronous completion in the submit response; submitting undefined or unadvertised job types; reusing one idempotency key for different request bodies; silently replacing all V2.1 search endpoints.
- **Side effects / retry:** May create a job and dispatch work. Same key plus identical body replays the existing job; same key plus a different body is a conflict, not an overwrite.
- **Neighbors:** Job reads/cancellation and the V2.1 search lifecycle. Jobs are a general work lifecycle, not a retroactive replacement for V2.1 search contracts.

### 1.4 Get one job
- **Identity:** `GET /brapi/v3/jobs/{jobDbId}`
- **operationId:** `genxGetAsyncJobById`
- **Catalogue ID:** `brapi-den.genx.v3.jobs.get`
- **Classification:** Cross-cutting C2, C3, C9.
- **Purpose:** Read one job's current state and any result still available under its expiry policy.
- **Use it for:** Polling a submitted job to a terminal state and retrieving a result before expiry.
- **Do not use it for:** Assuming completed results are retained indefinitely; treating EXPIRED as synonymous with FAILED; retrieving model artifacts or domain records directly.
- **Side effects / retry:** Read-only.

### 1.5 Request job cancellation
- **Identity:** `DELETE /brapi/v3/jobs/{jobDbId}`
- **operationId:** `genxRequestAsyncJobCancellation`
- **Catalogue ID:** `brapi-den.genx.v3.jobs.request-cancellation`
- **Classification:** Cross-cutting C3, C9.
- **Purpose:** Request cancellation of non-terminal asynchronous work while retaining the job record and history.
- **Use it for:** Asking a server to stop queued or running work, subject to state and implementation capability.
- **Do not use it for:** Deleting a job record; erasing its history; assuming the work stops immediately; changing terminal states such as COMPLETED, FAILED, CANCELLED, or EXPIRED.
- **Side effects / retry:** May request a lifecycle transition. Re-read the job to determine the resulting state.

## 2. Scientific terminology governance

### 2.1 List variable-term versions
- **Identity:** `GET /brapi/v3/variable-terms`
- **operationId:** `genxListVariableTermVersions`
- **Catalogue ID:** `brapi-den.genx.v3.variable-terms.list`
- **Classification:** Cross-cutting C1, C2, C4.
- **Purpose:** List paginated, namespaced observation-variable term versions, optionally filtered by term identity, ontology, or status.
- **Use it for:** Discovering published term definitions and versions.
- **Do not use it for:** Storing or returning measured values; assuming it defines the complete Trait, Method, Scale, or ontology-merging lifecycle; inferring semantic equivalence from similar labels.
- **Side effects / retry:** Read-only.
- **Neighbors:** V2.1 `/brapi/v2/variables` and the V2.1 `OntologyTerm` schema are related but not interchangeable contracts.

### 2.2 Publish a variable-term version
- **Identity:** `POST /brapi/v3/variable-terms`
- **operationId:** `genxPublishVariableTermVersion`
- **Catalogue ID:** `brapi-den.genx.v3.variable-terms.publish-version`
- **Classification:** Cross-cutting C1, C2, C4.
- **Purpose:** Publish a namespaced term as an immutable version, creating the identity when new or appending a version when known.
- **Use it for:** Publishing an explicit version with provenance; safe retries of an identical publication; rejecting conflicting definitions for the same identity/version.
- **Do not use it for:** Silently editing a published version; deleting a term referenced by historical observations; merging cross-authority terms without a separately defined mapping contract.
- **Side effects / retry:** Creates a term or version. Same identity/version plus identical body replays; a different body conflicts.

### 2.3 Get a variable-term version
- **Identity:** `GET /brapi/v3/variable-terms/{variableDbId}`
- **operationId:** `genxGetVariableTermVersion`
- **Catalogue ID:** `brapi-den.genx.v3.variable-terms.get-version`
- **Classification:** Cross-cutting C1, C2, C4.
- **Purpose:** Retrieve the requested term version, or the most recently created version when `version` is omitted.
- **Use it for:** Resolving an exact version referenced by reproducible work or reading the latest-created version.
- **Do not use it for:** Assuming an omitted version returns the highest semantic-version number; treating VariableTerm as V2.1 OntologyTerm; inferring cross-authority equivalence from a matching name.
- **Side effects / retry:** Read-only.
- **Open issue:** Version ordering remains a deferred decision in RFC-002 (D-05).

## 3. Material operations and traceability

### 3.1 List a seed lot's ledger
- **Identity:** `GET /brapi/v3/seedlots/{seedLotDbId}/ledger`
- **operationId:** `genxListSeedLotLedgerEntries`
- **Catalogue ID:** `brapi-den.genx.v3.seed-lot-ledger.list`
- **Classification:** D6; cross-cutting C1, C2, C6, C9.
- **Purpose:** Read one seed lot's append-only movement ledger in position order, optionally filtered by movement type.
- **Use it for:** Inspecting and auditing a single lot's history when entry and quantity semantics are understood.
- **Do not use it for:** Assuming a global order across lots or servers; treating the stream as an atomic multi-lot transfer; combining its movements with V2.1 SeedLotTransaction records as independent events.
- **Side effects / retry:** Read-only.
- **Critical neighbor:** SEM-01 / deferred decision D-20. The GenX ledger is not a declared wire-compatible replacement for V2.1 SeedLotTransaction.

### 3.2 Append a seed-lot ledger entry
- **Identity:** `POST /brapi/v3/seedlots/{seedLotDbId}/ledger`
- **operationId:** `genxAppendSeedLotLedgerEntry`
- **Catalogue ID:** `brapi-den.genx.v3.seed-lot-ledger.append`
- **Classification:** D6; cross-cutting C1, C2, C3, C6, C9.
- **Purpose:** Append one immutable movement entry to one seed lot's ledger with replay and conflict protection.
- **Use it for:** Recording one-lot adjustments, movements, handoffs, production, planting, or trade; retrying an identical entry safely.
- **Do not use it for:** Updating or deleting an existing entry; assuming multi-lot atomicity; automatically mirroring the same movement to V2.1 SeedLotTransaction; double-counting both streams.
- **Side effects / retry:** Appends one entry when accepted. Identical replay returns the existing entry; a conflicting body is rejected.
- **Open issues:** D-07 covers multi-lot atomicity; D-20 covers the relationship to V2.1 SeedLotTransaction.

## 4. Scientific analysis and model artifacts

### 4.1 List registered model versions
- **Identity:** `GET /brapi/v3/models`
- **operationId:** `genxListModelVersions`
- **Catalogue ID:** `brapi-den.genx.v3.models.list`
- **Classification:** D7; cross-cutting C1, C2, C6, C9.
- **Purpose:** List registered model artifact versions and lifecycle state.
- **Use it for:** Discovering model identities and versions, then selecting a candidate version subject to status and advertised inference support.
- **Do not use it for:** Training or running a model; assuming registration proves scientific validation or approval; comparing model metrics without defined semantics.
- **Side effects / retry:** Read-only.

### 4.2 Register a model version
- **Identity:** `POST /brapi/v3/models`
- **operationId:** `genxRegisterModelVersion`
- **Catalogue ID:** `brapi-den.genx.v3.models.register-version`
- **Classification:** D7; cross-cutting C1, C2, C3, C6, C9.
- **Purpose:** Register a model version with namespaced identity, immutable artifact digest, training provenance, framework, metrics, and lifecycle state.
- **Use it for:** Publishing model metadata and integrity references and registering new immutable versions.
- **Do not use it for:** Training or inference; assuming it uploads model bytes; treating a `revoked` flag as a full approval/governance workflow.
- **Side effects / retry:** Creates an identity/version. Identical registration replays; conflicting content for the same version is rejected.
- **Open issues:** Model approval/governance and artifact transport remain deferred in RFC-004 (D-09 and D-10).

### 4.3 Get one model version
- **Identity:** `GET /brapi/v3/models/{modelDbId}`
- **operationId:** `genxGetModelVersion`
- **Catalogue ID:** `brapi-den.genx.v3.models.get-version`
- **Classification:** D7; cross-cutting C1, C2, C6, C9.
- **Purpose:** Retrieve metadata for one registered model identity/version.
- **Use it for:** Inspecting digest, provenance, version, and lifecycle status before selecting an inference model.
- **Do not use it for:** Executing inference or training; assuming it serves model bytes; assuming lifecycle status alone proves suitability for a scientific use.
- **Side effects / retry:** Read-only.
- **Neighbor:** Inference is submitted through the Jobs interface as an explicitly supported job type, not through a synchronous model endpoint.

## 5. Genomic matrix references

### 5.1 List variant-matrix references
- **Identity:** `GET /brapi/v3/variantmatrices`
- **operationId:** `genxListVariantMatrixReferences`
- **Catalogue ID:** `brapi-den.genx.v3.variant-matrices.list`
- **Classification:** D3; cross-cutting C1, C2, C5, C6, C9.
- **Purpose:** List external variant-matrix references, optionally filtered by VariantSet identity and format.
- **Use it for:** Discovering matrix formats, digests, counts, locations, and declared external retrieval services.
- **Do not use it for:** Retrieving matrix bytes inline; replacing VariantSet, CallSet, or Calls; assuming this endpoint slices matrices or controls authorization on external bytes.
- **Side effects / retry:** Read-only.

### 5.2 Register a variant-matrix reference
- **Identity:** `POST /brapi/v3/variantmatrices`
- **operationId:** `genxRegisterVariantMatrixReference`
- **Catalogue ID:** `brapi-den.genx.v3.variant-matrices.register`
- **Classification:** D3; cross-cutting C1, C2, C5, C6, C9.
- **Purpose:** Register a content-addressed reference to an externally stored genomic matrix, including format, location, digest, and optional dimensions/access-service metadata.
- **Use it for:** Publishing a resolvable, integrity-verifiable reference to a supported matrix format.
- **Do not use it for:** Uploading or serving matrix bytes; replacing V2.1 genotyping resources; assuming a new matrix-slicing protocol or authorization contract.
- **Side effects / retry:** Creates a reference; identical registration replays; changed content under the same identity conflicts and requires a new identity.

### 5.3 Get one variant-matrix reference
- **Identity:** `GET /brapi/v3/variantmatrices/{matrixDbId}`
- **operationId:** `genxGetVariantMatrixReference`
- **Catalogue ID:** `brapi-den.genx.v3.variant-matrices.get`
- **Classification:** D3; cross-cutting C1, C2, C5, C6, C9.
- **Purpose:** Retrieve metadata for one registered variant-matrix reference.
- **Use it for:** Resolving the metadata needed to retrieve and verify bytes through the declared external service.
- **Do not use it for:** Expecting the matrix file or selected variants in the response; treating a matrix reference as a VariantSet or CallSet.
- **Side effects / retry:** Read-only.
- **Neighbor:** V2.1 VariantSet/Variant/CallSet/Calls remain their own resources. See SEM-04.

## 6. Data exchange, publication and access metadata

### 6.1 List FAIR-package metadata
- **Identity:** `GET /brapi/v3/fair-packages`
- **operationId:** `genxListFairPackageMetadata`
- **Catalogue ID:** `brapi-den.genx.v3.fair-packages.list-metadata`
- **Classification:** Cross-cutting C1, C2, C5, C6, C9.
- **Purpose:** List package metadata, optionally filtered by access rights or license.
- **Use it for:** Discovering citation, licensing, access, embargo, and payload-reference metadata.
- **Do not use it for:** Downloading payload bytes; assuming the package service stores them; minting identifiers or approving access requests; assuming all embargo rules are finalized.
- **Side effects / retry:** Read-only.

### 6.2 Register a FAIR package
- **Identity:** `POST /brapi/v3/fair-packages`
- **operationId:** `genxRegisterFairPackage`
- **Catalogue ID:** `brapi-den.genx.v3.fair-packages.register`
- **Classification:** Cross-cutting C1, C2, C5, C6, C9.
- **Purpose:** Register a licensed, access-controlled metadata envelope binding one or more payload references into a citable unit.
- **Use it for:** Recording package identifiers, license, access rights, embargo, creators, and payload references.
- **Do not use it for:** Uploading/storing payload bytes, minting persistent identifiers, license negotiation, or implementing restricted-access approval.
- **Side effects / retry:** Creates metadata; identical registration replays and conflicting content under the same identity is rejected.

### 6.3 Get one FAIR package
- **Identity:** `GET /brapi/v3/fair-packages/{packageDbId}`
- **operationId:** `genxGetFairPackageMetadata`
- **Catalogue ID:** `brapi-den.genx.v3.fair-packages.get-metadata`
- **Classification:** Cross-cutting C1, C2, C5, C6, C9.
- **Purpose:** Retrieve one package metadata envelope, subject to the current proposal's embargo gate.
- **Use it for:** Reading package metadata when the access contract permits it.
- **Do not use it for:** Retrieving payload bytes; assuming embargoed metadata stays visible; treating the endpoint as an access-approval workflow.
- **Side effects / retry:** Read-only. The current reference behavior denies the entire record with HTTP 403 while embargoed; the metadata-visible alternative remains unresolved under D-15.
- **Neighbor:** V2.1 file references are not equivalent to a package-level license/embargo contract. See SEM-05.

## 7. Sensor time-series telemetry

### 7.1 Query telemetry samples or aggregates
- **Identity:** `GET /brapi/v3/telemetry`
- **operationId:** `genxQueryTelemetrySamplesOrAggregates`
- **Catalogue ID:** `brapi-den.genx.v3.telemetry.query`
- **Classification:** Context-dependent D4 or D5; cross-cutting C1, C2, C3, C7, C9.
- **Purpose:** Read raw device/sensor samples in timestamp order or calculate deterministic aggregates over a time range.
- **Use it for:** Raw time-series retrieval; mean, minimum, maximum, and count aggregates; an inclusive `from` timestamp and exclusive `to` timestamp.
- **Do not use it for:** Automatically converting every point into a BrAPI Observation; assuming links to a study, observation unit, or observation variable; assuming unspecified gap-filling, resampling, or timezone behavior.
- **Side effects / retry:** Read-only. The same query over the same stored sample set yields deterministic aggregation under the defined rules.
- **Classification rule:** Soil moisture/weather readings are D5; measured plant traits are D4. Classify by phenomenon, not by sensor type.

### 7.2 Append a telemetry batch
- **Identity:** `POST /brapi/v3/telemetry`
- **operationId:** `genxAppendTelemetryBatch`
- **Catalogue ID:** `brapi-den.genx.v3.telemetry.append-batch`
- **Classification:** Context-dependent D4 or D5; cross-cutting C1, C2, C3, C7, C9.
- **Purpose:** Append a batch of timestamped device/sensor samples and report new, replayed, and conflicting elements.
- **Use it for:** Sensor ingestion and safe retry of identical samples; rejecting conflicting values for an already-used natural key without discarding unrelated valid batch elements.
- **Do not use it for:** Silently replacing existing samples; assuming the whole batch is all-or-nothing; treating every sample as a complete observation record or assuming every reading is environmental.
- **Side effects / retry:** Appends non-conflicting points and reports replays/conflicts element-wise. Natural key: deviceDbId + sensorDbId + timestamp.
- **Neighbor:** Telemetry does not automatically equal the V2.1 Observation/ObservationVariable model; explicit mapping rules are required. See SEM-03.

## 8. Rules for extending this catalogue

1. Every new operation must have an explicit, globally unique `operationId` and `catalogId`.
2. Every operation must include `x-brapi-den` metadata: primary domain or explicit cross-cutting classification, purpose, supported uses, non-uses, side effects, idempotency, semantic neighbors, relevant decisions, and proposal status.
3. The description must state what the operation does and must not imply. “Create/read/update” alone is insufficient when lifecycle and replay semantics matter.
4. Request/response schemas, status codes, and parameters live in the operation's OpenAPI definition. Do not copy them into this catalogue as a second authoritative contract.
5. New paths and operations must be checked against all existing BrAPI-Den versions for method/path overlaps, operation identifier collisions, and semantic-neighbor overlaps. Register overlaps in `Conformance/endpoint-overlaps.yaml`.
6. For neighboring endpoints, classify their relationship explicitly: same resource/versioned contract, successor with differences, complementary, distinct, or unresolved semantic overlap.
7. Unresolved high-risk overlaps block claims of interchangeability and automated dual-write behavior.
8. A catalogue entry describes a proposed contract; it does not prove that an implementation is deployed, reachable, secure, or conformant.
