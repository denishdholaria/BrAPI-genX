# RFC-051 — GxE Analysis (Scientific Compute)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `../CLASSIFICATION.md` (D7).

## 1. Problem

Genotype-by-environment (GxE) results require a defined genotype population,
environment design, trait, statistical model and uncertainty interpretation to
support cross-study comparison. This GenX candidate proposes a separately
identified analysis-result record alongside official BrAPI version 2.1
resources, but does not require those inputs or prove reproducibility.

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
- `analysisMethodDbId` is a required string reference, not an enforced join
  to an exact AnalysisMethod version or proof of method execution.
- A result is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `gxeAnalysisResultDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional results linked by `supersedes`.
- `analysisMethodDbId` is required, but `gxeEffect`, `studyDbId`, `traitDbId`,
  `jobDbId` and provenance are optional.
- `gxeEffect` is an unconstrained object without required genotype or
  environment identity, interaction estimand, inferential uncertainty,
  statistical test, or multiple-testing rule.
- A result does not imply a validated interaction, statistical significance,
  scientific approval or cross-environment comparability.

## 6. Deferred questions

- D-151: Should `gxeEffect` be required? (Current: optional.)
- D-152: Should GxE results link to GenX `GenomicDataset`? (Current:
  no `genomicDatasetDbId` field is modelled in this schema.)
- D-153: Should GxE results require a GenX Job reference? (Current:
  optional.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C6, C9.