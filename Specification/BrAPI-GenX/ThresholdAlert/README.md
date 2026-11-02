# BrAPI-GenX — ThresholdAlert

ThresholdAlert records describe ThresholdAlert entries.
BrAPI v2.1 has no ThresholdAlert record.

- `POST /genx/v1/threshold-alerts` (`genxRegisterThresholdAlert`) registers one
  `ThresholdAlert` (`Schemas/ThresholdAlertNewRequest.yaml`). Same
  `thresholdAlertDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/threshold-alerts` (`genxListThresholdAlerts`) lists records,
  optionally filtered by status.
- `GET /genx/v1/threshold-alerts/{thresholdAlertDbId}`
  (`genxGetThresholdAlert`) retrieves one record.

Details and falsifiers: `../RFC-126-ThresholdAlert.md`.
