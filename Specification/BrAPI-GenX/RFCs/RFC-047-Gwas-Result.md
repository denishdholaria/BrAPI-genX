# RFC-047 — GWAS Result (Scientific Compute)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `../CLASSIFICATION.md` (D7).

## 1. Problem

BrAPI v2.1 has no GWAS result record. Genome-wide association results
need citable identities, method/version binding, and provenance. Without
this record, GWAS results cannot be audited or reproduced.

## 2. Object

`GwasResult` — one immutable GWAS result record.

## 3. Endpoints

- `GET /genx/v1/gwas-results` (`genxListGwasResults`)
- `POST /genx/v1/gwas-results` (`genxRecordGwasResult`)
- `GET /genx/v1/gwas-results/{gwasResultDbId}` (`genxGetGwasResult`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- GWAS results reference GenX AnalysisMethod by identifier; they do not
  duplicate that resource.
- A result is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `gwasResultDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional results linked by `supersedes`.
- `analysisMethodDbId` is required.
- A result does not imply scientific validation or approval.

## 6. Deferred questions

- D-139: Should `significantMarkers` and `topPValue` be required? (Current:
  optional.)
- D-140: Should GWAS results link to GenX `GenomicDataset`? (Current:
  optional, not required.)
- D-141: Should GWAS results require a GenX Job reference? (Current:
  optional.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C6, C9.