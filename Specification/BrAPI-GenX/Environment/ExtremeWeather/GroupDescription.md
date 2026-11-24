# Group ExtremeWeather

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 042. `ExtremeWeatherEvent` proposes an environmental event record, not a validated meteorological extreme, climate attribution, official warning, or quantified crop-loss assessment.

The registration request requires `extremeWeatherEventDbId`, `locationDbId`, `occurredAt` (date-time format), and `eventType`; the response additionally requires lifecycle `status`. `severity`, `description`, and `provenance` are optional. `severity` uses broad categories `low`, `moderate`, `high`, `extreme`, but no required measured magnitude, threshold, climatological baseline, probability, observation period, station, precipitation, temperature, drought-index method or uncertainty supports those labels. `eventType` is a free-text string, not a governed event taxonomy.

**Scientific and identity boundary:** `locationDbId` is a required BrAPI (Breeding Application Programming Interface) Location identifier string, not an authority-qualified or independently validated join. A timestamp and event label do not prove that an extreme condition occurred at the referenced field or that it caused crop damage. There is no modelled `weatherObservationDbId` link, despite deferred D-125. D-124 and D-126 remain open; registration and draft replay semantics are not external meteorological validation.

**Sources:** [module overview](./README.md), [response schema](./Schemas/ExtremeWeatherEvent.yaml), [registration schema](./Schemas/ExtremeWeatherEventNewRequest.yaml), [operations](./ExtremeWeather_GET_POST.yaml), [RFC](../../RFCs/RFC-042-Extreme-Weather.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
