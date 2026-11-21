# BrAPI-GenX — Ontology Term (Terminology)

Ontology term and synonym entries describe terms from external ontologies.
BrAPI v2.1 has no ontology term record.

- `POST /genx/v1/ontology-terms` (`genxRegisterOntologyTerm`) registers one
  `OntologyTermRecord` (`Schemas/OntologyTermNewRequest.yaml`). Same
  `ontologyTermDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/ontology-terms` (`genxListOntologyTerms`) lists entries,
  optionally filtered by status.
- `GET /genx/v1/ontology-terms/{ontologyTermDbId}`
  (`genxGetOntologyTerm`) retrieves one entry.

Details and falsifiers: `../../RFCs/RFC-085-Ontology-Term.md`.
