# RFC-134 — Yield Forecast (O)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (O).

## 1. Problem

BrAPI v2.1 has no place to record yield forecasts. Yield forecasts
circulate without a stated forecast type, value, date, or provenance, so
they cannot be used for planning or advisory decisions.

## 2. Object

`YieldForecast` — one immutable yield forecast record, with its forecast
type, value, date, horizon, and provenance.

## 3. Endpoints

- `GET /genx/v1/yield-forecasts` (`genxListYieldForecasts`)
- `POST /genx/v1/yield-forecasts` (`genxRegisterYieldForecast`)
- `GET /genx/v1/yield-forecasts/{yieldForecastDbId}` (`genxGetYieldForecast`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `yieldForecastDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-400: Should `forecastValue` be required? (Current: optional.)
- D-401: Should `forecastType` be a controlled vocabulary? (Current: free-form string.)
- D-402: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting O).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
