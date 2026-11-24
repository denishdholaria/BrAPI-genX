# RFC-110 — Capture Workflow (Phenotyping)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D4).

## 1. Problem

BrAPI version 2.1 already models Studies, Observation Units, observations, variables and metadata about data collection. A separate capture-workflow record might describe orchestration, but this candidate contains only an optional workflowType string and lifecycle metadata; it does not define a runnable workflow, observation association or authenticated collection protocol.

## 2. Object

`CaptureWorkflow` — one immutable capture workflow record, with its workflow
type and provenance.

## 3. Endpoints

- `GET /genx/v1/capture-workflows` (`genxListCaptureWorkflows`)
- `POST /genx/v1/capture-workflows` (`genxRegisterCaptureWorkflow`)
- `GET /genx/v1/capture-workflows/{captureWorkflowDbId}` (`genxGetCaptureWorkflow`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- No typed link to an official BrAPI Observation or GenX PhenotypeCapture record is present in this candidate schema; D-330 remains unresolved. Matching labels or navigation links do not create scientific identity.
- A record is not a BrAPI Observation and must not be treated as one.

## 5. Invariants

- A published `captureWorkflowDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the workflow is validated or endorsed.

## 6. Deferred questions

- D-328: Should `workflowType` be required? (Current: optional.)
- D-329: Should `workflowType` be a controlled vocabulary? (Current: free-form
  string.)
- D-330: Should records link to GenX `PhenotypeCapture`? (Current: no link.)

## 7. Classification

Primary domain: D4 — Phenotyping and Plant Measurements.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
