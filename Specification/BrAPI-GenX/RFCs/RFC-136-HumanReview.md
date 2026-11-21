# RFC-136 — Human Review (O)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (O).

## 1. Problem

BrAPI v2.1 has no place to record human reviews. Human review decisions
(accept/reject of advisories) circulate without a stated reviewer, decision,
date, or provenance, so they cannot be audited.

## 2. Object

`HumanReview` — one immutable human review record, with its review type,
reviewer, decision, date, comments, and provenance.

## 3. Endpoints

- `GET /genx/v1/human-reviews` (`genxListHumanReviews`)
- `POST /genx/v1/human-reviews` (`genxRegisterHumanReview`)
- `GET /genx/v1/human-reviews/{humanReviewDbId}` (`genxGetHumanReview`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `humanReviewDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-406: Should `comments` be required? (Current: optional.)
- D-407: Should `reviewDecision` be a controlled vocabulary? (Current: free-form string.)
- D-408: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting O).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
