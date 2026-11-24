# RFC-106 — Treatment Assignment (Experimental Design)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D6).

## 1. Problem

BrAPI v2.1 Observation Unit `treatments` already represents applied treatment-factor values, while Events record actual interventions. This candidate explores separate planned assignment records, but neither randomized allocation nor field execution is validated by its current minimal schema.

## 2. Object

`TreatmentAssignment` — one immutable treatment assignment record, with its
field linkage, treatment, and provenance.

## 3. Endpoints

- `GET /genx/v1/treatment-assignments` (`genxListTreatmentAssignments`)
- `POST /genx/v1/treatment-assignments` (`genxRegisterTreatmentAssignment`)
- `GET /genx/v1/treatment-assignments/{treatmentAssignmentDbId}` (`genxGetTreatmentAssignment`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- The draft only has optional free-text `fieldDbId`; no typed BrAPI `studyDbId`, `locationDbId` or `observationUnitDbId` exists. No authoritative cross-resource join is established.
- A record is not a BrAPI Observation and must not be treated as one.

## 5. Invariants

- A published `treatmentAssignmentDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the assignment was randomized, validated, applied or endorsed. `fieldDbId`, `treatment` and provenance are optional, and no `experimentalDesignDbId` link exists.

## 6. Deferred questions

- D-316: Should `fieldDbId` be required? (Current: optional.)
- D-317: Should `treatment` be a controlled vocabulary? (Current: free-form
  string.)
- D-318: Should records link to GenX `ExperimentalDesign`? (Current: no
  link.)

## 7. Classification

Primary domain: D6 — Field Agronomy and Crop Operations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
