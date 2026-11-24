# BrAPI-GenX — Expression QTL (Scientific Compute)

ExpressionQtl proposes a record for expression quantitative trait loci (eQTL)
analysis, not a validated regulatory association. Its `qtls` data are
optional and unconstrained. No expression platform, tissue, sample identity,
statistical test, multiple-testing correction or effect-size model is required.

Official BrAPI version 2.1 records remain unchanged. A candidate eQTL object
does not establish gene regulation, statistical significance or causality.

- `POST /genx/v1/expression-qtls` (`genxRecordExpressionQtl`) registers one
  `ExpressionQtl` (`Schemas/ExpressionQtlNewRequest.yaml`). Same
  `expressionQtlDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/expression-qtls` (`genxListExpressionQtls`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/expression-qtls/{expressionQtlDbId}`
  (`genxGetExpressionQtl`) retrieves one result.

Details and falsifiers: `../../RFCs/RFC-058-Expression-Qtl.md`.