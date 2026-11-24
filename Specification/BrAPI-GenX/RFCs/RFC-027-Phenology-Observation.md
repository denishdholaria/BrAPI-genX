# RFC-027 — Phenology Observation (Phenotyping)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D4).

## 1. Problem

BrAPI version 2.1 standardizes Observation and ObservationVariable
resources that can represent phenology values. GenX proposes a separate
stage-event identity with required observation time and free-text stage;
it does not replace a BrAPI Observation or automatically establish a
controlled developmental-stage vocabulary, interoperable scale, or
independently validated field observation.

## 2. Object

`PhenologyObservation` — one immutable phenology observation record.

## 3. Endpoints

- `GET /genx/v1/phenology-observations` (`genxListPhenologyObservations`)
- `POST /genx/v1/phenology-observations` (`genxRecordPhenologyObservation`)
- `GET /genx/v1/phenology-observations/{phenologyObservationDbId}` (`genxGetPhenologyObservation`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- `studyDbId` and `observationUnitDbId` are required string references,
  but their existence, authority, ownership and association are not
  enforced by the candidate schema. They do not duplicate BrAPI resources.
- A phenology observation is not a BrAPI Observation and must not be treated
  as one.

## 5. Invariants

- A published `phenologyObservationDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional observations linked by `supersedes`.
- `stage`, `studyDbId`, `observationUnitDbId`, and `observedAt` are
  required with record identity; `bbchCode` and provenance are optional.
- `stage` is free text and `bbchCode` has no enforced crop-specific
  vocabulary or observed-stage scale definition.
- A recorded event does not prove field-observer calibration,
  comparable developmental stage or a complete phenotype dataset.

## 6. Deferred questions

- D-78: Should `bbchCode` be required for flowering stages? (Current:
  optional.)
- D-79: Should phenology observations link to GenX `MeasurementSeries`?
  (Current: no `measurementSeriesDbId` field is modelled.)
- D-80: Should stage be a governed vocabulary? (Current: free string.)

## 7. Classification

Primary domain: D4 — Phenotyping and Plant Observations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.