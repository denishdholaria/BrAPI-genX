# BrAPI-GenX — Environmental Treatment (Environment)

Environmental treatment and stress exposure records describe treatments or
stress applied to a site. BrAPI v2.1 has no environmental treatment record.

- `POST /genx/v1/environmental-treatments` (`genxRegisterEnvironmentalTreatment`) registers one
  `EnvironmentalTreatment` (`Schemas/EnvironmentalTreatmentNewRequest.yaml`). Same
  `environmentalTreatmentDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/environmental-treatments` (`genxListEnvironmentalTreatments`) lists records,
  optionally filtered by site or status.
- `GET /genx/v1/environmental-treatments/{environmentalTreatmentDbId}`
  (`genxGetEnvironmentalTreatment`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-078-Environmental-Treatment.md`.
