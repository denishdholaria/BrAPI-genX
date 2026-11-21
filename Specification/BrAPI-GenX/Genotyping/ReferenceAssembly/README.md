# BrAPI-GenX — Reference Assembly (Genotyping)

Reference assembly records describe reference genome assemblies.
BrAPI v2.1 has no reference assembly record.

- `POST /genx/v1/reference-assemblies` (`genxRegisterReferenceAssembly`) registers one
  `ReferenceAssembly` (`Schemas/ReferenceAssemblyNewRequest.yaml`). Same
  `referenceAssemblyDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/reference-assemblies` (`genxListReferenceAssemblies`) lists records,
  optionally filtered by status.
- `GET /genx/v1/reference-assemblies/{referenceAssemblyDbId}`
  (`genxGetReferenceAssembly`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-115-Reference-Assembly.md`.