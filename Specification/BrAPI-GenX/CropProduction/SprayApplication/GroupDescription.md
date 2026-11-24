# Group SprayApplication

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 081; not a validated agronomic event ledger, official Breeding Application Programming Interface (BrAPI) version 2.1 resource, or independently tested persistent implementation.

The proposed `SprayApplication` contract defines an independently namespaced identity, optional `supersedes` and provenance metadata, and candidate operations for registration, listing and retrieval. The actual required scientific fields and lifecycle status vary by resource; their documented immutable publication and identical-body replay are candidate expectations, not demonstrated persistence guarantees.

**Agronomic and interoperability boundaries:** The rate is an unconstrained string; active product, formulation, dose unit, equipment calibration, operator, treatment area, target, withholding interval and legal label conditions are not validated. An `active` record is a lifecycle state, not proof that an intervention occurred or complied with jurisdictional pesticide rules. The optional fieldDbId is not a typed Location or FieldScouting reference. D-242 and D-243 remain undecided. Open scientific-design decisions include D-241 and the remaining unresolved questions in its governing RFC. Operation-neighbor links do not automatically establish biological identity, verified delivery, causality or transaction effects.

**Sources:** [module overview](./README.md), [record schema](./Schemas/SprayApplication.yaml), [registration schema](./Schemas/SprayApplicationNewRequest.yaml), [draft operation](./SprayApplication_GET_POST.yaml), [governing RFC](../../RFCs/RFC-081-Spray-Application.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
