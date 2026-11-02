# BrAPI-GenX — DiseaseResistance

DiseaseResistance records describe DiseaseResistance entries.
BrAPI v2.1 has no DiseaseResistance record.

- `POST /genx/v1/disease-resistances` (`genxRegisterDiseaseResistance`) registers one
  `DiseaseResistance` (`Schemas/DiseaseResistanceNewRequest.yaml`). Same
  `diseaseResistanceDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/disease-resistances` (`genxListDiseaseResistances`) lists records,
  optionally filtered by status.
- `GET /genx/v1/disease-resistances/{diseaseResistanceDbId}`
  (`genxGetDiseaseResistance`) retrieves one record.

Details and falsifiers: `../RFC-127-DiseaseResistance.md`.
