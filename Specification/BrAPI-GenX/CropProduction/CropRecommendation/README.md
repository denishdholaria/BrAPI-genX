# BrAPI-GenX — CropRecommendation

CropRecommendation records describe CropRecommendation entries.
BrAPI v2.1 has no CropRecommendation record.

- `POST /genx/v1/crop-recommendations` (`genxRegisterCropRecommendation`) registers one
  `CropRecommendation` (`Schemas/CropRecommendationNewRequest.yaml`). Same
  `cropRecommendationDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/crop-recommendations` (`genxListCropRecommendations`) lists records,
  optionally filtered by status.
- `GET /genx/v1/crop-recommendations/{cropRecommendationDbId}`
  (`genxGetCropRecommendation`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-129-CropRecommendation.md`.
