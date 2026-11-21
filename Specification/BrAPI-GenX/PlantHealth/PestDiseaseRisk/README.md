# BrAPI-GenX — PestDiseaseRisk

PestDiseaseRisk records describe PestDiseaseRisk entries.
BrAPI v2.1 has no PestDiseaseRisk record.

- `POST /genx/v1/pest-disease-risks` (`genxRegisterPestDiseaseRisk`) registers one
  `PestDiseaseRisk` (`Schemas/PestDiseaseRiskNewRequest.yaml`). Same
  `pestDiseaseRiskDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/pest-disease-risks` (`genxListPestDiseaseRisks`) lists records,
  optionally filtered by status.
- `GET /genx/v1/pest-disease-risks/{pestDiseaseRiskDbId}`
  (`genxGetPestDiseaseRisk`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-133-PestDiseaseRisk.md`.
