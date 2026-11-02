# RFC-067 — Carbon Stock (Environment and Climate)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-023 (Soil Profile), RFC-033 (Climate Normals), `CLASSIFICATION.md` (D5).

## 1. Problem

BrAPI v2.1 covers weather observations and locations but has no record of carbon
stocks in soil, biomass, litter, or coarse woody debris. Carbon reporting,
cropping-system comparison, and climate-smart breeding claims all depend on
comparable stock measurements with a stated pool, depth, and method. Without a
record, the same site can carry contradictory carbon claims with no audit trail.

## 2. Object

`CarbonStock` — one immutable carbon stock observation for a named pool.

## 3. Endpoints

- `GET /genx/v1/carbon-stocks` (`genxListCarbonStocks`)
- `POST /genx/v1/carbon-stocks` (`genxRecordCarbonStock`)
- `GET /genx/v1/carbon-stocks/{carbonStockDbId}` (`genxGetCarbonStock`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Carbon stocks reference BrAPI `Study` and `Location` by identifier; they do
  not duplicate those resources.
- A carbon stock record is not a BrAPI data resource and must not be treated as
  one.
- A carbon stock record is not an emissions factor, a carbon credit, or a
  certification.

## 5. Invariants

- A published `carbonStockDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- `stockMgPerHa` is always in megagrams per hectare; unit conversion is the
  client's responsibility and must not be silently applied.
- `depthCm` is only meaningful for soil and litter pools.
- A record does not imply measurement quality, verification, or accreditation.

## 6. Deferred questions

- D-199: Should `stockMgPerHa` be required, or should the record permit
  modelled-only estimates with no numeric stock? (Current: optional.)
- D-200: Should `depthCm` be required for soil and litter pools? (Current:
  optional for every pool.)
- D-201: Should carbon records link to a GenX `Telemetry` stream or
  `AnalysisResult` when the value is modelled rather than measured? (Current:
  only via provenance.)

## 7. Classification

Primary domain: D5 — Environment, Soil, Weather and Climate.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
