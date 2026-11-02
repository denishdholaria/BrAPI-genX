# BrAPI-GenX — Ontology Mapping (Terminology)

Ontology mapping and crosswalk entries describe mappings between ontologies.
BrAPI v2.1 has no ontology mapping record.

- `POST /genx/v1/ontology-mappings` (`genxRegisterOntologyMapping`) registers one
  `OntologyMapping` (`Schemas/OntologyMappingNewRequest.yaml`). Same
  `ontologyMappingDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/ontology-mappings` (`genxListOntologyMappings`) lists entries,
  optionally filtered by status.
- `GET /genx/v1/ontology-mappings/{ontologyMappingDbId}`
  (`genxGetOntologyMapping`) retrieves one entry.

Details and falsifiers: `../RFC-086-Ontology-Mapping.md`.
