# RFC-128 — Crop Health Image (N)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (N).

## 1. Problem

BrAPI v2.1 has no place to record crop health images. Crop health imagery
circulates without a stated image type, capture date, sensor, or provenance,
so it cannot be used for crop monitoring or stress detection.

## 2. Object

`CropHealthImage` — one immutable crop health image record, with its image
type, capture date, sensor/platform, vegetation index, health status, and
provenance.

## 3. Endpoints

- `GET /genx/v1/crop-health-images` (`genxListCropHealthImages`)
- `POST /genx/v1/crop-health-images` (`genxRegisterCropHealthImage`)
- `GET /genx/v1/crop-health-images/{cropHealthImageDbId}` (`genxGetCropHealthImage`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `cropHealthImageDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-382: Should `vegetationIndex` be required? (Current: optional.)
- D-383: Should `imageType` be a controlled vocabulary? (Current: free-form string.)
- D-384: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting N).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
