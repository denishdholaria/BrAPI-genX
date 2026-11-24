# RFC-121 — Biodiversity Export (Cross-cutting S)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (S).

## 1. Problem

The checked official BrAPI v2.1 source has Germplasm collecting/passport
metadata, but no dedicated BiodiversityExport record. The GenX candidate
requires only its own identifier on registration: occurrence reference,
collection date, specimen type, taxon, location and provenance are all
optional. It cannot itself demonstrate an actual biodiversity-data export,
a validated occurrence or a publication accepted by an external network.

## 2. Object

`BiodiversityExport` — a proposed immutable export-*description* record.
The typed schema does not define a dataset payload, export destination,
Darwin Core Archive representation, delivery state or publisher license.

## 3. Endpoints

- `GET /genx/v1/biodiversity-exports` (`genxListBiodiversityExports`)
- `POST /genx/v1/biodiversity-exports` (`genxRegisterBiodiversityExport`)
- `GET /genx/v1/biodiversity-exports/{biodiversityExportDbId}` (`genxGetBiodiversityExport`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.
- No `germplasmDbId`, Darwin Core crosswalk, archive address, or verified
  export receipt is modelled; `active` is a record lifecycle state, not
  evidence that the data was delivered, published or accepted.

## 5. Invariants

- A published `biodiversityExportDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- The optional `collectionDate` has no date format validation; optional
  location and taxon strings do not prove coordinates or taxonomic authority.
  No biodiversity export payload or external publication job is defined.

## 6. Deferred questions

- D-361: Should `occurrenceId` be required? (Current: optional.)
- D-362: Should `taxon` be a controlled vocabulary? (Current: free-form string.)
- D-363: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting S).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
