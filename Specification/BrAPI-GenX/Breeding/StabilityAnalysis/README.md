# BrAPI-GenX — Stability Analysis (Scientific Compute)

Stability analysis results record genotype stability and adaptability across
environments. BrAPI v2.1 has no stability analysis record.

- `POST /genx/v1/stability-analyses` (`genxRecordStabilityAnalysis`) registers one
  `StabilityAnalysisResult` (`Schemas/StabilityAnalysisResultNewRequest.yaml`). Same
  `stabilityAnalysisResultDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/stability-analyses` (`genxListStabilityAnalyses`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/stability-analyses/{stabilityAnalysisResultDbId}`
  (`genxGetStabilityAnalysis`) retrieves one result.

Details and falsifiers: `../../RFCs/RFC-049-Stability-Analysis.md`.