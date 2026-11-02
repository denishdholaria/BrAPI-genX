# BrAPI-GenX — TelemetryNormalization

TelemetryNormalization records describe TelemetryNormalization entries.
BrAPI v2.1 has no TelemetryNormalization record.

- `POST /genx/v1/telemetry-normalizations` (`genxRegisterTelemetryNormalization`) registers one
  `TelemetryNormalization` (`Schemas/TelemetryNormalizationNewRequest.yaml`). Same
  `telemetryNormalizationDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/telemetry-normalizations` (`genxListTelemetryNormalizations`) lists records,
  optionally filtered by status.
- `GET /genx/v1/telemetry-normalizations/{telemetryNormalizationDbId}`
  (`genxGetTelemetryNormalization`) retrieves one record.

Details and falsifiers: `../RFC-148-TelemetryNormalization.md`.
