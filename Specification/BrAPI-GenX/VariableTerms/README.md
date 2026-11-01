# BrAPI GenX — Versioned Variable-Term Governance

Versioned, namespaced variable terms. Conflicting redefinitions are rejected,
never merged silently.

- `POST /genx/v1/variable-terms` (`genxPublishVariableTermVersion`) creates a term version (`Schemas/VariableTermNewRequest.yaml`).
  Same `(variableDbId, version)` + identical body replays the existing record;
  same pair + different body is rejected with `409`.
- `GET /genx/v1/variable-terms` (`genxListVariableTermVersions`) lists terms across versions with standard pagination.
- `GET /genx/v1/variable-terms/{variableDbId}` (`genxGetVariableTermVersion`) fetches one term (latest created when
  `version` is omitted) or `404`.

There is no `DELETE`: terms are deprecated explicitly (`status: deprecated` +
`supersededBy`), so historical observations keep resolvable definitions.
Details and falsifiers: `../RFC-002-Variable-Term-Governance.md`.
