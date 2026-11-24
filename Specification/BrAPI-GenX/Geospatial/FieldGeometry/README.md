# BrAPI-GenX — FieldGeometry

FieldGeometry records describe FieldGeometry entries.
Official BrAPI version 2.1 Locations already carry GeoJSON coordinates; this separate candidate field geometry has no typed Location or field identity and does not validate its free-form geometry object.

- `POST /genx/v1/field-geometries` (`genxRegisterFieldGeometry`) registers one
  `FieldGeometry` (`Schemas/FieldGeometryNewRequest.yaml`). Same
  `fieldGeometryDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/field-geometries` (`genxListFieldGeometries`) lists records,
  optionally filtered by status.
- `GET /genx/v1/field-geometries/{fieldGeometryDbId}`
  (`genxGetFieldGeometry`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-142-FieldGeometry.md`.
