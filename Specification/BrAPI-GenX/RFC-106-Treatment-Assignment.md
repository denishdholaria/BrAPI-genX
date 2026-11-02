# RFC-106 — Treatment Assignment (Experimental Design)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (D6).

## 1. Problem

BrAPI v2.1 has no place to record treatment assignments. Treatment assignments
are the routine reference for experimental design. Without a record, assignments
arrive as unversioned notes with no stated field, treatment, or provenance, so
they cannot be audited or reproduced.

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
- Treatment assignment records reference BrAPI `Study`/`Location` by
  identifier; they do not duplicate those resources.
- A record is not a BrAPI Observation and must not be treated as one.

## 5. Invariants

- A published `treatmentAssignmentDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the assignment is validated or endorsed.

## 6. Deferred questions

- D-316: Should `fieldDbId` be required? (Current: optional.)
- D-317: Should `treatment` be a controlled vocabulary? (Current: free-form
  string.)
- D-318: Should records link to GenX `ExperimentalDesign`? (Current: no
  link.)

## 7. Classification

Primary domain: D6 — Field Agronomy and Crop Operations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
