# RFC-141 — Spatial Index (M)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (M).

## 1. Problem

BrAPI v2.1 has no place to record spatial indexes. Spatial indexes
circulate without a stated index type, coverage area, or provenance, so they
cannot be used for spatial queries.

## 2. Object

`SpatialIndex` — one immutable spatial index record, with its index type,
name, coverage area, resolution, and provenance.

## 3. Endpoints

- `GET /genx/v1/spatial-indexes` (`genxListSpatialIndexes`)
- `POST /genx/v1/spatial-indexes` (`genxRegisterSpatialIndex`)
- `GET /genx/v1/spatial-indexes/{spatialIndexDbId}` (`genxGetSpatialIndex`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `spatialIndexDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-421: Should `resolution` be required? (Current: optional.)
- D-422: Should `indexType` be a controlled vocabulary? (Current: free-form string.)
- D-423: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting M).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
