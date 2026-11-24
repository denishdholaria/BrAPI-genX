# RFC-146 — Vegetation Index (M)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (M).

## 1. Problem

GenX proposes a separately identified vegetation-index **metadata**
catalogue alongside official BrAPI version 2.1 resources. The current
candidate does not require index type, coordinate reference system,
resolution, acquisition date, scientific algorithm, numeric index value,
raster reference, calibrated bands or provenance. Registering a catalogue
identity cannot itself substantiate vegetation monitoring, phenotypic
observations or source-image integrity.

## 2. Object

`VegetationIndex` — one proposed immutable *metadata* record. Index type,
name, acquisition date, coordinate reference system, resolution and
provenance are optional, with no index value or raster payload reference.

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

- A published `vegetationIndexDbId` record is proposed to be immutable.
- Replay is a draft contract: same id + identical body replays; same id +
  different body → 409. Persistent-service behavior requires testing.
- Corrections are proposed as additional records linked by `supersedes`.
- Only `vegetationIndexDbId` is required for registration. No
  `indexValue`, `rasterRef`, pixel source or vegetation-index formula
  is modelled, so the record cannot be assumed to contain measurements.

## 6. Deferred questions

- D-436: Should `resolution` be required? (Current: optional.)
- D-437: Should `indexType` be a controlled vocabulary? (Current: free-form string.)
- D-438: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting M).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
