# BrAPI-GenX — Reusable List (Reference Data)

Reusable list and cohort records describe reusable germplasm/sample lists.
Official BrAPI v2.1 already defines generic `List` resources and
`/brapi/v2/lists` operations. The GenX proposal is an optional, namespaced,
immutable list/cohort record, not a replacement or an established identity
mapping to BrAPI Lists.

- `POST /genx/v1/reusable-lists` (`genxRegisterReusableList`) registers one
  `ReusableList` (`Schemas/ReusableListNewRequest.yaml`). Same
  `reusableListDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/reusable-lists` (`genxListReusableLists`) lists records,
  optionally filtered by status.
- `GET /genx/v1/reusable-lists/{reusableListDbId}`
  (`genxGetReusableList`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-090-Reusable-List.md`.
