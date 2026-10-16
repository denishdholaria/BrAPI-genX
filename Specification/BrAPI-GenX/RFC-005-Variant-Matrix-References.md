# RFC-005: Variant Matrix References

- Status: **proposal** (not accepted, not normative, grants no implementation authority)
- Builds on: RFC-001 (compatibility law, `409` evidence, reference-not-reinvent)
- Scope: content-addressed references to external allele-matrix files
- Non-scope: matrix slicing/query APIs, byte transport, access control for
  bytes, call-levelInline pagination fixes — slicing belongs to htsget or a
  future RFC

## 1. Problem

V2.1 genotyping paginates `Calls` inline. At biobank scale (hundreds of
thousands of samples × hundreds of millions of variants, hundreds of TiB of
VCF), inline pagination is unusable: row-wise VCF is itself the bottleneck,
and the community is moving to chunked-columnar stores (VCF Zarr, ~5X smaller
in published biobank conversions) served from object stores. BrAPI must stop
pretending matrices fit in `result.data` and instead describe, address, and
verify external matrices — while leaving byte transport and sub-setting to
standards built for it.

External standards (researched 2026-09, cited as references, not vendored):

- GA4GH **htsget** v1.3: ticket-based streaming of reads/variants subsections
  (VCF/BCF/BAM/CRAM) with `service-info` capability advertisement. Slicing
  belongs here.
- GA4GH **DRS** v1.4 (approved Nov 2024): logical ID → byte-retrieval means,
  checksums, access methods. The pattern for `fileURL`/`fileDigest`.
- **VCF Zarr** specification (GigaScience 2025): chunked-columnar VCF
  encoding. A first-class `format` value, not a BrAPI redefinition.

## 2. Object — VariantMatrix

Files: `Genomics/Schemas/VariantMatrix.yaml`,
`Genomics/Schemas/VariantMatrixNewRequest.yaml`,
`Genomics/VariantMatrices_GET_POST.yaml`,
`Genomics/VariantMatrices_MatrixDbId_GET.yaml`.

Purpose: make a matrix a named, verifiable, retrievable fact: what bytes, how
much, in what layout, where to fetch them (including via htsget/DRS), built
from what evidence.

Fields: `matrixDbId` (`{authority}:matrix:{localId}`, required),
`variantSetDbId?` (link into V2.1 genotyping), `format` (`VCF`|`BCF`|
`VCF_ZARR`|`PLINK_BED`|`OTHER`, required), `fileURL` (required —
`https://` or `drs://`), `fileDigest` (SHA-256 hex, required),
`fileSize?` (bytes), `indexURL?` + `indexDigest?`, `sampleCount?`,
`variantCount?`, `referenceDbId?` / `assemblyName?`, `accessService?`
(`{type: htsget|drs|https, endpoint}` — where to stream subsets),
`provenance?` (`ProvenanceEnvelope` — conversion pipeline, source files).

Responsibilities: matrix identity, integrity, coordinates, retrieval means.
Non-responsibilities: byte transport; access control on bytes (the access
service's own auth applies); slicing semantics (htsget); call-level values
(V2.1 `Calls` stays frozen for small-scale use).

Invariants:

1. Bytes are immutable under an id. Same `matrixDbId` + identical body
   replays the existing record. Same id + different `fileDigest` (or any
   other difference) is rejected with `409`. New bytes get a new id —
   clients SHOULD derive ids from digests.
2. `fileURL` is retrievable out of band. `drs://` URLs resolve per GA4GH DRS;
   `accessService` with `type: htsget` points at a ticket endpoint per htsget
   §service-info conventions. GenX defines no new transport.
3. Counts are advisory metadata for planning, not queryable guarantees;
   authoritative dimensions come from the bytes (or the access service).

## 3. Endpoints

- `POST /brapi/v3/variantmatrices` (`genxRegisterVariantMatrixReference`) with `VariantMatrixNewRequest` → `200` + single
  record (create, replay, or `409` conflict with plain-text body).
- `GET /brapi/v3/variantmatrices` (`genxListVariantMatrixReferences`) with `variantSetDbId?`, `format?` filters + standard
  pagination → list of records.
- `GET /brapi/v3/variantmatrices/{matrixDbId}` (`genxGetVariantMatrixReference`) → single record or `404`.

## 4. Hypothesis, falsifier, verification

- Hypothesis: two systems can exchange matrix references such that bytes are
  verifiable before use, subsetting needs are served by htsget, and no client
  needs inline `Calls` pagination for large matrices.
- Falsifier: a mutated `fileDigest` under a published id; an unresolvable
  `fileURL` scheme passing validation; a replay that duplicates a record.
- Verification: static probes S-15/S-16 plus live probes L-16/L-17 in
  `Conformance/probes.yaml` against the reference test server.

## 5. Explicit unknowns and requires-decision

1. `requires decision`: a GenX slice/query API (ranges over variants/samples)
   — deferred; htsget is the current answer.
2. `requires decision`: authorization flows for byte retrieval (DRS
   Passports vs BrAPI bearer) — the access service decides today.
3. `assumption`: `format: OTHER` records are opaque to generic clients;
   format-specific clients negotiate out of band.
4. `unknown`: pangenome graph encodings (beyond VCF-coordinate models) — no
   format value is claimed for them yet.

## 6. File map

```text
Specification/BrAPI-GenX/
  RFC-005-Variant-Matrix-References.md   this document
  Genomics/README.md + GroupDescription.md
    + Schemas/VariantMatrix.yaml + Schemas/VariantMatrixNewRequest.yaml
    + VariantMatrices_GET_POST.yaml + VariantMatrices_MatrixDbId_GET.yaml
```
