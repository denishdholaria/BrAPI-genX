# RFC-042 — Extreme Weather (Environment)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D5).

## 1. Problem

GenX proposes a separate extreme-weather **event report** alongside official
BrAPI version 2.1 Location resources. A named event type and timestamp do
not themselves establish measured weather extremity, statistical rarity,
crop damage or legal warning status. The draft does not require instrument
measurements, climatological thresholds, source station, uncertainty or
independently verified provenance.

## 2. Object

`ExtremeWeatherEvent` — one immutable extreme weather event record.

## 3. Endpoints

- `GET /genx/v1/extreme-weather-events` (`genxListExtremeWeatherEvents`)
- `POST /genx/v1/extreme-weather-events` (`genxRecordExtremeWeather`)
- `GET /genx/v1/extreme-weather-events/{extremeWeatherEventDbId}` (`genxGetExtremeWeatherEvent`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- `locationDbId` is a mandatory plain string rather than a validated,
  authority-matched official BrAPI Location join. The record does not
  duplicate the official Location resource.
- An event is not a BrAPI Location and must not be treated as one.

## 5. Invariants

- A published `extremeWeatherEventDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional events linked by `supersedes`.
- `extremeWeatherEventDbId`, `locationDbId`, `eventType` and
  `occurredAt` are required for registration.
- `eventType` is free text; `severity` is optional and uses broad
  qualitative labels with no mandatory magnitude or meteorological threshold.
- An event does not imply validated weather extremes, causal crop impact,
  official warning, or a complete climate record.

## 6. Deferred questions

- D-124: Should `severity` be required? (Current: optional.)
- D-125: Should extreme weather events link to GenX `WeatherObservation`?
  (Current: no `weatherObservationDbId` field is modelled.)
- D-126: Should event type be a governed vocabulary? (Current: free
  string.)

## 7. Classification

Primary domain: D5 — Environment, Agroecology and Field Context.
Cross-cutting: C1, C2, C3 (POST), C6, C9.