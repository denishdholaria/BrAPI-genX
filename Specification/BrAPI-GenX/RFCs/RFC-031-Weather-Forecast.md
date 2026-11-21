# RFC-031 — Weather Forecast (Environment)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-007 (Telemetry Streams), `../CLASSIFICATION.md` (D5).

## 1. Problem

BrAPI v2.1 has no weather forecast record. Predicted environmental
conditions are essential for crop models and agronomy. Without this record,
forecasts cannot be cited or linked to studies with provenance.

## 2. Object

`WeatherForecast` — one immutable weather forecast record.

## 3. Endpoints

- `GET /genx/v1/weather-forecasts` (`genxListWeatherForecasts`)
- `POST /genx/v1/weather-forecasts` (`genxRegisterWeatherForecast`)
- `GET /genx/v1/weather-forecasts/{weatherForecastDbId}` (`genxGetWeatherForecast`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Weather forecasts reference BrAPI Location by identifier; they do not
  duplicate that resource.
- A forecast is not a BrAPI Location and must not be treated as one.

## 5. Invariants

- A published `weatherForecastDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional forecasts linked by `supersedes`.
- `validFrom`, `validTo`, and `measurements` are required.
- A forecast does not imply a complete climate record.

## 6. Deferred questions

- D-90: Should `measurements` require at least one entry? (Current: required
  array, may be empty.)
- D-91: Should forecasts link to GenX `WeatherObservation`? (Current:
  optional, not required.)
- D-92: Should source be a governed vocabulary? (Current: free string.)

## 7. Classification

Primary domain: D5 — Environment, Agroecology and Field Context.
Cross-cutting: C1, C2, C3 (POST), C6, C7, C9.