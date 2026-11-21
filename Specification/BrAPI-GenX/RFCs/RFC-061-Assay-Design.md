# RFC-061 — Assay Design (Genomics)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `../CLASSIFICATION.md` (D3).

## 1. Problem

BrAPI v2.1 has no assay design record. Assay designs are essential for
genotyping workflows. Without this record, assay designs cannot be audited
or reproduced.

## 2. Object

`AssayDesign` — one immutable assay design record.

## 3. Endpoints

- `GET /genx/v1/assay-designs` (`genxListAssayDesigns`)
- `POST /genx/v1/assay-designs` (`genxRecordAssayDesign`)
- `GET /genx/v1/assay-designs/{assayDesignDbId}` (`genxGetAssayDesign`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Assay designs reference GenX AnalysisMethod by identifier when applicable;
  they do not duplicate that resource.
- A design is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `assayDesignDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional designs linked by `supersedes`.
- A design does not imply scientific validation or approval.

## 6. Deferred questions

- D-181: Should `platform` be required? (Current: optional.)
- D-182: Should assay designs link to GenX `GenomicDataset`? (Current:
  optional, not required.)
- D-183: Should marker count be required? (Current: optional.)

## 7. Classification

Primary domain: D3 — Genotyping and Molecular Genomics.
Cross-cutting: C1, C2, C3 (POST), C6, C9.