# BrAPI-GenX — Genotype QC (Genomics)

GenotypeQcReport is a candidate quality-control (QC) metadata record alongside
official BrAPI version 2.1 genotype resources. Its optional dataset/import
identifiers and unconstrained metrics object do not establish a validated
CallSet, required quality measurements or an independently verified verdict.

- `POST /genx/v1/genotype-qc-reports` (`genxRecordGenotypeQcReport`) registers one
  `GenotypeQcReport` (`Schemas/GenotypeQcReportNewRequest.yaml`). Same
  `genotypeQcReportDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/genotype-qc-reports` (`genxListGenotypeQcReports`) lists reports,
  optionally filtered by dataset, import, or status.
- `GET /genx/v1/genotype-qc-reports/{genotypeQcReportDbId}`
  (`genxGetGenotypeQcReport`) retrieves one report.

Details and falsifiers: `../../RFCs/RFC-064-Genotype-Qc.md`.
