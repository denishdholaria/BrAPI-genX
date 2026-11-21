# RFC-024 — Irrigation Operation (Crop Production)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D6).

## 1. Problem

BrAPI v2.1 has locations but no irrigation record. Water application events
are essential for crop models and agronomy. Without this record, water use
cannot be audited or linked to studies with provenance.

## 2. Object

`IrrigationEvent` — one immutable irrigation-event record.

## 3. Endpoints

- `GET /genx/v1/irrigation-operations` (`genxListIrrigations`)
- `POST /genx/v1/irrigation-operations` (`genxRecordIrrigation`)
- `GET /genx/v1/irrigation-operations/{irrigationEventDbId}` (`genxGetIrrigation`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Irrigation events reference BrAPI Location and Study by identifier; they do
  not duplicate those resources.
- An irrigation event is not a BrAPI Location and must not be treated as one.

## 5. Invariants

- A published `irrigationEventDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional events linked by `supersedes`.
- `method`, `volume`, and `duration` are recorded, not inferred.
- An event does not imply a complete water-use record.

## 6. Deferred questions

- D-69: Should `volume` and `duration` be required? (Current: optional.)
- D-70: Should irrigation events link to GenX `WeatherObservation`?
  (Current: optional, not required.)
- D-71: Should irrigation method be a governed enumeration? (Current: free
  string.)

## 7. Classification

Primary domain: D6 — Crop Production and Material Operations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.