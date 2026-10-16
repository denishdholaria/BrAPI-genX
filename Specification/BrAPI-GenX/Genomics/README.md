# BrAPI GenX — Variant Matrix References

Content-addressed references to external allele-matrix files. BrAPI names,
verifies, and links matrices; bytes move through DRS/htsget/HTTPS, and
sub-setting belongs to htsget — not to paginated `Calls`.

- `POST /brapi/v3/variantmatrices` (`genxRegisterVariantMatrixReference`) registers a `VariantMatrix`
  (`Schemas/VariantMatrixNewRequest.yaml`). Same `matrixDbId` + identical
  body replays; same id + different bytes (`fileDigest`) is rejected with
  `409`. New bytes get a new id.
- `GET /brapi/v3/variantmatrices` (`genxListVariantMatrixReferences`) lists records; `GET /brapi/v3/variantmatrices/{matrixDbId}` (`genxGetVariantMatrixReference`) retrieves one record.

V2.1 `Calls`/`Variants` stay frozen for small-scale use. Details and
falsifiers: `../RFC-005-Variant-Matrix-References.md`.
