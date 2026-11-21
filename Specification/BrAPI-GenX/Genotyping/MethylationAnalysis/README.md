# BrAPI-GenX — Methylation Analysis (Scientific Compute)

Methylation analysis results record methylation patterns and provenance.
BrAPI v2.1 has no methylation analysis result record.

- `POST /genx/v1/methylation-analyses` (`genxRecordMethylationAnalysis`) registers one
  `MethylationAnalysis` (`Schemas/MethylationAnalysisNewRequest.yaml`). Same
  `methylationAnalysisDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/methylation-analyses` (`genxListMethylationAnalyses`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/methylation-analyses/{methylationAnalysisDbId}`
  (`genxGetMethylationAnalysis`) retrieves one result.

Details and falsifiers: `../../RFCs/RFC-057-Methylation-Analysis.md`.