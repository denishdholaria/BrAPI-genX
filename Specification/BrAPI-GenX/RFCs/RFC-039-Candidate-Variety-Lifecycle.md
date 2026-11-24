# RFC-039 — Candidate Variety Lifecycle (Breeding)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D2).

## 1. Problem

GenX proposes a separate breeding-program candidate-variety lifecycle
record alongside official BrAPI version 2.1 Germplasm and Program resources.
A local lifecycle label does not establish a legally recognized variety,
national registration, statutory release, seed certification or marketing
approval. The candidate schema has no required regulatory authority,
registration decision, jurisdiction, certificate or cross-resource join,
and therefore cannot independently substantiate any such claim.

## 2. Object

`CandidateVariety` — one immutable candidate variety lifecycle record.

## 3. Endpoints

- `GET /genx/v1/candidate-varieties` (`genxListCandidateVarieties`)
- `POST /genx/v1/candidate-varieties` (`genxRegisterCandidateVariety`)
- `GET /genx/v1/candidate-varieties/{candidateVarietyDbId}` (`genxGetCandidateVariety`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- `programDbId` is a required string reference but is not an
  authority-qualified, verified Program join. No `germplasmDbId`
  or `breedingPipelineDbId` is modelled; these resources remain separate.
- A record is not a BrAPI Program and must not be treated as one.

## 5. Invariants

- A published `candidateVarietyDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- `candidateVarietyDbId`, `programDbId`, and `varietyName` are required
  for registration; response `status` is required, but request `status`
  is optional and defaults to `candidate`.
- `registeredAt` is optional even if the enum status is `registered`.
  The `registered` and `released` labels are not independently
  verified government acts or compliance decisions.
- A record does not imply an approved, notified or commercially released
  variety, legal status, or validated germplasm identity.

## 6. Deferred questions

- D-115: Should `status` transitions be recorded as separate events?
  (Current: status is a field on the record.)
- D-116: Should candidate varieties link to GenX `BreedingPipeline`?
  (Current: no `breedingPipelineDbId` field is modelled.)
- D-117: Should `registeredAt` be required for registered status?
  (Current: optional.)

## 7. Classification

Primary domain: D2 — Breeding Programs and Experimental Design.
Cross-cutting: C1, C2, C3 (POST), C6, C9.