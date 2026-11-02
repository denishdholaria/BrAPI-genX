# RFC-078 — Environmental Treatment (Environment)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-042 (Extreme Weather), `CLASSIFICATION.md` (D5).

## 1. Problem

BrAPI v2.1 has no place to record environmental treatments or stress exposures.
These are the routine inputs to stress and climate experiments. Without a
record, treatments arrive as unversioned notes with no stated site, type,
exposure, or provenance, so they cannot be audited or reproduced.

## 2. Object

`EnvironmentalTreatment` — one immutable record of an environmental treatment
or stress exposure for a site, with its type, exposure, and provenance.

## 3. Endpoints

- `GET /genx/v1/environmental-treatments` (`genxListEnvironmentalTreatments`)
- `POST /genx/v1/environmental-treatments` (`genxRegisterEnvironmentalTreatment`)
- `GET /genx/v1/environmental-treatments/{environmentalTreatmentDbId}` (`genxGetEnvironmentalTreatment`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Treatment records reference BrAPI `Location` and GenX `ExtremeWeather` by
  identifier; they do not duplicate those resources.
- A treatment record is not a BrAPI Observation and must not be treated as one.

## 5. Invariants

- A published `environmentalTreatmentDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
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
