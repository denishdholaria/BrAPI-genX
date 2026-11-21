# RFC-041 — Acquisition (Genebank Conservation)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D1).

## 1. Problem

BrAPI v2.1 has germplasm and seed lots but no acquisition record. Intake of
conserved material is essential for genebank management. Without this record,
acquisition events cannot be audited or linked to seed lots with provenance.

## 2. Object

`AcquisitionRecord` — one immutable acquisition record.

## 3. Endpoints

- `GET /genx/v1/acquisitions` (`genxListAcquisitions`)
- `POST /genx/v1/acquisitions` (`genxRecordAcquisition`)
- `GET /genx/v1/acquisitions/{acquisitionRecordDbId}` (`genxGetAcquisition`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Acquisition records reference BrAPI SeedLot by identifier; they do not
  duplicate that resource.
- An acquisition record is not a BrAPI SeedLot transaction and must not be
  treated as one.

## 5. Invariants

- A published `acquisitionRecordDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- `source` and `acquiredAt` are required.
- A record does not imply a complete conservation record.

## 6. Deferred questions

- D-121: Should `source` be a governed vocabulary? (Current: free string.)
- D-122: Should acquisitions link to GenX `QuarantineRecord`? (Current:
  optional, not required.)
- D-123: Should acquisition records link to collecting missions? (Current:
  optional, not required.)

## 7. Classification

Primary domain: D1 — Germplasm and Biological Resources.
Cross-cutting: C1, C2, C3 (POST), C6, C9.