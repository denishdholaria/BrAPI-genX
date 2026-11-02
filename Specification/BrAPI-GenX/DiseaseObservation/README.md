# BrAPI-GenX — DiseaseObservation

DiseaseObservation records describe DiseaseObservation entries.
BrAPI v2.1 has no DiseaseObservation record.

- `POST /genx/v1/disease-observations` (`genxRegisterDiseaseObservation`) registers one
  `DiseaseObservation` (`Schemas/DiseaseObservationNewRequest.yaml`). Same
  `diseaseObservationDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/disease-observations` (`genxListDiseaseObservations`) lists records,
  optionally filtered by status.
- `GET /genx/v1/disease-observations/{diseaseObservationDbId}`
  (`genxGetDiseaseObservation`) retrieves one record.

Details and falsifiers: `../RFC-123-DiseaseObservation.md`.
