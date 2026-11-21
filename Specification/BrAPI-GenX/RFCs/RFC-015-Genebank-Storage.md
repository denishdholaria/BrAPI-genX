# RFC-015 — Genebank Storage (Conservation)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D1).

## 1. Problem

BrAPI v2.1 standardizes germplasm and seed lots but not the physical storage
locations, capacity, or environmental conditions of conserved material.
Without this record, conservation capacity and conditions cannot be audited or
managed through the standard.

## 2. Object

`StorageLocation` — one immutable genebank storage location record.

## 3. Endpoints

- `GET /genx/v1/genebank-storage` (`genxListStorageLocations`)
- `POST /genx/v1/genebank-storage` (`genxRegisterStorageLocation`)
- `GET /genx/v1/genebank-storage/{storageLocationDbId}` (`genxGetStorageLocation`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Storage locations do not imply BrAPI SeedLot transactions or germplasm
  identity; they are complementary records.

## 5. Invariants

- A published `storageLocationDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A location does not imply a BrAPI SeedLot or germplasm record.
- Capacity and environment are recorded, not inferred.

## 6. Deferred questions

- D-42: Should viability/germination testing be a separate object?
  (Current: not in this slice.)
- D-43: Should safety duplication and backup sites be separate records?
  (Current: not in this slice.)
- D-44: Should storage locations link to GenX `LotLedger` entries?
  (Current: optional, not required.)

## 7. Classification

Primary domain: D1 — Germplasm and Biological Resources.
Cross-cutting: C1, C2, C3 (POST), C6, C9.