# Group PestDiseaseRisk

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 133; not a scientifically validated recommendation, official Breeding Application Programming Interface (BrAPI) version 2.1 contract, or independently verified service.

The `PestDiseaseRisk` record requires its namespaced identifier and a lifecycle `status` (`active`, `superseded`, `withdrawn`), while `riskType`, `targetPestOrDisease`, `riskLevel`, `probability`, `regionOrZone`, `supersedes`, and provenance are optional. The draft supports register, list, and retrieve operations; its purported idempotency and immutable-publication semantics have no independent persistent-service evidence.

**Scientific and operational boundaries:** The probability is a string, not a validated numeric probability with calibration, forecast horizon, model version, underlying observations or uncertainty interval. A named region is not a verified geospatial footprint. A risk label does not establish disease presence or justify control action. Requiredness, controlled vocabularies, and reference relationships remain unresolved under decisions D-397 and its associated RFC question list. Any semantic-neighbor links between proposed operations are advisory only, not scientific causality or executable workflow dependencies.

**Sources:** [module overview](./README.md), [candidate record schema](./Schemas/PestDiseaseRisk.yaml), [registration schema](./Schemas/PestDiseaseRiskNewRequest.yaml), [candidate operations](./PestDiseaseRisk_GET_POST.yaml), [RFC source](../../RFCs/RFC-133-PestDiseaseRisk.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
