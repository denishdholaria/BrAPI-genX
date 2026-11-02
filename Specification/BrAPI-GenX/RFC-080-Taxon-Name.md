# RFC-080 — Taxon Name (Reference Data)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-002 (Variable Term Governance), `CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record taxon names and synonyms. Taxon names are
the routine reference for germplasm and species resolution. Without a record,
taxon names arrive as unversioned strings with no stated synonyms or
provenance, so they cannot be audited or reproduced.

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
- Taxon name entries reference BrAPI `Germplasm` by identifier; they do not
  duplicate those resources.
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
