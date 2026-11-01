# RFC-038 — Tillage (Crop Production)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (D6).

## 1. Problem

BrAPI v2.1 has locations but no tillage record. Soil preparation events
are essential for crop models and agronomy. Without this record, tillage
cannot be audited or linked to studies with provenance.

## 2. Object

`TillageRecord` — one immutable tillage record.

## 3. Endpoints

- `GET /genx/v1/tillage-records` (`genxListTillageRecords`)
- `POST /genx/v1/tillage-records` (`genxRecordTillage`)
- `GET /genx/v1/tillage-records/{tillageRecordDbId}` (`genxGetTillage`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Tillage records reference BrAPI Location and Study by identifier; they do
  not duplicate those resources.
- A tillage record is not a BrAPI Location and must not be treated as one.

## 5. Invariants

- A published `tillageRecordDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- `method` and `tilledAt` are required.
- A record does not imply a complete soil record.

## 6. Deferred questions

- D-112: Should `depth` be required? (Current: optional.)
- D-113: Should tillage records link to GenX `SoilProfile`? (Current:
  optional, not required.)
- D-114: Should method be a governed vocabulary? (Current: free string.)

## 7. Classification

Primary domain: D6 — Crop Production and Material Operations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.