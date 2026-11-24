# Group SensorDevice

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 149, not an approved instrumentation calibration standard, independent service conformance result, or certified measurement workflow.

The proposed group registers, lists by optional lifecycle status and retrieves immutable namespaced metadata records. Identical-body replay and changed-body conflict remain **candidate behavior**, not evidence of a persistent implementation. The candidate requires namespaced `sensorDeviceDbId` and lifecycle `status`; optional `deviceType`, `sensorType`, `manufacturer`, `model`, `serialNumber`, `supersedes`, and provenance do not prove device identity, certification, measurement precision or calibration. D-445–D-447 remain open.

**Boundaries:** A physical instrument cannot be assumed calibrated, a gateway cannot be assumed healthy, and measurement normalization cannot be assumed mathematically correct merely because the candidate record exists. String references to devices or raw telemetry do not establish authenticated identity, unit compatibility, time alignment or provenance verification. The absent typed GenX `ResearchAsset` link (D-447) remains an unresolved question; any operation-neighbor links are advisory navigation only. Published Breeding Application Programming Interface (BrAPI) version 2.1 observation meanings remain unchanged.

**Sources:** [module overview](./README.md), [candidate record](./Schemas/SensorDevice.yaml), [registration request](./Schemas/SensorDeviceNewRequest.yaml), [draft operations](./SensorDevice_GET_POST.yaml), [RFC-149](../../RFCs/RFC-149-SensorDevice.md), and [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
