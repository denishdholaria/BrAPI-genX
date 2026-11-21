# RFC-011 — Harvest Records (Crop Production)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-003 (Seed-Lot Ledger), `../CLASSIFICATION.md` (D6).

## 1. Problem

BrAPI v2.1 standardizes seed lots and seed-lot transactions but has no record
for the harvest event that produced a lot: quantity, moisture, quality grade,
area harvested, and linkage to study/location/germplasm. Without this record,
yield tracking and seed-lot provenance cannot be audited or reproduced.

## 2. Object

`HarvestRecord` — one immutable harvest-event record.

## 3. Endpoints

- `GET /genx/v1/harvest-records` (`genxListHarvestRecords`)
- `POST /genx/v1/harvest-records` (`genxRecordHarvest`)
- `GET /genx/v1/harvest-records/{harvestRecordDbId}` (`genxGetHarvestRecord`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Harvest records reference BrAPI Study, Location, Germplasm, and SeedLot by
  identifier; they do not duplicate those resources.
- A harvest record is not a SeedLotTransaction and must not be mirrored or
  double-counted with V2.1 transactions without resolving D-20.

## 5. Invariants

- A published `harvestRecordDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply a yield forecast or prediction.
- Quantity and unit are required; moisture and quality are optional.

## 6. Deferred questions

- D-30: Should `seedLotDbId` be required when the harvest produces a lot?
  (Current: optional.)
- D-31: Should harvest records support multi-lot splits from one event?
  (Current: one record per event; use multiple records if needed.)
- D-32: Should area harvested be required for yield-per-area calculations?
  (Current: optional.)

## 7. Classification

Primary domain: D6 — Crop Production and Material Operations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.