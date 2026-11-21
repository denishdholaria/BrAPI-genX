# RFC-093 — Reference Data Version (Reference Data)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record reference data versions. Reference data
versioning is the routine reference for reproducible analysis. Without a
record, versions arrive as unversioned strings with no stated source, version,
or provenance, so they cannot be audited or reproduced.

## 2. Object

`ReferenceDataVersion` — one immutable reference data version record, with its
source, version label, and provenance.

## 3. Endpoints

- `GET /genx/v1/reference-data-versions` (`genxListReferenceDataVersions`)
- `POST /genx/v1/reference-data-versions` (`genxRegisterReferenceDataVersion`)
- `GET /genx/v1/reference-data-versions/{referenceDataVersionDbId}` (`genxGetReferenceDataVersion`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Reference data version records reference BrAPI entities by identifier; they
  do not duplicate those resources.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `referenceDataVersionDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the reference data is validated or endorsed.

## 6. Deferred questions

- D-277: Should `source` be required? (Current: optional.)
- D-278: Should `version` be required? (Current: optional.)
- D-279: Should records link to GenX `VariableTerm`? (Current: no link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
