# BrAPI-GenX — SpatialQuery

SpatialQuery is a **STRUCTURAL_DRAFT**, metadata-only registration candidate.
`queryType`, `queryGeometry`, `queryParams` and `resultReference` are optional;
no query target, execution step or returned-result validity is established.
Mission 090's G-090-2 governance decision is open.

- `POST /genx/v1/spatial-queries` (`genxRegisterSpatialQuery`) registers one
  `SpatialQuery` (`Schemas/SpatialQueryNewRequest.yaml`). Same
  `spatialQueryDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/spatial-queries` (`genxListSpatialQueries`) lists records,
  optionally filtered by status.
- `GET /genx/v1/spatial-queries/{spatialQueryDbId}`
  (`genxGetSpatialQuery`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-143-SpatialQuery.md`.
