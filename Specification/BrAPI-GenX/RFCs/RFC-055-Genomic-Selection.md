# RFC-055 — Genomic Selection (Scientific Compute)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `../CLASSIFICATION.md` (D7).

## 1. Problem

BrAPI v2.1 has no genomic selection result record. Selection outcomes are
essential for breeding programs. Without this record, genomic selections
cannot be audited or reproduced.

## 2. Object

`GenomicSelection` — one immutable genomic selection result record.

## 3. Endpoints

- `GET /genx/v1/genomic-selections` (`genxListGenomicSelections`)
- `POST /genx/v1/genomic-selections` (`genxRecordGenomicSelection`)
- `GET /genx/v1/genomic-selections/{genomicSelectionDbId}` (`genxGetGenomicSelection`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Genomic selections reference GenX AnalysisMethod by identifier; they do not
  duplicate that resource.
- A result is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `genomicSelectionDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional results linked by `supersedes`.
- `analysisMethodDbId` is required.
- A result does not imply scientific validation or approval.

## 6. Deferred questions

- D-163: Should `selectedGermplasm` be required? (Current: optional.)
- D-164: Should genomic selections link to GenX `GenomicDataset`? (Current:
  optional, not required.)
- D-165: Should selection threshold be required? (Current: optional.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C6, C9.