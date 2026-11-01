# BrAPI-GenX — Parent Candidate Selection (Breeding)

Parent candidate selection records the verdict reached for a candidate parent
in a breeding program, with criterion and rationale. BrAPI v2.1 has no parent
candidate selection record.

- `POST /genx/v1/parent-candidate-selections` (`genxRecordParentCandidateSelection`) records one
  `ParentCandidateSelection` (`Schemas/ParentCandidateSelectionNewRequest.yaml`). Same
  `parentCandidateSelectionDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/parent-candidate-selections` (`genxListParentCandidateSelections`) lists records,
  optionally filtered by program, candidate, or decision.
- `GET /genx/v1/parent-candidate-selections/{parentCandidateSelectionDbId}`
  (`genxGetParentCandidateSelection`) retrieves one record.

Details and falsifiers: `../RFC-028-Parent-Candidate-Selection.md`.