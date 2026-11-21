# BrAPI-GenX — Measurement Scale (Terminology)

Measurement scale and value domain entries describe scales and allowed values.
BrAPI v2.1 has no measurement scale record.

- `POST /genx/v1/measurement-scales` (`genxRegisterMeasurementScale`) registers one
  `MeasurementScale` (`Schemas/MeasurementScaleNewRequest.yaml`). Same
  `measurementScaleDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/measurement-scales` (`genxListMeasurementScales`) lists entries,
  optionally filtered by status.
- `GET /genx/v1/measurement-scales/{measurementScaleDbId}`
  (`genxGetMeasurementScale`) retrieves one entry.

Details and falsifiers: `../../RFCs/RFC-087-Measurement-Scale.md`.
