# RFC-056 — Genomic Relationship (Scientific Compute)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `CLASSIFICATION.md` (D7).

## 1. Problem

BrAPI v2.1 has no genomic relationship matrix record. Relationship matrices
are essential for genomic analysis. Without this record, genomic relationships
cannot be audited or reproduced.

## 2. Object

`GenomicRelationship` — one immutable genomic relationship matrix record.

## 3. Endpoints

- `GET /genx/v1/genomic-relationships` (`genxListGenomicRelationships`)
- `POST /genx/v1/genomic-relationships` (`genxRegisterGenomicRelationship`)
- `GET /genx/v1/genomic-relationships/{genomicRelationshipDbId}` (`genxGetGenomicRelationship`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Genomic relationships reference GenX AnalysisMethod by identifier; they do not
  duplicate that resource.
- A matrix is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `genomicRelationshipDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional matrices linked by `supersedes`.
- `analysisMethodDbId` is required.
- A matrix does not imply scientific validation or approval.

## 6. Deferred questions

- D-166: Should `matrixRef` be required? (Current: optional.)
- D-167: Should genomic relationships link to GenX `GenomicDataset`? (Current:
  optional, not required.)
- D-168: Should matrix digest be required? (Current: optional.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C5, C6, C9.