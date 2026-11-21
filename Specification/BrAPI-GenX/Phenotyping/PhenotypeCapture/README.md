# BrAPI-GenX — Phenotype Capture (Observation Workflow)

Phenotype capture records the act of capturing observations for an observation
unit, including quality flags, missingness, corrections, and image linkage.
BrAPI v2.1 standardizes observations and observation units but not the capture
workflow, quality, or correction lifecycle.

- `POST /genx/v1/phenotype-captures` (`genxRecordPhenotypeCapture`) records one
  `PhenotypeCapture` (`Schemas/PhenotypeCaptureNewRequest.yaml`). Same
  `phenotypeCaptureDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/phenotype-captures` (`genxListPhenotypeCaptures`) lists
  captures, optionally filtered by study, observation unit, or capture method.
- `GET /genx/v1/phenotype-captures/{phenotypeCaptureDbId}`
  (`genxGetPhenotypeCapture`) retrieves one capture.

Details and falsifiers: `../../RFCs/RFC-012-Phenotype-Capture.md`.