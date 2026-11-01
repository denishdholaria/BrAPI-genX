# RFC-018 — Experimental Design (Trial Layout)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (D2).

## 1. Problem

BrAPI v2.1 standardizes studies and observation units but not the experimental
design: layout, replication, randomization, and treatment assignment. Without
this record, trial structure and randomization cannot be audited or reproduced.

## 2. Object

`ExperimentalDesign` — one immutable experimental design record.

## 3. Endpoints

- `GET /genx/v1/experimental-designs` (`genxListExperimentalDesigns`)
- `POST /genx/v1/experimental-designs` (`genxRegisterExperimentalDesign`)
- `GET /genx/v1/experimental-designs/{experimentalDesignDbId}` (`genxGetExperimentalDesign`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Experimental designs reference BrAPI Study by identifier; they do not
  duplicate that resource.
- A design is not a BrAPI Study or Observation Unit and must not be treated as
  one.

## 5. Invariants

- A published `experimentalDesignDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional designs linked by `supersedes`.
- `designType`, `replicationCount`, and `treatmentAssignments` are recorded,
  not inferred.
- A design does not imply an approved protocol or release.

## 6. Deferred questions

- D-51: Should `treatmentAssignments` require BrAPI ObservationUnit
  references? (Current: free-text plot IDs.)
- D-52: Should randomization seed be required? (Current: optional.)
- D-53: Should block/replication be separate records? (Current: embedded.)

## 7. Classification

Primary domain: D2 — Breeding Programs and Experimental Design.
Cross-cutting: C1, C2, C3 (POST), C6, C9.