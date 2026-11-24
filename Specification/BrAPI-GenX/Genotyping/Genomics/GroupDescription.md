# Group Genomics — External Variant Matrix References

**Status:** BrAPI-GenX candidate profile for external variant-matrix references (RFC-005), supported by contract-validation fixtures but not a normative extension to official BrAPI version 2.1.

The group proposes `VariantMatrix` metadata that identifies a referenced matrix artifact, its scientific context and its content digest. Register/list/retrieve operations manage **references** rather than serving arbitrary subsets of large matrix bytes. The candidate contract expects downstream byte delivery through a separately specified retrieval protocol or transport, with integrity checks matched to the declared artifact.

**Scope boundary:** This module does **not** redefine official BrAPI `Calls`, `Variants`, or `VariantSets`, nor does it guarantee that a registered digest makes underlying scientific genotypes accurate. Data Repository Service (DRS), htsget and Hypertext Transfer Protocol Secure (HTTPS) retrieval have their own authorization and transport semantics. Pangenome graph encodings and some specialized matrix slicing remain unresolved; a GenX catalogue link must not imply a valid conversion or scientific equivalence.

**Sources:** [Module contract](./README.md), [matrix schema](./Schemas/VariantMatrix.yaml), [candidate operations](./VariantMatrices_GET_POST.yaml), [RFC-005](../../RFCs/RFC-005-Variant-Matrix-References.md), and [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
