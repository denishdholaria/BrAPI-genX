# RFC-019 — Progeny Records (Breeding)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (D2).

## 1. Problem

BrAPI v2.1 standardizes pedigree and crosses but not progeny/family records
that link parents to offspring within a breeding program, including generation
and family identity. Without this record, lineage and family structure cannot
be audited or reproduced independently of pedigree graphs.

## 2. Object

`ProgenyRecord` — one immutable progeny/family record.

## 3. Endpoints

- `GET /genx/v1/progeny-records` (`genxListProgenyRecords`)
- `POST /genx/v1/progeny-records` (`genxRecordProgeny`)
- `GET /genx/v1/progeny-records/{progenyRecordDbId}` (`genxGetProgenyRecord`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Progeny records reference BrAPI Program, Germplasm, and Cross by
  identifier; they do not duplicate those resources.
- A progeny record is not a BrAPI Pedigree or Cross and must not be treated
  as one.

## 5. Invariants

- A published `progenyRecordDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- `parentDbIds` and `progenyDbId` are required.
- A record does not imply an approved breeding plan or release.

## 6. Deferred questions

- D-54: Should `parentDbIds` be limited to two parents? (Current: array.)
- D-55: Should generation be a governed enumeration? (Current: free string.)
- D-56: Should progeny records require a BrAPI Cross reference?
  (Current: optional.)

## 7. Classification

Primary domain: D2 — Breeding Programs and Experimental Design.
Cross-cutting: C1, C2, C3 (POST), C6, C9.