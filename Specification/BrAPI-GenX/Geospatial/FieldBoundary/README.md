# BrAPI-GenX — Field Boundary (Field Agronomy)

Operational field boundary and history records describe boundary versions and
geometry references for a field or site. Official BrAPI version 2.1 Locations already carry GeoJSON coordinates. This GenX candidate proposes operational boundary history, but an optional URI without checksum or format is not a verified geometry payload.

- `POST /genx/v1/field-boundaries` (`genxRegisterFieldBoundary`) registers one
  `FieldBoundary` (`Schemas/FieldBoundaryNewRequest.yaml`). Same
  `fieldBoundaryDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/field-boundaries` (`genxListFieldBoundaries`) lists records,
  optionally filtered by field or status.
- `GET /genx/v1/field-boundaries/{fieldBoundaryDbId}`
  (`genxGetFieldBoundary`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-075-Field-Boundary.md`.
