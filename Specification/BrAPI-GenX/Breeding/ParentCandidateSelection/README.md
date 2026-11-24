# BrAPI-GenX — Parent Candidate Selection (Breeding)

This **STRUCTURAL_DRAFT** records a proposed parent-specific Boolean selection outcome. `programDbId` and `candidateGermplasmDbId` are required but only as strings; selection criteria, rationale and provenance are optional. It does not identify decision authority, make a PlannedCross or link to a typed GenX SelectionDecision. Official BrAPI version 2.1 CrossParent already identifies parents for actual/planned crossing resources.

- `POST /genx/v1/parent-candidate-selections` (`genxRecordParentCandidateSelection`) registers `ParentCandidateSelection` (`Schemas/ParentCandidateSelectionNewRequest.yaml`). Identical-body replay and `409` conflict are candidate service behavior.
- `GET /genx/v1/parent-candidate-selections` (`genxListParentCandidateSelections`) lists by optional program, candidate or Boolean verdict.
- `GET /genx/v1/parent-candidate-selections/{parentCandidateSelectionDbId}` (`genxGetParentCandidateSelection`) retrieves one record.

A false value cannot be equated to a generic rejected/deferred verdict. See [evidence](./GroupDescription.md), [RFC-028](../../RFCs/RFC-028-Parent-Candidate-Selection.md); D-81–D-83 remain unratified.
