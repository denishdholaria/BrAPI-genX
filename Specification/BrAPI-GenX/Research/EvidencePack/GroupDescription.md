# Group EvidencePack

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 122; not approved research governance, independently validated model evidence, or official Breeding Application Programming Interface (BrAPI) version 2.1 conformance.

The candidate `EvidencePack` record defines a namespaced identifier, a required lifecycle `status` and optional descriptive content, `supersedes` and provenance. It offers draft register/list/retrieve operations. Immutable-publication and replay guarantees are proposed, not proven against a real persistent and independently implemented service.

**Evidence, reproducibility and human authority boundaries:** The optional `contents` field is a plain string, not a typed artifact manifest with immutable identifiers, hashes, verified provenance chain, license or completeness check. A record named `reproducibility pack` does not demonstrate reproducibility, repository storage, accessible datasets or integrity of referenced evidence. An operation or historical navigation neighbor does not establish scientific identity, validated causality, evidence sufficiency or permission to act. The questions beginning at D-364 remain unratified.

**Sources:** [module overview](./README.md), [candidate record schema](./Schemas/EvidencePack.yaml), [registration schema](./Schemas/EvidencePackNewRequest.yaml), [draft operation](./EvidencePack_GET_POST.yaml), [governing RFC](../../RFCs/RFC-122-EvidencePack.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
