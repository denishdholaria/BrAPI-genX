# RFC-049 — Stability Analysis (Scientific Compute)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `../CLASSIFICATION.md` (D7).

## 1. Problem

BrAPI v2.1 has no stability analysis result record. Stability and
adaptability across environments are essential for breeding. Without this
record, stability results cannot be audited or reproduced.

## 2. Object

`StabilityAnalysisResult` — one immutable stability analysis result record.

## 3. Endpoints

- `GET /genx/v1/stability-analyses` (`genxListStabilityAnalyses`)
- `POST /genx/v1/stability-analyses` (`genxRecordStabilityAnalysis`)
- `GET /genx/v1/stability-analyses/{stabilityAnalysisResultDbId}` (`genxGetStabilityAnalysis`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Stability results reference GenX AnalysisMethod by identifier; they do
  not duplicate that resource.
- A result is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `stabilityAnalysisResultDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional results linked by `supersedes`.
- `analysisMethodDbId` is required.
- A result does not imply scientific validation or approval.

## 6. Deferred questions

- D-145: Should `stabilityIndex` be required? (Current: optional.)
- D-146: Should stability results link to GenX `GenomicDataset`? (Current:
  optional, not required.)
- D-147: Should stability index be a structured quantity? (Current: number.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C6, C9.