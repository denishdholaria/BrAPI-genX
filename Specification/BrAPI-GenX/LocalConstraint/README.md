# BrAPI-GenX — LocalConstraint

LocalConstraint records describe LocalConstraint entries.
BrAPI v2.1 has no LocalConstraint record.

- `POST /genx/v1/local-constraints` (`genxRegisterLocalConstraint`) registers one
  `LocalConstraint` (`Schemas/LocalConstraintNewRequest.yaml`). Same
  `localConstraintDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/local-constraints` (`genxListLocalConstraints`) lists records,
  optionally filtered by status.
- `GET /genx/v1/local-constraints/{localConstraintDbId}`
  (`genxGetLocalConstraint`) retrieves one record.

Details and falsifiers: `../RFC-139-LocalConstraint.md`.
