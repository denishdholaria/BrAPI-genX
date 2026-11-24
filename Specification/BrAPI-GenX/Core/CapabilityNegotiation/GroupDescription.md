# Group CapabilityNegotiation

**Status:** BrAPI-GenX **DEFERRED** proposal under RFC-153. The source schemas and operation drafts are retained for review; they do not define a ratified negotiation protocol or an official BrAPI version 2.1 capability.

This group sketches immutable `CapabilityNegotiation` records identified by a namespaced `capabilityNegotiationDbId`. The record schema requires an identifier and lifecycle `status` (`active`, `superseded`, or `withdrawn`); `negotiationType`, `counterparty`, `lastSeen`, `supersedes`, and provenance are optional. Proposed GenX operations register one record, list records with an optional status filter, and retrieve a record. The draft's same-identifier identical-body replay and changed-body conflict are specifications **to be tested**, not proof of deployed persistence or correct concurrency.

**Boundaries:** Retaining a negotiation record does not demonstrate a completed two-party handshake, agreement on compatible functionality, authentication, authorization, or live service discovery. This record proposal is distinct from the read-only `ServerInfoV3` capability advertisement; neither schema establishes a typed join between them. RFC-153 leaves `lastSeen` requiredness, `negotiationType` vocabulary, and any `ResearchAsset` linkage open. Do not promote this deferred draft or its operation-neighbor navigation to semantic authority.

**Sources:** [Module overview](./README.md), [record schema](./Schemas/CapabilityNegotiation.yaml), [registration schema](./Schemas/CapabilityNegotiationNewRequest.yaml), [draft operations](./CapabilityNegotiation_GET_POST.yaml), [deferred RFC-153](../../RFCs/RFC-153-CapabilityNegotiation.md), and [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
