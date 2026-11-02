# BrAPI-GenX — SpatialIndex

SpatialIndex records describe SpatialIndex entries.
BrAPI v2.1 has no SpatialIndex record.

- `POST /genx/v1/spatial-indexes` (`genxRegisterSpatialIndex`) registers one
  `SpatialIndex` (`Schemas/SpatialIndexNewRequest.yaml`). Same
  `spatialIndexDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/spatial-indexes` (`genxListSpatialIndexes`) lists records,
  optionally filtered by status.
- `GET /genx/v1/spatial-indexes/{spatialIndexDbId}`
  (`genxGetSpatialIndex`) retrieves one record.

Details and falsifiers: `../RFC-141-SpatialIndex.md`.
