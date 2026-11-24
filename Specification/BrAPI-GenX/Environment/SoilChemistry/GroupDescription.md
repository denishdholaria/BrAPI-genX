# Group SoilChemistry

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 077. `SoilChemistry` proposes soil-texture and chemistry metadata, not a validated laboratory soil test, certified soil-health score, calibrated moisture measurement, or official BrAPI (Breeding Application Programming Interface) version 2.1 Observation.

The registration request requires **only** `soilChemistryDbId`; the response additionally requires lifecycle `status`. `siteDbId`, `texture`, `chemistry`, `moistureDepthCm`, and `provenance` are optional. The `chemistry` field is an unconstrained object without mandatory analytes, units, measurement methods, calibration, detection limits, sampling depth, sampling date, replicate counts or laboratory quality controls. `moistureDepthCm` is a numerical **measurement depth**, not a moisture-content value, and has no schema-enforced range or paired water-content value.

**Scientific and identity boundary:** `siteDbId` is an optional plain string, not a validated BrAPI Location or GenX SoilProfile relationship. No `soilProfileDbId` is modelled; an advisory semantic neighbor does not create a typed source link. Without sampling metadata and consistent methods, soil-chemistry values cannot be assumed comparable across fields, seasons, soil horizons or laboratories. D-229–D-231 remain open, and no approval or analytical reproducibility is implied.

**Sources:** [module overview](./README.md), [response schema](./Schemas/SoilChemistry.yaml), [registration schema](./Schemas/SoilChemistryNewRequest.yaml), [operations](./SoilChemistry_GET_POST.yaml), [RFC](../../RFCs/RFC-077-Soil-Chemistry.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
