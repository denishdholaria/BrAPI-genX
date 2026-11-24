# RFC-067 — Carbon Stock (Environment and Climate)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-023 (Soil Profile), RFC-033 (Climate Normals), `../CLASSIFICATION.md` (D5).

## 1. Problem

BrAPI v2.1 covers weather observations and locations but has no record of carbon
stocks in soil, biomass, litter, or coarse woody debris. Carbon reporting and comparison require identified pools, sampling strata,
measurement or estimation methods, uncertainty, depth and provenance. The
current GenX candidate requires **only its identifier** at registration;
none of those scientific parameters is mandatory. A registry record is not
an audited carbon inventory or a climate-smart breeding claim.

## 2. Object

`CarbonStock` — proposed immutable stock *metadata* for an optionally named
pool; the current source does not require a carbon quantity or sampling evidence.

## 3. Endpoints

- `GET /genx/v1/carbon-stocks` (`genxListCarbonStocks`)
- `POST /genx/v1/carbon-stocks` (`genxRecordCarbonStock`)
- `GET /genx/v1/carbon-stocks/{carbonStockDbId}` (`genxGetCarbonStock`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- `studyDbId` and `locationDbId` are optional strings; there is no
  authority-checked BrAPI Study or Location join defined by the schema.
- A carbon stock record is not a BrAPI data resource and must not be treated as
  one.
- A carbon stock record is not an emissions factor, a carbon credit, or a
  certification.

## 5. Invariants

- A published `carbonStockDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- The optional numeric `stockMgPerHa` has a nominal unit of megagrams per
  hectare; its presence does not validate sampling, stock calculation, pool
  boundaries or the reported mass basis.
- Optional `depthCm` is not constrained by pool type; the source contains no
  condition requiring a depth for soil or litter or disallowing it elsewhere.
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
