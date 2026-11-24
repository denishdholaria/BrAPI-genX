# BrAPI-GenX — Location Geometry (Reference Data)

Location geometry records describe geometry references for locations.
Official BrAPI version 2.1 Location already has GeoJSON-compatible coordinates and uncertainty. The GenX draft proposes optional external geometry-URI metadata, without a payload verification mechanism.

- `POST /genx/v1/location-geometries` (`genxRegisterLocationGeometry`) registers one
  `LocationGeometry` (`Schemas/LocationGeometryNewRequest.yaml`). Same
  `locationGeometryDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/location-geometries` (`genxListLocationGeometries`) lists records,
  optionally filtered by status.
- `GET /genx/v1/location-geometries/{locationGeometryDbId}`
  (`genxGetLocationGeometry`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-092-Location-Geometry.md`.
