# RFC-001: BrAPI GenX Skeleton

- Status: **proposal** (not accepted, not normative, grants no implementation authority)
- Scope: principles, compatibility law, and the first three GenX objects
- Non-scope: genomics-v2 references, phenomics streams, ontology governance,
  model registry, seed-traceability ledger, FAIR/FDO wrapper — each needs its
  own RFC before any schema is written

## 1. Why GenX, and what it borrows

BrAPI V2.1 (frozen July 2022, `201` endpoints) standardizes breeding-data
exchange but has no answer for: method/algorithm versioning and uncertainty on
results; async work beyond `POST /brapi/v2/search` polling; capability negotiation
beyond per-call `serverinfo`; multi-tenant SaaS identity; idempotent writes.

These gaps were met independently while implementing BrAPI-backed breeding
software (BijMantra prototype, pre-production architecture research): every
scientific result there must carry inputs, algorithm/version, assumptions,
tolerance, uncertainty, and provenance; every write is idempotent under
`(tenant, idempotencyKey)`; identity is OIDC JWT with issuer/audience/tenant
binding; long work runs as cancellable jobs; evidence links bind answers to
source endpoint, schema, and response digest. GenX adopts those shapes in
BrAPI-idiomatic form. BijMantra is evidence only — it confers no authority on
this RFC, and this RFC imposes nothing on BijMantra.

## 2. Principles

1. One authoritative owner per datum. IDs are namespaced
   `{authority}:{type}:{id}`; cross-server ID collisions are a defect, not a
   client problem.
2. Provenance and uncertainty are first-class on every computed result, not
   decoration.
3. Writes are idempotent and replay-safe. Retrying a request never duplicates
   an effect; replays return the existing record.
4. Long work is a job (submit, poll, cancel, expire), never an unbounded
   synchronous call or a poll-the-search loop.
5. Servers advertise what they implement. Clients negotiate via
   `ServerInfoV3`, never by probing endpoints.
6. Enforcement is at the runtime boundary (tenant, role, scope), never by
   hiding UI surfaces.
7. Reference, don't reinvent: genomic files (VCF/Zarr/GFF3), geospatial
   (GeoTIFF), weather, analytics pipelines, FAIR/PROV/DOI stay external
   standards linked by digest and URL.

## 3. Compatibility law (normative for all GenX work)

1. V2.1 is frozen. No GenX change may alter V2.1 request/response semantics.
2. GenX objects are additive and optional in both directions (server may omit,
   client must tolerate absence).
3. GenX lives under `/genx/v1/` (see `GeneralInfo/URL_Structure.md` pattern:
   `https://<server>/genx/v1/<endpoint>`). V2.1 keeps `/brapi/v2/`.
4. Standard response envelope (`metadata`/`result`, pagination, `datafiles`,
   `status`) is unchanged. GenX schemas compose into it.
5. HTTP status codes follow `GeneralInfo/Error_Handling.md`. The one proposed
   addition (`409` for idempotency-key conflict) is `requires decision` — see
   §6.
6. Wiring into `generator/` + `BrAPI-Schema/` + `Generated/` is deferred until
   a second RFC. Until then this directory is inert to the V2.1 build.

## 4. Object 1 — ProvenanceEnvelope (embedded schema)

File: `../Core/Provenance/Schemas/ProvenanceEnvelope.yaml`.

Purpose: attach method identity, inputs, assumptions, uncertainty, and evidence
to any computed result (observation, analysis, prediction). Optional on every
host object; absence means "unprovenanced", never an error.

Responsibilities: identify how a value was produced and what it depends on, so
a client can re-derive or distrust it.
Non-responsibilities: licensing/DOI/embargo (future FAIR wrapper RFC);
ontology versioning and conflict policy (future ontology RFC); file payloads
(use `metadata.datafiles`).

Fields: `methodVersion`, `algorithm` + `algorithmVersion`, `inputsDigest`
(SHA-256 over canonical inputs, hex), `assumptions[]`, `uncertainty{type,
value, unit}`, `recordedAt`, `actor`, `sources[]{sourceType, sourceId,
sourceEndpoint}`, `evidenceLinks[]{endpoint, schemaVersion, responseDigest,
queryDigest}`.

Invariants: digests are lowercase hex; `recordedAt` follows
`GeneralInfo/Date_Time_Encoding.md`; unknown fields inside the envelope must be
tolerated by readers.

## 5. Object 2 — Jobs (async execution)

Files: `../Core/Jobs/Schemas/Job.yaml`, `../Core/Jobs/Schemas/JobNewRequest.yaml`,
`../Core/Jobs/Jobs_GET_POST.yaml`, `../Core/Jobs/Jobs_JobDbId_GET_DELETE.yaml`.

Purpose: give every long-running operation (searches, analyses, exports, model
inference) one lifecycle: submit → poll → retrieve-or-cancel → expire.

- `POST /genx/v1/jobs` (`genxSubmitAsyncJob`) with `JobNewRequest{jobType, parameters, idempotencyKey?}`.
  Returns `202` + `Job`. If `idempotencyKey` was already accepted with a
  byte-identical body, the server must return the existing `Job` with zero new
  effects (replay returns existing).
