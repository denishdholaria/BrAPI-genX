# BrAPI-GenX — Pedigree Analysis (Scientific Compute)

PedigreeAnalysis proposes a record for pedigree-derived analysis metadata,
not a validated estimate of inbreeding or kinship. The pedigreeMetrics
object, provenance and analysis Job are optional, and no parentage pedigree
completeness, ancestor-depth, or estimator constraints are required.

This result does not replace authoritative BrAPI version 2.1 Germplasm
identities or establish equivalence to genomic relatedness matrices.

- `POST /genx/v1/pedigree-analyses` (`genxRecordPedigreeAnalysis`) registers one
  `PedigreeAnalysis` (`Schemas/PedigreeAnalysisNewRequest.yaml`). Same
  `pedigreeAnalysisDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/pedigree-analyses` (`genxListPedigreeAnalyses`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/pedigree-analyses/{pedigreeAnalysisDbId}`
  (`genxGetPedigreeAnalysis`) retrieves one result.

Details and falsifiers: `../../RFCs/RFC-060-Pedigree-Analysis.md`.