# BrAPI-GenX — Methylation Analysis (Scientific Compute)

MethylationAnalysis proposes metadata for DNA (Deoxyribonucleic Acid)
methylation patterns, not an independently validated epigenetic assay.
The `regions` object, study, job and provenance are optional, and no
methylation-context, coordinate, coverage or measurement-scale semantics
are enforced.

Official BrAPI version 2.1 contracts remain unchanged. The example `level`
value within an opaque object is not a required calibrated result.

- `POST /genx/v1/methylation-analyses` (`genxRecordMethylationAnalysis`) registers one
  `MethylationAnalysis` (`Schemas/MethylationAnalysisNewRequest.yaml`). Same
  `methylationAnalysisDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/methylation-analyses` (`genxListMethylationAnalyses`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/methylation-analyses/{methylationAnalysisDbId}`
  (`genxGetMethylationAnalysis`) retrieves one result.

Details and falsifiers: `../../RFCs/RFC-057-Methylation-Analysis.md`.