# RFC-095 — Crop Species (Reference Data)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-002 (Variable Term Governance), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

Official BrAPI version 2.1 already exposes supported common crop names and germplasm genus, species and source-scoped taxon identifiers. A candidate standalone crop/species record may address a different governance workflow, but its separate authority and necessity have not yet been evidenced.

## 2. Object

`CropSpecies` — one immutable crop and species registry entry, with its
scientific name, crop name, and provenance.

## 3. Endpoints

- `GET /genx/v1/crop-species` (`genxListCropSpecies`)
- `POST /genx/v1/crop-species` (`genxRegisterCropSpecies`)
- `GET /genx/v1/crop-species/{cropSpeciesDbId}` (`genxGetCropSpecies`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- The candidate has no typed BrAPI Germplasm or GenX TaxonName identifier link. Matching crop and scientific-name strings do not establish equivalence; D-285 remains open.
- An entry is not a BrAPI Germplasm and must not be treated as one.

## 5. Invariants

- A published `cropSpeciesDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional entries linked by `supersedes`.
- A record does not imply that the species is validated or endorsed.

## 6. Deferred questions

- D-283: Should `scientificName` be required? (Current: optional.)
- D-284: Should `cropName` be required? (Current: optional.)
- D-285: Should entries link to GenX `TaxonName`? (Current: no link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C4, C9.
