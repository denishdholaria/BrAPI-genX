# Group ResearchLocation

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate/proposed research reference, not an accepted official Breeding Application Programming Interface (BrAPI) version 2.1 resource or independently verified service. 

The historical/draft `ResearchLocation` metadata record defines a namespaced identifier, required lifecycle status, and optional name or descriptive data, `supersedes` and provenance. Existing proposed register/list/retrieve files must not be interpreted as accepted interoperability or persistent runtime conformance.

**Scope and reference-identity boundaries:** Official BrAPI version 2.1 already defines Locations. This proposed record has only an optional name besides its identifier/status/provenance. It lacks a geographic geometry, coordinates, CRS (Coordinate Reference System), official Location identifier or GenX Farm link. The need for separate identity is unproven; D-299/D-300 explicitly defer such references. Decisions D-298 and the remaining RFC questions are not resolved by an operation's existence. Advisory links are navigation only, not typed or legally authorized scientific relationships.

**Sources:** [module overview](./README.md), [candidate record schema](./Schemas/ResearchLocation.yaml), [registration schema](./Schemas/ResearchLocationNewRequest.yaml), [candidate operations](./ResearchLocation_GET_POST.yaml), [historical RFC](../../RFCs/RFC-100-Research-Location.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md), [official BrAPI locations](../../../BrAPI-Core/Locations/README.md).
