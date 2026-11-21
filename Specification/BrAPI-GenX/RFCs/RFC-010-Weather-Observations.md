# RFC-010 — Weather Observations (Environmental Context)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-007 (Telemetry Streams), `../CLASSIFICATION.md` (D5).

## 1. Problem

BrAPI v2.1 standardizes locations but has no resource for weather or
environmental observations. Environmental context is essential for trials,
studies, and crop models, yet it is currently captured only as device telemetry
or left outside the standard entirely. Without a governed record, environmental
data cannot be cited, quality-controlled, or linked to studies with provenance.

## 2. Object

`WeatherObservation` — one environmental/weather observation record.

## 3. Endpoints

- `GET /genx/v1/weather-observations` (`genxListWeatherObservations`)
- `POST /genx/v1/weather-observations` (`genxRecordWeatherObservation`)
- `GET /genx/v1/weather-observations/{weatherObservationDbId}` (`genxGetWeatherObservation`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Weather observations reference BrAPI Location and GenX VariableTerm by
  identifier; they do not duplicate those resources.
- Telemetry remains the device/sensor stream; WeatherObservation is a
  scientific environmental record. They are complementary, not equivalent.

## 5. Invariants

- A published `weatherObservationDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional observations linked by `supersedes`.
- An observation does not imply a BrAPI scientific Observation.
- Quality flags are recorded, not inferred.

## 6. Deferred questions

- D-27: Should `measurements` require at least one BrAPI Observation Variable
  reference? (Current: requires variableDbId per measurement.)
- D-28: Should forecast and climate-normal products be separate objects?
  (Current: only observations.)
- D-29: Should `qualityFlag` be governed by a controlled vocabulary beyond
  the four listed? (Current: four values.)

## 7. Classification

Primary domain: D5 — Environment, Agroecology and Field Context.
Cross-cutting: C1, C2, C3 (POST), C6, C7, C9.