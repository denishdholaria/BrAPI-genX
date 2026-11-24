# BrAPI-GenX — Terminology Version (Terminology)

Terminology version entries describe versioned terminology/vocabulary records.
Official BrAPI version 2.1 ontology metadata already contains a `version` field and `/brapi/v2/ontologies` operations. The GenX proposal concerns separate terminology release records, not replacement ontology version semantics or a typed VariableTerm linkage.

- `POST /genx/v1/terminology-versions` (`genxRegisterTerminologyVersion`) registers one
  `TerminologyVersion` (`Schemas/TerminologyVersionNewRequest.yaml`). Same
  `terminologyVersionDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/terminology-versions` (`genxListTerminologyVersions`) lists entries,
  optionally filtered by status.
- `GET /genx/v1/terminology-versions/{terminologyVersionDbId}`
  (`genxGetTerminologyVersion`) retrieves one entry.

Details and falsifiers: `../../RFCs/RFC-084-Terminology-Version.md`.
