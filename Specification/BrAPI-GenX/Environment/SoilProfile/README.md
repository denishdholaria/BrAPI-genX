# BrAPI-GenX — Soil Profile (Environment)

Soil profiles record soil texture, chemistry, moisture, and health
measurements at a location. Official BrAPI version 2.1 supplies Location context; this proposed soil record does not specify sampling depth or controlled nutrient measurement units.

- `POST /genx/v1/soil-profiles` (`genxRegisterSoilProfile`) registers one
  `SoilProfile` (`Schemas/SoilProfileNewRequest.yaml`). Same
  `soilProfileDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/soil-profiles` (`genxListSoilProfiles`) lists profiles,
  optionally filtered by location or status.
- `GET /genx/v1/soil-profiles/{soilProfileDbId}`
  (`genxGetSoilProfile`) retrieves one profile.

Details and falsifiers: `../../RFCs/RFC-023-Soil-Profile.md`.