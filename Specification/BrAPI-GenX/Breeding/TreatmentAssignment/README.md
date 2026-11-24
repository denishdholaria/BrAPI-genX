# BrAPI-GenX — Treatment Assignment (Experimental Design)

This **STRUCTURAL_DRAFT** registers a proposed assignment description, not a verified planned allocation or applied field operation. Official BrAPI version 2.1 Observation Unit `treatments` already represents factor/modality information; Events represent interventions.

- `POST /genx/v1/treatment-assignments` (`genxRegisterTreatmentAssignment`) registers a `TreatmentAssignment` (`Schemas/TreatmentAssignmentNewRequest.yaml`). Only `treatmentAssignmentDbId` is required; both `fieldDbId` and `treatment` are optional. Identical-body replay and `409` conflict are candidate behavior.
- `GET /genx/v1/treatment-assignments` (`genxListTreatmentAssignments`) lists by optional field/status.
- `GET /genx/v1/treatment-assignments/{treatmentAssignmentDbId}` (`genxGetTreatmentAssignment`) retrieves a record.

The free-text field identifier is not a typed BrAPI Study, Location or Observation Unit link, and there is no `experimentalDesignDbId`. Details: [evidence review](./GroupDescription.md), [RFC-106](../../RFCs/RFC-106-Treatment-Assignment.md); D-316–D-318 remain open.
