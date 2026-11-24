# RFC-033 — Climate Normals (Environment)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D5).

## 1. Problem

BrAPI v2.1 has locations but no climate normal record. Long-term averages
are essential for crop models and agronomy. Without this record, climate
normals cannot be cited or linked to locations with provenance.

## 2. Object

`ClimateNormal` — one immutable climate normal record.

## 3. Endpoints

- `GET /genx/v1/climate-normals` (`genxListClimateNormals`)
- `POST /genx/v1/climate-normals` (`genxRegisterClimateNormal`)
- `GET /genx/v1/climate-normals/{climateNormalDbId}` (`genxGetClimateNormal`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Climate normals reference BrAPI Location and Observation Variable by
  identifier; they do not duplicate those resources.
- A climate normal is not a BrAPI Location and must not be treated as one.
- There is no typed GenX `WeatherObservation` reference (D-97); its mean is not independently validated.

## 5. Invariants

- A published `climateNormalDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional normals linked by `supersedes`.
- `mean`, `min`, and `max` are recorded, not inferred.
- A normal does not imply a complete climate record.

## 6. Deferred questions

- D-96: Should `mean`, `min`, and `max` be required? (Current: mean
  required, min/max optional.)
- D-97: Should climate normals link to GenX `WeatherObservation`? (Current:
  no typed WeatherObservation reference property exists in the candidate schema.)
- D-98: Should period be a governed vocabulary? (Current: free string.)

## 7. Classification

Primary domain: D5 — Environment, Agroecology and Field Context.
Cross-cutting: C1, C2, C3 (POST), C6, C9.