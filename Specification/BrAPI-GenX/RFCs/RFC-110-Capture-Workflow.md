# RFC-110 — Capture Workflow (Phenotyping)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D4).

## 1. Problem

BrAPI v2.1 has no place to record capture workflows. Capture workflows are the
routine reference for phenotyping. Without a record, workflows arrive as
unversioned notes with no stated type or provenance, so they cannot be audited
or reproduced.

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
- Capture workflow records reference BrAPI `Study`/`Location` by identifier;
  they do not duplicate those resources.
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
