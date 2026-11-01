# RFC-035 — Population Advancement (Breeding)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (D2).

## 1. Problem

BrAPI v2.1 has no population advancement record. Movement of populations
between breeding stages is essential for breeding process tracking. Without
this record, advancement cannot be audited or linked to programs with
provenance.

## 2. Object

`PopulationAdvancement` — one immutable population advancement record.

## 3. Endpoints

- `GET /genx/v1/population-advancements` (`genxListPopulationAdvancements`)
- `POST /genx/v1/population-advancements` (`genxRecordPopulationAdvancement`)
- `GET /genx/v1/population-advancements/{populationAdvancementDbId}` (`genxGetPopulationAdvancement`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Population advancements reference BrAPI Program by identifier; they do not
  duplicate that resource.
- A record is not a BrAPI Program and must not be treated as one.

## 5. Invariants

- A published `populationAdvancementDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- `fromStage`, `toStage`, and `advancedAt` are required.
- A record does not imply an approved breeding plan or release.

## 6. Deferred questions

- D-102: Should `populationDbId` be required? (Current: required.)
- D-103: Should advancement require a GenX `BreedingPipeline` reference?
  (Current: optional, not required.)
- D-104: Should stages be a governed vocabulary? (Current: free string.)

## 7. Classification

Primary domain: D2 — Breeding Programs and Experimental Design.
Cross-cutting: C1, C2, C3 (POST), C6, C9.