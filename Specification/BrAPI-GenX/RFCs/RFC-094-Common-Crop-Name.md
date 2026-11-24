# RFC-094 — Common Crop Name (Reference Data)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-002 (Variable Term Governance), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 already publishes common crop names through
`GET /brapi/v2/commoncropnames`, which is required for multi-crop
servers. The candidate GenX record instead explores separate namespaced,
immutable common-name/scientific-name metadata. Its distinct necessity,
authority, and compatibility with the official server-advertised crop
names have not yet been established.

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
- The candidate schema contains no typed Germplasm, official
  `commoncropnames`, or GenX `TaxonName` reference. D-282 remains open;
  no equivalence with an official crop-name value is assumed.
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
