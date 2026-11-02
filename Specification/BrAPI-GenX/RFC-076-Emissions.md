# RFC-076 — Emissions (Environment)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-023 (Soil Profile), RFC-067 (Carbon Stock), `CLASSIFICATION.md` (D5).

## 1. Problem

BrAPI v2.1 has no place to record greenhouse gas emissions for a site or period.
Emissions are the routine output of carbon accounting and sustainability
reporting. Without a record, emissions arrive as unversioned figures with no
stated site, period, gas, or provenance, so they cannot be audited or
reproduced.

## 2. Object

`Emissions` — one immutable record of greenhouse gas emissions for a site or
period, with its gas, quantity, unit, and provenance.

## 3. Endpoints

- `GET /genx/v1/emissions` (`genxListEmissions`)
- `POST /genx/v1/emissions` (`genxRegisterEmissions`)
- `GET /genx/v1/emissions/{emissionsDbId}` (`genxGetEmissions`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Emissions records reference BrAPI `Location` and GenX `CarbonStock` by
  identifier; they do not duplicate those resources.
- An emissions record is not a BrAPI Observation and must not be treated as
  one.

## 5. Invariants

- A published `emissionsDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
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
