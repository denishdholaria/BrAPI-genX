# RFC-104 — Duplicate Review (Germplasm)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record duplicate reviews. Duplicate reviews are the
routine reference for germplasm and genetic resources. Without a record,
reviews arrive as unversioned notes with no stated candidate, decision, or
provenance, so they cannot be audited or reproduced.

## 2. Object

`DuplicateReview` — one immutable duplicate review record, with its candidate
reference, decision, and provenance.

## 3. Endpoints

- `GET /genx/v1/duplicate-reviews` (`genxListDuplicateReviews`)
- `POST /genx/v1/duplicate-reviews` (`genxRegisterDuplicateReview`)
- `GET /genx/v1/duplicate-reviews/{duplicateReviewDbId}` (`genxGetDuplicateReview`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Duplicate review records reference BrAPI `Germplasm` by identifier; they do
  not duplicate those resources.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `duplicateReviewDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the review is validated or endorsed.

## 6. Deferred questions

- D-310: Should `candidateDbId` be required? (Current: optional.)
- D-311: Should `decision` be a controlled vocabulary? (Current: free-form
  string.)
- D-312: Should records link to GenX `Crosswalk`? (Current: no link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
