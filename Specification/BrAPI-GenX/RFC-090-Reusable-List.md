# RFC-090 — Reusable List (Reference Data)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record reusable lists and cohorts. Reusable lists
are the routine reference for research organization. Without a record, lists
arrive as unversioned notes with no stated members or provenance, so they
cannot be audited or reproduced.

## 2. Object

`ReusableList` — one immutable reusable list or cohort record, with its name,
members, and provenance.

## 3. Endpoints

- `GET /genx/v1/reusable-lists` (`genxListReusableLists`)
- `POST /genx/v1/reusable-lists` (`genxRegisterReusableList`)
- `GET /genx/v1/reusable-lists/{reusableListDbId}` (`genxGetReusableList`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Reusable list records reference BrAPI `Germplasm`/`Sample` by identifier;
  they do not duplicate those resources.
- A list record is not a BrAPI Study and must not be treated as one.

## 5. Invariants

- A published `reusableListDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the list is validated or endorsed.

## 6. Deferred questions

- D-268: Should `name` be required? (Current: optional.)
- D-269: Should `members` be required? (Current: optional.)
- D-270: Should members be BrAPI identifiers or free-form strings? (Current:
  free-form strings.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
