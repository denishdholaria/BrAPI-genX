# RFC-025 — Repeated Measurement (Phenotyping)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-007 (Telemetry Streams), `../CLASSIFICATION.md` (D4).

## 1. Problem

BrAPI v2.1 standardizes observations but not repeated measurement series or
time-series capture for an observation unit and variable. Without this record,
phenotype monitoring and time-series analysis cannot be audited or reproduced.

## 2. Object

`MeasurementSeries` — one immutable repeated-measurement series record.

## 3. Endpoints

- `GET /genx/v1/repeated-measurements` (`genxListMeasurementSeries`)
- `POST /genx/v1/repeated-measurements` (`genxRecordMeasurementSeries`)
- `GET /genx/v1/repeated-measurements/{measurementSeriesDbId}` (`genxGetMeasurementSeries`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Measurement series reference BrAPI Study, ObservationUnit, and Observation
  Variable by identifier; they do not duplicate those resources.
- A measurement series is not a BrAPI Observation and must not be treated as
  one.

## 5. Invariants

- A published `measurementSeriesDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional series linked by `supersedes`.
- `measurements` are time-ordered; quality flags are recorded, not inferred.
- A series does not imply a complete phenotype dataset.

## 6. Deferred questions

- D-72: Should `measurements` require at least one entry? (Current: required
  array, may be empty.)
- D-73: Should missing values require a `missingReason`? (Current: qualityFlag
  `missing` only.)
- D-74: Should measurement series link to GenX `PhenotypeCapture`? (Current:
  optional, not required.)

## 7. Classification

Primary domain: D4 — Phenotyping and Plant Observations.
Cross-cutting: C1, C2, C3 (POST), C6, C7, C9.