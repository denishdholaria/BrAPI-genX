# RFC-048 — Mixed Model (Scientific Compute)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `../CLASSIFICATION.md` (D7).

## 1. Problem

BrAPI v2.1 has no mixed model result record. Variance components and BLUPs
are essential for breeding value estimation. Without this record, mixed model
results cannot be audited or reproduced.

## 2. Object

`MixedModelResult` — one immutable mixed model result record.

## 3. Endpoints

- `GET /genx/v1/mixed-model-results` (`genxListMixedModelResults`)
- `POST /genx/v1/mixed-model-results` (`genxRecordMixedModelResult`)
- `GET /genx/v1/mixed-model-results/{mixedModelResultDbId}` (`genxGetMixedModelResult`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Mixed model results reference GenX AnalysisMethod by identifier; they do
  not duplicate that resource.
- A result is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `mixedModelResultDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional results linked by `supersedes`.
- `analysisMethodDbId` is required.
- A result does not imply scientific validation or approval.

## 6. Deferred questions

- D-142: Should `varianceComponents` be required? (Current: optional.)
- D-143: Should mixed model results link to GenX `GenomicDataset`?
  (Current: optional, not required.)
- D-144: Should BLUP values be a structured array? (Current: object.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C6, C9.