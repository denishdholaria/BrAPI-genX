# RFC-140 — CRS Transform (M)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (M).

## 1. Problem

BrAPI v2.1 has no place to record CRS transforms. CRS transformations
circulate without a stated source/target CRS, method, or provenance, so they
cannot be audited or reproduced.

## 2. Object

`CrsTransform` — one immutable CRS transform record, with its source CRS,
target CRS, method, parameters, and provenance.

## 3. Endpoints

- `GET /genx/v1/crs-transforms` (`genxListCrsTransforms`)
- `POST /genx/v1/crs-transforms` (`genxRegisterCrsTransform`)
- `GET /genx/v1/crs-transforms/{crsTransformDbId}` (`genxGetCrsTransform`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `crsTransformDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-418: Should `parameters` be required? (Current: optional.)
- D-419: Should `transformMethod` be a controlled vocabulary? (Current: free-form string.)
- D-420: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting M).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
