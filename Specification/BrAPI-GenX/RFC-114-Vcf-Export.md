# RFC-114 — VCF Export (Genotyping)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-043 (VCF Import), `CLASSIFICATION.md` (D3).

## 1. Problem

BrAPI v2.1 has no place to record VCF exports. VCF exports are the routine
reference for genotyping. Without a record, exports arrive as unversioned
files with no stated format or provenance, so they cannot be audited or
reproduced.

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
- VCF export records reference GenX `VcfImport` by identifier; they do not
  duplicate those resources.
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
