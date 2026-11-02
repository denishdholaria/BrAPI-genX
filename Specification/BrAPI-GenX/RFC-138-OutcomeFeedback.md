# RFC-138 — Outcome Feedback (O)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (O).

## 1. Problem

BrAPI v2.1 has no place to record outcome feedback. Outcome feedback
(observed results vs predictions) circulates without a stated feedback type,
value, source, or provenance, so it cannot be used for model improvement.

## 2. Object

`OutcomeFeedback` — one immutable outcome feedback record, with its feedback
type, value, source, date, and provenance.

## 3. Endpoints

- `GET /genx/v1/outcome-feedbacks` (`genxListOutcomeFeedbacks`)
- `POST /genx/v1/outcome-feedbacks` (`genxRegisterOutcomeFeedback`)
- `GET /genx/v1/outcome-feedbacks/{outcomeFeedbackDbId}` (`genxGetOutcomeFeedback`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `outcomeFeedbackDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-412: Should `feedbackValue` be required? (Current: optional.)
- D-413: Should `feedbackType` be a controlled vocabulary? (Current: free-form string.)
- D-414: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting O).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
