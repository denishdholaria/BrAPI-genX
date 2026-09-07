# BrAPI GenX — Variant Matrix References

Content-addressed references to external allele-matrix files. BrAPI names,
verifies, and links matrices; bytes move through DRS/htsget/HTTPS, and
sub-setting belongs to htsget — not to paginated `Calls`.

- `POST /variantmatrices` registers a `VariantMatrix`
  (`Schemas/VariantMatrixNewRequest.yaml`). Same `matrixDbId` + identical
  body replays; same id + different bytes (`fileDigest`) is rejected with
  `409`. New bytes get a new id.
- `GET /variantmatrices`, `GET /variantmatrices/{matrixDbId}` read records.

V2.1 `Calls`/`Variants` stay frozen for small-scale use. Details and
falsifiers: `../RFC-005-Variant-Matrix-References.md`.
