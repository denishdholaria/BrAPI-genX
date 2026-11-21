# BrAPI-GenX — Haplotype Analysis (Scientific Compute)

Haplotype analysis results record haplotype blocks and provenance.
BrAPI v2.1 has no haplotype analysis result record.

- `POST /genx/v1/haplotype-analyses` (`genxRecordHaplotypeAnalysis`) registers one
  `HaplotypeAnalysis` (`Schemas/HaplotypeAnalysisNewRequest.yaml`). Same
  `haplotypeAnalysisDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/haplotype-analyses` (`genxListHaplotypeAnalyses`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/haplotype-analyses/{haplotypeAnalysisDbId}`
  (`genxGetHaplotypeAnalysis`) retrieves one result.

Details and falsifiers: `../../RFCs/RFC-059-Haplotype-Analysis.md`.