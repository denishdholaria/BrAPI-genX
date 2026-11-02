# BrAPI-GenX — Emissions (Environment)

Emissions records describe greenhouse gas emissions for a site or period.
BrAPI v2.1 has no emissions record.

- `POST /genx/v1/emissions` (`genxRegisterEmissions`) registers one
  `Emissions` (`Schemas/EmissionsNewRequest.yaml`). Same
  `emissionsDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/emissions` (`genxListEmissions`) lists records,
  optionally filtered by site or status.
- `GET /genx/v1/emissions/{emissionsDbId}`
  (`genxGetEmissions`) retrieves one record.

Details and falsifiers: `../RFC-076-Emissions.md`.
