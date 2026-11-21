# BrAPI-GenX — Repeated Measurement (Phenotyping)

Repeated measurement series record time-series observations for an observation
unit and variable, with quality flags. BrAPI v2.1 has observations but no
time-series capture record.

- `POST /genx/v1/repeated-measurements` (`genxRecordMeasurementSeries`) records one
  `MeasurementSeries` (`Schemas/MeasurementSeriesNewRequest.yaml`). Same
  `measurementSeriesDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/repeated-measurements` (`genxListMeasurementSeries`) lists series,
  optionally filtered by study, observation unit, or variable.
- `GET /genx/v1/repeated-measurements/{measurementSeriesDbId}`
  (`genxGetMeasurementSeries`) retrieves one series.

Details and falsifiers: `../../RFCs/RFC-025-Repeated-Measurement.md`.