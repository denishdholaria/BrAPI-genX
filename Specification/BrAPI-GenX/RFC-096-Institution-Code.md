# RFC-096 — Institution Code (Reference Data)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-002 (Variable Term Governance), `CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record institution and collection codes. Institution
codes are the routine reference for germplasm and collection resolution.
Without a record, codes arrive as unversioned strings with no stated name or
provenance, so they cannot be audited or reproduced.

## 2. Object

`InstitutionCode` — one immutable institution and collection code entry, with
its code, name, and provenance.

## 3. Endpoints

- `GET /genx/v1/institution-codes` (`genxListInstitutionCodes`)
- `POST /genx/v1/institution-codes` (`genxRegisterInstitutionCode`)
- `GET /genx/v1/institution-codes/{institutionCodeDbId}` (`genxGetInstitutionCode`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Institution code entries reference BrAPI entities by identifier; they do not
  duplicate those resources.
- An entry is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `institutionCodeDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional entries linked by `supersedes`.
- A record does not imply that the code is validated or endorsed.

## 6. Deferred questions

- D-286: Should `code` be required? (Current: optional.)
- D-287: Should `name` be required? (Current: optional.)
- D-288: Should entries link to GenX `TaxonName`? (Current: no link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C4, C9.
