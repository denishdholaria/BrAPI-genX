# BrAPI-GenX — Extreme Weather (Environment)

ExtremeWeatherEvent proposes metadata about a reported extreme-weather
event, not a calibrated meteorological warning or independently verified
crop-impact estimate. Location, event time and free-text event type are
required; severity and provenance are optional.

No measured meteorological threshold, climatological baseline, observation
station or authoritative location join is required. Official BrAPI version
2.1 location resources remain unchanged.

- `POST /genx/v1/extreme-weather-events` (`genxRecordExtremeWeather`) registers one
  `ExtremeWeatherEvent` (`Schemas/ExtremeWeatherEventNewRequest.yaml`). Same
  `extremeWeatherEventDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/extreme-weather-events` (`genxListExtremeWeatherEvents`) lists events,
  optionally filtered by location, type, or severity.
- `GET /genx/v1/extreme-weather-events/{extremeWeatherEventDbId}`
  (`genxGetExtremeWeatherEvent`) retrieves one event.

Details and falsifiers: `../../RFCs/RFC-042-Extreme-Weather.md`.