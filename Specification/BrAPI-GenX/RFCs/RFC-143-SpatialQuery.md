# RFC-143 — Spatial Query (M)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (M).

## 1. Problem

BrAPI v2.1 has no dedicated saved-spatial-query metadata registry. This
candidate records optional descriptive query fields, but does not define
execution, dataset authority, query validation or a verifiable result. Its
registration alone cannot establish a reproducible or auditable spatial query.

## 2. Object

`SpatialQuery` — one proposed immutable metadata record. Its query type,
geometry, parameters, result reference and provenance are optional; `queryParams`
is a string and `queryGeometry` is an unconstrained object, despite their examples.
The record does not execute a query or validate a spatial result.

## 3. Endpoints

- `GET /genx/v1/spatial-queries` (`genxListSpatialQueries`)
- `POST /genx/v1/spatial-queries` (`genxRegisterSpatialQuery`)
- `GET /genx/v1/spatial-queries/{spatialQueryDbId}` (`genxGetSpatialQuery`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `spatialQueryDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-427: Should `queryParams` be required? (Current: optional.)
- D-428: Should `queryType` be a controlled vocabulary? (Current: free-form string.)
- D-429: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting M).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
