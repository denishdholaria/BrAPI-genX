# RFC-137 — Explanation Evidence (O)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (O).

## 1. Problem

BrAPI v2.1 has no place to record explanation evidence. AI/ML explanations
circulate without a stated evidence type, uncertainty, or provenance, so they
cannot be audited or trusted.

## 2. Object

`ExplanationEvidence` — one immutable explanation evidence record, with its
evidence type, explanation text, uncertainty, confidence, and provenance.

## 3. Endpoints

- `GET /genx/v1/explanation-evidences` (`genxListExplanationEvidences`)
- `POST /genx/v1/explanation-evidences` (`genxRegisterExplanationEvidence`)
- `GET /genx/v1/explanation-evidences/{explanationEvidenceDbId}` (`genxGetExplanationEvidence`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `explanationEvidenceDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-409: Should `confidence` be required? (Current: optional.)
- D-410: Should `evidenceType` be a controlled vocabulary? (Current: free-form string.)
- D-411: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting O).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
