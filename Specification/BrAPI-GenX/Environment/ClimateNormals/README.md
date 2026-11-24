# BrAPI-GenX — Climate Normals (Environment)

Climate normals record long-term average environmental conditions for a
location and reference period. Its draft period string and mean do not prove statistically derived climate normals, underlying sample completeness or a typed WeatherObservation link.

- `POST /genx/v1/climate-normals` (`genxRegisterClimateNormal`) registers one
  `ClimateNormal` (`Schemas/ClimateNormalNewRequest.yaml`). Same
  `climateNormalDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/climate-normals` (`genxListClimateNormals`) lists normals,
  optionally filtered by location, variable, or period.
- `GET /genx/v1/climate-normals/{climateNormalDbId}`
  (`genxGetClimateNormal`) retrieves one normal.

Details and falsifiers: `../../RFCs/RFC-033-Climate-Normals.md`.