# BrAPI-GenX — Pedigree Analysis (Scientific Compute)

Pedigree analysis results record pedigree-derived metrics and provenance.
BrAPI v2.1 has no pedigree analysis result record.

- `POST /genx/v1/pedigree-analyses` (`genxRecordPedigreeAnalysis`) registers one
  `PedigreeAnalysis` (`Schemas/PedigreeAnalysisNewRequest.yaml`). Same
  `pedigreeAnalysisDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/pedigree-analyses` (`genxListPedigreeAnalyses`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/pedigree-analyses/{pedigreeAnalysisDbId}`
  (`genxGetPedigreeAnalysis`) retrieves one result.

Details and falsifiers: `../../RFCs/RFC-060-Pedigree-Analysis.md`.