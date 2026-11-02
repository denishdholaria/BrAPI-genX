# BrAPI-GenX — Trial Network (Experimental Design)

Trial network and MET design records describe trial networks.
BrAPI v2.1 has no trial network record.

- `POST /genx/v1/trial-networks` (`genxRegisterTrialNetwork`) registers one
  `TrialNetwork` (`Schemas/TrialNetworkNewRequest.yaml`). Same
  `trialNetworkDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/trial-networks` (`genxListTrialNetworks`) lists records,
  optionally filtered by status.
- `GET /genx/v1/trial-networks/{trialNetworkDbId}`
  (`genxGetTrialNetwork`) retrieves one record.

Details and falsifiers: `../RFC-109-Trial-Network.md`.
