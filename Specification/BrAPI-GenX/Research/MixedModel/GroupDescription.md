# Group MixedModel

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 048; not normative scientific analysis, validated mathematical inference, or independent production implementation.

The proposed `MixedModelResult` resource defines a namespaced identity, a lifecycle state, `supersedes` or comparable version information where defined by its own schema, and proposed register/list/retrieve endpoints. The presence of a schema or request route does not itself establish successful numerical execution, reproducibility or independently tested persistence.

**Methods, provenance and scientific boundaries:** The required AnalysisMethod identifier lacks a pinned method version; optional varianceComponents and blupValues are unstructured objects with no defined genotype identity, trait scale, covariance structure, residual model, unit, estimation method or standard errors. Such entries are not proof of an evaluated Best Linear Unbiased Prediction (BLUP) analysis or genetic merit. Deferred design decisions beginning at D-142 and related questions in the governing RFC remain open. Endpoint navigation neighbors and textual identity descriptions are not verified foreign keys or published cross-system mappings.

**Sources:** [module overview](./README.md), [candidate result schema](./Schemas/MixedModelResult.yaml), [registration request](./Schemas/MixedModelResultNewRequest.yaml), [proposed operations](./MixedModel_GET_POST.yaml), [RFC](../../RFCs/RFC-048-Mixed-Model.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
