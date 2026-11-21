# RFC-027 — Phenology Observation (Phenotyping)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D4).

## 1. Problem

BrAPI v2.1 standardizes observations but not phenology-specific records:
developmental stage, BBCH code, and timing. Without this record, phenology
monitoring cannot be audited or linked to studies with provenance.

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
- Phenology observations reference BrAPI Study and ObservationUnit by
  identifier; they do not duplicate those resources.
- A phenology observation is not a BrAPI Observation and must not be treated
  as one.

## 5. Invariants

- A published `phenologyObservationDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional observations linked by `supersedes`.
- `stage` is required; `bbchCode` is optional.
- An observation does not imply a complete phenotype dataset.

## 6. Deferred questions

- D-78: Should `bbchCode` be required for flowering stages? (Current:
  optional.)
- D-79: Should phenology observations link to GenX `MeasurementSeries`?
  (Current: optional, not required.)
- D-80: Should stage be a governed vocabulary? (Current: free string.)

## 7. Classification

Primary domain: D4 — Phenotyping and Plant Observations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.