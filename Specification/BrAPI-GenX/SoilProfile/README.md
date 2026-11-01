# BrAPI-GenX — Soil Profile (Environment)

Soil profiles record soil texture, chemistry, moisture, and health
measurements at a location. BrAPI v2.1 has locations but no soil record.

- `POST /genx/v1/soil-profiles` (`genxRegisterSoilProfile`) registers one
  `SoilProfile` (`Schemas/SoilProfileNewRequest.yaml`). Same
  `soilProfileDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/soil-profiles` (`genxListSoilProfiles`) lists profiles,
  optionally filtered by location or status.
- `GET /genx/v1/soil-profiles/{soilProfileDbId}`
  (`genxGetSoilProfile`) retrieves one profile.

Details and falsifiers: `../RFC-023-Soil-Profile.md`.