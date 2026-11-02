# RFC-064 — Genotype QC (Genomics)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-013 (Genomic Datasets), RFC-043 (VCF Import), `CLASSIFICATION.md` (D3).

## 1. Problem

BrAPI v2.1 standardizes variants, call sets, and calls but has no place to
record the quality control outcome of a genotyping run. Call rate, missingness,
heterozygosity, duplicate rate, and the thresholds applied are exactly the
evidence a reviewer needs to decide whether a call set is usable. Without a QC
record, the same dataset can be re-released with different quality claims and no
audit trail.

## 2. Object

`GenotypeQcReport` — one immutable record of QC metrics and the thresholds
applied to a prepared genotyping dataset.

## 3. Endpoints

- `GET /genx/v1/genotype-qc-reports` (`genxListGenotypeQcReports`)
- `POST /genx/v1/genotype-qc-reports` (`genxRecordGenotypeQcReport`)
- `GET /genx/v1/genotype-qc-reports/{genotypeQcReportDbId}` (`genxGetGenotypeQcReport`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- QC reports reference GenX `GenomicDataset` and `VcfImport` by identifier; they
  do not duplicate those resources.
- A QC report is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `genotypeQcReportDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional reports linked by `supersedes`.
- `metrics` is opaque to the transport; the metric vocabulary and pass/fail
  interpretation are governed by the referenced method and provenance.
- A report does not imply that a dataset passed, was released, or is scientifically
  valid. Pass/fail policy is separate evidence.

## 6. Deferred questions

- D-190: Should `genomicDatasetDbId` be required? (Current: optional, so a report
  can be attached to a bare import.)
- D-191: Should pass/fail verdict be a first-class field rather than derived from
  `metrics`? (Current: no verdict field.)
- D-192: Should the QC metric vocabulary be a controlled GenX terminology instead
  of a free-form object? (Current: free-form object.)

## 7. Classification

Primary domain: D3 — Genotyping and Molecular Genomics.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
