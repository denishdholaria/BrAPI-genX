# RFC-008 — Selection Decisions (Breeding Verdicts)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (D2).

## 1. Problem

BrAPI v2.1 standardizes breeding programs, trials, studies, observations, and
germplasm, but it has no record for the **verdict** a breeder reaches for a
candidate: selected, rejected, deferred, or advanced. Programs and trials exist;
the decision and its rationale do not. Without this record, breeding history
cannot be audited or reproduced, and downstream selection decisions cannot cite
their evidence.

## 2. Object

`SelectionDecision` — one immutable breeding selection verdict.

## 3. Endpoints

- `GET /brapi/v3/selection-decisions` (`genxListSelectionDecisions`)
- `POST /brapi/v3/selection-decisions` (`genxRecordSelectionDecision`)
- `GET /brapi/v3/selection-decisions/{selectionDecisionDbId}` (`genxGetSelectionDecision`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Selection decisions reference BrAPI Program, Study, and Germplasm by their
  existing identifiers; they do not duplicate those resources.

## 5. Invariants

- A published `(selectionDecisionDbId)` record never mutates in place.
- Corrections are recorded as additional decisions linked by `supersedes`.
- Replay: same id + identical body replays; same id + different body → 409.
- `decision` is one of `selected`, `rejected`, `deferred`, `advanced`.
- A decision does not imply release, registration, or commercial approval.

## 6. Deferred questions

- D-21: Should selection decisions be scoped per breeding program only, or
  also per trial/study? (Current: program required, study optional.)
- D-22: Should `linkedObservationDbIds` be required when `decision` is
  `selected`? (Current: optional.)
- D-23: Should a decision be cancellable/superseded only by the original
  decision maker or by any authorized breeder? (Current: requires decision.)

## 7. Classification

Primary domain: D2 — Breeding Programs and Experimental Design.
Cross-cutting: C1, C2, C3 (POST), C9.