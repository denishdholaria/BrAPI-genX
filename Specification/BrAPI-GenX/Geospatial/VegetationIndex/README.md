# BrAPI-GenX — VegetationIndex

VegetationIndex records describe VegetationIndex entries.
BrAPI v2.1 has no VegetationIndex record.

- `POST /genx/v1/vegetation-index` (`genxRegisterVegetationIndex`) registers one
  `VegetationIndex` (`Schemas/VegetationIndexNewRequest.yaml`). Same
  `vegetationIndexDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/vegetation-index` (`genxListVegetationIndex`) lists records,
  optionally filtered by status.
- `GET /genx/v1/vegetation-index/{vegetationIndexDbId}`
  (`genxGetVegetationIndex`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-146-VegetationIndex.md`.
