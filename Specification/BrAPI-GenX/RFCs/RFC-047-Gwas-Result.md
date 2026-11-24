# RFC-047 — GWAS Result (Scientific Compute)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `../CLASSIFICATION.md` (D7).

## 1. Problem

The GenX proposal provides a separately identified genome-wide association
study (GWAS) result record alongside official BrAPI v2.1 data resources.
Citable identity, exact method-version binding, population context,
multiple-testing policy, and provenance are important for interpreting
association evidence; the current candidate does not require all of them.
A registered result is not, by itself, scientifically reproducible.

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
- `analysisMethodDbId` is required as a string reference but the result
  does not require `methodVersion` or verify authority-matched method
  resolution. A named method is not evidence of execution.
- A result is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `gwasResultDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional results linked by `supersedes`.
- `analysisMethodDbId` is required; an exact method version, job reference,
  study context and provenance are not required by the result schema.
- `significantMarkers` and `topPValue` are optional, with no required
  significance threshold, multiple-testing correction, or calibrated
  interpretation; `resultData` is an opaque optional object.
- A result does not imply scientific validation, approval, causality,
  cross-study comparability or independent reproducibility.

## 6. Deferred questions

- D-139: Should `significantMarkers` and `topPValue` be required? (Current:
  optional.)
- D-140: Should GWAS results link to GenX `GenomicDataset`? (Current:
  no `genomicDatasetDbId` field is modelled in the `GwasResult` schema.)
- D-141: Should GWAS results require a GenX Job reference? (Current:
  optional.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C6, C9.