# RFC-050 — Heritability (Scientific Compute)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `CLASSIFICATION.md` (D7).

## 1. Problem

BrAPI v2.1 has no heritability estimate record. Heritability is essential
for breeding value estimation. Without this record, heritability estimates
cannot be audited or reproduced.

## 2. Object

`HeritabilityEstimate` — one immutable heritability estimate record.

## 3. Endpoints

- `GET /genx/v1/heritability-estimates` (`genxListHeritabilityEstimates`)
- `POST /genx/v1/heritability-estimates` (`genxRecordHeritability`)
- `GET /genx/v1/heritability-estimates/{heritabilityEstimateDbId}` (`genxGetHeritabilityEstimate`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Heritability estimates reference GenX AnalysisMethod by identifier; they
  do not duplicate that resource.
- An estimate is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `heritabilityEstimateDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional estimates linked by `supersedes`.
- `analysisMethodDbId` is required.
- An estimate does not imply scientific validation or approval.

## 6. Deferred questions

- D-148: Should `heritabilityValue` be required? (Current: optional.)
- D-149: Should heritability estimates link to GenX `GenomicDataset`?
  (Current: optional, not required.)
- D-150: Should heritability be a structured quantity? (Current: number.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C6, C9.