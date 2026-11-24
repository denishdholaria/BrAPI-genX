# Group CapabilityMetadata

**Status:** BrAPI-GenX candidate, **STRUCTURAL_DRAFT** under RFC-099; this is not a finalized capability-governance contract, a certified implementation, or an official BrAPI version 2.1 resource.

This group proposes a record of advertised server or profile capabilities under a namespaced `capabilityMetadataDbId`. Its draft `CapabilityMetadata` schema contains an optional `profile`, a free-form `capabilities` object, a required lifecycle `status` (`active`, `superseded`, or `withdrawn`), and optional `supersedes` and provenance fields. Proposed GenX operations register, list (with an optional status filter), and retrieve these records. RFC-099 specifies immutable publication, identical-body replay for the same identifier, and a conflict for different content under that identifier; those are **candidate behaviors**, not independent-service conformance evidence.

**Boundaries:** A recorded capability does not establish that an operation exists, is healthy, is authorized for a caller, or has been validated or endorsed. This record catalogue is distinct from the `ServerInfoV3` server-advertisement document; RFC-099 leaves a typed linkage between them undecided. The `capabilities` shape and requiredness of `profile` remain open (D-295 through D-297). Historical operation neighbors are advisory navigation, not proven typed scientific or authorization relationships.

**Sources:** [Module contract](./README.md), [record schema](./Schemas/CapabilityMetadata.yaml), [registration schema](./Schemas/CapabilityMetadataNewRequest.yaml), [draft operations](./CapabilityMetadata_GET_POST.yaml), [RFC-099 proposal](../../RFCs/RFC-099-Capability-Metadata.md), and [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
