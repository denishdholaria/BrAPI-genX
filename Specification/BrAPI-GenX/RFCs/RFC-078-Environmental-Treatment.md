# RFC-078 — Environmental Treatment (Environment)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-042 (Extreme Weather), `../CLASSIFICATION.md` (D5).

## 1. Problem

BrAPI v2.1 has no place to record environmental treatments or stress exposures.
Environmental stress trials require measured or defined treatment conditions,
site and experimental-unit identity, time interval, comparisons, methods and
provenance. The current candidate only requires its identifier; type,
exposure and site are optional strings and do not establish a reproducible
or independently validated treatment.

## 2. Object

`EnvironmentalTreatment` — proposed immutable treatment metadata. Site,
treatment type, exposure and provenance remain optional.

## 3. Endpoints

- `GET /genx/v1/environmental-treatments` (`genxListEnvironmentalTreatments`)
- `POST /genx/v1/environmental-treatments` (`genxRegisterEnvironmentalTreatment`)
- `GET /genx/v1/environmental-treatments/{environmentalTreatmentDbId}` (`genxGetEnvironmentalTreatment`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- `siteDbId` is an optional string rather than an authority-verified BrAPI
  Location link. No `extremeWeatherEventDbId` or other typed ExtremeWeather
  reference exists in the current model.
- A treatment record is not a BrAPI Observation and must not be treated as one.

## 5. Invariants

- A published `environmentalTreatmentDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- `exposure` is free text without schema-enforced dose, unit, duration,
  baseline, intervention confirmation or a link to observational outcomes.
- A record does not imply that the treatment was validated or effective.

## 6. Deferred questions

- D-232: Should `siteDbId` be required? (Current: optional.)
- D-233: Should `exposure` be a structured object rather than free text?
  (Current: free text.)
- D-234: Should treatment type be a controlled GenX terminology? (Current:
  free-form string.)

## 7. Classification

Primary domain: D5 — Environment, Soil, Weather, and Climate.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
