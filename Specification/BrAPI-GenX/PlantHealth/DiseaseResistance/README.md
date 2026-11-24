# BrAPI-GenX — DiseaseResistance

DiseaseResistance records describe DiseaseResistance entries.
Official BrAPI v2.1 already exchanges phenotypic disease-resistance measurements through `/brapi/v2/observations` and observation variables. This proposed separate GenX summary is a structural draft, not proof of an absent official measurement capability.

- `POST /genx/v1/disease-resistances` (`genxRegisterDiseaseResistance`) registers one
  `DiseaseResistance` (`Schemas/DiseaseResistanceNewRequest.yaml`). Same
  `diseaseResistanceDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/disease-resistances` (`genxListDiseaseResistances`) lists records,
  optionally filtered by status.
- `GET /genx/v1/disease-resistances/{diseaseResistanceDbId}`
  (`genxGetDiseaseResistance`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-127-DiseaseResistance.md`.
