# RFC-092 — Location Geometry (Reference Data)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record location geometry. Location geometry is
the routine reference for spatial analysis. Without a record, geometries arrive
as unversioned references with no stated location, version, or provenance, so
they cannot be audited or reproduced.

## 2. Object

`LocationGeometry` — one immutable location geometry record, with its location
reference, geometry URI, and provenance.

## 3. Endpoints

- `GET /genx/v1/location-geometries` (`genxListLocationGeometries`)
- `POST /genx/v1/location-geometries` (`genxRegisterLocationGeometry`)
- `GET /genx/v1/location-geometries/{locationGeometryDbId}` (`genxGetLocationGeometry`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Location geometry records reference BrAPI `Location` by identifier; they do
  not duplicate those resources.
- A location geometry record is not a BrAPI Location and must not be treated as
  one.
- Geometry bytes are not transported by this API. The record names and verifies
  the payload; retrieval uses the referenced geometry URI.

## 5. Invariants

- A published `locationGeometryDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the geometry is validated or endorsed.

## 6. Deferred questions

- D-274: Should `locationDbId` be required? (Current: optional.)
- D-275: Should `geometryUri` be required? (Current: optional.)
- D-276: Should the API define a standard geometry format/CRS? (Current: no
  format/CRS field.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
