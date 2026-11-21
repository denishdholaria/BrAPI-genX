# RFC-043 — VCF Import (Genotyping)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-005 (Variant Matrix References), RFC-013 (Genomic Datasets), `../CLASSIFICATION.md` (D3).

## 1. Problem

BrAPI v2.1 standardizes variants and external matrix references but not the
import of VCF or other variant file formats into a genomic dataset. Without
this record, import provenance and counts cannot be audited or linked to
datasets.

## 2. Object

`VcfImport` — one immutable VCF import record.

## 3. Endpoints

- `GET /genx/v1/vcf-imports` (`genxListVcfImports`)
- `POST /genx/v1/vcf-imports` (`genxRecordVcfImport`)
- `GET /genx/v1/vcf-imports/{vcfImportDbId}` (`genxGetVcfImport`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- VCF imports reference GenX GenomicDataset by identifier; they do not
  duplicate that resource.
- A VCF import is not a BrAPI VariantSet and must not be treated as one.

## 5. Invariants

- A published `vcfImportDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional imports linked by `supersedes`.
- `sourceFormat` and `importedAt` are required.
- An import does not imply a complete genomic repository.

## 6. Deferred questions

- D-127: Should `sourceFile` be required? (Current: optional.)
- D-128: Should VCF imports link to GenX `VariantMatrix`? (Current:
  optional, not required.)
- D-129: Should source format be a governed vocabulary? (Current: free
  string.)

## 7. Classification

Primary domain: D3 — Genotyping and Molecular Genomics.
Cross-cutting: C1, C2, C3 (POST), C5, C6, C9.