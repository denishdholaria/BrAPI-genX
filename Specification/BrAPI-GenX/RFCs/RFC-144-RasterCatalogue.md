# RFC-144 — Raster Catalogue (M)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (M).

## 1. Problem

BrAPI v2.1 has no place to record raster catalogues. Raster datasets
circulate without a stated type, resolution, CRS, or provenance, so they
cannot be used for spatial analysis.

## 2. Object

`RasterCatalogue` — one immutable raster catalogue record, with its dataset
name, type, resolution, CRS, extent, and provenance.

## 3. Endpoints

- `GET /genx/v1/raster-catalogues` (`genxListRasterCatalogues`)
- `POST /genx/v1/raster-catalogues` (`genxRegisterRasterCatalogue`)
- `GET /genx/v1/raster-catalogues/{rasterCatalogueDbId}` (`genxGetRasterCatalogue`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `rasterCatalogueDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-430: Should `extent` be required? (Current: optional.)
- D-431: Should `datasetType` be a controlled vocabulary? (Current: free-form string.)
- D-432: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting M).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
