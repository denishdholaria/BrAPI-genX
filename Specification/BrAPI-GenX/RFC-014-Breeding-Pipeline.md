# RFC-014 — Breeding Pipeline (Stage Gates)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-008 (Selection Decisions), `CLASSIFICATION.md` (D2).

## 1. Problem

BrAPI v2.1 standardizes breeding programs, trials, studies, and crosses but
not the pipeline of stages, entry/exit criteria, and advancement rules that
connect them. Without this record, breeding process structure and stage-gate
decisions cannot be audited or reproduced.

## 2. Object

`BreedingPipeline` — one immutable breeding pipeline definition.

## 3. Endpoints

- `GET /genx/v1/breeding-pipelines` (`genxListBreedingPipelines`)
- `POST /genx/v1/breeding-pipelines` (`genxRegisterBreedingPipeline`)
- `GET /genx/v1/breeding-pipelines/{breedingPipelineDbId}` (`genxGetBreedingPipeline`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Breeding pipelines reference BrAPI Program by identifier; they do not
  duplicate that resource.
- A pipeline is not a BrAPI Program or Study and must not be treated as one.

## 5. Invariants

- A published `breedingPipelineDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional pipelines linked by `supersedes`.
- Stages are ordered by `stageOrder`; gaps are allowed.
- A pipeline does not imply an approved breeding plan or release.

## 6. Deferred questions

- D-39: Should stages reference GenX `SelectionDecision` or `AnalysisMethod`
  records? (Current: free-text criteria.)
- D-40: Should a pipeline be versioned independently of its program?
  (Current: yes, via `supersedes`.)
- D-41: Should stage transitions be recorded as separate events?
  (Current: not in this slice.)

## 7. Classification

Primary domain: D2 — Breeding Programs and Experimental Design.
Cross-cutting: C1, C2, C3 (POST), C6, C9.