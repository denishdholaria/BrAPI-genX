# Group OntologyTerm

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 085, not an authoritative external ontology registry or an official Breeding Application Programming Interface (BrAPI) version 2.1 resource.

This group sketches immutable `OntologyTermRecord` metadata identified by namespaced `ontologyTermDbId` with required lifecycle `status` (`active`, `superseded`, `withdrawn`). Proposed optional `term`, string-array `synonyms`, `ontology` name, `supersedes`, and provenance fields describe an entry. Proposed operations register, list with an optional status filter, and retrieve it. Identical-body replay and changed-body conflict are specified only as **candidate behavior**.

**Boundaries:** A source ontology name and term text are insufficient to identify a particular versioned ontology class or to attest to synonym quality, preferred labels, external concept identifiers, language scope, or scientific endorsement. No typed `VariableTerm` link appears in the current record schema (D-255 remains open); requiredness of `term` (D-253) and governance of `ontology` (D-254) are also unresolved. Official BrAPI observation variables retain their published semantics, including their existing ontology metadata. Operation-neighbor navigation cannot be interpreted as semantic identity.

**Sources:** [Module overview](./README.md), [record schema](./Schemas/OntologyTerm.yaml), [registration schema](./Schemas/OntologyTermNewRequest.yaml), [proposed operations](./OntologyTerm_GET_POST.yaml), [RFC-085](../../RFCs/RFC-085-Ontology-Term.md), [official BrAPI observation variables](../../../BrAPI-Phenotyping/ObservationVariables/README.md), and [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
