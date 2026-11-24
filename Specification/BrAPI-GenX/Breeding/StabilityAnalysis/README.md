# BrAPI-GenX — Stability Analysis (Scientific Compute)

StabilityAnalysisResult proposes analysis metadata for genotype performance
stability across environments, not a verified adaptability or stability
conclusion. The `stabilityIndex`, trait, study, job and provenance are
optional; the index is a bare number without a specified estimation method,
orientation, range, environmental design or uncertainty.

Official BrAPI version 2.1 data resources are unchanged. Method identity alone
does not establish an applied model version or comparable stability measure.

- `POST /genx/v1/stability-analyses` (`genxRecordStabilityAnalysis`) registers one
  `StabilityAnalysisResult` (`Schemas/StabilityAnalysisResultNewRequest.yaml`). Same
  `stabilityAnalysisResultDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/stability-analyses` (`genxListStabilityAnalyses`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/stability-analyses/{stabilityAnalysisResultDbId}`
  (`genxGetStabilityAnalysis`) retrieves one result.

Details and falsifiers: `../../RFCs/RFC-049-Stability-Analysis.md`.