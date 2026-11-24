# BrAPI-GenX — Soil Chemistry (Environment)

SoilChemistry proposes a draft soil-data metadata record, not a verified
laboratory analysis or standardized soil-health observation. The registration
request requires only its identity. Site, texture, chemistry and provenance
are optional. The chemistry object is unconstrained; `moistureDepthCm`
is a measurement depth, **not** an actual soil-water-content value.

No mandatory sampling date, depth interval, analyte units, analytical method
or validated official BrAPI version 2.1 Location join is modelled.

- `POST /genx/v1/soil-chemistry` (`genxRegisterSoilChemistry`) registers one
  `SoilChemistry` (`Schemas/SoilChemistryNewRequest.yaml`). Same
  `soilChemistryDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/soil-chemistry` (`genxListSoilChemistry`) lists records,
  optionally filtered by site or status.
- `GET /genx/v1/soil-chemistry/{soilChemistryDbId}`
  (`genxGetSoilChemistry`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-077-Soil-Chemistry.md`.
