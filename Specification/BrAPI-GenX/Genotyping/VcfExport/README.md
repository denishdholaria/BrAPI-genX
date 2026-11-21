# BrAPI-GenX — VCF Export (Genotyping)

VCF export records describe VCF exports.
BrAPI v2.1 has no VCF export record.

- `POST /genx/v1/vcf-exports` (`genxRegisterVcfExport`) registers one
  `VcfExport` (`Schemas/VcfExportNewRequest.yaml`). Same
  `vcfExportDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/vcf-exports` (`genxListVcfExports`) lists records,
  optionally filtered by status.
- `GET /genx/v1/vcf-exports/{vcfExportDbId}`
  (`genxGetVcfExport`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-114-Vcf-Export.md`.
