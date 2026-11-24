# RFC-092 — Location Geometry (Reference Data)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

Official BrAPI version 2.1 Location already includes GeoJSON-compatible `coordinates` and coordinate uncertainty. A proposed separate immutable geometry-URI metadata record may address externally stored or versioned geometry, but its distinct identity, authoritative source and retrieval behavior remain unverified.

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
- The candidate `locationDbId` string names a BrAPI Location but does not prove external referential integrity, authorization, geometry consistency, or an independently implemented adapter.
- A location geometry record is not a BrAPI Location and must not be treated as
  one.
- Geometry bytes are not transported by this API. The record optionally names a geometry URI, but defines no required format, checksum, fetch-and-verify operation, or retrieval guarantee.

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
