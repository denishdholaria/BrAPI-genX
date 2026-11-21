# BrAPI-GenX — Crop Cycle (Crop Production)

Crop cycles record the planting-to-harvest cycle for a location or study.
BrAPI v2.1 has locations and studies but no crop cycle record.

- `POST /genx/v1/crop-cycles` (`genxRegisterCropCycle`) registers one
  `CropCycle` (`Schemas/CropCycleNewRequest.yaml`). Same
  `cropCycleDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/crop-cycles` (`genxListCropCycles`) lists cycles,
  optionally filtered by location, study, or status.
- `GET /genx/v1/crop-cycles/{cropCycleDbId}`
  (`genxGetCropCycle`) retrieves one cycle.

Details and falsifiers: `../../RFCs/RFC-029-Crop-Cycle.md`.