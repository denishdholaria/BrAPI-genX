# Mission 088 — Cloud-mask and raster-catalogue evidence boundaries

**Parent:** Mission 087 draft branch at `e4f59299cdcced94a3b1ee1ef11f9f00f9597457`.  
**Scope:** documentation science review, README route/link repair, source-backed guard and tests. No official BrAPI (Breeding Application Programming Interface) v2.1 contract, GenX wire schema, endpoint registry, maturity register or governance decision is changed.

## Source-grounded findings

1. **CloudMask (RFC-147; D-439–D-441):** registration requires only `cloudMaskDbId`, and the response adds `status`. Mask type, acquisition date, coordinate reference system, spatial resolution, extent and provenance are optional strings or objects. No schema representation of mask pixels, an asset URI, cloud percentage, source image or validated grid/classification exists. `maskType` has no enum; `acquisitionDate` has no format constraint. The original README incorrectly named the GET operation `genxListCloudMask` and linked to nonexistent `../RFC-146-CloudMask.md`. The source operation is `genxListCloudMasks`, and the source RFC is `../../RFCs/RFC-147-CloudMask.md`. Both are corrected without altering an endpoint.
2. **RasterCatalogue (RFC-144; D-430–D-432):** registration requires only `rasterCatalogueDbId`, response adds `status`. Dataset name/type, CRS, resolution, extent and provenance remain optional. No raster asset reference, spectral bands, pixel grid or quality assurance is modelled; even an NDVI (normalized difference vegetation index) dataset-type example is not a measured index.
3. **Official overlap:** official BrAPI `ImageNewRequest` already exposes `imageURL`, `imageLocation`, dimensions and timestamp. Neither of the new GenX draft modules has a verified association to that Image resource or to GenX RemoteSensingMetadata; broad claims that official BrAPI has no image metadata are misleading. This source review does not imply scientific spatial/remote-sensing interoperability.

## Implementation

- Two evidence-backed `STRUCTURAL_DRAFT` GroupDescriptions and corrected READMEs/RFCs, each with direct local source links.
- Protected documentation inventory proposed to **139 of 156**, leaving **17 evidence-deferred** if tests pass.
- Regression checks bind required and optional field sets to real source schemas, verify absence of mask/raster payload links, inspect official Image fields, preserve deferred decision references and pin CloudMask's plural source operation and valid RFC path.

**Not approved:** raster access, cloud-classification correctness, coordinate transform, radiometric calibration, scientific reflectance, standardized dataset types, ResearchAsset relations or maturity promotion.

## Verification required

```sh
python Scripts/check_genx_group_descriptions.py
python Scripts/test_genx_group_descriptions.py
python Scripts/report_genx_evidence_coverage.py --check
python Scripts/checkGenXConformance.py
python Scripts/checkEndpointRegistry.py
python Scripts/auditEndpointRegistrySourceConsistency.py --strict
python Scripts/generateEndpointArtifacts.py --check
```

Full hosted static and live conformance and generated-artifact verification must succeed before merging. **Status: draft, test execution pending.**
