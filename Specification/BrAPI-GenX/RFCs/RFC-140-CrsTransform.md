# RFC-140 — CRS Transform (M)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (M).

## 1. Problem

Spatial coordinate transformations require explicit source and target coordinate reference systems, executable transformation parameters and error/accuracy considerations. The proposed GenX `CrsTransform` record is only optional metadata: neither a transformation function nor validation of actual geometry coordinates follows from recording a method string.

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
- There is no typed GenX `ResearchAsset` link in the candidate schema; D-420 remains open.

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
