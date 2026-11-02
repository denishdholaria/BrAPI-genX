# BrAPI-GenX — ArtifactCatalogue

ArtifactCatalogue records describe ArtifactCatalogue entries.
BrAPI v2.1 has no ArtifactCatalogue record.

- `POST /genx/v1/artifact-catalogues` (`genxRegisterArtifactCatalogue`) registers one
  `ArtifactCatalogue` (`Schemas/ArtifactCatalogueNewRequest.yaml`). Same
  `artifactCatalogueDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/artifact-catalogues` (`genxListArtifactCatalogues`) lists records,
  optionally filtered by status.
- `GET /genx/v1/artifact-catalogues/{artifactCatalogueDbId}`
  (`genxGetArtifactCatalogue`) retrieves one record.

Details and falsifiers: `../RFC-118-ArtifactCatalogue.md`.
