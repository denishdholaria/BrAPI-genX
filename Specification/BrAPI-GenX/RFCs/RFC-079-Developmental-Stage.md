# RFC-079 — Developmental Stage (Terminology)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-002 (Variable Term Governance), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

The checked official BrAPI v2.1 source has ObservationVariables and
Observations that can encode phenology measurements, but no dedicated
`DevelopmentalStage` resource. A separate entry could document a crop,
stage code, definition and provenance. These fields are currently optional;
the candidate cannot guarantee that a stage term is standardized,
crop-qualified, traceable to a controlled BBCH vocabulary, or comparable.

## 2. Object

`DevelopmentalStage` — a proposed immutable stage-vocabulary entry. The
`cropDbId`, `stageCode`, name, definition and provenance are optional, and
no controlled stage-code vocabulary is enforced.

## 3. Endpoints

- `GET /genx/v1/developmental-stages` (`genxListDevelopmentalStages`)
- `POST /genx/v1/developmental-stages` (`genxRegisterDevelopmentalStage`)
- `GET /genx/v1/developmental-stages/{developmentalStageDbId}` (`genxGetDevelopmentalStage`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Optional `cropDbId` is a string, not an enforced official Germplasm or
  crop-authority relationship; no GenX `VariableTerm` or official
  `ObservationVariable` crosswalk is modelled.
- A stage entry is not a BrAPI Observation or ObservationVariable and must
  not be treated as one.

## 5. Invariants

- A published `developmentalStageDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional entries linked by `supersedes`.
- A record does not imply that the stage term is validated or endorsed.

## 6. Deferred questions

- D-235: Should `cropDbId` be required? (Current: optional, global stages
  allowed.)
- D-236: Should `stageCode` follow a controlled vocabulary (e.g. BBCH)?
  (Current: free-form string.)
- D-237: Should entries link to GenX `VariableTerm`? (Current: no link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C4, C9.
