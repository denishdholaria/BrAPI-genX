# RFC-012 — Phenotype Capture (Observation Workflow)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (D4).

## 1. Problem

BrAPI v2.1 standardizes observations and observation units but not the capture
workflow: how observations were entered, quality flags, missingness reasons,
corrections, and image linkage. Without this record, phenotype data cannot be
audited for capture quality or corrected with provenance.

## 2. Object

`PhenotypeCapture` — one immutable phenotype capture record.

## 3. Endpoints

- `GET /genx/v1/phenotype-captures` (`genxListPhenotypeCaptures`)
- `POST /genx/v1/phenotype-captures` (`genxRecordPhenotypeCapture`)
- `GET /genx/v1/phenotype-captures/{phenotypeCaptureDbId}` (`genxGetPhenotypeCapture`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Phenotype captures reference BrAPI Study, ObservationUnit, and Image by
  identifier; they do not duplicate those resources.
- A capture is not a BrAPI Observation and must not be treated as one.

## 5. Invariants

- A published `phenotypeCaptureDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional captures linked by `supersedes`.
- Missing values require a `missingReason` when `qualityFlag` is `missing`.
- Quality flags are recorded, not inferred.

## 6. Deferred questions

- D-33: Should `entries` require at least one BrAPI Observation Variable
  reference? (Current: requires variableDbId per entry.)
- D-34: Should repeated measurements/time series be a separate object?
  (Current: each capture is one event; time series is a sequence of captures.)
- D-35: Should bulk capture require a field-book reference? (Current: optional.)

## 7. Classification

Primary domain: D4 — Phenotyping and Plant Observations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.