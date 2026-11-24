# BrAPI-GenX — RasterCatalogue

`RasterCatalogue` proposes a **draft descriptive record** for raster-dataset discovery. It does not provide a raster asset address, pixels, verified grid geometry, spectral-band metadata, access rights, or the scientific interpretation of a computed vegetation index.

Only `rasterCatalogueDbId` is required on registration; dataset name/type, coordinate reference system, resolution, extent, and provenance are optional free-form strings or objects. Official BrAPI (Breeding Application Programming Interface) version 2.1 already exposes Image metadata including `imageURL`, `imageLocation`, dimensions and timestamps, but no verified mapping connects it to this proposed catalogue.

- `POST /genx/v1/raster-catalogues` (`genxRegisterRasterCatalogue`) registers one `RasterCatalogue` (`Schemas/RasterCatalogueNewRequest.yaml`). Same `rasterCatalogueDbId` and identical request body is described as replayable; a different body is rejected with `409`.
- `GET /genx/v1/raster-catalogues` (`genxListRasterCatalogues`) lists records, optionally filtered by status.
- `GET /genx/v1/raster-catalogues/{rasterCatalogueDbId}` (`genxGetRasterCatalogue`) retrieves a record.

Source limits and deferred questions: [group description](./GroupDescription.md), [RFC-144](../../RFCs/RFC-144-RasterCatalogue.md).
