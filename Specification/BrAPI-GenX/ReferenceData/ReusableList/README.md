# BrAPI-GenX — Reusable List (Reference Data)

Reusable list and cohort records describe reusable germplasm/sample lists.
BrAPI v2.1 has no reusable list record.

- `POST /genx/v1/reusable-lists` (`genxRegisterReusableList`) registers one
  `ReusableList` (`Schemas/ReusableListNewRequest.yaml`). Same
  `reusableListDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/reusable-lists` (`genxListReusableLists`) lists records,
  optionally filtered by status.
- `GET /genx/v1/reusable-lists/{reusableListDbId}`
  (`genxGetReusableList`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-090-Reusable-List.md`.
