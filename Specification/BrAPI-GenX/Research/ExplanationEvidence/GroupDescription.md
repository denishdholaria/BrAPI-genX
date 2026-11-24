# Group ExplanationEvidence

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 137; not approved research governance, independently validated model evidence, or official Breeding Application Programming Interface (BrAPI) version 2.1 conformance.

The candidate `ExplanationEvidence` record defines a namespaced identifier, a required lifecycle `status` and optional descriptive content, `supersedes` and provenance. It offers draft register/list/retrieve operations. Immutable-publication and replay guarantees are proposed, not proven against a real persistent and independently implemented service.

**Evidence, reproducibility and human authority boundaries:** The explanation, confidence and uncertainty fields are optional free text; they provide no model identity, feature attribution method, reference dataset, numerical uncertainty, causal test, or faithfulness/validation result. A natural-language explanation is not proof of predictive validity or scientific causality. An operation or historical navigation neighbor does not establish scientific identity, validated causality, evidence sufficiency or permission to act. The questions beginning at D-409 remain unratified.

**Sources:** [module overview](./README.md), [candidate record schema](./Schemas/ExplanationEvidence.yaml), [registration schema](./Schemas/ExplanationEvidenceNewRequest.yaml), [draft operation](./ExplanationEvidence_GET_POST.yaml), [governing RFC](../../RFCs/RFC-137-ExplanationEvidence.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
