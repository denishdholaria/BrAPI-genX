# BrAPI-GenX — RasterCatalogue

RasterCatalogue records describe RasterCatalogue entries.
BrAPI v2.1 has no RasterCatalogue record.

- `POST /genx/v1/raster-catalogues` (`genxRegisterRasterCatalogue`) registers one
  `RasterCatalogue` (`Schemas/RasterCatalogueNewRequest.yaml`). Same
  `rasterCatalogueDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/raster-catalogues` (`genxListRasterCatalogues`) lists records,
  optionally filtered by status.
- `GET /genx/v1/raster-catalogues/{rasterCatalogueDbId}`
  (`genxGetRasterCatalogue`) retrieves one record.

Details and falsifiers: `../RFC-144-RasterCatalogue.md`.
