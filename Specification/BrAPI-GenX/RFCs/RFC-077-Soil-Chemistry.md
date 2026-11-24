# RFC-077 — Soil Chemistry (Environment)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-023 (Soil Profile), `../CLASSIFICATION.md` (D5).

## 1. Problem

GenX proposes separately identified soil texture and chemistry metadata
alongside official BrAPI version 2.1 observations and locations.
Soil analysis requires a known sampling site, depth, date, laboratory
method, analytes and units to be comparable. The current candidate requires
none of those data on registration, and a generic chemistry object cannot
independently substantiate scientific reproducibility.

## 2. Object

`SoilChemistry` — one proposed immutable record; texture, site, chemistry,
measurement depth and provenance are optional and unvalidated.

## 3. Endpoints

- `GET /genx/v1/soil-chemistry` (`genxListSoilChemistry`)
- `POST /genx/v1/soil-chemistry` (`genxRegisterSoilChemistry`)
- `GET /genx/v1/soil-chemistry/{soilChemistryDbId}` (`genxGetSoilChemistry`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- `siteDbId` is an optional plain string; the schema does not enforce an
  authority-matched BrAPI Location or a GenX SoilProfile relationship.
  No `soilProfileDbId` field is modelled. Advisory operation neighbors
  do not establish typed links.
- A soil chemistry record is not a BrAPI Observation and must not be treated
  as one.

## 5. Invariants

- A published `soilChemistryDbId` is proposed to be immutable.
- Replay: same id + identical body replays; same id + different body → 409;
  this requires independent persistent-service testing.
- Corrections are proposed as additional records linked by `supersedes`.
- Only `soilChemistryDbId` is required on registration. `chemistry` is an
  optional, unconstrained object; `moistureDepthCm` indicates a depth,
  not a validated moisture-content measurement.
- A record does not imply analytically comparable results, independent
  laboratory validation, soil certification or scientific approval.

## 6. Deferred questions

- D-229: Should `siteDbId` be required? (Current: optional.)
- D-230: Should `chemistry` be a controlled vocabulary instead of a free-form
  object? (Current: free-form object.)
- D-231: Should moisture depth be required when moisture is reported? (Current:
  optional.)

## 7. Classification

Primary domain: D5 — Environment, Soil, Weather, and Climate.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
