# Group YieldForecast

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 134, not an approved agronomic decision model, official Breeding Application Programming Interface (BrAPI) version 2.1 resource, or independently demonstrated persistent-service implementation.

The proposed `YieldForecast` record has a namespaced identifier and lifecycle `status`, optional `supersedes` and provenance metadata, and candidate register/list/retrieve operations. Data-field requiredness differs among these drafts, and the schema is the authority for actual required properties. Idempotent replay and immutable revision claims remain proposed behavior, not proof of a running service.

**Scientific boundaries:** The forecastValue is an unconstrained optional string, potentially mixing numeric yield and units; horizon, zone and forecastDate are also optional free text. There is no typed model version, observation baseline, uncertainty range, unit validation, geospatial footprint, or independent forecast skill assessment. A forecast must not be confused with harvested yield or an official observation. Outstanding questions start at D-400 and remain unratified. Adjacent operation names do not confer typed links, biological equivalence, or actual field intervention evidence.

**Sources:** [module overview](./README.md), [candidate schema](./Schemas/YieldForecast.yaml), [registration schema](./Schemas/YieldForecastNewRequest.yaml), [draft operations](./YieldForecast_GET_POST.yaml), [RFC](../../RFCs/RFC-134-YieldForecast.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
