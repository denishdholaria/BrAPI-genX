# BrAPI-GenX — Genotype QC (Genomics)

Genotype QC records report quality control outcomes for a prepared genotyping
dataset. BrAPI v2.1 has no genotype QC report record.

- `POST /genx/v1/genotype-qc-reports` (`genxRecordGenotypeQcReport`) registers one
  `GenotypeQcReport` (`Schemas/GenotypeQcReportNewRequest.yaml`). Same
  `genotypeQcReportDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/genotype-qc-reports` (`genxListGenotypeQcReports`) lists reports,
  optionally filtered by dataset, import, or status.
- `GET /genx/v1/genotype-qc-reports/{genotypeQcReportDbId}`
  (`genxGetGenotypeQcReport`) retrieves one report.

Details and falsifiers: `../../RFCs/RFC-064-Genotype-Qc.md`.
