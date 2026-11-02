# RFC-129 — Crop Recommendation (O)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (O).

## 1. Problem

BrAPI v2.1 has no place to record crop recommendations. Advisory outputs
(crop, variety, practice) circulate without a stated type, region, season,
or provenance, so they cannot be traced or evaluated.

## 2. Object

`CropRecommendation` — one immutable crop recommendation record, with its
recommendation type, recommended variety/practice, region/zone, season, and
provenance.

## 3. Endpoints

- `GET /genx/v1/crop-recommendations` (`genxListCropRecommendations`)
- `POST /genx/v1/crop-recommendations` (`genxRegisterCropRecommendation`)
- `GET /genx/v1/crop-recommendations/{cropRecommendationDbId}` (`genxGetCropRecommendation`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `cropRecommendationDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-385: Should `season` be required? (Current: optional.)
- D-386: Should `recommendationType` be a controlled vocabulary? (Current: free-form string.)
- D-387: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting O).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
