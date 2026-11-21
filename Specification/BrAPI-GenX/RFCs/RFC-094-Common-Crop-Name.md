# RFC-094 — Common Crop Name (Reference Data)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-002 (Variable Term Governance), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record common crop names. Common crop names are
the routine reference for germplasm and species resolution. Without a record,
names arrive as unversioned strings with no stated scientific name or
provenance, so they cannot be audited or reproduced.

## 2. Object

`CommonCropName` — one immutable common crop name entry, with its scientific
name, common name, and provenance.

## 3. Endpoints

- `GET /genx/v1/common-crop-names` (`genxListCommonCropNames`)
- `POST /genx/v1/common-crop-names` (`genxRegisterCommonCropName`)
- `GET /genx/v1/common-crop-names/{commonCropNameDbId}` (`genxGetCommonCropName`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Common crop name entries reference BrAPI `Germplasm` by identifier; they do
  not duplicate those resources.
- An entry is not a BrAPI Germplasm and must not be treated as one.

## 5. Invariants

- A published `commonCropNameDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional entries linked by `supersedes`.
- A record does not imply that the name is validated or endorsed.

## 6. Deferred questions

- D-280: Should `scientificName` be required? (Current: optional.)
- D-281: Should `commonName` be required? (Current: optional.)
- D-282: Should entries link to GenX `TaxonName`? (Current: no link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C4, C9.
