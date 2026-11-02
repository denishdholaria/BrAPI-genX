# RFC-135 — Crop Suitability (O)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (O).

## 1. Problem

BrAPI v2.1 has no place to record crop suitability. Crop suitability
assessments circulate without a stated suitability type, score, region, or
provenance, so they cannot be used for site selection decisions.

## 2. Object

`CropSuitability` — one immutable crop suitability record, with its
suitability type, suitable crop, score, region/zone, season, and provenance.

## 3. Endpoints

- `GET /genx/v1/crop-suitabilities` (`genxListCropSuitabilities`)
- `POST /genx/v1/crop-suitabilities` (`genxRegisterCropSuitability`)
- `GET /genx/v1/crop-suitabilities/{cropSuitabilityDbId}` (`genxGetCropSuitability`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `cropSuitabilityDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-403: Should `suitabilityScore` be required? (Current: optional.)
- D-404: Should `suitabilityType` be a controlled vocabulary? (Current: free-form string.)
- D-405: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting O).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
