# BrAPI-GenX — Crop Species (Reference Data)

Crop and species registry entries describe crop species.
BrAPI v2.1 has no crop species record.

- `POST /genx/v1/crop-species` (`genxRegisterCropSpecies`) registers one
  `CropSpecies` (`Schemas/CropSpeciesNewRequest.yaml`). Same
  `cropSpeciesDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/crop-species` (`genxListCropSpecies`) lists entries,
  optionally filtered by status.
- `GET /genx/v1/crop-species/{cropSpeciesDbId}`
  (`genxGetCropSpecies`) retrieves one entry.

Details and falsifiers: `../RFC-095-Crop-Species.md`.
