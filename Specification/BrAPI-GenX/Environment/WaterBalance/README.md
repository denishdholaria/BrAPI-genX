# BrAPI-GenX — Water Balance (Environment and Climate)

Water balance records document the water inputs, outputs, and storage change for
a location over a period. BrAPI v2.1 has no water balance record.

- `POST /genx/v1/water-balances` (`genxRecordWaterBalance`) registers one
  `WaterBalance` (`Schemas/WaterBalanceNewRequest.yaml`). Same
  `waterBalanceDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/water-balances` (`genxListWaterBalances`) lists records,
  optionally filtered by study, location, or status.
- `GET /genx/v1/water-balances/{waterBalanceDbId}`
  (`genxGetWaterBalance`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-068-Water-Balance.md`.
