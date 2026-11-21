# BrAPI-GenX — Weather Forecast (Environment)

Weather forecasts record predicted environmental conditions for a station or
location over a validity window. BrAPI v2.1 has no forecast record.

- `POST /genx/v1/weather-forecasts` (`genxRegisterWeatherForecast`) registers one
  `WeatherForecast` (`Schemas/WeatherForecastNewRequest.yaml`). Same
  `weatherForecastDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/weather-forecasts` (`genxListWeatherForecasts`) lists forecasts,
  optionally filtered by station, location, or validity window.
- `GET /genx/v1/weather-forecasts/{weatherForecastDbId}`
  (`genxGetWeatherForecast`) retrieves one forecast.

Details and falsifiers: `../../RFCs/RFC-031-Weather-Forecast.md`.