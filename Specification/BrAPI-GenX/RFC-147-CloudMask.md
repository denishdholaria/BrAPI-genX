# RFC-147 — Cloud Mask (M)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (M).

## 1. Problem

BrAPI v2.1 has no place to record cloud mask records. Cloud masks
circulate without a stated type, CRS, resolution, or provenance, so they
cannot be used for cloud masking analysis.

## 2. Object

`CloudMask` — one immutable cloud mask record, with its mask type,
acquisition date, CRS, resolution, extent, and provenance.

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

## 6. Deferred questions

- D-439: Should `resolution` be required? (Current: optional.)
- D-440: Should `maskType` be a controlled vocabulary? (Current: free-form string.)
- D-441: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting M).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
