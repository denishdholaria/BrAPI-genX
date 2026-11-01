# RFC-029 — Crop Cycle (Crop Production)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (D6).

## 1. Problem

BrAPI v2.1 has locations and studies but no crop cycle record. Planting-to-
harvest cycles are essential for crop models and agronomy. Without this
record, crop timing cannot be audited or linked to studies with provenance.

## 2. Object

`CropCycle` — one immutable crop cycle record.

## 3. Endpoints

- `GET /genx/v1/crop-cycles` (`genxListCropCycles`)
- `POST /genx/v1/crop-cycles` (`genxRegisterCropCycle`)
- `GET /genx/v1/crop-cycles/{cropCycleDbId}` (`genxGetCropCycle`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Crop cycles reference BrAPI Location and Study by identifier; they do not
  duplicate those resources.
- A cycle is not a BrAPI Study and must not be treated as one.

## 5. Invariants

- A published `cropCycleDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional cycles linked by `supersedes`.
- `plantingDate` and `harvestDate` are recorded, not inferred.
- A cycle does not imply a complete crop record.

## 6. Deferred questions

- D-84: Should `plantingDate` and `harvestDate` be required? (Current:
  optional.)
- D-85: Should crop cycles link to GenX `HarvestRecord`? (Current:
  optional, not required.)
- D-86: Should crop name be a governed vocabulary? (Current: free string.)

## 7. Classification

Primary domain: D6 — Crop Production and Material Operations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.