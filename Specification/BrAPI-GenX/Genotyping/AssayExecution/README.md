# BrAPI-GenX — Assay Execution (Genotyping)

AssayExecution is a candidate registration record, distinct from official
BrAPI version 2.1 Sample, CallSet and result resources. Its optional
`assayDbId` is not a validated link to GenX `assayDesignDbId`, and
registration does not establish that a laboratory run occurred.

- `POST /genx/v1/assay-executions` (`genxRegisterAssayExecution`) registers one
  `AssayExecution` (`Schemas/AssayExecutionNewRequest.yaml`). Same
  `assayExecutionDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/assay-executions` (`genxListAssayExecutions`) lists records,
  optionally filtered by status.
- `GET /genx/v1/assay-executions/{assayExecutionDbId}`
  (`genxGetAssayExecution`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-113-Assay-Execution.md`.
