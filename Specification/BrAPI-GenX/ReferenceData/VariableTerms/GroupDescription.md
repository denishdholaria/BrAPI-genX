# Group: Versioned Observation-Variable Terms

**Status:** BrAPI-GenX candidate contract with fixture-based contract validation (RFC-002); not an official or normatively accepted BrAPI extension. Independent security and interoperability review remain outstanding.

The group proposes versioned, namespace-qualified `VariableTerm` records to prevent conflicting terminology redefinitions from silently replacing earlier definitions. Proposed operations allow publishing a new term version, listing versions, and retrieving a term by identity and optional version. Under the current candidate behavior, replay of an identical `(variableDbId, version)` does not create a second version; different content under the same identity conflicts.

**Boundaries:** Existing BrAPI Trait, Method, Scale and ObservationVariable contracts retain their published meanings. This group does not establish an automatic equivalence to any official observation-variable resource or ontology identifier. Deprecation is represented in the record rather than destructive deletion; the semantics of version ordering and the complete external ontology authority model remain subject to pending decisions D-05 and D-06.

**Sources:** [Module contract](./README.md), [term schema](./Schemas/VariableTerm.yaml), [draft operations](./VariableTerms_GET_POST.yaml), [RFC-002](../../RFCs/RFC-002-Variable-Term-Governance.md), and [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
