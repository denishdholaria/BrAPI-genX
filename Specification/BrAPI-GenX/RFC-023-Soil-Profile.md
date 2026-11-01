# RFC-023 — Soil Profile (Environment)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (D5).

## 1. Problem

BrAPI v2.1 has locations but no soil profile record. Soil texture, chemistry,
moisture, and health measurements are essential for crop models and agronomy.
Without this record, soil data cannot be cited or linked to studies with
provenance.

## 2. Object

`SoilProfile` — one immutable soil profile record.

## 3. Endpoints

- `GET /genx/v1/soil-profiles` (`genxListSoilProfiles`)
- `POST /genx/v1/soil-profiles` (`genxRegisterSoilProfile`)
- `GET /genx/v1/soil-profiles/{soilProfileDbId}` (`genxGetSoilProfile`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Soil profiles reference BrAPI Location by identifier; they do not duplicate
  that resource.
- A soil profile is not a BrAPI Location and must not be treated as one.

## 5. Invariants

- A published `soilProfileDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional profiles linked by `supersedes`.
- `texture`, `ph`, `organicMatter`, and `moisture` are recorded, not inferred.
- A profile does not imply a complete soil survey.

## 6. Deferred questions

- D-66: Should `nutrients` require a governed vocabulary? (Current: free
  strings.)
- D-67: Should soil profiles link to GenX `WeatherObservation`? (Current:
  optional, not required.)
- D-68: Should sampling depth be recorded? (Current: not in this slice.)

## 7. Classification

Primary domain: D5 — Environment, Agroecology and Field Context.
Cross-cutting: C1, C2, C3 (POST), C6, C9.