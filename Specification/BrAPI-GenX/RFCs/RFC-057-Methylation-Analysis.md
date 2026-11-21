# RFC-057 — Methylation Analysis (Scientific Compute)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `../CLASSIFICATION.md` (D7).

## 1. Problem

BrAPI v2.1 has no methylation analysis result record. Methylation patterns
are essential for epigenetic analysis. Without this record, methylation
results cannot be audited or reproduced.

## 2. Object

`MethylationAnalysis` — one immutable methylation analysis result record.

## 3. Endpoints

- `GET /genx/v1/methylation-analyses` (`genxListMethylationAnalyses`)
- `POST /genx/v1/methylation-analyses` (`genxRecordMethylationAnalysis`)
- `GET /genx/v1/methylation-analyses/{methylationAnalysisDbId}` (`genxGetMethylationAnalysis`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Methylation analyses reference GenX AnalysisMethod by identifier; they do not
  duplicate that resource.
- A result is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `methylationAnalysisDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional results linked by `supersedes`.
- `analysisMethodDbId` is required.
- A result does not imply scientific validation or approval.

## 6. Deferred questions

- D-169: Should `regions` be required? (Current: optional.)
- D-170: Should methylation analyses link to GenX `GenomicDataset`? (Current:
  optional, not required.)
- D-171: Should methylation level be required? (Current: optional.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C6, C9.