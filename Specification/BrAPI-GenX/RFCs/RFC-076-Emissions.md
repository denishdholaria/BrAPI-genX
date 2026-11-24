# RFC-076 — Emissions (Environment)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-023 (Soil Profile), RFC-067 (Carbon Stock), `../CLASSIFICATION.md` (D5).

## 1. Problem

BrAPI v2.1 has no place to record greenhouse gas emissions for a site or period.
Emissions accounting requires a specified gas or category, quantity, unit,
reporting period, scope, factor method and evidence. The current candidate
requires only the record identifier and therefore cannot guarantee that
any of these items is available or scientifically comparable.

## 2. Object

`Emissions` — proposed immutable emissions metadata; site, period,
reported gas/category, quantity, unit and provenance are all optional.

## 3. Endpoints

- `GET /genx/v1/emissions` (`genxListEmissions`)
- `POST /genx/v1/emissions` (`genxRegisterEmissions`)
- `GET /genx/v1/emissions/{emissionsDbId}` (`genxGetEmissions`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Optional `siteDbId` is not a verified BrAPI Location join. No
  `carbonStockDbId` exists in either schema, so there is **no modelled**
  CarbonStock association. Carbon stocks and emissions flows are not equivalent.
- An emissions record is not a BrAPI Observation and must not be treated as
  one.

## 5. Invariants

- A published `emissionsDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- `period` is an unconstrained string, not a validated reporting interval.
  `greenhouseGas` and `unit` are free text. The illustrative CO2e (carbon
  dioxide equivalent) label is a derived reporting category, not a gas species.
- A record does not imply that the emissions were validated, certified, or
  scientifically endorsed.

## 6. Deferred questions

- D-226: Should `siteDbId` be required? (Current: optional.)
- D-227: Should `quantity` and `unit` be required? (Current: optional.)
- D-228: Should greenhouse gas be a controlled GenX terminology? (Current:
  free-form string.)

## 7. Classification

Primary domain: D5 — Environment, Soil, Weather, and Climate.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
