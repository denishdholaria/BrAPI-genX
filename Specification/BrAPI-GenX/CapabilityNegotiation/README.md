# BrAPI-GenX — CapabilityNegotiation

CapabilityNegotiation records describe CapabilityNegotiation entries.
BrAPI v2.1 has no CapabilityNegotiation record.

- `POST /genx/v1/capability-negotiations` (`genxRegisterCapabilityNegotiation`) registers one
  `CapabilityNegotiation` (`Schemas/CapabilityNegotiationNewRequest.yaml`). Same
  `capabilityNegotiationDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/capability-negotiations` (`genxListCapabilityNegotiations`) lists records,
  optionally filtered by status.
- `GET /genx/v1/capability-negotiations/{capabilityNegotiationDbId}`
  (`genxGetCapabilityNegotiation`) retrieves one record.

Details and falsifiers: `../RFC-153-CapabilityNegotiation.md`.
