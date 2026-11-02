# BrAPI-GenX — Taxon Name (Reference Data)

Taxon name and synonym entries describe scientific names for crops and species.
BrAPI v2.1 has no taxon name record.

- `POST /genx/v1/taxon-names` (`genxRegisterTaxonName`) registers one
  `TaxonName` (`Schemas/TaxonNameNewRequest.yaml`). Same
  `taxonNameDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/taxon-names` (`genxListTaxonNames`) lists entries,
  optionally filtered by status.
- `GET /genx/v1/taxon-names/{taxonNameDbId}`
  (`genxGetTaxonName`) retrieves one entry.

Details and falsifiers: `../RFC-080-Taxon-Name.md`.
