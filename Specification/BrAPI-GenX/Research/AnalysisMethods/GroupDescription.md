# Group AnalysisMethods

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 009; not normative scientific analysis, validated mathematical inference, or independent production implementation.

The proposed `AnalysisMethod` resource defines a namespaced identity, a lifecycle state, `supersedes` or comparable version information where defined by its own schema, and proposed register/list/retrieve endpoints. The presence of a schema or request route does not itself establish successful numerical execution, reproducibility or independently tested persistence.

**Methods, provenance and scientific boundaries:** The draft versioned AnalysisMethod identity requires a name, opaque methodVersion, methodType and status, but inputSchemaRef, outputSchemaRef and implementationRef are optional. The presence of a method label or container tag does not establish reproducible executable behavior, versioned source integrity, scientific validity or external implementability. The registry's proposed revoked state is not proof that separately deployed job schedulers enforce revocation. Deferred design decisions beginning at D-24 and related questions in the governing RFC remain open. Endpoint navigation neighbors and textual identity descriptions are not verified foreign keys or published cross-system mappings.

**Sources:** [module overview](./README.md), [candidate result schema](./Schemas/AnalysisMethod.yaml), [registration request](./Schemas/AnalysisMethodNewRequest.yaml), [proposed operations](./AnalysisMethods_GET_POST.yaml), [RFC](../../RFCs/RFC-009-Analysis-Methods.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
