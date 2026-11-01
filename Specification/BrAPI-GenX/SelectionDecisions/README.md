# BrAPI GenX — Selection Decisions (Breeding Verdicts)

Selection decisions record the verdict reached for a candidate in a breeding
program or trial: selected, rejected, deferred, or advanced. They bind the
candidate, the criterion, the decision maker, the evidence inputs, and the
provenance of the decision, so that breeding history is auditable and
reproducible. BrAPI v2.1 has no equivalent record; programs, trials, and
observations exist, but the verdict and its rationale do not.

- `POST /brapi/v3/selection-decisions` (`genxRecordSelectionDecision`) records
  one `SelectionDecision` (`Schemas/SelectionDecisionNewRequest.yaml`). Same
  `selectionDecisionDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /brapi/v3/selection-decisions` (`genxListSelectionDecisions`) lists
  decisions, optionally filtered by program, study, candidate, or decision.
- `GET /brapi/v3/selection-decisions/{selectionDecisionDbId}`
  (`genxGetSelectionDecision`) retrieves one decision.

Details and falsifiers: `../RFC-008-Selection-Decisions.md`.