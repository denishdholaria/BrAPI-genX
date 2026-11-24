# Group CaptureWorkflow

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 110. This record proposal is not an official Breeding Application Programming Interface (BrAPI) version 2.1 Observation contract or verified measurement-quality workflow.

Proposed operations register, list by lifecycle status, and retrieve immutable namespaced metadata. Same-body replay and changed-body conflict remain candidate behavior without independent persistent-service evidence. The candidate requires namespaced `captureWorkflowDbId` and `status`; optional `workflowType`, `supersedes` and provenance do not define a runnable state machine, instrument integration, permission, or measurement lineage. There is no typed BrAPI Study/Location or GenX PhenotypeCapture relationship. D-328–D-330 remain open.

**Boundaries:** BrAPI version 2.1 Observations already carry reported value, timestamp, variable, observation-unit, study and collector context. The draft metadata must not be assumed to mutate these official observations, authenticate collectors, validate a sensor reading, infer scientific missingness, or perform a correction. Advisory neighbor links establish no typed relationship. Further policy and scientific semantics require explicit decisions.

**Sources:** [candidate overview](./README.md), [candidate schema](./Schemas/CaptureWorkflow.yaml), [registration request](./Schemas/CaptureWorkflowNewRequest.yaml), [draft operations](./CaptureWorkflow_GET_POST.yaml), [RFC-110](../../RFCs/RFC-110-Capture-Workflow.md), [official BrAPI Observation request](../../../BrAPI-Phenotyping/Observations/Schemas/ObservationNewRequest.yaml), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
