# RFC-142 — Field Geometry (M)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (M).

## 1. Problem

Official BrAPI version 2.1 Location already provides GeoJSON-compatible coordinates. This separate field-geometry metadata candidate may cover operational polygons, but its schema currently has no `fieldDbId` or typed BrAPI Location reference and cannot by itself establish field ownership or spatial identity.

## 2. Object

`FieldGeometry` — one immutable field geometry record, with its geometry type,
geometry, CRS, area, and provenance.

## 3. Endpoints

- `GET /genx/v1/field-geometries` (`genxListFieldGeometries`)
- `POST /genx/v1/field-geometries` (`genxRegisterFieldGeometry`)
- `GET /genx/v1/field-geometries/{fieldGeometryDbId}` (`genxGetFieldGeometry`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.
- There is no typed GenX `ResearchAsset` link in the candidate schema; D-426 remains open.

## 5. Invariants

- A published `fieldGeometryDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-424: Should `area` be required? (Current: optional.)
- D-425: Should `geometryType` be a controlled vocabulary? (Current: free-form string.)
- D-426: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting M).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
