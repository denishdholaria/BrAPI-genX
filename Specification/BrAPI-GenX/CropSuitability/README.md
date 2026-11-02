# BrAPI-GenX — CropSuitability

CropSuitability records describe CropSuitability entries.
BrAPI v2.1 has no CropSuitability record.

- `POST /genx/v1/crop-suitabilities` (`genxRegisterCropSuitability`) registers one
  `CropSuitability` (`Schemas/CropSuitabilityNewRequest.yaml`). Same
  `cropSuitabilityDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/crop-suitabilities` (`genxListCropSuitabilities`) lists records,
  optionally filtered by status.
- `GET /genx/v1/crop-suitabilities/{cropSuitabilityDbId}`
  (`genxGetCropSuitability`) retrieves one record.

Details and falsifiers: `../RFC-135-CropSuitability.md`.
