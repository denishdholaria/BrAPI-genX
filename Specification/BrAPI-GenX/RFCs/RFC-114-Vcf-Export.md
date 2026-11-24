# RFC-114 — VCF Export (Genotyping)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-043 (VCF Import), `../CLASSIFICATION.md` (D3).

## 1. Problem

BrAPI v2.1 provides genotype retrieval and `POST /brapi/v2/variantsets/extract`
to create a VariantSet from selected Calls; this is not itself a verified
Variant Call Format (VCF) file export. The candidate metadata register does
not identify an export source, file, digest or VCF version. Its additional
interoperability value and file semantics require evidence.

## 2. Object

`VcfExport` — one immutable VCF export record, with its format and provenance.

## 3. Endpoints

- `GET /genx/v1/vcf-exports` (`genxListVcfExports`)
- `POST /genx/v1/vcf-exports` (`genxRegisterVcfExport`)
- `GET /genx/v1/vcf-exports/{vcfExportDbId}` (`genxGetVcfExport`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- The current schema has no `vcfImportDbId`, `genomicDatasetDbId`,
  `variantSetDbId`, output-file locator or content digest; no typed
  import/dataset/VariantSet relationship is present and registration is
  not evidence that a VCF file was generated.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `vcfExportDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the export is validated or endorsed.

## 6. Deferred questions

- D-340: Should `format` be required? (Current: optional.)
- D-341: Should `format` be a controlled vocabulary? (Current: free-form
  string.)
- D-342: Should records link to GenX `GenomicDataset`? (Current: no link.)

## 7. Classification

Primary domain: D3 — Genotyping and Molecular Genomics.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
