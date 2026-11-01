# BrAPI-GenX — Analysis Method Registry

Analysis methods get identities, versions, input/output contracts, and a
revocable lifecycle. Scientific results and jobs can then name the exact method
and version used, so analyses are reproducible and comparable. BrAPI v2.1 has
no equivalent record; it standardizes data resources, not the analytical
methods applied to them.

- `POST /genx/v1/analysis-methods` (`genxRegisterAnalysisMethod`) registers an
  `AnalysisMethod` (`Schemas/AnalysisMethodNewRequest.yaml`). Same
  `(analysisMethodDbId, methodVersion)` + identical body replays; different
  body is rejected with `409`.
- `GET /genx/v1/analysis-methods` (`genxListAnalysisMethods`) lists method
  records.
- `GET /genx/v1/analysis-methods/{analysisMethodDbId}`
  (`genxGetAnalysisMethod`) retrieves one registered method version (latest
  created when `version` is omitted).

Details and falsifiers: `../RFC-009-Analysis-Methods.md`.