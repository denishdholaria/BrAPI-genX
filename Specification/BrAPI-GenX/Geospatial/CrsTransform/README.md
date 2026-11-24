# BrAPI-GenX — CrsTransform

CrsTransform records describe CrsTransform entries.
The GenX candidate only records source/target coordinate reference system strings and optional transform metadata. It is not an executable or accuracy-validated coordinate transformation.

- `POST /genx/v1/crs-transforms` (`genxRegisterCrsTransform`) registers one
  `CrsTransform` (`Schemas/CrsTransformNewRequest.yaml`). Same
  `crsTransformDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/crs-transforms` (`genxListCrsTransforms`) lists records,
  optionally filtered by status.
- `GET /genx/v1/crs-transforms/{crsTransformDbId}`
  (`genxGetCrsTransform`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-140-CrsTransform.md`.
