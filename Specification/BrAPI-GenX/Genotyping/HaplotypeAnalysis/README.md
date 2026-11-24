# BrAPI-GenX — Haplotype Analysis (Scientific Compute)

HaplotypeAnalysis proposes metadata for inferred haplotype blocks, not a
scientifically validated phased genotype result. The `haplotypes` payload,
study, job and provenance are optional; no typed sample identities,
ploidy, phase-confidence or reference assembly are required.

Official BrAPI version 2.1 contracts remain unchanged. A draft result is not
a verified alternate representation of official Variant or Call resources.

- `POST /genx/v1/haplotype-analyses` (`genxRecordHaplotypeAnalysis`) registers one
  `HaplotypeAnalysis` (`Schemas/HaplotypeAnalysisNewRequest.yaml`). Same
  `haplotypeAnalysisDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/haplotype-analyses` (`genxListHaplotypeAnalyses`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/haplotype-analyses/{haplotypeAnalysisDbId}`
  (`genxGetHaplotypeAnalysis`) retrieves one result.

Details and falsifiers: `../../RFCs/RFC-059-Haplotype-Analysis.md`.