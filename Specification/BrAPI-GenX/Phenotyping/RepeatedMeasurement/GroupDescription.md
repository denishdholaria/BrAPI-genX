# Group RepeatedMeasurement

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 025, not an official BrAPI Observation series or a verified time-series chronology.

The proposed `MeasurementSeries` record requires namespaced `measurementSeriesDbId`, `studyDbId`, `observationUnitDbId`, `variableDbId`, a `measurements` array, and lifecycle `status`. Every measurement requires `timestamp` and `value`; the value is a non-nullable number. Unit, qualityFlag, `supersedes` and provenance are optional. The candidate describes time ordering, but the current array schema does not enforce chronological sorting or uniqueness.

**Boundaries:** Official Breeding Application Programming Interface (BrAPI) version 2.1 already records timestamped observations. A series wrapper is not an alternate authoritative observation identity or proof of temporal reproducibility. The schema permits an empty `measurements` array (D-72), has no `missingReason` and requires a numerical `value` even for `qualityFlag=missing` (D-73). There is no typed GenX `PhenotypeCapture` link (D-74). Missingness behavior, duplicate time points, value types and sorting require explicit policy rather than silent inference.

**Sources:** [candidate overview](./README.md), [candidate schema](./Schemas/MeasurementSeries.yaml), [registration schema](./Schemas/MeasurementSeriesNewRequest.yaml), [draft operation](./RepeatedMeasurement_GET_POST.yaml), [RFC-025](../../RFCs/RFC-025-Repeated-Measurement.md), [official Observation request](../../../BrAPI-Phenotyping/Observations/Schemas/ObservationNewRequest.yaml), and [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
