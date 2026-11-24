# BrAPI-GenX — Water Balance (Environment and Climate)

Water balance entries document optional water inputs, outputs and storage-change metadata. Official BrAPI version 2.1 supplies Location and Observation context, not a validated water budget; the proposed GenX record requires neither an accounting window nor closed-balance evidence.

- `POST /genx/v1/water-balances` (`genxRecordWaterBalance`) registers one
  `WaterBalance` (`Schemas/WaterBalanceNewRequest.yaml`). Same
  `waterBalanceDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/water-balances` (`genxListWaterBalances`) lists records,
  optionally filtered by study, location, or status.
- `GET /genx/v1/water-balances/{waterBalanceDbId}`
  (`genxGetWaterBalance`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-068-Water-Balance.md`.
