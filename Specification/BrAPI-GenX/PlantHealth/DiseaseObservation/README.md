# BrAPI-GenX — DiseaseObservation

DiseaseObservation records describe DiseaseObservation entries.
Official BrAPI v2.1 already exchanges phenotypic observations through `/brapi/v2/observations`, potentially including disease symptoms and severity. This separate GenX event record is only a structural draft; the case for a distinct identity and mapping remains unresolved.

- `POST /genx/v1/disease-observations` (`genxRegisterDiseaseObservation`) registers one
  `DiseaseObservation` (`Schemas/DiseaseObservationNewRequest.yaml`). Same
  `diseaseObservationDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/disease-observations` (`genxListDiseaseObservations`) lists records,
  optionally filtered by status.
- `GET /genx/v1/disease-observations/{diseaseObservationDbId}`
  (`genxGetDiseaseObservation`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-123-DiseaseObservation.md`.
