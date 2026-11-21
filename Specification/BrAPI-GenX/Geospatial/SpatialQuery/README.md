# BrAPI-GenX — SpatialQuery

SpatialQuery records describe SpatialQuery entries.
BrAPI v2.1 has no SpatialQuery record.

- `POST /genx/v1/spatial-queries` (`genxRegisterSpatialQuery`) registers one
  `SpatialQuery` (`Schemas/SpatialQueryNewRequest.yaml`). Same
  `spatialQueryDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/spatial-queries` (`genxListSpatialQueries`) lists records,
  optionally filtered by status.
- `GET /genx/v1/spatial-queries/{spatialQueryDbId}`
  (`genxGetSpatialQuery`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-143-SpatialQuery.md`.
