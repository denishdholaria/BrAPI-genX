# Mission 029 — Enforce D-027 terminal decision exact binding

**Date:** 2026-11-24. **Parent commit:** `0d992373e7b0c2955051025606956951954374b4`.

The maintainer approved D-026 and D-027 architectural boundaries.
An empty authorized terminal-decision manifest and its 21-test validator
were committed in the previous slice. This integration adds the fail-closed
check to the canonical governance validator before processing ledger
transitions. The status `rejected` or `superseded` now requires a
`SEM-DEC-` entry with matching original relationship identity,
action and successor. A generic source document is not an approval.

Existing full-checkout mutation tests are adjusted to put synthetic
approval records **inside temporary copied checkouts only** and test
that a plausible `RFC-002` label cannot authorize retirement.
A well-formed fixture record does not prove a real maintainer signed
the approval. A real record requires the maintainer to verify and
control its underlying GitHub issue-comment or commit provenance.
This is a distinct operational trust boundary; the checker cannot
cryptographically prove it and must not be described as doing so.

The static-conformance workflow watches both checker and tests, and
runs the 21-test helper suite. The helper's tests passed locally and
their Git blobs match exactly:
`80524bafcd1c198d1303f99e64b06b713c06e733` (checker),
`cba2ece4b6bb18613c8737c3d759c27d5fa93e50` (tests).

**Full checked-out repository validation (including changed canonical
integration mutation tests) remains unexecuted** because the large
endpoint registry is not mounted locally and GitHub cloning is unavailable.
Run the full canonical suite and historical drift check when possible.
No 153 baseline neighbor IDs, public routes, source contracts or RFC
maturity statuses were changed.
