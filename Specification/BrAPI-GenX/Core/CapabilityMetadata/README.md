# BrAPI-GenX — Capability Metadata (Reference Data)

Capability metadata records describe server and profile capabilities.
BrAPI v2.1 has no capability metadata record.

- `POST /genx/v1/capability-metadata` (`genxRegisterCapabilityMetadata`) registers one
  `CapabilityMetadata` (`Schemas/CapabilityMetadataNewRequest.yaml`). Same
  `capabilityMetadataDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/capability-metadata` (`genxListCapabilityMetadata`) lists records,
  optionally filtered by status.
- `GET /genx/v1/capability-metadata/{capabilityMetadataDbId}`
  (`genxGetCapabilityMetadata`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-099-Capability-Metadata.md`.
