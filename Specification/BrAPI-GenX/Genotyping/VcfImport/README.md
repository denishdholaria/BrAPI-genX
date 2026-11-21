# BrAPI-GenX — VCF Import (Genotyping)

VCF import records capture the ingestion of VCF or other variant file formats
into a genomic dataset. BrAPI v2.1 has variants but no import record.

- `POST /genx/v1/vcf-imports` (`genxRecordVcfImport`) registers one
  `VcfImport` (`Schemas/VcfImportNewRequest.yaml`). Same
  `vcfImportDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/vcf-imports` (`genxListVcfImports`) lists imports,
  optionally filtered by dataset or status.
- `GET /genx/v1/vcf-imports/{vcfImportDbId}`
  (`genxGetVcfImport`) retrieves one import.

Details and falsifiers: `../../RFCs/RFC-043-Vcf-Import.md`.