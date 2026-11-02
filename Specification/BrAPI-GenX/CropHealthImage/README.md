# BrAPI-GenX — CropHealthImage

CropHealthImage records describe CropHealthImage entries.
BrAPI v2.1 has no CropHealthImage record.

- `POST /genx/v1/crop-health-images` (`genxRegisterCropHealthImage`) registers one
  `CropHealthImage` (`Schemas/CropHealthImageNewRequest.yaml`). Same
  `cropHealthImageDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/crop-health-images` (`genxListCropHealthImages`) lists records,
  optionally filtered by status.
- `GET /genx/v1/crop-health-images/{cropHealthImageDbId}`
  (`genxGetCropHealthImage`) retrieves one record.

Details and falsifiers: `../RFC-128-CropHealthImage.md`.
