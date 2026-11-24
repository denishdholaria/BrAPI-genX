# RFC-054 — Genomic Prediction (Scientific Compute)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `../CLASSIFICATION.md` (D7).

## 1. Problem

GenX proposes separately identified genomic prediction results alongside
official BrAPI v2.1 records. Predicted breeding values require defined
training and target populations, trait scale, models and independent
validation to establish interpretability and portability. The current
candidate does not require all such evidence, and registration alone does
not establish reproducibility.

## 2. Object

`GenomicPrediction` — one immutable genomic prediction result record.

## 3. Endpoints

- `GET /genx/v1/genomic-predictions` (`genxListGenomicPredictions`)
- `POST /genx/v1/genomic-predictions` (`genxRecordGenomicPrediction`)
- `GET /genx/v1/genomic-predictions/{genomicPredictionDbId}` (`genxGetGenomicPrediction`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- `analysisMethodDbId` is a required string reference, but the record does
  not require a matching `methodVersion`, verified method ownership or
  evidence that the method was executed.
- A result is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `genomicPredictionDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional results linked by `supersedes`.
- `analysisMethodDbId` is required; `predictions`, `accuracy`, `studyDbId`,
  `traitDbId`, `jobDbId`, and provenance remain optional.
- The `predictions` object is unconstrained. The numeric `accuracy` has no
  enforced range, estimation method, holdout/cross-validation design, or
  independence evidence.
- A result does not imply valid GEBVs, population transferability, scientific
  validation, breeding approval or independent reproducibility.

## 6. Deferred questions

- D-160: Should `predictions` be required? (Current: optional.)
- D-161: Should genomic predictions link to GenX `GenomicDataset`? (Current:
  no `genomicDatasetDbId` property is modelled.)
- D-162: Should accuracy be required? (Current: optional.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C6, C9.