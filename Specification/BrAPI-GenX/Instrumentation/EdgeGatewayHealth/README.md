# BrAPI-GenX — EdgeGatewayHealth

EdgeGatewayHealth records describe EdgeGatewayHealth entries.
BrAPI v2.1 has no EdgeGatewayHealth record.

- `POST /genx/v1/edge-gateway-healths` (`genxRegisterEdgeGatewayHealth`) registers one
  `EdgeGatewayHealth` (`Schemas/EdgeGatewayHealthNewRequest.yaml`). Same
  `edgeGatewayHealthDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/edge-gateway-healths` (`genxListEdgeGatewayHealths`) lists records,
  optionally filtered by status.
- `GET /genx/v1/edge-gateway-healths/{edgeGatewayHealthDbId}`
  (`genxGetEdgeGatewayHealth`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-151-EdgeGatewayHealth.md`.
