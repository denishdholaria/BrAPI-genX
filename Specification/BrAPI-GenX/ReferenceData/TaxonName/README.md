# BrAPI-GenX — Taxon Name (Reference Data)

Taxon name and synonym entries describe scientific names for crops and species.
Official BrAPI version 2.1 Germplasm already provides genus, species, species authority and source-scoped taxon identifiers. This separate GenX candidate is not an accepted-name registry or a typed Germplasm reference.

- `POST /genx/v1/taxon-names` (`genxRegisterTaxonName`) registers one
  `TaxonName` (`Schemas/TaxonNameNewRequest.yaml`). Same
  `taxonNameDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/taxon-names` (`genxListTaxonNames`) lists entries,
  optionally filtered by status.
- `GET /genx/v1/taxon-names/{taxonNameDbId}`
  (`genxGetTaxonName`) retrieves one entry.

Details and falsifiers: `../../RFCs/RFC-080-Taxon-Name.md`.
