# RFC-079 — Developmental Stage (Terminology)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-002 (Variable Term Governance), `CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record developmental stage vocabulary. Growth-stage
terms (BBCH, etc.) are the routine reference for phenology and observation
annotation. Without a record, stage terms arrive as unversioned strings with no
stated crop, code, definition, or provenance, so they cannot be audited or
reproduced.

## 2. Object

`DevelopmentalStage` — one immutable developmental stage vocabulary entry for a
crop, with its code, name, definition, and provenance.

## 3. Endpoints

- `GET /genx/v1/developmental-stages` (`genxListDevelopmentalStages`)
- `POST /genx/v1/developmental-stages` (`genxRegisterDevelopmentalStage`)
- `GET /genx/v1/developmental-stages/{developmentalStageDbId}` (`genxGetDevelopmentalStage`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Developmental stage entries reference BrAPI `Germplasm`/crop by identifier;
  they do not duplicate those resources.
- A stage entry is not a BrAPI Observation and must not be treated as one.

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
