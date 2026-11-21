# BrAPI-GenX — YieldForecast

YieldForecast records describe YieldForecast entries.
BrAPI v2.1 has no YieldForecast record.

- `POST /genx/v1/yield-forecasts` (`genxRegisterYieldForecast`) registers one
  `YieldForecast` (`Schemas/YieldForecastNewRequest.yaml`). Same
  `yieldForecastDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/yield-forecasts` (`genxListYieldForecasts`) lists records,
  optionally filtered by status.
- `GET /genx/v1/yield-forecasts/{yieldForecastDbId}`
  (`genxGetYieldForecast`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-134-YieldForecast.md`.
