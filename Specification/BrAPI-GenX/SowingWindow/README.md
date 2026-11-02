# BrAPI-GenX — SowingWindow

SowingWindow records describe SowingWindow entries.
BrAPI v2.1 has no SowingWindow record.

- `POST /genx/v1/sowing-windows` (`genxRegisterSowingWindow`) registers one
  `SowingWindow` (`Schemas/SowingWindowNewRequest.yaml`). Same
  `sowingWindowDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/sowing-windows` (`genxListSowingWindows`) lists records,
  optionally filtered by status.
- `GET /genx/v1/sowing-windows/{sowingWindowDbId}`
  (`genxGetSowingWindow`) retrieves one record.

Details and falsifiers: `../RFC-130-SowingWindow.md`.
