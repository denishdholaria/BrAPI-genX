# RFC-060 — Pedigree Analysis (Scientific Compute)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `../CLASSIFICATION.md` (D7).

## 1. Problem

GenX proposes separately identified pedigree-analysis metadata alongside
official BrAPI version 2.1 Germplasm resources. Pedigree-derived inference
requires source parentage, pedigree completeness, population assumptions
and a defined estimator. An unconstrained metrics object alone does not
validate ancestry, inbreeding or reproducibility.

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
- `analysisMethodDbId` is required as a string reference but does not
  establish exact version binding, pedigree-source validation, or execution.
- A result is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `pedigreeAnalysisDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional results linked by `supersedes`.
- `analysisMethodDbId` is required; `pedigreeMetrics`, `jobDbId`,
  `studyDbId` and provenance are optional.
- No required parentage set, pedigree depth/completeness or inbreeding
  estimator and uncertainty are defined; `pedigreeMetrics` is an opaque object.
- An analysis record does not establish pedigree correctness, equivalence
  to genomic relatedness, scientific approval or reproducibility.

## 6. Deferred questions

- D-178: Should `pedigreeMetrics` be required? (Current: optional.)
- D-179: Should pedigree analyses link to GenX `GenomicDataset`? (Current:
  no `genomicDatasetDbId` field is modelled.)
- D-180: Should inbreeding coefficient be required? (Current: optional.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C6, C9.