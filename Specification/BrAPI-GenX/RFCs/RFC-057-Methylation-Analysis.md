# RFC-057 — Methylation Analysis (Scientific Compute)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `../CLASSIFICATION.md` (D7).

## 1. Problem

GenX proposes a separate DNA (Deoxyribonucleic Acid) methylation analysis
metadata record alongside official BrAPI version 2.1 resources. Scientific
interpretation depends on sample and tissue identity, assay method, cytosine
context, reference coordinates, coverage and calibrated measurements. The
candidate does not require these, so registration is not proof of valid
epigenetic inference.

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
- `analysisMethodDbId` is a required identifier string, but an exact method
  version and independently verified assay execution are not required.
- A result is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `methylationAnalysisDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional results linked by `supersedes`.
- `analysisMethodDbId` is required; `regions`, `jobDbId`,
  `studyDbId` and provenance are optional.
- `regions` is an unconstrained object with no enforced cytosine context,
  sample identity, coverage, coordinate convention, units or confidence.
- A result does not imply scientific approval, reproducible differential
  methylation, calibration or biological function.

## 6. Deferred questions

- D-169: Should `regions` be required? (Current: optional.)
- D-170: Should methylation analyses link to GenX `GenomicDataset`? (Current:
  no `genomicDatasetDbId` field is modelled.)
- D-171: Should methylation level be required? (Current: no first-class
  methylation-level field is modelled; the `regions` object is opaque.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C6, C9.