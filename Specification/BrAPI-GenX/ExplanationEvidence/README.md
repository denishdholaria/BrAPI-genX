# BrAPI-GenX — ExplanationEvidence

ExplanationEvidence records describe ExplanationEvidence entries.
BrAPI v2.1 has no ExplanationEvidence record.

- `POST /genx/v1/explanation-evidences` (`genxRegisterExplanationEvidence`) registers one
  `ExplanationEvidence` (`Schemas/ExplanationEvidenceNewRequest.yaml`). Same
  `explanationEvidenceDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/explanation-evidences` (`genxListExplanationEvidences`) lists records,
  optionally filtered by status.
- `GET /genx/v1/explanation-evidences/{explanationEvidenceDbId}`
  (`genxGetExplanationEvidence`) retrieves one record.

Details and falsifiers: `../RFC-137-ExplanationEvidence.md`.
