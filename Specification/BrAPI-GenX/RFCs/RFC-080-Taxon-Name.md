# RFC-080 — Taxon Name (Reference Data)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-002 (Variable Term Governance), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

Official BrAPI version 2.1 Germplasm already contains genus, species, species authority and source-scoped taxon identifiers. An independently governed synonym and taxonomic-name service is a potential additional workflow, not an already proven deficiency in BrAPI. The need for a distinct candidate identity remains to be demonstrated.

## 2. Object

`TaxonName` — one immutable taxon name or synonym entry, with its scientific
name, synonyms, and provenance.

## 3. Endpoints

- `GET /genx/v1/taxon-names` (`genxListTaxonNames`)
- `POST /genx/v1/taxon-names` (`genxRegisterTaxonName`)
- `GET /genx/v1/taxon-names/{taxonNameDbId}` (`genxGetTaxonName`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- The candidate has no typed BrAPI Germplasm or TaxonID identifier link. Scientific-name strings and synonyms do not establish accepted-name or external taxonomic identity; D-240 remains open.
- A taxon name entry is not a BrAPI Germplasm and must not be treated as one.

## 5. Invariants

- A published `taxonNameDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional entries linked by `supersedes`.
- A record does not imply that the taxon is validated or endorsed.

## 6. Deferred questions

- D-238: Should `scientificName` be required? (Current: optional.)
- D-239: Should synonyms be a controlled vocabulary? (Current: free-form array.)
- D-240: Should entries link to an external taxonomy (e.g. NCBI)? (Current: no
  link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C4, C9.
