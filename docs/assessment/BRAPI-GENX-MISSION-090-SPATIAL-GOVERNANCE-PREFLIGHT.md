# Mission 090 — Spatial execution and yield-map authority: decision preflight

**Date:** 2026-11-24. **Base:** integrated `main` at `17c195f7b08ccb00d59487eedd0e037f7a19c9b9` (Mission 088).  
**Status:** evidence-backed **decision package only**, **no ratification**, no schema/registry/endpoint change and **no promotion** of the three modules below from evidence-deferred. BrAPI means Breeding Application Programming Interface; RFC means Request for Comments.

## Objective

Determine whether three remaining BrAPI-GenX geospatial candidates represent (a) descriptive registry metadata, (b) executable spatial functionality, or (c) scientifically validated payloads. Their present OpenAPI (Open Application Programming Interface) schemas do **not** establish equivalence among those interpretations.

All three `GroupDescription.md` files remain title-only on this baseline and are intentionally **not** included in the reviewed-description guard by this decision preflight. Correctness has priority over increasing coverage counts.

## Verified current source facts

| Module | Current required registration fields | Optional illustrative metadata | Missing or unverified capability | Existing deferred decisions |
| --- | --- | --- | --- | --- |
| `Geospatial/SpatialIndex` | `spatialIndexDbId` only | `indexType`, `indexName`, `coverageArea`, `resolution`, `provenance` | No indexed dataset identity or spatial-index object/asset, geometry coordinate reference system, search strategy, index-construction request, latency/accuracy evidence, or executable query binding | D-421, D-422, D-423 (RFC-141) |
| `Geospatial/SpatialQuery` | `spatialQueryDbId` only | `queryType`, `queryGeometry`, `queryParams`, `resultReference`, `provenance` | No required query predicate, dataset/index target, geometry validity rule, result schema, submitted query execution, access-control semantics or result provenance contract. `queryGeometry` is an unstructured object and `queryParams` is a **string**, despite its object-shaped example | D-427, D-428, D-429 (RFC-143) |
| `Geospatial/YieldMap` | `yieldMapDbId` only | `studyDbId`, `locationDbId`, `cropCycleDbId`, `harvestRecordDbId`, `mapType`, numeric `resolutionM`, `storageUri`, `fileDigest`, `provenance` | **Neither storage URI nor digest is required.** There is no coordinate reference system field, map unit/scale, validated source relationship, raster grid metadata, checksum format/enforcement or proof of accessible pixels. `mapType` enum alone does not make a measurement | D-208, D-209, D-210 (RFC-070) |

The response schemas additionally require lifecycle `status`. All optional references above are strings, not schema-enforced foreign-key or authority-verified joins. An RFC's prose about immutability/replay or a value example does not itself demonstrate a deployed invariant.

## Source/claim discrepancies to resolve

1. **SpatialIndex RFC-141** says that without a descriptive index record spatial queries cannot be performed. That is an unjustified implication: database spatial indexing and querying are runtime capabilities independent of this metadata registry, while the current GenX record does not model a usable index.
2. **SpatialQuery RFC-143** describes reproducibility; a free-form optional query type, generic geometry object, string `queryParams`, optional `resultReference`, and no specified target dataset cannot independently establish reproducible zonal statistics or an executed query.
3. **YieldMap RFC-070 and README** describe a map reference as locating and verifying the payload, yet `storageUri` and `fileDigest` are optional and unvalidated. A lifecycle `status` such as `active` is not evidence that bytes exist or match a checksum. The RFC says updated bytes require a new digest, but no source contract validates that claim.
4. YieldMap's optional `harvestRecordDbId`, `studyDbId`, `locationDbId` and `cropCycleDbId` are not authoritative links. `resolutionM` is nominal metadata, not scientific spatial accuracy or sampling support.
5. Official BrAPI version 2.1 and the existing GenX Image/remote-sensing proposals must be checked for actual overlapping fields or retrieval behavior **before** accepting any new interoperable geospatial model. A named neighbor in an advisory relationship registry is not a typed crosswalk.

## Decision options — NOT YET ACCEPTED

### G-090-1: SpatialIndex contract meaning

- **A — Metadata-only** (recommended as the present accurate description): a discoverable `SpatialIndex` candidate, with no claim of executable indexing.
- **B — Executable service:** require a separate, evidenced design of input dataset identity, index building and versioning, coordinate reference system and query semantics. Do not infer these from the existing CRUD-shaped registration operations.
- **C — Defer:** withdraw promotion until a concrete interoperability need not already handled by database query infrastructure is demonstrated.

**Maintainer must choose** whether to continue as metadata-only, design an executable capability, or defer.

### G-090-2: SpatialQuery execution and authority

- **A — Stored query description** (recommended under present schema limitations): the record describes a proposed query; `resultReference` is not proof that any query ran.
- **B — Executable query job:** define spatial predicate schema, GeoJSON validation or other geometry standard, input dataset/authority identity, job state, result type, provenance and authorization; test with invalid geometries and cross-authority inputs.
- **C — Defer:** no promotion if no independently verified result contract is forthcoming.

**Maintainer must choose** and keep query execution separate from mere registration.

### G-090-3: YieldMap published-payload integrity

- **A — Optional metadata placeholder** (present truthful interpretation): a map record may exist with no URI or digest, so neither retrieval nor digest verification is promised.
- **B — Published payload lifecycle:** if ratified, define explicit draft/published states, URI/digest requirements for publication, digest algorithm and canonical encoding, content retrieval/integrity verification, CRS/grid metadata, units, study/harvest authority, and correction semantics. New source schemas and interoperability tests would require a separate approved implementation mission.
- **C — Defer:** continue source-only evidence review without claims of scientific use.

**Maintainer must decide** whether to require published-payload invariants. No status or field is made mandatory by this document.

## Required evidence before any normative change

- Confirm demonstrated use cases and scientific interpretation for an index, a query and a map **separately**; do not conflate their identities.
- Compare with official BrAPI Observation/Image/Location capabilities and documented GenX Geospatial/RemoteSensingMetadata candidates, recording overlap precisely.
- Define authority boundaries for Study, Location, harvest source and raster storage; require negative tests for invalid/foreign references.
- Test geometry parsing, coordinate reference transformations, missing asset/digest behavior, scale/units, access failure and scientific provenance.
- Record accepted decisions in the canonical project decision register **only after explicit maintainer approval**; do not treat this assessment as a new governing decision.

## Non-goals and integration guard

This mission changes **one assessment Markdown file**. It intentionally leaves `SpatialIndex`, `SpatialQuery` and `YieldMap` unreviewed/evidence-deferred; neither registry nor scientific maturity counts change.

Verify that the only diff is this file and the existing conformance/generation checks remain unweakened. The next implementation slice should be gated by the decisions above; independent source-only audits of unrelated modules can proceed without waiting for them.
