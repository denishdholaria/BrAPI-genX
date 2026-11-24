# RFC-068 — Water Balance (Environment and Climate)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-010 (Weather Observations), RFC-023 (Soil Profile), RFC-024 (Irrigation Operation), RFC-029 (Crop Cycle), RFC-067 (Carbon Stock), `../CLASSIFICATION.md` (D5).

## 1. Problem

BrAPI version 2.1 includes Locations and Observation records but does not define this proposed water-balance accounting object. WeatherObservation and IrrigationOperation are distinct GenX candidates, not official BrAPI v2.1 source records. Irrigation scheduling,
drought-stress interpretation, drainage and runoff accounting, and climate
reporting all require a period-level statement of inputs, outputs, and storage
change. Without a balance record, the same field can carry contradictory water
claims and no auditable budget.

## 2. Object

`WaterBalance` — one immutable water balance record for a location and period.

## 3. Endpoints

- `GET /genx/v1/water-balances` (`genxListWaterBalances`)
- `POST /genx/v1/water-balances` (`genxRecordWaterBalance`)
- `GET /genx/v1/water-balances/{waterBalanceDbId}` (`genxGetWaterBalance`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- The candidate has optional string `studyDbId` and `locationDbId` fields. It has no typed GenX `CropCycle`, `WeatherObservation`, or `IrrigationOperation` references (D-204). Source data reconciliation is not implemented by this record.
- A water balance record is not a BrAPI data resource and must not be treated
  as one.
- A water balance record is not irrigation advice, a water right, or a
  regulatory allocation.

## 5. Invariants

- A published `waterBalanceDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- Every quantity is in millimetres over the stated period; unit conversion is
  the client's responsibility and must not be silently applied.
- `periodStart` and `periodEnd` can describe an accounting window when supplied, but neither is required. A common window and components from consistent source intervals are proposed obligations, not enforced schema rules.
- The sign convention for `storageChangeMm` is the change in stored water, not
  a flux; consumers must not treat it as an input or output.
- A record does not imply measurement quality, model validation, or that the
  components close to zero residual. Residual accounting is separate evidence.

## 6. Deferred questions

- D-202: Should the balance require a closed-budget check
  (`precipitation + irrigation − evapotranspiration − runoff − drainage −
  storageChange ≈ 0`), and should a non-closing record be rejected? (Current:
  no check; components are recorded as supplied.)
- D-203: Should `periodStart` and `periodEnd` be required? (Current: optional,
  so an instantaneous or unspecified window can be recorded.)
- D-204: Should balances reference the specific `WeatherObservation` and
  `IrrigationOperation` records that contributed, rather than only study,
  location, and crop cycle? (Current: not modelled.)

## 7. Classification

Primary domain: D5 — Environment, Soil, Weather and Climate.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
