# BrAPI-GenX (proposal)

Next-generation BrAPI design surface. **Proposal status: not accepted, not normative.**

- V2.1 (`BrAPI-Core`, `BrAPI-Phenotyping`, `BrAPI-Genotyping`, `BrAPI-Germplasm`)
  stays frozen. Nothing in this directory changes V2.1 behavior.
- GenX objects are **additive and optional**: a V2.1 client must keep working
  against a GenX server, and a GenX client must tolerate a server that does not
  implement a GenX object.
- Start point: [RFC-001-GenX-Skeleton](./RFC-001-GenX-Skeleton.md) — principles,
  compatibility law, and the first three objects.
- Wiring into `generator/` and `BrAPI-Schema/` (built `Generated/` artifacts) is
  deferred as `requires decision` in the RFC. This directory is inert to the
  V2.1 build until that decision is taken.

## Objects

| Directory | Object | Kind |
|---|---|---|
| `Provenance/` | `ProvenanceEnvelope` — method/algorithm version, inputs digest, assumptions, uncertainty, evidence links | Embedded schema, no endpoints |
| `Jobs/` | `Job` — async execution with idempotency key, status, cancel | `GET /brapi/v3/jobs` (`genxListJobs`); `POST /brapi/v3/jobs` (`genxSubmitAsyncJob`); `GET /brapi/v3/jobs/{jobDbId}` (`genxGetAsyncJobById`); `DELETE /brapi/v3/jobs/{jobDbId}` (`genxRequestAsyncJobCancellation`) |
| `ServerInfoV3/` | `ServerInfoV3` — capability negotiation under `/brapi/v3` | `GET /brapi/v3/serverinfo` (`genxGetServerInfoV3`) |
| `VariableTerms/` | `VariableTerm` — versioned, namespaced observation-variable terms; conflicts rejected | `GET /brapi/v3/variable-terms` (`genxListVariableTermVersions`); `POST /brapi/v3/variable-terms` (`genxPublishVariableTermVersion`); `GET /brapi/v3/variable-terms/{variableDbId}` (`genxGetVariableTermVersion`) |
| `LotLedger/` | `LotLedgerEntry` — append-only, idempotent lot movements | `GET /brapi/v3/seedlots/{seedLotDbId}/ledger` (`genxListSeedLotLedgerEntries`); `POST /brapi/v3/seedlots/{seedLotDbId}/ledger` (`genxAppendSeedLotLedgerEntry`) |
| `Models/` | `ModelArtifact` — registered models; inference binds by digest | `GET /brapi/v3/models` (`genxListModelVersions`); `POST /brapi/v3/models` (`genxRegisterModelVersion`); `GET /brapi/v3/models/{modelDbId}` (`genxGetModelVersion`); execute inference through `POST /brapi/v3/jobs` (`genxSubmitAsyncJob`) with a declared inference `jobType` |
| `Genomics/` | `VariantMatrix` — content-addressed matrix references | `GET /brapi/v3/variantmatrices` (`genxListVariantMatrixReferences`); `POST /brapi/v3/variantmatrices` (`genxRegisterVariantMatrixReference`); `GET /brapi/v3/variantmatrices/{matrixDbId}` (`genxGetVariantMatrixReference`) |
| `FAIR/` | `FAIRPackage` — licensed, embargo-aware payload envelopes | `GET /brapi/v3/fair-packages` (`genxListFairPackageMetadata`); `POST /brapi/v3/fair-packages` (`genxRegisterFairPackage`); `GET /brapi/v3/fair-packages/{packageDbId}` (`genxGetFairPackageMetadata`) |
| `Telemetry/` | `TelemetryPoint` — sensor streams, idempotent ingest, aggregates | `GET /brapi/v3/telemetry` (`genxQueryTelemetrySamplesOrAggregates`); `POST /brapi/v3/telemetry` (`genxAppendTelemetryBatch`) |
| `Conformance/` | Probes + fixtures + runner contract (`probes.yaml`) | Static tier runs now; live tier needs `--server` |

RFCs: [RFC-001-GenX-Skeleton](./RFC-001-GenX-Skeleton.md) (principles + first
three objects), [RFC-002-Variable-Term-Governance](./RFC-002-Variable-Term-Governance.md),
[RFC-003-Seed-Lot-Ledger](./RFC-003-Seed-Lot-Ledger.md),
[RFC-004-Model-Registry](./RFC-004-Model-Registry.md),
[RFC-005-Variant-Matrix-References](./RFC-005-Variant-Matrix-References.md),
[RFC-006-FAIR-Packages](./RFC-006-FAIR-Packages.md),
[RFC-007-Telemetry-Streams](./RFC-007-Telemetry-Streams.md).

[DECISIONS.md](./DECISIONS.md) logs deferred questions (D-01…D-20, need
authorization) and autonomous drafting decisions (A-01…A-12, reviewable).

[ENDPOINT-IDENTITY.md](./ENDPOINT-IDENTITY.md) defines stable operation identities and guards against semantic endpoint collisions.

[ADOPTION.md](./ADOPTION.md) is the incremental adoption guide for V2.1
servers (order, compat rules, conformance commands, anti-patterns).
