# BrAPI-GenX — Farm (Field Agronomy)

Farm records describe the site reference above BrAPI Locations: the holding that
groups fields, plots, and stations. BrAPI v2.1 has no farm record.

- `POST /genx/v1/farms` (`genxRegisterFarm`) registers one `Farm`
  (`Schemas/FarmNewRequest.yaml`). Same `farmDbId` + identical body replays;
  different body is rejected with `409`.
- `GET /genx/v1/farms` (`genxListFarms`) lists farms, optionally filtered by
  location or status.
- `GET /genx/v1/farms/{farmDbId}` (`genxGetFarm`) retrieves one farm.

Details and falsifiers: `../../RFCs/RFC-069-Farm.md`.
