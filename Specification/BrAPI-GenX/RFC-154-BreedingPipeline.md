# RFC-154 — Breeding Pipeline (D2)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (D2).

## 1. Problem

BrAPI v2.1 has no place to record breeding pipeline records. Breeding pipelines
circulate without a stated type, breeding program reference, pipeline stage, or
provenance, so breeding program advancement cannot be tracked or audited.

## 2. Object

`BreedingPipeline` — one immutable breeding pipeline record, with its pipeline
type, breeding program reference, pipeline stage, target trait, and provenance.

## 3. Endpoints

- `GET /genx/v1/breeding-pipelines` (`genxListBreedingPipelines`)
- `POST /genx/v1/breeding-pipelines` (`genxRegisterBreedingPipeline`)
- `GET /genx/v1/breeding-pipelines/{breedingPipelineDbId}` (`genxGetBreedingPipeline`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `breedingPipelineDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-454: Should `targetTrait` be required? (Current: optional.)
- D-455: Should `pipelineType` be a controlled vocabulary? (Current: free-form string.)
- D-456: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: D2.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
