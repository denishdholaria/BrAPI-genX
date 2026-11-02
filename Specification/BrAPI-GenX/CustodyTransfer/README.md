# BrAPI-GenX — Custody Transfer (Genebank Conservation)

Custody transfer records capture the movement of a biological sample or seed
lot between responsible parties. BrAPI v2.1 has no chain-of-custody record.

- `POST /genx/v1/custody-transfers` (`genxRecordCustodyTransfer`) registers one
  `CustodyTransfer` (`Schemas/CustodyTransferNewRequest.yaml`). Same
  `custodyTransferDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/custody-transfers` (`genxListCustodyTransfers`) lists transfers,
  optionally filtered by sample, lot, or status.
- `GET /genx/v1/custody-transfers/{custodyTransferDbId}`
  (`genxGetCustodyTransfer`) retrieves one transfer.

Details and falsifiers: `../RFC-063-Custody-Transfer.md`.
