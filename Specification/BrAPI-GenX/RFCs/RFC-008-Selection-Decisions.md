# RFC-008 — Selection Decisions (Breeding Verdicts)

- Status: proposal, non-normative; retain and refine as an actual selection verdict.
- Supersedes: none.
- Decision: preserve the separation between actual selection verdicts and pipeline/scheme design-time task definitions; exact pipeline and scheme versions may be referenced where applicable.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D2).

## 1. Problem

BrAPI v2.1 standardizes breeding programs, trials, studies, observations, and
germplasm, but it has no record for the **verdict** a breeder reaches for a
candidate: selected, rejected, deferred, or advanced. Programs and trials exist;
there is no dedicated typed verdict resource. This candidate provides a dated, enumerated verdict, but rationale, responsible actor, candidate Germplasm and linked observations are optional, so historical audit completeness is not guaranteed.

## 2. Object

`SelectionDecision` — one immutable breeding selection verdict.

## 3. Endpoints

- `GET /genx/v1/selection-decisions` (`genxListSelectionDecisions`)
- `POST /genx/v1/selection-decisions` (`genxRecordSelectionDecision`)
- `GET /genx/v1/selection-decisions/{selectionDecisionDbId}` (`genxGetSelectionDecision`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Selection decisions reference BrAPI Program, Study, Germplasm and Observation
  by authority-qualified references; they do not duplicate those resources.

## 5. Invariants

- A published `(selectionDecisionDbId)` record never mutates in place.
- Corrections are recorded as additional decisions linked by `supersedes`.
- Replay: same id + identical body replays; same id + different body → 409.
- `decision` is one of `selected`, `rejected`, `deferred`, `advanced`.
- A decision does not imply release, registration, commercial approval, an actual cross, or verified decision-maker authority. `decisionMaker`, `candidateGermplasmReference`, rationale, linked observations and provenance are optional.

## 6. Deferred questions

- RFC-008-Q1: Should selection decisions be scoped per breeding program only, or
  also per trial/study? (Current: program required, study optional.)
- RFC-008-Q2: Should linked BrAPI Observation evidence be required when `decision`
  is `selected`? (Current: optional authority-qualified `linkedObservationReferences`.)
- RFC-008-Q3: Should a decision be cancellable/superseded only by the original decision maker or by any authorized breeder? (Current: requires decision; `decisionMaker` is optional and cannot enforce original-actor authorization alone.)

## 7. Classification

Primary domain: D2 — Breeding Programs and Experimental Design.
Cross-cutting: C1, C2, C3 (POST), C9.

## 8. Pipeline and scheme context

The current candidate schema uses nested optional context envelopes:
- `pipelineContext` contains the stable `breedingPipelineDbId` and exact `breedingPipelineVersionDbId`;
- `schemeContext` contains `breedingSchemeDbId` and exact `breedingSchemeVersionDbId`, with optional `stageId` nested inside it.

If both contexts are supplied, the referenced pipeline revision must contain the exact scheme version in its embedded scheme bindings. A scheme context without pipeline context is valid; a decision made outside a registered strategy may omit both contexts. An event must not put scheme-local stage identifiers at the top level.

The selection verdict, rationale, actor and evidence remain owned by SelectionDecision. A scheme TaskDefinition describes the intended selection process and is not a verdict.

## 9. Authority-qualified list filters

The list operation accepts `programDbId` only with `programServer`, `studyDbId` only with `studyServer`, and `candidateGermplasmDbId` only with `candidateGermplasmServer`. Server parameters identify the authoritative BrAPI v2.1 base URI that issued the identifier. Implementations must reject incomplete pairs and must not resolve identifiers by guessing the server.
