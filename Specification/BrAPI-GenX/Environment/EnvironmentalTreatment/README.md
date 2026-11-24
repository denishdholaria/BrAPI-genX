# BrAPI-GenX — EnvironmentalTreatment (Environment)

`EnvironmentalTreatment` proposes an immutable description of an intended or recorded stress treatment. Registration requires only `environmentalTreatmentDbId`; site, treatment type, exposure and provenance are optional. `exposure` is free text, not calibrated duration, dose, soil-moisture treatment or verified applied stress. The candidate does not measure phenotypic outcomes or establish a controlled experiment.

The current schema has **no `extremeWeatherEventDbId`**, contrary to the older RFC's implied GenX ExtremeWeather relationship. Optional `siteDbId` does not prove an official BrAPI (Breeding Application Programming Interface) Location join. D-232–D-234 remain deferred.

- `POST /genx/v1/environmental-treatments` (`genxRegisterEnvironmentalTreatment`) registers one `EnvironmentalTreatment` (`Schemas/EnvironmentalTreatmentNewRequest.yaml`); replay and conflict behavior remain candidate invariants.
- `GET /genx/v1/environmental-treatments` (`genxListEnvironmentalTreatments`) lists records, optionally filtered by site or status.
- `GET /genx/v1/environmental-treatments/{environmentalTreatmentDbId}` (`genxGetEnvironmentalTreatment`) retrieves a record.

See [source-backed group description](./GroupDescription.md) and [RFC-078](../../RFCs/RFC-078-Environmental-Treatment.md).
