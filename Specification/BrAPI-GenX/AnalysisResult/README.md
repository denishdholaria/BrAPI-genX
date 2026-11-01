# BrAPI-GenX — Analysis Result (Scientific Compute)

Analysis results record the output of a scientific analysis, bound to a method
and job, with provenance and uncertainty. BrAPI v2.1 has no analysis result
record.

- `POST /genx/v1/analysis-results` (`genxRecordAnalysisResult`) registers one
  `AnalysisResult` (`Schemas/AnalysisResultNewRequest.yaml`). Same
  `analysisResultDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/analysis-results` (`genxListAnalysisResults`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/analysis-results/{analysisResultDbId}`
  (`genxGetAnalysisResult`) retrieves one result.

Details and falsifiers: `../RFC-045-Analysis-Result.md`.