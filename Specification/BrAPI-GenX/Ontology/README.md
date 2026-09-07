# BrAPI GenX — Ontology Term Governance

Versioned, namespaced variable terms. Conflicting redefinitions are rejected,
never merged silently.

- `POST /variables` creates a term version (`Schemas/VariableTermNewRequest.yaml`).
  Same `(variableDbId, version)` + identical body replays the existing record;
  same pair + different body is rejected with `409`.
- `GET /variables` lists terms across versions with standard pagination.
- `GET /variables/{variableDbId}` fetches one term (latest created when
  `version` is omitted) or `404`.

There is no `DELETE`: terms are deprecated explicitly (`status: deprecated` +
`supersededBy`), so historical observations keep resolvable definitions.
Details and falsifiers: `../RFC-002-Ontology-Governance.md`.
