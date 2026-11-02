# RFC-097 — Person Reference (Reference Data)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record person references. Person references are
the routine reference for research organization. Without a record, people
arrive as unversioned strings with no stated name, role, or provenance, so
they cannot be audited or reproduced.

## 2. Object

`PersonReference` — one immutable person reference entry, with its name, role,
and provenance.

## 3. Endpoints

- `GET /genx/v1/person-references` (`genxListPersonReferences`)
- `POST /genx/v1/person-references` (`genxRegisterPersonReference`)
- `GET /genx/v1/person-references/{personReferenceDbId}` (`genxGetPersonReference`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Person reference entries reference BrAPI entities by identifier; they do not
  duplicate those resources.
- An entry is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `personReferenceDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional entries linked by `supersedes`.
- A record does not imply that the person is validated or endorsed.

## 6. Deferred questions

- D-289: Should `name` be required? (Current: optional.)
- D-290: Should `role` be required? (Current: optional.)
- D-291: Should entries link to GenX `Project`? (Current: no link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C4, C9.
