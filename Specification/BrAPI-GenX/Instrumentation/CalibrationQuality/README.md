# BrAPI-GenX — CalibrationQuality

CalibrationQuality records describe CalibrationQuality entries.
BrAPI v2.1 has no CalibrationQuality record.

- `POST /genx/v1/calibration-qualities` (`genxRegisterCalibrationQuality`) registers one
  `CalibrationQuality` (`Schemas/CalibrationQualityNewRequest.yaml`). Same
  `calibrationQualityDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/calibration-qualities` (`genxListCalibrationQualitys`) lists records,
  optionally filtered by status.
- `GET /genx/v1/calibration-qualities/{calibrationQualityDbId}`
  (`genxGetCalibrationQuality`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-150-CalibrationQuality.md`.
