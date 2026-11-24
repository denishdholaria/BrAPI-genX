# Group PlantingOperation

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 066; not a validated agronomic event ledger, official Breeding Application Programming Interface (BrAPI) version 2.1 resource, or independently tested persistent implementation.

The proposed `PlantingOperation` contract defines an independently namespaced identity, optional `supersedes` and provenance metadata, and candidate operations for registration, listing and retrieval. The actual required scientific fields and lifecycle status vary by resource; their documented immutable publication and identical-body replay are candidate expectations, not demonstrated persistence guarantees.

**Agronomic and interoperability boundaries:** A `planned` planting record cannot be treated as a completed field operation; `completed` is a claimed lifecycle state, not verified seed establishment. The draft lacks a structured unit for numeric seedingRate, and an optional Study/ObservationUnit/CropCycle identifier cannot prove plot ownership or experimental-design validity. D-197 remains open for rate units; records do not imply germination, emergence or yield. Open scientific-design decisions include D-196 and the remaining unresolved questions in its governing RFC. Operation-neighbor links do not automatically establish biological identity, verified delivery, causality or transaction effects.

**Sources:** [module overview](./README.md), [record schema](./Schemas/PlantingOperation.yaml), [registration schema](./Schemas/PlantingOperationNewRequest.yaml), [draft operation](./PlantingOperation_GET_POST.yaml), [governing RFC](../../RFCs/RFC-066-Planting-Operation.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
