# RFC-028 — Parent Candidate Selection (Breeding)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D2).

## 1. Problem

BrAPI v2.1 has no record for parent candidate selection: whether a candidate
was selected as a parent, the criterion, and rationale. Without this record,
parent selection decisions cannot be audited or reproduced.

## 2. Object

`ParentCandidateSelection` — one immutable parent candidate selection record.

## 3. Endpoints

- `GET /genx/v1/parent-candidate-selections` (`genxListParentCandidateSelections`)
- `POST /genx/v1/parent-candidate-selections` (`genxRecordParentCandidateSelection`)
- `GET /genx/v1/parent-candidate-selections/{parentCandidateSelectionDbId}` (`genxGetParentCandidateSelection`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Parent candidate selections store required `programDbId` and `candidateGermplasmDbId` as strings, without typed authoritative-server references or proven cross-resource joins. They do not replace official Program/Germplasm records.
- A record is not a BrAPI Germplasm or Cross and must not be treated as one.

## 5. Invariants

- A published `parentCandidateSelectionDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- `candidateGermplasmDbId` and `selected` are required.
- A record does not imply an approved breeding plan, authorized decision, performed cross or release. `selectionCriterion`, rationale, decision-maker evidence and provenance are not required; `selected: false` cannot distinguish rejection from deferral.

## 6. Deferred questions

- D-81: Should `selected` be required? (Current: required.)
- D-82: Should selection criterion be a governed enumeration? (Current: free
  string.)
- D-83: Should records link to GenX `SelectionDecision`? (Current: no `selectionDecisionDbId` or typed relationship in the schema; a link is not implemented.)

## 7. Classification

Primary domain: D2 — Breeding Programs and Experimental Design.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
