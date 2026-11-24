# BrAPI-GenX — VCF Export (Genotyping)

VcfExport is a candidate metadata record, not proof that a Variant Call
Format (VCF) file was generated. Official BrAPI version 2.1 already supports
`POST /brapi/v2/variantsets/extract` to create a VariantSet; the GenX record
has no VcfImport, dataset, output-file or digest reference.

- `POST /genx/v1/vcf-exports` (`genxRegisterVcfExport`) registers one
  `VcfExport` (`Schemas/VcfExportNewRequest.yaml`). Same
  `vcfExportDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/vcf-exports` (`genxListVcfExports`) lists records,
  optionally filtered by status.
- `GET /genx/v1/vcf-exports/{vcfExportDbId}`
  (`genxGetVcfExport`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-114-Vcf-Export.md`.
