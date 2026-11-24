# RFC-050 — Heritability (Scientific Compute)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `../CLASSIFICATION.md` (D7).

## 1. Problem

The GenX proposal introduces a separately identified statistical heritability
estimate alongside official BrAPI version 2.1 records. Interpretation depends
on population, sampling design, chosen estimand, variance components and
method/version assumptions. The present candidate does not require all of
these and therefore does not alone establish an auditable or reproducible
heritability analysis.

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
- `analysisMethodDbId` is a required string reference, not a required exact
  `methodVersion` or independently verified, authority-matched method join.
- An estimate is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `heritabilityEstimateDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional estimates linked by `supersedes`.
- `analysisMethodDbId` is required, but `heritabilityValue`, `traitDbId`,
  `studyDbId`, `jobDbId` and provenance are optional.
- The numeric `heritabilityValue` has no enforced heritability estimand,
  variance-decomposition model, uncertainty interval, or interpretation range.
- An estimate does not imply scientific validation, comparable genetic
  parameters, breeding-value accuracy or independent reproducibility.

## 6. Deferred questions

- D-148: Should `heritabilityValue` be required? (Current: optional.)
- D-149: Should heritability estimates link to GenX `GenomicDataset`?
  (Current: `genomicDatasetDbId` is not modelled in this schema.)
- D-150: Should heritability be a structured quantity? (Current: number.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C6, C9.