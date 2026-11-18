# RFC-035 — Population Advancement (Breeding)

- Status: proposal, non-normative; retain and refine as an actual execution event.
- Supersedes: none.
- Decision: D-BP-10 — actual population progression remains a distinct GenX event; whenever scheme-local stage identifiers are supplied, they must resolve through the exact scheme version.
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
- `advancedAt` is required. Scheme stage IDs are not required when the event is outside a registered scheme.
- A record does not imply an approved breeding plan or release.

## 6. Deferred questions

- D-102: Which BrAPI resource types are valid targets for `populationReference`? (Current: authority-qualified reference; Germplasm is the default when the population/family is represented as biological material.)
- D-103: Should advancement require a registered pipeline or scheme context? (Current: both are optional; events outside a registered strategy remain valid.)
- D-104: Should scheme stages use a global vocabulary? (Current: no; stage IDs are local to an exact immutable scheme version and are resolved through `schemeContext`.)

## 7. Classification

Primary domain: D2 — Breeding Programs and Experimental Design.
Cross-cutting: C1, C2, C3 (POST), C6, C9.

## 8. Pipeline and scheme context

The current candidate schema uses nested optional context envelopes:
- `pipelineContext` contains the stable `breedingPipelineDbId` and exact `breedingPipelineVersionDbId`;
- `schemeContext` contains `breedingSchemeDbId` and exact `breedingSchemeVersionDbId`, with optional `fromStageId` and `toStageId` nested inside it.

If both contexts are supplied, the referenced pipeline revision must contain the exact scheme version in one of its embedded scheme bindings. A scheme context without pipeline context is valid; an event with neither context is valid when no registered strategy governed it. An event must not put stage identifiers at the top level.

`PopulationAdvancement` remains an actual material-progression event. It does not own, define, or mutate the scheme's permitted transition graph. The transition graph resides in the immutable `BreedingSchemeVersion` embedded in the pipeline revision.
