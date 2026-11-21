# BrAPI-GenX — Assay Execution (Genotyping)

Assay execution records describe assay executions.
BrAPI v2.1 has no assay execution record.

- `POST /genx/v1/assay-executions` (`genxRegisterAssayExecution`) registers one
  `AssayExecution` (`Schemas/AssayExecutionNewRequest.yaml`). Same
  `assayExecutionDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/assay-executions` (`genxListAssayExecutions`) lists records,
  optionally filtered by status.
- `GET /genx/v1/assay-executions/{assayExecutionDbId}`
  (`genxGetAssayExecution`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-113-Assay-Execution.md`.
