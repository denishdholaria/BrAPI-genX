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
| `Jobs/` | `Job` — async execution with idempotency key, status, cancel | Endpoints `POST /jobs`, `GET /jobs/{jobDbId}`, `DELETE /jobs/{jobDbId}` |
| `ServerInfoV3/` | `ServerInfoV3` — capability negotiation under `/brapi/v3` | Endpoint `GET /serverinfo` |
| `Ontology/` | `VariableTerm` — versioned, namespaced terms; conflicts rejected | Endpoints `POST /variables`, `GET /variables`, `GET /variables/{variableDbId}` |
| `LotLedger/` | `LotLedgerEntry` — append-only, idempotent lot movements | Endpoints `POST/GET /seedlots/{seedLotDbId}/ledger` |
| `Models/` | `ModelArtifact` — registered models; inference binds by digest | Endpoints `POST/GET /models`, `GET /models/{modelDbId}`, Jobs `inference` |
| `Genomics/` | `VariantMatrix` — content-addressed matrix references | Endpoints `POST/GET /variantmatrices`, `GET /variantmatrices/{matrixDbId}` |
| `FAIR/` | `FAIRPackage` — licensed, embargo-aware payload envelopes | Endpoints `POST/GET /fair-packages`, `GET /fair-packages/{packageDbId}` |
| `Telemetry/` | `TelemetryPoint` — sensor streams, idempotent ingest, aggregates | Endpoints `POST/GET /telemetry` |
| `Conformance/` | Probes + fixtures + runner contract (`probes.yaml`) | Static tier runs now; live tier needs `--server` |

RFCs: [RFC-001-GenX-Skeleton](./RFC-001-GenX-Skeleton.md) (principles + first
three objects), [RFC-002-Ontology-Governance](./RFC-002-Ontology-Governance.md),
[RFC-003-Seed-Lot-Ledger](./RFC-003-Seed-Lot-Ledger.md),
[RFC-004-Model-Registry](./RFC-004-Model-Registry.md),
[RFC-005-Variant-Matrix-References](./RFC-005-Variant-Matrix-References.md),
[RFC-006-FAIR-Packages](./RFC-006-FAIR-Packages.md),
[RFC-007-Telemetry-Streams](./RFC-007-Telemetry-Streams.md).

[DECISIONS.md](./DECISIONS.md) logs deferred questions (D-01…D-19, need
authorization) and autonomous drafting decisions (A-01…A-12, reviewable).

[ADOPTION.md](./ADOPTION.md) is the incremental adoption guide for V2.1
servers (order, compat rules, conformance commands, anti-patterns).
