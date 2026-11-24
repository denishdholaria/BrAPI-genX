# Group IpmStrategy

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 125; not a scientifically validated recommendation, official Breeding Application Programming Interface (BrAPI) version 2.1 contract, or independently verified service.

The `IpmStrategy` record requires its namespaced identifier and a lifecycle `status` (`active`, `superseded`, `withdrawn`), while `strategyName`, `targetPestOrDisease`, `strategyType`, `tactics`, `supersedes`, and provenance are optional. The draft supports register, list, and retrieve operations; its purported idempotency and immutable-publication semantics have no independent persistent-service evidence.

**Scientific and operational boundaries:** Free-text tactics are not a controlled operational protocol, intervention order, dose, timing, field suitability assessment, pesticide label or evidence of implementation. Neither observed pest density nor strategy effectiveness is established. This proposal cannot authorize pesticide treatment or certify regulatory compliance. Requiredness, controlled vocabularies, and reference relationships remain unresolved under decisions D-373 and its associated RFC question list. Any semantic-neighbor links between proposed operations are advisory only, not scientific causality or executable workflow dependencies.

**Sources:** [module overview](./README.md), [candidate record schema](./Schemas/IpmStrategy.yaml), [registration schema](./Schemas/IpmStrategyNewRequest.yaml), [candidate operations](./IpmStrategy_GET_POST.yaml), [RFC source](../../RFCs/RFC-125-IpmStrategy.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
