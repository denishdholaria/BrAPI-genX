# BrAPI-GenX — OutcomeFeedback

OutcomeFeedback records describe OutcomeFeedback entries.
BrAPI v2.1 has no OutcomeFeedback record.

- `POST /genx/v1/outcome-feedbacks` (`genxRegisterOutcomeFeedback`) registers one
  `OutcomeFeedback` (`Schemas/OutcomeFeedbackNewRequest.yaml`). Same
  `outcomeFeedbackDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/outcome-feedbacks` (`genxListOutcomeFeedbacks`) lists records,
  optionally filtered by status.
- `GET /genx/v1/outcome-feedbacks/{outcomeFeedbackDbId}`
  (`genxGetOutcomeFeedback`) retrieves one record.

Details and falsifiers: `../RFC-138-OutcomeFeedback.md`.
