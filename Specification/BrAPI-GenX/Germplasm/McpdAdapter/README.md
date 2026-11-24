# BrAPI-GenX — MCPD Adapter (Germplasm)

MCPD adapter records describe MCPD source adapters.
Official BrAPI version 2.1 already provides `GET /brapi/v2/germplasm/{germplasmDbId}/mcpd` and a GermplasmMCPD schema. This candidate adapter record includes only an optional source string and provenance; it does not execute a transform, define a verified data mapping, or replace the official MCPD representation.

- `POST /genx/v1/mcpd-adapters` (`genxRegisterMcpdAdapter`) registers one
  `McpdAdapter` (`Schemas/McpdAdapterNewRequest.yaml`). Same
  `mcpdAdapterDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/mcpd-adapters` (`genxListMcpdAdapters`) lists records,
  optionally filtered by status.
- `GET /genx/v1/mcpd-adapters/{mcpdAdapterDbId}`
  (`genxGetMcpdAdapter`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-103-Mcpd-Adapter.md`.
