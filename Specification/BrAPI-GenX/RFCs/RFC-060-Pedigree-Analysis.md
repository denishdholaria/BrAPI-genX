# RFC-060 — Pedigree Analysis (Scientific Compute)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `../CLASSIFICATION.md` (D7).

## 1. Problem

BrAPI v2.1 has no pedigree analysis result record. Pedigree-derived metrics
are essential for breeding programs. Without this record, pedigree analysis
results cannot be audited or reproduced.

## 2. Object

`PedigreeAnalysis` — one immutable pedigree analysis result record.

## 3. Endpoints

- `GET /genx/v1/pedigree-analyses` (`genxListPedigreeAnalyses`)
- `POST /genx/v1/pedigree-analyses` (`genxRecordPedigreeAnalysis`)
- `GET /genx/v1/pedigree-analyses/{pedigreeAnalysisDbId}` (`genxGetPedigreeAnalysis`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Pedigree analyses reference GenX AnalysisMethod by identifier; they do not
  duplicate that resource.
- A result is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `pedigreeAnalysisDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional results linked by `supersedes`.
- `analysisMethodDbId` is required.
- A result does not imply scientific validation or approval.

## 6. Deferred questions

- D-178: Should `pedigreeMetrics` be required? (Current: optional.)
- D-179: Should pedigree analyses link to GenX `GenomicDataset`? (Current:
  optional, not required.)
- D-180: Should inbreeding coefficient be required? (Current: optional.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C6, C9.