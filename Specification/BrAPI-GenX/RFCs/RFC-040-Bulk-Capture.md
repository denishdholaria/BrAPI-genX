# RFC-040 — Bulk Capture (Phenotyping)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D4).

## 1. Problem

Official BrAPI v2.1 already accepts an array of ObservationNewRequest
entities through `POST /observations`; it therefore already supports batch
observation submission. This GenX proposal instead describes an *event
record* around an attempted capture, with its own identifier and optional
entry-level metadata. That record does not guarantee atomic creation of
BrAPI Observations, scientific validation, audit completeness or durable
provenance links between the envelope and individual observations.

## 2. Object

`BulkCapture` — one immutable bulk capture record.

## 3. Endpoints

- `GET /genx/v1/bulk-captures` (`genxListBulkCaptures`)
- `POST /genx/v1/bulk-captures` (`genxRecordBulkCapture`)
- `GET /genx/v1/bulk-captures/{bulkCaptureDbId}` (`genxGetBulkCapture`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- `studyDbId` is a required string; `observationUnitDbId` is **optional**
  per entry. Neither property establishes an authority-matched or validated
  reference to a BrAPI Study or ObservationUnit.
- No entry-level `observationDbId` or official `observationVariableDbId`
  mapping is modelled; an event is not a BrAPI Observation.

## 5. Invariants

- A published `bulkCaptureDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional captures linked by `supersedes`.
- `entries` is required, but has no `minItems` and may be **empty**. Each
  entry requires only `variableDbId`; numeric `value`, `unit`,
  `observationUnitDbId` and `qualityFlag` are optional. A quality flag is
  **not** guaranteed to be recorded and no missingness rule is enforced.
- A capture does not imply a complete phenotype dataset, official Observation
  insertion, transactional success, or a validated categorical scale.

## 6. Deferred questions

- D-118: Should `entries` require at least one item? (Current: required
  array, may be empty.)
- D-119: Should bulk captures link to GenX `PhenotypeCapture`? (Current:
  no `phenotypeCaptureDbId` property is modelled.)
- D-120: Should bulk capture require a field-book reference? (Current:
  no `fieldBookDbId` property is modelled.)

## 7. Classification

Primary domain: D4 — Phenotyping and Plant Observations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.