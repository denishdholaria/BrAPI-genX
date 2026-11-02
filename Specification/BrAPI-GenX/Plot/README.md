# BrAPI-GenX — Plot (Experimental Design)

Plot identity records describe plots in experimental designs.
BrAPI v2.1 has no plot identity record.

- `POST /genx/v1/plots` (`genxRegisterPlot`) registers one
  `Plot` (`Schemas/PlotNewRequest.yaml`). Same
  `plotDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/plots` (`genxListPlots`) lists records,
  optionally filtered by field or status.
- `GET /genx/v1/plots/{plotDbId}`
  (`genxGetPlot`) retrieves one record.

Details and falsifiers: `../RFC-107-Plot.md`.
