# BrAPI-GenX — Extreme Weather (Environment)

Extreme weather records capture severe weather events affecting a location.
BrAPI v2.1 has no extreme weather record.

- `POST /genx/v1/extreme-weather-events` (`genxRecordExtremeWeather`) registers one
  `ExtremeWeatherEvent` (`Schemas/ExtremeWeatherEventNewRequest.yaml`). Same
  `extremeWeatherEventDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/extreme-weather-events` (`genxListExtremeWeatherEvents`) lists events,
  optionally filtered by location, type, or severity.
- `GET /genx/v1/extreme-weather-events/{extremeWeatherEventDbId}`
  (`genxGetExtremeWeatherEvent`) retrieves one event.

Details and falsifiers: `../../RFCs/RFC-042-Extreme-Weather.md`.