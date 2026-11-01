# BrAPI-GenX — GxE Analysis (Scientific Compute)

GxE analysis results record genotype-by-environment interaction effects.
BrAPI v2.1 has no GxE analysis record.

- `POST /genx/v1/gxe-analyses` (`genxRecordGxeAnalysis`) registers one
  `GxeAnalysisResult` (`Schemas/GxeAnalysisResultNewRequest.yaml`). Same
  `gxeAnalysisResultDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/gxe-analyses` (`genxListGxeAnalyses`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/gxe-analyses/{gxeAnalysisResultDbId}`
  (`genxGetGxeAnalysis`) retrieves one result.

Details and falsifiers: `../RFC-051-Gxe-Analysis.md`.