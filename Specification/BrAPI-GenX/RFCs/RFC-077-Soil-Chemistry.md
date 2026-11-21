# RFC-077 — Soil Chemistry (Environment)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-023 (Soil Profile), `../CLASSIFICATION.md` (D5).

## 1. Problem

BrAPI v2.1 has no place to record soil texture, chemistry, and moisture
observations. These are the routine inputs to agronomic and environmental
analysis. Without a record, soil observations arrive as unversioned figures
with no stated site, depth, or provenance, so they cannot be audited or
reproduced.

## 2. Object

`SoilChemistry` — one immutable record of soil texture, chemistry, and
moisture observations for a site, with depth and provenance.

## 3. Endpoints

- `GET /genx/v1/soil-chemistry` (`genxListSoilChemistry`)
- `POST /genx/v1/soil-chemistry` (`genxRegisterSoilChemistry`)
- `GET /genx/v1/soil-chemistry/{soilChemistryDbId}` (`genxGetSoilChemistry`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Soil chemistry records reference BrAPI `Location` and GenX `SoilProfile` by
  identifier; they do not duplicate those resources.
- A soil chemistry record is not a BrAPI Observation and must not be treated
  as one.

## 5. Invariants

- A published `soilChemistryDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the soil was validated or certified.

## 6. Deferred questions

- D-229: Should `siteDbId` be required? (Current: optional.)
- D-230: Should `chemistry` be a controlled vocabulary instead of a free-form
  object? (Current: free-form object.)
- D-231: Should moisture depth be required when moisture is reported? (Current:
  optional.)

## 7. Classification

Primary domain: D5 — Environment, Soil, Weather, and Climate.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
