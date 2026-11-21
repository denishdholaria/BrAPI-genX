# BrAPI-GenX — CrsTransform

CrsTransform records describe CrsTransform entries.
BrAPI v2.1 has no CrsTransform record.

- `POST /genx/v1/crs-transforms` (`genxRegisterCrsTransform`) registers one
  `CrsTransform` (`Schemas/CrsTransformNewRequest.yaml`). Same
  `crsTransformDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/crs-transforms` (`genxListCrsTransforms`) lists records,
  optionally filtered by status.
- `GET /genx/v1/crs-transforms/{crsTransformDbId}`
  (`genxGetCrsTransform`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-140-CrsTransform.md`.
