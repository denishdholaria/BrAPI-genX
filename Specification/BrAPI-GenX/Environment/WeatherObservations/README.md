# BrAPI-GenX — Weather Observations (Environmental Context)

Weather and environmental observations record measured conditions at a station
or location over time, with quality flags and provenance. They provide the
environmental context for trials, studies and models. Official BrAPI version 2.1 already represents Locations and Observations; the separate GenX weather candidate contains numerical environmental entries and does not prove station identity or scientific quality.

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