- `GET /genx/v1/jobs/{jobDbId}` (`genxGetAsyncJobById`) returns the current `Job{jobDbId, jobType, status,
  progress, createdAt, updatedAt, expiresAt, result?}`. `status` is one of
  `SUBMITTED, RUNNING, COMPLETED, FAILED, CANCELLED, EXPIRED`.
- `DELETE /genx/v1/jobs/{jobDbId}` (`genxRequestAsyncJobCancellation`) requests cancellation; terminal states are
  immutable.
- `result`, when `COMPLETED`, uses the standard envelope (`result.data` +
  pagination, or `metadata.datafiles` for file outputs).

Relationship to V2.1 `/brapi/v2/search/*`: unchanged. Servers may additionally expose an
async search as a `jobType`, but clients must not assume it. The three V2.0
search flavors (immediate/saved/async) stay valid; Jobs is the path forward,
not a retrofit.

Failure modes proved by conformance probes (to be written): replay with same
key + same body creates nothing; cancel of a terminal job is rejected;
unknown `jobType` is rejected; expired jobs report `EXPIRED` and refuse
retrieval.

## 6. Object 3 — ServerInfoV3 (capability negotiation)

Files: `../Core/ServerInfoV3/Schemas/ServerInfoV3.yaml`,
`../Core/ServerInfoV3/ServerInfoV3_GET.yaml`.

Purpose: let a client learn, in one call, which BrAPI generations, GenX
objects, auth profiles, and scopes a server supports.

- `GET /genx/v1/serverinfo` (`genxGetServerInfoV3`) (V2.1 `GET /brapi/v2/serverinfo` is untouched).
- `ServerInfoV3` keeps every V2.1 `ServerInfo` field and adds:
  `brapiVersions[]` (e.g. `["2.1", "3.0-draft"]`),
  `capabilities[]{name, versions[], methods[], scopes[]}` where `name` is a
  GenX object (`provenanceEnvelope`, `jobs`, …) or an existing call family,
  and `authProfiles[]{name, issuer?, scopes[]}`.
- GenX auth profile `oidc`: OIDC JWT bearer token; server validates signature
  against the provider JWKS, requires and binds `iss`, `aud`, `exp`, and reads
  tenant membership from a documented claim. Client-chosen tenant/actor
  headers are never trusted. HMAC algorithms are rejected before key lookup
  (algorithm-confusion guard). Servers not implementing `oidc` keep V2.1
  bearer semantics.

## 7. Hypothesis, falsifier, verification

- Hypothesis: the three objects can be adopted independently by two
  interoperating implementations with zero changes to their V2.1 paths.
- Falsifier: any required V2.1 behavior change; any object that cannot be
  omitted by one side without breaking the other; any replay that duplicates
  an effect; any provenance claim that cannot name its inputs digest.
- Verification (before advancing past skeleton): conformance probes for
  idempotent replay, key-conflict rejection, job cancel/expire transitions,
  `ServerInfoV3` negotiation against a V2.1-only server, and round-trip of a
  provenanced observation through `datafiles`-linked payloads.

## 8. Explicit unknowns and requires-decision

1. `requires decision`: HTTP status for same-key/different-body conflict
   (proposed `409` with plain-text body; not in `Error_Handling.md` today).
2. `requires decision`: digest canonicalization (which JSON canonical form
   feeds `inputsDigest` / `responseDigest`).
3. `requires decision`: OIDC claim name for tenant membership and multi-tenant
   scope vocabulary.
4. `requires decision`: wiring GenX into `generator/`, `BrAPI-Schema/`, and
   `Generated/` build outputs.
5. `assumption`: servers can retain idempotency keys at least until the
   advertised `expiresAt`. Retention floor uncalibrated.
6. `unknown`: real-world async workloads to calibrate job expiry, progress
   reporting, and result-retention budgets — needs implementer evidence, not
   invention.

## 9. File map

```text
Specification/BrAPI-GenX/
  ../README.md                  module entry, status, object index
  RFC-001-GenX-Skeleton.md   this document
  ../swaggerMetaData.yaml        proposal-level metadata, inert to V2.1 build
  ../Core/Provenance/README.md + GroupDescription.md + Schemas/ProvenanceEnvelope.yaml
  ../Core/Jobs/README.md + GroupDescription.md + Schemas/Job.yaml
    + Schemas/JobNewRequest.yaml + Jobs_GET_POST.yaml
    + Jobs_JobDbId_GET_DELETE.yaml
  ../Core/ServerInfoV3/README.md + GroupDescription.md
    + Schemas/ServerInfoV3.yaml + ServerInfoV3_GET.yaml
  ../Conformance/README.md + probes.yaml + fixtures/*.json (runner: Scripts/checkGenXConformance.py)
  ../Conformance/RESULTS.md         recorded runs (static 8/8, live 15/15 vs reference server)
  Scripts/genx_test_server.py    reference test server (repo Scripts/, stdlib only)
```

Next RFCs (not started): FAIR exchange wrapper, genomics-v2 references,
phenomics/sensor streams, ontology governance, model registry, seed-traceability
ledger. Each must state its own hypothesis and falsifier before schemas.
