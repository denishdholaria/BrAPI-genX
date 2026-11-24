# BrAPI-GenX — SpatialIndex

SpatialIndex is a **STRUCTURAL_DRAFT**, metadata-only registration candidate.
An entry does not construct a spatial index, identify an indexed dataset or
serve an executable query. Mission 090's G-090-1 governance decision is open.

- `POST /genx/v1/spatial-indexes` (`genxRegisterSpatialIndex`) registers one
  `SpatialIndex` (`Schemas/SpatialIndexNewRequest.yaml`). Same
  `spatialIndexDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/spatial-indexes` (`genxListSpatialIndexes`) lists records,
  optionally filtered by status.
- `GET /genx/v1/spatial-indexes/{spatialIndexDbId}`
  (`genxGetSpatialIndex`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-141-SpatialIndex.md`.
