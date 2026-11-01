# RFC-026 — Fertilizer Application (Crop Production)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (D6).

## 1. Problem

BrAPI v2.1 has no fertilizer application record. Nutrient application events
are essential for crop models and agronomy. Without this record, nutrient use
cannot be audited or linked to studies with provenance.

## 2. Object

`FertilizerApplication` — one immutable fertilizer-application record.

## 3. Endpoints

- `GET /genx/v1/fertilizer-applications` (`genxListFertilizerApplications`)
- `POST /genx/v1/fertilizer-applications` (`genxRecordFertilizerApplication`)
- `GET /genx/v1/fertilizer-applications/{fertilizerApplicationDbId}` (`genxGetFertilizerApplication`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Fertilizer applications reference BrAPI Location and Study by identifier;
  they do not duplicate those resources.
- An application is not a BrAPI Location and must not be treated as one.

## 5. Invariants

- A published `fertilizerApplicationDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional applications linked by `supersedes`.
- `product`, `quantity`, and `unit` are required.
- An application does not imply a complete nutrient record.

## 6. Deferred questions

- D-75: Should `quantity` and `unit` be required? (Current: required.)
- D-76: Should fertilizer applications link to GenX `SoilProfile`? (Current:
  optional, not required.)
- D-77: Should product be a governed vocabulary? (Current: free string.)

## 7. Classification

Primary domain: D6 — Crop Production and Material Operations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.