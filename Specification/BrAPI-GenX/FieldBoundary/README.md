# BrAPI-GenX — Field Boundary (Field Agronomy)

Operational field boundary and history records describe boundary versions and
geometry references for a field or site. BrAPI v2.1 has no field boundary record.

- `POST /genx/v1/field-boundaries` (`genxRegisterFieldBoundary`) registers one
  `FieldBoundary` (`Schemas/FieldBoundaryNewRequest.yaml`). Same
  `fieldBoundaryDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/field-boundaries` (`genxListFieldBoundaries`) lists records,
  optionally filtered by field or status.
- `GET /genx/v1/field-boundaries/{fieldBoundaryDbId}`
  (`genxGetFieldBoundary`) retrieves one record.

Details and falsifiers: `../RFC-075-Field-Boundary.md`.
