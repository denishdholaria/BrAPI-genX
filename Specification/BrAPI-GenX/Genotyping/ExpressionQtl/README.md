# BrAPI-GenX — Expression QTL (Scientific Compute)

Expression QTL results record expression quantitative trait loci and provenance.
BrAPI v2.1 has no expression QTL result record.

- `POST /genx/v1/expression-qtls` (`genxRecordExpressionQtl`) registers one
  `ExpressionQtl` (`Schemas/ExpressionQtlNewRequest.yaml`). Same
  `expressionQtlDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/expression-qtls` (`genxListExpressionQtls`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/expression-qtls/{expressionQtlDbId}`
  (`genxGetExpressionQtl`) retrieves one result.

Details and falsifiers: `../../RFCs/RFC-058-Expression-Qtl.md`.