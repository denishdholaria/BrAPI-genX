# BrAPI-GenX — Common Crop Name (Reference Data)

Common crop name entries describe common names for crops.
Official BrAPI v2.1 already offers `GET /brapi/v2/commoncropnames` for
advertised crop names. This GenX proposal describes a distinct candidate
metadata record and does not replace the official call or infer compatible
crop-name authority.

- `POST /genx/v1/common-crop-names` (`genxRegisterCommonCropName`) registers one
  `CommonCropName` (`Schemas/CommonCropNameNewRequest.yaml`). Same
  `commonCropNameDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/common-crop-names` (`genxListCommonCropNames`) lists entries,
  optionally filtered by status.
- `GET /genx/v1/common-crop-names/{commonCropNameDbId}`
  (`genxGetCommonCropName`) retrieves one entry.

Details and falsifiers: `../../RFCs/RFC-094-Common-Crop-Name.md`.
