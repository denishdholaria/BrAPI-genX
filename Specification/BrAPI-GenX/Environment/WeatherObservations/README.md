# BrAPI-GenX — Weather Observations (Environmental Context)

Weather and environmental observations record measured conditions at a station
or location over time, with quality flags and provenance. They provide the
environmental context for trials, studies, and crop models. BrAPI v2.1 has
locations but no weather or environmental observation resource.

- `POST /genx/v1/weather-observations` (`genxRecordWeatherObservation`) records
  one `WeatherObservation` (`Schemas/WeatherObservationNewRequest.yaml`). Same
  `weatherObservationDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/weather-observations` (`genxListWeatherObservations`) lists
  observations, optionally filtered by station, location, variable, or time
  range.
- `GET /genx/v1/weather-observations/{weatherObservationDbId}`
  (`genxGetWeatherObservation`) retrieves one observation.

Details and falsifiers: `../../RFCs/RFC-010-Weather-Observations.md`.