# BrAPI-GenX — GWAS Result (Scientific Compute)

GwasResult proposes metadata for a genome-wide association study (GWAS), not a
statistically validated or reproducible analysis. Only result identity and the
analysis-method identifier are mandatory in a registration request; marker count,
smallest p-value, study, job, provenance and result payload are optional.

No schema-enforced association threshold, multiple-testing correction, exact
method version, or scientific comparability rule is supplied. This is a draft
GenX record, not a replacement for official BrAPI version 2.1 resources.

- `POST /genx/v1/gwas-results` (`genxRecordGwasResult`) registers one
  `GwasResult` (`Schemas/GwasResultNewRequest.yaml`). Same
  `gwasResultDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/gwas-results` (`genxListGwasResults`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/gwas-results/{gwasResultDbId}`
  (`genxGetGwasResult`) retrieves one result.

Details and falsifiers: `../../RFCs/RFC-047-Gwas-Result.md`.