# BrAPI-GenX — SchemaMapping

SchemaMapping records describe SchemaMapping entries.
BrAPI v2.1 has no SchemaMapping record.

- `POST /genx/v1/schema-mappings` (`genxRegisterSchemaMapping`) registers one
  `SchemaMapping` (`Schemas/SchemaMappingNewRequest.yaml`). Same
  `schemaMappingDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/schema-mappings` (`genxListSchemaMappings`) lists records,
  optionally filtered by status.
- `GET /genx/v1/schema-mappings/{schemaMappingDbId}`
  (`genxGetSchemaMapping`) retrieves one record.

Details and falsifiers: `../RFC-152-SchemaMapping.md`.
