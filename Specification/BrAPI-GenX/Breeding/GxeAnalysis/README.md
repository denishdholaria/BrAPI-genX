# BrAPI-GenX — GxE Analysis (Scientific Compute)

GxeAnalysisResult proposes metadata for genotype-by-environment (GxE)
analysis, not independently verified genotype-response interactions. Its
`gxeEffect`, `traitDbId`, `studyDbId`, job reference and provenance are
optional. The effect is an unconstrained object, without prescribed genotype
or environment identities, model, test statistic or inferential uncertainty.

Official BrAPI version 2.1 resources remain unchanged. A recorded candidate
does not establish statistical significance or cross-environment comparability.

- `POST /genx/v1/gxe-analyses` (`genxRecordGxeAnalysis`) registers one
  `GxeAnalysisResult` (`Schemas/GxeAnalysisResultNewRequest.yaml`). Same
  `gxeAnalysisResultDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/gxe-analyses` (`genxListGxeAnalyses`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/gxe-analyses/{gxeAnalysisResultDbId}`
  (`genxGetGxeAnalysis`) retrieves one result.

Details and falsifiers: `../../RFCs/RFC-051-Gxe-Analysis.md`.