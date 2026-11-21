# RFC-120 — Publication Review (Cross-cutting S)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (S).

## 1. Problem

BrAPI v2.1 has no place to record publication reviews. Publications related to
breeding and genomics research circulate without a structured review status,
venue, or provenance, so they cannot be tracked or audited.

## 2. Object

`PublicationReview` — one immutable publication review record, with its title,
type, venue, year, and provenance.

## 3. Endpoints

- `GET /genx/v1/publication-reviews` (`genxListPublicationReviews`)
- `POST /genx/v1/publication-reviews` (`genxRegisterPublicationReview`)
- `GET /genx/v1/publication-reviews/{publicationReviewDbId}` (`genxGetPublicationReview`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `publicationReviewDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-358: Should `year` be required? (Current: optional.)
- D-359: Should `publicationType` be a controlled vocabulary? (Current: free-form string.)
- D-360: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting S).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
