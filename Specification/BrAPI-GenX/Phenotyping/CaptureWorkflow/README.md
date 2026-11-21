# BrAPI-GenX — Capture Workflow (Phenotyping)

Capture workflow records describe capture workflows.
BrAPI v2.1 has no capture workflow record.

- `POST /genx/v1/capture-workflows` (`genxRegisterCaptureWorkflow`) registers one
  `CaptureWorkflow` (`Schemas/CaptureWorkflowNewRequest.yaml`). Same
  `captureWorkflowDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/capture-workflows` (`genxListCaptureWorkflows`) lists records,
  optionally filtered by status.
- `GET /genx/v1/capture-workflows/{captureWorkflowDbId}`
  (`genxGetCaptureWorkflow`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-110-Capture-Workflow.md`.
