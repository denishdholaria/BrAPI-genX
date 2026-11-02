# BrAPI-GenX — Soil Chemistry (Environment)

Soil texture, chemistry, and moisture records describe soil observations for a
site. BrAPI v2.1 has no soil chemistry record.

- `POST /genx/v1/soil-chemistry` (`genxRegisterSoilChemistry`) registers one
  `SoilChemistry` (`Schemas/SoilChemistryNewRequest.yaml`). Same
  `soilChemistryDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/soil-chemistry` (`genxListSoilChemistry`) lists records,
  optionally filtered by site or status.
- `GET /genx/v1/soil-chemistry/{soilChemistryDbId}`
  (`genxGetSoilChemistry`) retrieves one record.

Details and falsifiers: `../RFC-077-Soil-Chemistry.md`.
