# RFC-045 — Analysis Result (Scientific Compute)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-004 (Model Registry), RFC-009 (Analysis Methods), `../CLASSIFICATION.md` (D7).

## 1. Problem

BrAPI v2.1 has no analysis result record. Scientific analyses produce
results that need citable identities, method/version binding, and provenance.
Without this record, results cannot be audited or reproduced.

## 2. Object

`AnalysisResult` — one immutable analysis result record.

## 3. Endpoints

- `GET /genx/v1/analysis-results` (`genxListAnalysisResults`)
- `POST /genx/v1/analysis-results` (`genxRecordAnalysisResult`)
- `GET /genx/v1/analysis-results/{analysisResultDbId}` (`genxGetAnalysisResult`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Analysis results reference GenX AnalysisMethod and Job by identifier; they
  do not duplicate those resources.
- A result is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `analysisResultDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional results linked by `supersedes`.
- `analysisMethodDbId` is required.
- A result does not imply scientific validation or approval.

## 6. Deferred questions

- D-133: Should `resultData` be required? (Current: optional.)
- D-134: Should results require a GenX Job reference? (Current: optional.)
- D-135: Should uncertainty be a structured quantity? (Current: object.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C6, C9.