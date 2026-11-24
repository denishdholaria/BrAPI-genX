# BrAPI-GenX — Crop Species (Reference Data)

Crop and species registry entries describe crop species.
Official BrAPI version 2.1 already exposes supported common crop names and Germplasm taxonomic metadata. This separate GenX draft does not define a typed relationship to an official germplasm or a GenX TaxonName.

- `POST /genx/v1/crop-species` (`genxRegisterCropSpecies`) registers one
  `CropSpecies` (`Schemas/CropSpeciesNewRequest.yaml`). Same
  `cropSpeciesDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/crop-species` (`genxListCropSpecies`) lists entries,
  optionally filtered by status.
- `GET /genx/v1/crop-species/{cropSpeciesDbId}`
  (`genxGetCropSpecies`) retrieves one entry.

Details and falsifiers: `../../RFCs/RFC-095-Crop-Species.md`.
