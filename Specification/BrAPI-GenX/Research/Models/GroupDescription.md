# Group Models — Model Registry and Inference

**Status:** BrAPI-GenX candidate contract described by RFC-004, with contract-validation evidence but no completed independent security or deployment conformance.

This group proposes identity, versioning, provenance and artifact references for computational models. A `ModelArtifact` associates model identity and version with input/output assumptions and a fingerprint or artifact digest under its declared candidate schema. Separate registration, listing and retrieval operations provide the metadata surface. Executing model inference is deliberately handled through the **Jobs** resource with an explicitly advertised job type, not through an invented direct model-execution endpoint.

**Scope boundary:** A model's recorded lifecycle status does not establish that its predictions are scientifically validated, safe for a particular crop or approved for operational decisions. Artifact byte transport, actor permissions, revocation governance, independent model evaluation, and the exact cryptographic digest/profile remain distinct requirements. The project accepts separate digest and idempotency architectures in D-02, D-24 and D-25; those decisions do not prove that a particular model registration is authorized or reproducible.

**Sources:** [Module scope](./README.md), [model schema](./Schemas/ModelArtifact.yaml), [model operations](./Models_GET_POST.yaml), [RFC-004](../../RFCs/RFC-004-Model-Registry.md), and [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
