# RFC-059 — Haplotype Analysis (Scientific Compute)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `../CLASSIFICATION.md` (D7).

## 1. Problem

GenX proposes a separate record for haplotype-block metadata alongside
official BrAPI version 2.1 genotype resources. Meaningful inference requires
reference assembly, sample identities, ploidy, phased allele representation,
coordinate rules and inference confidence. This candidate does not require
those concepts and does not itself establish comparable, reproducible phase.

## 2. Object

`HaplotypeAnalysis` — one immutable haplotype analysis result record.

## 3. Endpoints

- `GET /genx/v1/haplotype-analyses` (`genxListHaplotypeAnalyses`)
- `POST /genx/v1/haplotype-analyses` (`genxRecordHaplotypeAnalysis`)
- `GET /genx/v1/haplotype-analyses/{haplotypeAnalysisDbId}` (`genxGetHaplotypeAnalysis`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- `analysisMethodDbId` is a required string reference, not a verified exact
  method version, genotype-source join, or proof of phasing execution.
- A result is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `haplotypeAnalysisDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional results linked by `supersedes`.
- `analysisMethodDbId` is required, while `haplotypes`, `jobDbId`,
  `studyDbId`, and provenance are optional.
- The `haplotypes` object is unconstrained, with no required sample identity,
  phasing confidence, allele encodings, reference coordinates or block length.
- A registered record does not establish valid phase, completeness,
  reproducibility or scientific approval.

## 6. Deferred questions

- D-175: Should `haplotypes` be required? (Current: optional.)
- D-176: Should haplotype analyses link to GenX `GenomicDataset`? (Current:
  no `genomicDatasetDbId` property is modelled.)
- D-177: Should haplotype length be required? (Current: no dedicated
  haplotype-length field is modelled; `haplotypes` is opaque.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C6, C9.