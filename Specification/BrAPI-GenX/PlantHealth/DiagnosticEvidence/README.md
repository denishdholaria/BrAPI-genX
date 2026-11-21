# BrAPI-GenX — DiagnosticEvidence

DiagnosticEvidence records describe DiagnosticEvidence entries.
BrAPI v2.1 has no DiagnosticEvidence record.

- `POST /genx/v1/diagnostic-evidences` (`genxRegisterDiagnosticEvidence`) registers one
  `DiagnosticEvidence` (`Schemas/DiagnosticEvidenceNewRequest.yaml`). Same
  `diagnosticEvidenceDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/diagnostic-evidences` (`genxListDiagnosticEvidences`) lists records,
  optionally filtered by status.
- `GET /genx/v1/diagnostic-evidences/{diagnosticEvidenceDbId}`
  (`genxGetDiagnosticEvidence`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-124-DiagnosticEvidence.md`.
