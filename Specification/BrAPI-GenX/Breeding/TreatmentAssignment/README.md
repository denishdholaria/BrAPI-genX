# BrAPI-GenX — Treatment Assignment (Experimental Design)

Treatment assignment records describe treatment assignments to fields.
BrAPI v2.1 has no treatment assignment record.

- `POST /genx/v1/treatment-assignments` (`genxRegisterTreatmentAssignment`) registers one
  `TreatmentAssignment` (`Schemas/TreatmentAssignmentNewRequest.yaml`). Same
  `treatmentAssignmentDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/treatment-assignments` (`genxListTreatmentAssignments`) lists records,
  optionally filtered by field or status.
- `GET /genx/v1/treatment-assignments/{treatmentAssignmentDbId}`
  (`genxGetTreatmentAssignment`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-106-Treatment-Assignment.md`.
