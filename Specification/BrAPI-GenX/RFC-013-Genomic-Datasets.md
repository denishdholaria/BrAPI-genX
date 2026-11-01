# RFC-013 — Genomic Datasets (Molecular Data Preparation)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-005 (Variant Matrix References), `CLASSIFICATION.md` (D3).

## 1. Problem

BrAPI v2.1 standardizes variants, call sets, calls, references, and external
matrix references, but not the prepared dataset as a whole: its reference
assembly, bioinformatics pipeline provenance, sample/variant counts, access
policy, and release status. Without this record, genomic datasets cannot be
cited, compared, or released with provenance.

## 2. Object

`GenomicDataset` — one immutable prepared genomic dataset record.

## 3. Endpoints

- `GET /genx/v1/genomic-datasets` (`genxListGenomicDatasets`)
- `POST /genx/v1/genomic-datasets` (`genxRegisterGenomicDataset`)
- `GET /genx/v1/genomic-datasets/{genomicDatasetDbId}` (`genxGetGenomicDataset`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Genomic datasets reference BrAPI VariantSet, CallSet, and GenX VariantMatrix
  by identifier; they do not duplicate those resources.
- A genomic dataset is not a VariantSet or VariantMatrix and must not be treated
  as one.

## 5. Invariants

- A published `genomicDatasetDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional datasets linked by `supersedes`.
- `accessPolicy` and `releaseStatus` are recorded, not inferred.
- A dataset does not imply scientific validation or approval.

## 6. Deferred questions

- D-36: Should `pipelineName`/`pipelineVersion` be required for all datasets?
  (Current: optional.)
- D-37: Should `inputDigest`/`outputDigest` be required for released datasets?
  (Current: optional.)
- D-38: Should access policy be governed by a separate authorization contract?
  (Current: recorded as a string; authorization is out of scope here.)

## 7. Classification

Primary domain: D3 — Genotyping and Molecular Genomics.
Cross-cutting: C1, C2, C3 (POST), C5, C6, C9.