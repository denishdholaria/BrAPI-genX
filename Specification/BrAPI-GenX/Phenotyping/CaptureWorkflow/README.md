# BrAPI-GenX — Capture Workflow (Phenotyping)

Capture workflow records describe capture workflows.
BrAPI version 2.1 already models Studies, Observation Units, observations, variables and metadata about data collection. A separate capture-workflow record might describe orchestration, but this candidate contains only an optional workflowType string and lifecycle metadata; it does not define a runnable workflow, observation association or authenticated collection protocol.

- `POST /genx/v1/capture-workflows` (`genxRegisterCaptureWorkflow`) registers one
  `CaptureWorkflow` (`Schemas/CaptureWorkflowNewRequest.yaml`). Same
  `captureWorkflowDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/capture-workflows` (`genxListCaptureWorkflows`) lists records,
  optionally filtered by status.
- `GET /genx/v1/capture-workflows/{captureWorkflowDbId}`
  (`genxGetCaptureWorkflow`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-110-Capture-Workflow.md`.
