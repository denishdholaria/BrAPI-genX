# BrAPI-GenX — Reference Assembly (Genotyping)

Reference assembly records describe reference genome assemblies.
Official BrAPI version 2.1 already has `ReferenceSet` and `Reference` resources representing reference genome assemblies. This distinct GenX candidate has no typed mapping to an official ReferenceSet or GenX GenomicDataset.

- `POST /genx/v1/reference-assemblies` (`genxRegisterReferenceAssembly`) registers one
  `ReferenceAssembly` (`Schemas/ReferenceAssemblyNewRequest.yaml`). Same
  `referenceAssemblyDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/reference-assemblies` (`genxListReferenceAssemblies`) lists records,
  optionally filtered by status.
- `GET /genx/v1/reference-assemblies/{referenceAssemblyDbId}`
  (`genxGetReferenceAssembly`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-115-Reference-Assembly.md`.