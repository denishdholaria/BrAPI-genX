# RFC-147 — Cloud Mask (M)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (M).

## 1. Problem

Official BrAPI v2.1 already exposes an Image resource with an image URL,
location, dimensions and acquisition timestamp, although its inspected
source does not provide a dedicated CloudMask resource. The proposed
metadata catalogue describes cloud masks without requiring the mask data,
its classification grid, source-image association or quality information;
registration of a metadata entry alone does not enable cloud masking analysis.

## 2. Object

`CloudMask` — proposed immutable cloud-mask *metadata*. The mask type,
acquisition date, coordinate reference system (CRS), resolution, extent and
provenance are **optional**, unstructured properties rather than validated
raster artefacts, controlled classifications or required references.

## 3. Endpoints

- `GET /genx/v1/cloud-masks` (`genxListCloudMasks`)
- `POST /genx/v1/cloud-masks` (`genxRegisterCloudMask`)
- `GET /genx/v1/cloud-masks/{cloudMaskDbId}` (`genxGetCloudMask`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `cloudMaskDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- No pixel mask, asset URI, cloud-percentage estimate, image relationship, or
  authoritative mask-data linkage is present in this source contract.

## 6. Deferred questions

- D-439: Should `resolution` be required? (Current: optional.)
- D-440: Should `maskType` be a controlled vocabulary? (Current: free-form string.)
- D-441: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting M).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
