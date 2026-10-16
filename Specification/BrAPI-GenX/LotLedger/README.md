# BrAPI GenX — Seed-Lot Ledger

Append-only, idempotent movement facts per seed lot. Retries never duplicate;
conflicts never merge; balances are derived, never stored.

- `POST /brapi/v3/seedlots/{seedLotDbId}/ledger` (`genxAppendSeedLotLedgerEntry`) appends a `LotLedgerEntry`
  (`Schemas/LotLedgerEntryNewRequest.yaml`). Same `idempotencyKey` +
  identical body replays the existing entry; same key + different body is
  rejected with `409`.
- `GET /brapi/v3/seedlots/{seedLotDbId}/ledger` (`genxListSeedLotLedgerEntries`) reads entries in per-lot `position`
  order with standard pagination. Positions are source-local cursors; no
  global ordering is claimed.

Corrections are new reversing entries, never edits: there is no `PUT` or
`DELETE`. Details and falsifiers: `../RFC-003-Seed-Lot-Ledger.md`.
