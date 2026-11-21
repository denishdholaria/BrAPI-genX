# RFC-066 — Planting Operation (Field Agronomy)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-024 (Irrigation Operation), RFC-026 (Fertilizer Application), RFC-029 (Crop Cycle), RFC-038 (Tillage), `../CLASSIFICATION.md` (D6).

## 1. Problem

BrAPI v2.1 describes studies, observation units, and observations, but it does
not record when and how material was planted. Sowing date, method, seeding rate,
and depth are the inputs that determine whether later observations are
comparable. Without a planting record, trials cannot be reproduced and
season-level agronomy cannot be audited.

## 2. Object

`PlantingOperation` — one immutable record of a sowing or transplanting
operation.

## 3. Endpoints

- `GET /genx/v1/planting-operations` (`genxListPlantingOperations`)
- `POST /genx/v1/planting-operations` (`genxRecordPlantingOperation`)
- `GET /genx/v1/planting-operations/{plantingOperationDbId}` (`genxGetPlantingOperation`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Planting operations reference BrAPI `Study` and `ObservationUnit` and GenX
  `CropCycle` by identifier; they do not duplicate those resources.
- A planting operation is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `plantingOperationDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional operations linked by `supersedes`.
- Only a `completed` record asserts that planting occurred.
- `planned` and `cancelled` records remain visible; they are never deleted.
- `seedingRate` is meaningless without a unit; the unit belongs in provenance
  until a units module exists (see D-197).
- An operation does not imply germination, establishment, or yield.

## 6. Deferred questions

- D-196: Should `studyDbId` or `observationUnitDbId` be required? (Current: both
  optional, so a field-level operation is representable.)
- D-197: Should `seedingRate` carry an explicit unit field or reference a GenX
  unit term? (Current: no unit field.)
- D-198: Should `method` be a controlled vocabulary aligned with an external
  agronomy ontology? (Current: free string.)

## 7. Classification

Primary domain: D6 — Field Agronomy and Crop Operations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
