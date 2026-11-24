# RFC-141 — Spatial Index (M)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (M).

## 1. Problem

BrAPI v2.1 has no dedicated spatial-index metadata registry. This optional
candidate records descriptive metadata; spatial indexes can be built and used
by database or geospatial systems without a GenX metadata record. Registration
here does **not** build an index, bind one to a dataset, or permit a query.

## 2. Object

`SpatialIndex` — one proposed immutable descriptive record. The index type,
name, coverage area, resolution and provenance are all optional. A record is
not a physical index, search plan or executable spatial service.

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
