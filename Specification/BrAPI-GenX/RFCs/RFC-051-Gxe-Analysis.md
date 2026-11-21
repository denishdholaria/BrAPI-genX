# RFC-051 — GxE Analysis (Scientific Compute)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `../CLASSIFICATION.md` (D7).

## 1. Problem

BrAPI v2.1 has no GxE analysis result record. Genotype-by-environment
interaction is essential for breeding. Without this record, GxE results
cannot be audited or reproduced.

## 2. Object

`GxeAnalysisResult` — one immutable GxE analysis result record.

## 3. Endpoints

- `GET /genx/v1/gxe-analyses` (`genxListGxeAnalyses`)
- `POST /genx/v1/gxe-analyses` (`genxRecordGxeAnalysis`)
- `GET /genx/v1/gxe-analyses/{gxeAnalysisResultDbId}` (`genxGetGxeAnalysis`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- GxE results reference GenX AnalysisMethod by identifier; they do not
  duplicate that resource.
- A result is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `gxeAnalysisResultDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional results linked by `supersedes`.
- `analysisMethodDbId` is required.
- A result does not imply scientific validation or approval.

## 6. Deferred questions

- D-151: Should `gxeEffect` be required? (Current: optional.)
- D-152: Should GxE results link to GenX `GenomicDataset`? (Current:
  optional, not required.)
- D-153: Should GxE results require a GenX Job reference? (Current:
  optional.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C6, C9.