# RFC-040 — Bulk Capture (Phenotyping)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D4).

## 1. Problem

BrAPI v2.1 standardizes observations but not bulk capture events. Batch
capture of observations is common in field phenotyping. Without this record,
bulk capture cannot be audited or linked to studies with provenance.

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
- Bulk captures reference BrAPI Study and ObservationUnit by identifier; they
  do not duplicate those resources.
- A bulk capture is not a BrAPI Observation and must not be treated as one.

## 5. Invariants

- A published `bulkCaptureDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional captures linked by `supersedes`.
- `entries` is required; quality flags are recorded, not inferred.
- A capture does not imply a complete phenotype dataset.

## 6. Deferred questions

- D-118: Should `entries` require at least one item? (Current: required
  array, may be empty.)
- D-119: Should bulk captures link to GenX `PhenotypeCapture`? (Current:
  optional, not required.)
- D-120: Should bulk capture require a field-book reference? (Current:
  optional, not required.)

## 7. Classification

Primary domain: D4 — Phenotyping and Plant Observations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.