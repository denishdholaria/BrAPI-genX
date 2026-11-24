# Group Crosswalk

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate (RFC-105), not a validated identity-equivalence service, a ratified mapping standard, or an official BrAPI version 2.1 extension.

This group proposes recording crosswalk metadata between source and target systems under a namespaced `crosswalkDbId`. Its record schema requires identity and lifecycle `status` (`active`, `superseded`, `withdrawn`), while `source` and `target` are optional plain strings; `supersedes` and provenance are also optional. Proposed operations register, list (with optional status filtering), and retrieve records. RFC-105 describes immutable publication, identical-body replay under one identity, and conflict on changed content with the same identity as candidate behavior.

**Boundaries:** The schema describes source and target **systems**, not a typed pair of germplasm identifiers or a mathematically defined, reversible mapping between entities. It must not be treated as proof of synonymy, biological identity, established ontology alignment, validation or endorsement. Existing official BrAPI germplasm identities retain their original authority. Requiredness of `source` and `target`, their vocabularies, and any linkage to the GenX `McpdAdapter` proposal remain unresolved as D-313 through D-315. Historical operation neighbors remain advisory rather than scientific relationships.

**Sources:** [Module overview](./README.md), [record schema](./Schemas/Crosswalk.yaml), [registration schema](./Schemas/CrosswalkNewRequest.yaml), [proposed operations](./Crosswalk_GET_POST.yaml), [RFC-105 proposal](../../RFCs/RFC-105-Crosswalk.md), and [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
