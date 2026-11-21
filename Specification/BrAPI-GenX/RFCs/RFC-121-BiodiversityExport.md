# RFC-121 — Biodiversity Export (Cross-cutting S)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (S).

## 1. Problem

BrAPI v2.1 has no place to record biodiversity occurrence/specimen exports.
Specimen exports occur without a stated type, occurrence reference, collection
date, or provenance, so they cannot be traced or audited.

## 2. Object

`BiodiversityExport` — one immutable biodiversity export record, with its
specimen type, occurrence reference, collection date, location, taxon, and
provenance.

## 3. Endpoints

- `GET /genx/v1/biodiversity-exports` (`genxListBiodiversityExports`)
- `POST /genx/v1/biodiversity-exports` (`genxRegisterBiodiversityExport`)
- `GET /genx/v1/biodiversity-exports/{biodiversityExportDbId}` (`genxGetBiodiversityExport`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `biodiversityExportDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-361: Should `occurrenceId` be required? (Current: optional.)
- D-362: Should `taxon` be a controlled vocabulary? (Current: free-form string.)
- D-363: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting S).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
