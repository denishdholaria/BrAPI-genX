# BrAPI-GenX — Plot (Experimental Design)

Plot identity records describe plots in experimental designs.
BrAPI version 2.1 Observation Units already represent a `plot` hierarchy level. A separate GenX plot identity must be justified and mapped explicitly; absence of a `/plots` route does not prove a missing plot concept.

- `POST /genx/v1/plots` (`genxRegisterPlot`) registers one
  `Plot` (`Schemas/PlotNewRequest.yaml`). Same
  `plotDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/plots` (`genxListPlots`) lists records,
  optionally filtered by field or status.
- `GET /genx/v1/plots/{plotDbId}`
  (`genxGetPlot`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-107-Plot.md`.
