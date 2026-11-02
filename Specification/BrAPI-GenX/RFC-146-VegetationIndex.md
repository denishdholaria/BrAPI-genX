# RFC-146 — Vegetation Index (M)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (M).

## 1. Problem

BrAPI v2.1 has no place to record vegetation index records. Vegetation
indices circulate without a stated type, CRS, resolution, or provenance, so
they cannot be used for vegetation monitoring.

## 2. Object

`VegetationIndex` — one immutable vegetation index record, with its index
type, name, acquisition date, CRS, resolution, and provenance.

## 3. Endpoints

- `GET /genx/v1/vegetation-indexes` (`genxListVegetationIndexes`)
- `POST /genx/v1/vegetation-indexes` (`genxRegisterVegetationIndex`)
- `GET /genx/v1/vegetation-indexes/{vegetationIndexDbId}` (`genxGetVegetationIndex`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `vegetationIndexDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-436: Should `resolution` be required? (Current: optional.)
- D-437: Should `indexType` be a controlled vocabulary? (Current: free-form string.)
- D-438: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting M).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
