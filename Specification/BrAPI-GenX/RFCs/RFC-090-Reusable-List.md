# RFC-090 — Reusable List (Reference Data)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 already provides the generic List resource and dedicated
`/brapi/v2/lists` operations for lists of item identifiers. This GenX
proposal explores a *separate* immutable, namespaced list/cohort record.
The need for a second list identity and any relationship to BrAPI List
remain unproven. A missing GenX-specific title is not evidence that BrAPI
lacks reusable lists.

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
- The candidate `members` array is currently a collection of unconstrained
  strings, not enforced typed BrAPI Germplasm or Sample references. D-270
  remains open, and no identity mapping to an official BrAPI List exists.
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
