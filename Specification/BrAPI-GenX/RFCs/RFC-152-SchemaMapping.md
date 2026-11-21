# RFC-152 — Schema Mapping (T/W/A)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (T/W/A).

## 1. Problem

BrAPI v2.1 has no place to record schema mappings. Schema mappings
circulate without a stated type, source, target, or provenance, so they
cannot be used for schema transformation.

## 2. Object

`SchemaMapping` — one immutable schema mapping record, with its mapping
type, source schema, target schema, mapping rules, and provenance.

## 3. Endpoints

- `GET /genx/v1/schema-mappings` (`genxListSchemaMappings`)
- `POST /genx/v1/schema-mappings` (`genxRegisterSchemaMapping`)
- `GET /genx/v1/schema-mappings/{schemaMappingDbId}` (`genxGetSchemaMapping`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `schemaMappingDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-457: Should `mappingRules` be required? (Current: optional.)
- D-458: Should `schemaType` be a controlled vocabulary? (Current: free-form string.)
- D-459: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting T/W/A).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
