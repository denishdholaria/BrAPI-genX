# Group IrrigationOperation

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 024; not a validated agronomic event ledger, official Breeding Application Programming Interface (BrAPI) version 2.1 resource, or independently tested persistent implementation.

The proposed `IrrigationEvent` contract defines an independently namespaced identity, optional `supersedes` and provenance metadata, and candidate operations for registration, listing and retrieval. The actual required scientific fields and lifecycle status vary by resource; their documented immutable publication and identical-body replay are candidate expectations, not demonstrated persistence guarantees.

**Agronomic and interoperability boundaries:** The required irrigatedAt timestamp and method do not establish a measured water balance. Volume, volumeUnit, duration, Study and Location identifiers are optional; no flowmeter calibration, water source, delivered-depth conversion, plot area, or WeatherObservation link is enforced. The schema does not prove an irrigation event occurred in the claimed location or volume. D-70 remains unresolved for weather linkage. Open scientific-design decisions include D-69 and the remaining unresolved questions in its governing RFC. Operation-neighbor links do not automatically establish biological identity, verified delivery, causality or transaction effects.

**Sources:** [module overview](./README.md), [record schema](./Schemas/IrrigationEvent.yaml), [registration schema](./Schemas/IrrigationEventNewRequest.yaml), [draft operation](./IrrigationOperation_GET_POST.yaml), [governing RFC](../../RFCs/RFC-024-Irrigation-Operation.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
