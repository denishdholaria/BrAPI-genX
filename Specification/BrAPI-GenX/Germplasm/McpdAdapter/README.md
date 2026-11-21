# BrAPI-GenX — MCPD Adapter (Germplasm)

MCPD adapter records describe MCPD source adapters.
BrAPI v2.1 has no MCPD adapter record.

- `POST /genx/v1/mcpd-adapters` (`genxRegisterMcpdAdapter`) registers one
  `McpdAdapter` (`Schemas/McpdAdapterNewRequest.yaml`). Same
  `mcpdAdapterDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/mcpd-adapters` (`genxListMcpdAdapters`) lists records,
  optionally filtered by status.
- `GET /genx/v1/mcpd-adapters/{mcpdAdapterDbId}`
  (`genxGetMcpdAdapter`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-103-Mcpd-Adapter.md`.
