# BrAPI-GenX — Common Crop Name (Reference Data)

Common crop name entries describe common names for crops.
BrAPI v2.1 has no common crop name record.

- `POST /genx/v1/common-crop-names` (`genxRegisterCommonCropName`) registers one
  `CommonCropName` (`Schemas/CommonCropNameNewRequest.yaml`). Same
  `commonCropNameDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/common-crop-names` (`genxListCommonCropNames`) lists entries,
  optionally filtered by status.
- `GET /genx/v1/common-crop-names/{commonCropNameDbId}`
  (`genxGetCommonCropName`) retrieves one entry.

Details and falsifiers: `../../RFCs/RFC-094-Common-Crop-Name.md`.
