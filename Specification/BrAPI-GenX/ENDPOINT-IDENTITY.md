# GenX Endpoint Identity and Semantic Collision Guardrails

- Status: **engineering guardrail for a non-normative proposal**; not community ratification.
- Applies to: every endpoint introduced under the GenX base path `/genx/v1`, all examples and tests that call it, and any future generated client or AI-agent-facing description.
- Purpose: prevent two operations from being given names that make them appear interchangeable when they have different request, response, effect, identity, permission, lifecycle, or data-ownership semantics.

## 1. The identity rule

An endpoint must never be identified by a short path fragment alone. The complete operation identity is the tuple:

1. **API generation and base path** (for example, `/brapi/v2` versus `/genx/v1`);
2. **HTTP method** and complete route template, including path parameters;
3. **stable OpenAPI `operationId`**;
4. **request schema and response schema(s)**;
5. **semantic action** (read, query, register, publish, append, cancel, or another precisely defined effect);
6. **resource identity/version rules** and side-effect/idempotency behavior;
7. **authorization scope/actor/tenant boundary**, when applicable; and
8. **explicit relationship to any similar existing operation**.

The URI is the dispatch address. The `operationId` is the stable contract-level name used by tooling and client code. Neither can substitute for the other. The OpenAPI Specification requires `operationId` values to be unique within an API description; GenX strengthens this for generated-client safety by requiring every GenX value to start with `genx` and to state a domain-specific action. [OpenAPI Operation Object](https://spec.openapis.org/oas/v3.1.2#operation-object).

**Never refer to an endpoint in a standard, issue, test, log, error report, or agent instruction only as “GET /variables”, “GET /variable-terms”, or “the model endpoint” when generation or behavior matters.** Include the full base path and `operationId`, plus the relevant schema name when discussing payload behavior.

## 2. Naming rules

Every GenX operation must satisfy all of these rules:

- Carry an explicit, case-sensitive `operationId` in its OpenAPI operation object. No inference from filename, HTTP method, summary, or URL is allowed.
- Start the identifier with `genx`, followed by an action and a domain-specific object, for example `genxGetAsyncJobById`. This keeps GenX names separate from older and future code-generated method names.
- Use a meaningful business action: distinguish **list** from **get**, **register** from **execute**, **append** from **replace**, and **request cancellation** from **delete the resource**.
- Make the noun as specific as the returned/changed resource. Avoid generic names such as `getData`, `postThing`, `getVariable`, `createModel`, or `process`.
- Keep `operationId` stable across editorial changes. Changing it can rename a generated client method even when the URI is unchanged.
- Do not create two operation IDs for the same method/path semantics, or reuse an operation ID for a new meaning.
- Require non-empty `summary` and `description`. The description must state what is read/created/changed, relevant request and response types, material side effects/replay behavior, and known non-responsibilities or neighboring operations.
- Treat path parameters, query parameters, request bodies, response schemas, status codes, ownership, and side effects as contract semantics, not merely documentation.
- A resource schema name and a collection path do not have to be lexically identical, but any mismatch must be explained in the operation description and semantic relationship register.

The `genx` prefix is a proposal-local engineering convention. It does not claim that the BrAPI community has ratified these names.

## 3. Versioned paths and semantic neighbors

Two operations may share a relative path in separate major API generations. They are different endpoints because their complete base paths and contracts differ. That reuse is safe only when the relationship is documented and client guidance says which schema applies.

Two paths may also be different but represent the same real-world concept (for example, seed-lot “transactions” and a seed-lot “ledger”). Different route strings do **not** prove different meaning. The review must classify each relationship as one of:

- **Same resource, versioned contract** — same purpose across generations, different versioned payload/behavior.
- **Versioned domain successor with contract differences** — same domain lineage but not wire-interchangeable.
- **Complementary** — related surfaces with a defined division of responsibility.
- **Distinct** — similar vocabulary, materially different resources.
- **Unresolved semantic overlap** — current evidence is insufficient to define an authoritative mapping or a safe dual-write rule. This is an adoption blocker for workflows that would rely on equivalence.

The machine-readable overlap and semantic-neighbor register is `Conformance/endpoint-overlaps.yaml`. Exact path reuse is checked by probe **S-21**. A code change that adds a new overlap must update the register in the same change; an undocumented overlap is a conformance failure, not a review note to handle later.

## 4. Cross-generation cases that must not be collapsed

### Server capability discovery

- V2.1: `GET /brapi/v2/serverinfo` — V2.1 `ServerInfo` contract.
- GenX: `GET /genx/v1/serverinfo`, `operationId=genxGetServerInfoV3` — `ServerInfoV3` including `brapiVersions`, `capabilities`, and `authProfiles`.

Both discover a server's surface, but the payloads are not interchangeable. A GenX client may use the documented V2.1 fallback when GenX is absent; it must not call an unadvertised GenX endpoint as a feature probe.

### V2.1 observation variables versus GenX versioned variable terms

- V2.1: `/brapi/v2/variables` returns `ObservationVariable` records, each a unique combination of Trait, Method, and Scale.
- GenX: `/genx/v1/variable-terms`, `operationId=genxListVariableTermVersions`, returns versioned, namespaced `VariableTerm` records. The related single-record operation is `genxGetVariableTermVersion`; publication is `genxPublishVariableTermVersion`.

GenX intentionally uses the distinct `/genx/v1/variable-terms` route rather than reusing `/brapi/v2/variables`. This makes the resource boundary visible in the path itself. The contracts are still domain-adjacent, not interchangeable: V2.1 bulk POST and GenX single-term publication have different request shapes and lifecycle semantics. Generated clients and AI agents must use the base path, route, `operationId`, and schema name together. GenX `VariableTerm` is also **not** the V2.1 Genotyping `OntologyTerm` label/reference schema.

### Seed-lot transaction versus ledger — unresolved and high risk

V2.1 `SeedLotTransaction` and GenX `LotLedgerEntry` can both describe material movement, but their contracts differ materially. V2.1 has transaction-level `fromSeedLotDbId`/`toSeedLotDbId` and numeric `amount`; GenX records per-lot ordered entries with decimal-string `quantity`, actor, and replay/conflict behavior. The GenX proposal does not yet prove a one-to-one mapping, shared event identity, transaction-level atomicity, or a safe mirrored-write contract.

**Until deferred decision D-20 is resolved, no client or implementation may assume that these are equivalent, that one stream is an automatic projection of the other, or that it is safe to write one real-world movement to both streams and count both.** GenX must not be advertised as a drop-in replacement for V2.1 seed-lot transactions.

### Other adjacent surfaces

| GenX surface | Neighboring V2.1 surface | Required distinction |
|---|---|---|
| `/genx/v1/jobs` | `/brapi/v2/search/*` | Jobs is a general asynchronous work lifecycle, not a retrofit of existing search services. Async search as a Job is optional and must be advertised. |
| `/genx/v1/telemetry` | Observations and Observation Variables | Telemetry represents device/sensor time-series points or aggregates. It is not automatically a scientific observation tied to a study, observation unit, and observation variable. Mapping requires explicit rules. |
| `/genx/v1/variantmatrices` | VariantSet, Variant, CallSet, Calls | A VariantMatrix is external matrix metadata/reference, not an alias for a V2.1 VariantSet and not an endpoint that streams matrix bytes. |
| `/genx/v1/fair-packages` | `metadata.datafiles` and external file retrieval | A FAIRPackage describes packaging, licensing, access rights, embargo, and identifiers; it is not a data-byte transport endpoint. |
| `/genx/v1/models` | GenX inference Jobs | Registering/getting a model is separate from executing it. Inference is submitted through Jobs with a declared `jobType`; no synchronous infer route is implied. |
| GenX `ProvenanceEnvelope` | result and source metadata | This is an embedded schema, not a standalone endpoint. Its presence must not cause agents to invent a `/provenance` route. |

## 5. Current operation catalogue

The OpenAPI endpoint files remain the machine-readable source of request/response contracts. The catalogue below is an agent-facing disambiguation index; its boundary column is mandatory guidance, not optional commentary.

| Full route | Method | Stable operation ID | Primary meaning | Boundary / do not infer |
|---|---|---|---|---|
| `/genx/v1/serverinfo` | GET | `genxGetServerInfoV3` | Discover advertised generations, capabilities, and authentication profiles | Not V2.1 `GET /brapi/v2/serverinfo`; a capability must not be assumed available unless advertised. |
| `/genx/v1/jobs` | GET | `genxListJobs` | List caller-visible asynchronous jobs | Not a V2.1 search-results resource; a query may be represented as a Job only when the server advertises that behavior. |
| `/genx/v1/jobs` | POST | `genxSubmitAsyncJob` | Submit one unit of asynchronous work | Submission is not synchronous execution; model registration and model inference are distinct actions. |
| `/genx/v1/jobs/{jobDbId}` | GET | `genxGetAsyncJobById` | Retrieve current job lifecycle/result state | Expired jobs may refuse result retrieval; do not assume a result is indefinitely available. |
| `/genx/v1/jobs/{jobDbId}` | DELETE | `genxRequestAsyncJobCancellation` | Request cancellation of one job | Requests cancellation; it does not delete the job record, and terminal states are not rewritten. |
| `/genx/v1/variable-terms` | GET | `genxListVariableTermVersions` | List versioned, namespaced variable-term definition records | Not V2.1 `ObservationVariable` records and not the V2.1 Genotyping `OntologyTerm` label/reference schema. |
| `/genx/v1/variable-terms` | POST | `genxPublishVariableTermVersion` | Publish one immutable version; identical writes replay and conflicting rewrites are rejected | Not V2.1 bulk publication of `ObservationVariableNewRequest[]`; body cardinality and lifecycle semantics differ. |
| `/genx/v1/variable-terms/{variableDbId}` | GET | `genxGetVariableTermVersion` | Retrieve a namespaced VariableTerm by identifier and optional version | `variableDbId` identifies a GenX VariableTerm, not V2.1 `observationVariableDbId`. When `version` is omitted, the current proposal uses most-recently-created; version ordering remains unresolved. |
| `/genx/v1/seedlots/{seedLotDbId}/ledger` | GET | `genxListSeedLotLedgerEntries` | List a single lot's ledger entries in source-local position order | Does not establish global chronology or compute an authoritative lot balance; entries are not proven equivalent to V2.1 `SeedLotTransaction` records (D-20). |
| `/genx/v1/seedlots/{seedLotDbId}/ledger` | POST | `genxAppendSeedLotLedgerEntry` | Append one entry to one lot with replay/conflict semantics | Append-only and per-lot; not an atomic two-lot transfer. Do not mirror or double-count with V2.1 transactions without resolving D-20. |
| `/genx/v1/models` | GET | `genxListModelVersions` | List registered model-version records | Lists registry metadata; does not run inference or imply that a model is approved or safe to execute. |
| `/genx/v1/models` | POST | `genxRegisterModelVersion` | Register model metadata/artifact identity and version | Registration does not execute the model, approve it for use, or establish artifact transport/approval policy. |
| `/genx/v1/models/{modelDbId}` | GET | `genxGetModelVersion` | Retrieve a registered model version | Retrieval is not inference; inference is submitted as a Job with an explicit `jobType`. |
| `/genx/v1/variantmatrices` | GET | `genxListVariantMatrixReferences` | List registered external matrix references | Not an alias for V2.1 `VariantSet`, `Variant`, `CallSet`, or `Calls`; does not return matrix bytes. |
| `/genx/v1/variantmatrices` | POST | `genxRegisterVariantMatrixReference` | Register matrix metadata and a content/location reference | Registers a reference; it does not upload or transmit the matrix payload bytes. |
| `/genx/v1/variantmatrices/{matrixDbId}` | GET | `genxGetVariantMatrixReference` | Retrieve one matrix-reference record | Returns metadata/reference only; byte retrieval and authorization follow a separate, still decision-sensitive contract. |
| `/genx/v1/fair-packages` | GET | `genxListFairPackageMetadata` | List FAIR package metadata | Not a payload download; license/embargo metadata does not itself transport package bytes. |
| `/genx/v1/fair-packages` | POST | `genxRegisterFairPackage` | Register package metadata and access-policy declarations | Does not itself ingest payload bytes, mint a DOI, or grant restricted-access approval. |
| `/genx/v1/fair-packages/{packageDbId}` | GET | `genxGetFairPackageMetadata` | Retrieve one FAIR package metadata record | Not payload transport; embargo visibility behavior remains an open decision, and the current prototype's behavior is not a normative requirement. |
| `/genx/v1/telemetry` | GET | `genxQueryTelemetrySamplesOrAggregates` | Read sensor/device samples or computed aggregates for a time range | Telemetry is not automatically a BrAPI `Observation`; scientific mapping requires explicit study, unit, variable, timestamp, quality, and provenance rules. |
| `/genx/v1/telemetry` | POST | `genxAppendTelemetryBatch` | Append a batch of sensor/device samples and report append/replay/conflict outcomes | Append operation, not replacement of a range; identical sample identity may replay, while conflicting content must not silently overwrite. |
| `/genx/v1/selection-decisions` | GET | `genxListSelectionDecisions` | List recorded breeding selection decisions | Does not create or change a verdict; not a BrAPI v2.1 program/trial/observation resource. |
| `/genx/v1/selection-decisions` | POST | `genxRecordSelectionDecision` | Record one breeding selection verdict | Append-only verdict record; does not imply release, registration, or commercial approval; replay/conflict semantics. |
| `/genx/v1/selection-decisions/{selectionDecisionDbId}` | GET | `genxGetSelectionDecision` | Retrieve one recorded breeding selection decision | Does not treat a superseded decision as current; not a BrAPI v2.1 resource. |
| `/genx/v1/breeding-pipelines` | GET | `genxListBreedingPipelines` | List breeding pipeline definitions | Does not create or change a pipeline; not a BrAPI Program or Study. |
| `/genx/v1/breeding-pipelines` | POST | `genxRegisterBreedingPipeline` | Register one breeding pipeline definition | Append-only record; replay/conflict semantics; does not imply an approved plan. |
| `/genx/v1/breeding-pipelines/{breedingPipelineDbId}` | GET | `genxGetBreedingPipeline` | Retrieve one breeding pipeline definition | Does not treat a superseded pipeline as current. |
| `/genx/v1/experimental-designs` | GET | `genxListExperimentalDesigns` | List experimental design records | Does not create or change a design; not a BrAPI Study. |
| `/genx/v1/experimental-designs` | POST | `genxRegisterExperimentalDesign` | Register one experimental design record | Append-only record; replay/conflict semantics. |
| `/genx/v1/experimental-designs/{experimentalDesignDbId}` | GET | `genxGetExperimentalDesign` | Retrieve one experimental design record | Does not treat a superseded design as current. |
| `/genx/v1/progeny-records` | GET | `genxListProgenyRecords` | List progeny/family records | Does not create or change a record; not a BrAPI Pedigree or Cross. |
| `/genx/v1/progeny-records` | POST | `genxRecordProgeny` | Record one progeny/family link | Append-only record; replay/conflict semantics. |
| `/genx/v1/progeny-records/{progenyRecordDbId}` | GET | `genxGetProgenyRecord` | Retrieve one progeny/family record | Does not treat a superseded record as current. |
| `/genx/v1/doubled-haploid-programs` | GET | `genxListDoubledHaploidPrograms` | List doubled haploid programs | Does not create or change a program; not a BrAPI Program. |
| `/genx/v1/doubled-haploid-programs` | POST | `genxRegisterDoubledHaploidProgram` | Register one doubled haploid program | Append-only record; replay/conflict semantics. |
| `/genx/v1/doubled-haploid-programs/{doubledHaploidProgramDbId}` | GET | `genxGetDoubledHaploidProgram` | Retrieve one doubled haploid program | Does not treat a superseded program as current. |
| `/genx/v1/speed-breeding-protocols` | GET | `genxListSpeedBreedingProtocols` | List speed breeding protocols | Does not create or change a protocol; not a BrAPI Program. |
| `/genx/v1/speed-breeding-protocols` | POST | `genxRegisterSpeedBreedingProtocol` | Register one speed breeding protocol | Append-only record; replay/conflict semantics. |
| `/genx/v1/speed-breeding-protocols/{speedBreedingProtocolDbId}` | GET | `genxGetSpeedBreedingProtocol` | Retrieve one speed breeding protocol | Does not treat a superseded protocol as current. |
| `/genx/v1/soil-profiles` | GET | `genxListSoilProfiles` | List soil profiles | Does not create or change a profile; not a BrAPI Location. |
| `/genx/v1/soil-profiles` | POST | `genxRegisterSoilProfile` | Register one soil profile | Append-only record; replay/conflict semantics. |
| `/genx/v1/soil-profiles/{soilProfileDbId}` | GET | `genxGetSoilProfile` | Retrieve one soil profile | Does not treat a superseded profile as current. |
| `/genx/v1/irrigation-operations` | GET | `genxListIrrigations` | List irrigation events | Does not create or change an event; not a BrAPI Location. |
| `/genx/v1/irrigation-operations` | POST | `genxRecordIrrigation` | Record one irrigation event | Append-only record; replay/conflict semantics. |
| `/genx/v1/irrigation-operations/{irrigationEventDbId}` | GET | `genxGetIrrigation` | Retrieve one irrigation event | Does not treat a superseded event as current. |
| `/genx/v1/repeated-measurements` | GET | `genxListMeasurementSeries` | List repeated measurement series | Does not create or change a series; not a BrAPI Observation. |
| `/genx/v1/repeated-measurements` | POST | `genxRecordMeasurementSeries` | Record one repeated measurement series | Append-only record; replay/conflict semantics. |
| `/genx/v1/repeated-measurements/{measurementSeriesDbId}` | GET | `genxGetMeasurementSeries` | Retrieve one repeated measurement series | Does not treat a superseded series as current. |
| `/genx/v1/fertilizer-applications` | GET | `genxListFertilizerApplications` | List fertilizer applications | Does not create or change an application; not a BrAPI Location. |
| `/genx/v1/fertilizer-applications` | POST | `genxRecordFertilizerApplication` | Record one fertilizer application | Append-only record; replay/conflict semantics. |
| `/genx/v1/fertilizer-applications/{fertilizerApplicationDbId}` | GET | `genxGetFertilizerApplication` | Retrieve one fertilizer application | Does not treat a superseded application as current. |
| `/genx/v1/phenology-observations` | GET | `genxListPhenologyObservations` | List phenology observations | Does not create or change an observation; not a BrAPI Observation. |
| `/genx/v1/phenology-observations` | POST | `genxRecordPhenologyObservation` | Record one phenology observation | Append-only record; replay/conflict semantics. |
| `/genx/v1/phenology-observations/{phenologyObservationDbId}` | GET | `genxGetPhenologyObservation` | Retrieve one phenology observation | Does not treat a superseded observation as current. |
| `/genx/v1/parent-candidate-selections` | GET | `genxListParentCandidateSelections` | List parent candidate selections | Does not create or change a record; not a BrAPI Germplasm or Cross. |
| `/genx/v1/parent-candidate-selections` | POST | `genxRecordParentCandidateSelection` | Record one parent candidate selection | Append-only record; replay/conflict semantics. |
| `/genx/v1/parent-candidate-selections/{parentCandidateSelectionDbId}` | GET | `genxGetParentCandidateSelection` | Retrieve one parent candidate selection | Does not treat a superseded record as current. |
| `/genx/v1/crop-cycles` | GET | `genxListCropCycles` | List crop cycles | Does not create or change a cycle; not a BrAPI Study. |
| `/genx/v1/crop-cycles` | POST | `genxRegisterCropCycle` | Register one crop cycle | Append-only record; replay/conflict semantics. |
| `/genx/v1/crop-cycles/{cropCycleDbId}` | GET | `genxGetCropCycle` | Retrieve one crop cycle | Does not treat a superseded cycle as current. |
| `/genx/v1/quarantine-records` | GET | `genxListQuarantineRecords` | List quarantine records | Does not create or change a record; not a BrAPI SeedLot transaction. |
| `/genx/v1/quarantine-records` | POST | `genxRecordQuarantine` | Record one quarantine | Append-only record; replay/conflict semantics. |
| `/genx/v1/quarantine-records/{quarantineRecordDbId}` | GET | `genxGetQuarantineRecord` | Retrieve one quarantine record | Does not treat a superseded record as current. |
| `/genx/v1/weather-forecasts` | GET | `genxListWeatherForecasts` | List weather forecasts | Does not create or change a forecast; not a BrAPI Location. |
| `/genx/v1/weather-forecasts` | POST | `genxRegisterWeatherForecast` | Register one weather forecast | Append-only record; replay/conflict semantics. |
| `/genx/v1/weather-forecasts/{weatherForecastDbId}` | GET | `genxGetWeatherForecast` | Retrieve one weather forecast | Does not treat a superseded forecast as current. |
| `/genx/v1/image-metadata` | GET | `genxListImageMetadata` | List image metadata records | Does not create or change metadata; not a BrAPI Image. |
| `/genx/v1/image-metadata` | POST | `genxRegisterImageMetadata` | Register one image metadata record | Append-only record; replay/conflict semantics. |
| `/genx/v1/image-metadata/{imageMetadataDbId}` | GET | `genxGetImageMetadata` | Retrieve one image metadata record | Does not treat a superseded record as current. |
| `/genx/v1/climate-normals` | GET | `genxListClimateNormals` | List climate normal records | Does not create or change a normal; not a BrAPI Location. |
| `/genx/v1/climate-normals` | POST | `genxRegisterClimateNormal` | Register one climate normal | Append-only record; replay/conflict semantics. |
| `/genx/v1/climate-normals/{climateNormalDbId}` | GET | `genxGetClimateNormal` | Retrieve one climate normal | Does not treat a superseded normal as current. |
| `/genx/v1/safety-duplications` | GET | `genxListSafetyDuplications` | List safety duplications | Does not create or change a record; not a BrAPI SeedLot transaction. |
| `/genx/v1/safety-duplications` | POST | `genxRegisterSafetyDuplication` | Register one safety duplication | Append-only record; replay/conflict semantics. |
| `/genx/v1/safety-duplications/{safetyDuplicationDbId}` | GET | `genxGetSafetyDuplication` | Retrieve one safety duplication | Does not treat a superseded record as current. |
| `/genx/v1/regeneration-records` | GET | `genxListRegenerations` | List regeneration records | Does not create or change a record; not a BrAPI SeedLot transaction. |
| `/genx/v1/regeneration-records` | POST | `genxRecordRegeneration` | Record one regeneration | Append-only record; replay/conflict semantics. |
| `/genx/v1/regeneration-records/{regenerationRecordDbId}` | GET | `genxGetRegeneration` | Retrieve one regeneration record | Does not treat a superseded record as current. |
| `/genx/v1/population-advancements` | GET | `genxListPopulationAdvancements` | List population advancements | Does not create or change a record; not a BrAPI Program. |
| `/genx/v1/population-advancements` | POST | `genxRecordPopulationAdvancement` | Record one population advancement | Append-only record; replay/conflict semantics. |
| `/genx/v1/population-advancements/{populationAdvancementDbId}` | GET | `genxGetPopulationAdvancement` | Retrieve one population advancement | Does not treat a superseded record as current. |
| `/genx/v1/crossing-schedules` | GET | `genxListCrossingSchedules` | List crossing schedules | Does not create or change a schedule; not a BrAPI Cross or CrossingProject. |
| `/genx/v1/crossing-schedules` | POST | `genxRegisterCrossingSchedule` | Register one crossing schedule | Append-only record; replay/conflict semantics. |
| `/genx/v1/crossing-schedules/{crossingScheduleDbId}` | GET | `genxGetCrossingSchedule` | Retrieve one crossing schedule | Does not treat a superseded schedule as current. |
| `/genx/v1/analysis-methods` | GET | `genxListAnalysisMethods` | List registered analysis method versions | Does not execute an analysis; not a BrAPI v2.1 resource. |
| `/genx/v1/analysis-methods` | POST | `genxRegisterAnalysisMethod` | Register one analysis method version | Does not execute or validate the method; replay/conflict semantics. |
| `/genx/v1/analysis-methods/{analysisMethodDbId}` | GET | `genxGetAnalysisMethod` | Retrieve one registered analysis method version | Does not execute an analysis; revoked methods deny new jobs. |
| `/genx/v1/weather-observations` | GET | `genxListWeatherObservations` | List recorded weather/environmental observations | Does not create or change an observation; complementary to Telemetry. |
| `/genx/v1/weather-observations` | POST | `genxRecordWeatherObservation` | Record one weather/environmental observation | Append-only record; replay/conflict semantics; does not imply a BrAPI Observation. |
| `/genx/v1/weather-observations/{weatherObservationDbId}` | GET | `genxGetWeatherObservation` | Retrieve one recorded weather/environmental observation | Does not treat a superseded observation as current. |
| `/genx/v1/harvest-records` | GET | `genxListHarvestRecords` | List recorded harvest events | Does not create or change a record; not a BrAPI SeedLot transaction. |
| `/genx/v1/harvest-records` | POST | `genxRecordHarvest` | Record one harvest event | Append-only record; replay/conflict semantics; does not imply a yield forecast. |
| `/genx/v1/harvest-records/{harvestRecordDbId}` | GET | `genxGetHarvestRecord` | Retrieve one recorded harvest event | Does not treat a superseded record as current. |
| `/genx/v1/phenotype-captures` | GET | `genxListPhenotypeCaptures` | List phenotype capture events | Does not create or change a capture; not a BrAPI Observation. |
| `/genx/v1/phenotype-captures` | POST | `genxRecordPhenotypeCapture` | Record one phenotype capture event | Append-only record; replay/conflict semantics; does not imply a BrAPI Observation. |
| `/genx/v1/phenotype-captures/{phenotypeCaptureDbId}` | GET | `genxGetPhenotypeCapture` | Retrieve one phenotype capture event | Does not treat a superseded capture as current. |
| `/genx/v1/genomic-datasets` | GET | `genxListGenomicDatasets` | List prepared genomic datasets | Does not create or change a dataset; not a BrAPI VariantSet or VariantMatrix. |
| `/genx/v1/genomic-datasets` | POST | `genxRegisterGenomicDataset` | Register one prepared genomic dataset | Append-only record; replay/conflict semantics; does not upload dataset bytes. |
| `/genx/v1/genomic-datasets/{genomicDatasetDbId}` | GET | `genxGetGenomicDataset` | Retrieve one prepared genomic dataset | Does not treat a withdrawn dataset as current. |
| `/genx/v1/genebank-storage` | GET | `genxListStorageLocations` | List genebank storage locations | Does not create or change a location; not a BrAPI SeedLot. |
| `/genx/v1/genebank-storage` | POST | `genxRegisterStorageLocation` | Register one genebank storage location | Append-only record; replay/conflict semantics. |
| `/genx/v1/genebank-storage/{storageLocationDbId}` | GET | `genxGetStorageLocation` | Retrieve one genebank storage location | Does not treat a decommissioned location as active. |
| `/genx/v1/viability-tests` | GET | `genxListViabilityTests` | List viability/germination tests | Does not create or change a test; not a BrAPI SeedLot transaction. |
| `/genx/v1/viability-tests` | POST | `genxRecordViabilityTest` | Record one viability/germination test | Append-only record; replay/conflict semantics. |
| `/genx/v1/viability-tests/{viabilityTestDbId}` | GET | `genxGetViabilityTest` | Retrieve one viability/germination test | Does not treat a superseded test as current. |
| `/genx/v1/research-assets` | GET | `genxListResearchAssets` | List research asset records | Does not create or change an asset; not a BrAPI data resource. |
| `/genx/v1/research-assets` | POST | `genxRegisterResearchAsset` | Register one research asset | Append-only record; replay/conflict semantics; does not mint a persistent identifier. |
| `/genx/v1/research-assets/{researchAssetDbId}` | GET | `genxGetResearchAsset` | Retrieve one research asset record | Does not treat a withdrawn asset as current. |
| `/genx/v1/measurement-methods` | GET | `genxListMeasurementMethods` | List measurement method definitions | Does not create or change a method; not a BrAPI Method. |
| `/genx/v1/measurement-methods` | POST | `genxRegisterMeasurementMethod` | Register one measurement method definition | Append-only record; replay/conflict semantics. |
| `/genx/v1/measurement-methods/{measurementMethodDbId}` | GET | `genxGetMeasurementMethod` | Retrieve one measurement method definition | Does not treat a superseded method as current. |

`ProvenanceEnvelope` is embedded in result/record schemas and has no standalone route in this proposal.

## 6. Change gate

Before an endpoint or resource is added, renamed, split, merged, or changes meaning, the change must:

1. define a stable operation ID and request/response schema names;
2. name the domain action and side effects in plain, testable terms;
3. search both exact route/method reuse and nearby semantic concepts across all relevant API generations;
4. classify every relation in the register (or state that no material neighbor was found);
5. explain differences in request shape, response type, identity/version model, error behavior, authorization, idempotency, and data ownership;
6. add falsifiable static/live probes that would fail if the operations were confused; and
7. obtain the appropriate community or governance decision for any semantic choice that affects interoperability.

If the review cannot state clearly what an endpoint is **for**, what it is **not for**, and how it differs from its nearest neighboring endpoint, the slice is not ready for implementation or adoption.


## 6. Semantic catalogue metadata is required

Every GenX OpenAPI operation MUST include an operation-level `x-brapi-genx` extension containing:

- a stable, globally unique `catalogId` in the `brapi-den.genx.*` namespace;
- exactly one primary domain class, or explicit `null` for a cross-cutting operation;
- the applicable cross-cutting capability facets and any contextual domains;
- a precise purpose, supported use cases, and explicit non-goals;
- side effects and idempotency/replay behavior;
- semantic neighbors and the relevant RFC/decision references; and
- the current proposal status.

This extension belongs on the operation itself so semantic intent travels with the method, path, request/response schemas, and `operationId`. The human-readable `GENX-ENDPOINT-CATALOG.md` is the navigational view; it must enumerate every operation and catalogue ID exactly once. `Scripts/checkGenXEndpointCatalog.py` rejects missing metadata, duplicate GenX operation or catalogue IDs, route-template collisions, collisions between GenX operation IDs and other BrAPI specification operations, and catalogue coverage drift.

For any semantic description, state both what the operation is for and what it explicitly does not do. Examples of required distinctions are register versus execute, request cancellation versus delete a record, metadata reference versus byte transport, an append-only ledger versus a mutable transaction, and sensor telemetry versus a scientific observation. A matching name or nearby classification is never evidence of interchangeable contracts.


## 7. Complete registry and focused views

The focused GenX view is `GENX-ENDPOINT-CATALOG.md`. The all-generation catalogue is at `../ENDPOINT-CATALOG.md`, and the structured master registry is `../ENDPOINT-REGISTRY.json`. All generated views derive from the same registry; operation metadata in the OpenAPI YAML and the master JSON are the contract and governance sources, respectively.
