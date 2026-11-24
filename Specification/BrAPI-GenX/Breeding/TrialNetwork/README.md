# BrAPI-GenX — Trial Network (Experimental Design)

Trial network and MET design records describe trial networks.
BrAPI version 2.1 already models Trials spanning multiple Studies and locations. A separately named GenX TrialNetwork record does not provide typed Study membership, environmental arrangement or a confirmed interoperability gap.

- `POST /genx/v1/trial-networks` (`genxRegisterTrialNetwork`) registers one
  `TrialNetwork` (`Schemas/TrialNetworkNewRequest.yaml`). Same
  `trialNetworkDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/trial-networks` (`genxListTrialNetworks`) lists records,
  optionally filtered by status.
- `GET /genx/v1/trial-networks/{trialNetworkDbId}`
  (`genxGetTrialNetwork`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-109-Trial-Network.md`.
