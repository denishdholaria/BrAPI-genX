# BrAPI-GenX — FieldGeometry

FieldGeometry records describe FieldGeometry entries.
BrAPI v2.1 has no FieldGeometry record.

- `POST /genx/v1/field-geometries` (`genxRegisterFieldGeometry`) registers one
  `FieldGeometry` (`Schemas/FieldGeometryNewRequest.yaml`). Same
  `fieldGeometryDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/field-geometries` (`genxListFieldGeometries`) lists records,
  optionally filtered by status.
- `GET /genx/v1/field-geometries/{fieldGeometryDbId}`
  (`genxGetFieldGeometry`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-142-FieldGeometry.md`.
