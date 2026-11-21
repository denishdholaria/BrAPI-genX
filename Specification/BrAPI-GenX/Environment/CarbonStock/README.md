# BrAPI-GenX — Carbon Stock (Environment and Climate)

Carbon stock records document measured or modelled carbon in soil and biomass
pools. BrAPI v2.1 has no carbon stock record.

- `POST /genx/v1/carbon-stocks` (`genxRecordCarbonStock`) registers one
  `CarbonStock` (`Schemas/CarbonStockNewRequest.yaml`). Same
  `carbonStockDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/carbon-stocks` (`genxListCarbonStocks`) lists records,
  optionally filtered by study, location, pool, or status.
- `GET /genx/v1/carbon-stocks/{carbonStockDbId}`
  (`genxGetCarbonStock`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-067-Carbon-Stock.md`.
