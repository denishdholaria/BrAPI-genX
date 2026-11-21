# BrAPI-GenX — GWAS Result (Scientific Compute)

GWAS results record the output of a genome-wide association study, including
significant markers and top p-values. BrAPI v2.1 has no GWAS result record.

- `POST /genx/v1/gwas-results` (`genxRecordGwasResult`) registers one
  `GwasResult` (`Schemas/GwasResultNewRequest.yaml`). Same
  `gwasResultDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/gwas-results` (`genxListGwasResults`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/gwas-results/{gwasResultDbId}`
  (`genxGetGwasResult`) retrieves one result.

Details and falsifiers: `../../RFCs/RFC-047-Gwas-Result.md`.