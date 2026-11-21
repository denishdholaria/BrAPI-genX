# RFC-039 — Candidate Variety Lifecycle (Breeding)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D2).

## 1. Problem

BrAPI v2.1 has no candidate variety lifecycle record. Tracking candidate
varieties through submission, registration, and release is essential for
breeding. Without this record, variety progression cannot be audited or linked
to programs with provenance.

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
- Candidate varieties reference BrAPI Program by identifier; they do not
  duplicate that resource.
- A record is not a BrAPI Program and must not be treated as one.

## 5. Invariants

- A published `candidateVarietyDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- `varietyName` and `status` are required.
- A record does not imply an approved or released variety.

## 6. Deferred questions

- D-115: Should `status` transitions be recorded as separate events?
  (Current: status is a field on the record.)
- D-116: Should candidate varieties link to GenX `BreedingPipeline`?
  (Current: optional, not required.)
- D-117: Should `registeredAt` be required for registered status?
  (Current: optional.)

## 7. Classification

Primary domain: D2 — Breeding Programs and Experimental Design.
Cross-cutting: C1, C2, C3 (POST), C6, C9.