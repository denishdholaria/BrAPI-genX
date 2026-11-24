# Group SchemaMapping

**Status:** BrAPI-GenX **DEFERRED** proposal (RFC-152). Its stored-mapping structure is not an accepted transformation language, executable converter, scientific equivalence rule, or official BrAPI version 2.1 contract.

This module proposes an immutable `SchemaMapping` record identified by a namespaced `schemaMappingDbId`. Its draft schema requires identity and lifecycle `status` (`active`, `superseded`, `withdrawn`) and optionally records `schemaType`, `sourceSchema`, `targetSchema`, text `mappingRules`, `supersedes`, and provenance. Proposed GenX operations register one record, list records (optionally filtering by status), and retrieve one. The same-identifier replay and changed-body conflict rules are proposed contract behavior rather than observed service conformance.

**Boundaries:** The `mappingRules` property is an unconstrained string; these files do not define an executable or lossless translation semantics, value-unit conversions, preservation of biological meaning, or certified ontology correspondence. A record's presence must not cause downstream systems to assume that a transformation has run or passed validation. RFC-152 leaves rule requiredness (D-457), controlled vocabulary for `schemaType` (D-458), and any `ResearchAsset` linkage (D-459) undecided. Operation-neighbor navigation does not establish a typed resource relationship.

**Sources:** [Module overview](./README.md), [record schema](./Schemas/SchemaMapping.yaml), [registration schema](./Schemas/SchemaMappingNewRequest.yaml), [proposed operations](./SchemaMapping_GET_POST.yaml), [deferred RFC-152](../../RFCs/RFC-152-SchemaMapping.md), and [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
