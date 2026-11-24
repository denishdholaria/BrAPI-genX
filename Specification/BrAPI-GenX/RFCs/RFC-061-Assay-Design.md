# RFC-061 — Assay Design (Genomics)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `../CLASSIFICATION.md` (D3).

## 1. Problem

BrAPI v2.1 provides Samples, Variants, CallSets and genotyping-result
operations, but does not define this proposed standalone assay-design
registration. Its absence does not itself prove that existing exchange
metadata or laboratory systems are insufficient. The candidate records
limited design metadata pending interoperable use-case evidence.

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
- The optional `analysisMethodDbId` string can name a proposed GenX
  AnalysisMethod; no referential integrity or stable mapping is enforced.
- The candidate contains no explicit GenomicDataset or MarkerProbe
  reference. Neither link may be inferred from navigational neighbors.
- A design is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `assayDesignDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional designs linked by `supersedes`.
- A design does not imply scientific validation or approval.

## 6. Deferred questions

- D-181: Should `platform` be required? (Current: optional.)
- D-182: Should assay designs link to GenX `GenomicDataset`? (Current:
  no explicit dataset field; no link is defined.)
- D-183: Should marker count be required? (Current: optional.)

## 7. Classification

Primary domain: D3 — Genotyping and Molecular Genomics.
Cross-cutting: C1, C2, C3 (POST), C6, C9.