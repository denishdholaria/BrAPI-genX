# RFC-018 — Experimental Design (Trial Layout)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D2).

## 1. Problem

BrAPI v2.1 `StudyNewRequest.experimentalDesign` already records experimental-design description and an ontology reference; Observation Unit hierarchy and positions encode plot/block layout and treatment metadata. This draft explores a separate versioned identity and planned allocation, but its incremental value and scientific reproducibility are not yet demonstrated.

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
- Experimental designs store a required `studyDbId` string, but the draft does not validate an authoritative BrAPI Study link or replace official design metadata.
- A design is not a BrAPI Study or Observation Unit and must not be treated as
  one.

## 5. Invariants

- A published `experimentalDesignDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional designs linked by `supersedes`.
- `designType` is required; `replicationCount`, `randomizationSeed` and `treatmentAssignments` are optional. No allocation balance, complete plot identity mapping or statistically reproducible design is validated.
- A design does not imply an approved protocol or release.

## 6. Deferred questions

- D-51: Should `treatmentAssignments` require BrAPI ObservationUnit
  references? (Current: free-text plot IDs.)
- D-52: Should randomization seed be required? (Current: optional.)
- D-53: Should block/replication be separate records? (Current: embedded.)

## 7. Classification

Primary domain: D2 — Breeding Programs and Experimental Design.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
