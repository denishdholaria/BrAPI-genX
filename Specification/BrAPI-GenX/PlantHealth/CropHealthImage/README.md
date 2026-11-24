# BrAPI-GenX — CropHealthImage

CropHealthImage records describe CropHealthImage entries.
Official BrAPI v2.1 already provides image metadata and image-content operations through `/brapi/v2/images`. This GenX crop-health classification entry is only a proposed metadata record and currently has no image reference or content identifier.

- `POST /genx/v1/crop-health-images` (`genxRegisterCropHealthImage`) registers one
  `CropHealthImage` (`Schemas/CropHealthImageNewRequest.yaml`). Same
  `cropHealthImageDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/crop-health-images` (`genxListCropHealthImages`) lists records,
  optionally filtered by status.
- `GET /genx/v1/crop-health-images/{cropHealthImageDbId}`
  (`genxGetCropHealthImage`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-128-CropHealthImage.md`.
