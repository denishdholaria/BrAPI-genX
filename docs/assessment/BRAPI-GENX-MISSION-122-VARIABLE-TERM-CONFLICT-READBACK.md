# Mission 122 — Variable-term conflict retained-state verification

**Status:** implemented, pending required hosted verification.  
**Scope:** registered live probe L-09, the existing reference server and
supporting mutation tests.  
**Dependency:** Mission 121; no official BrAPI version 2.1 or GenX schema changes.

## Gap

L-09 promises that rejecting a conflicting rewrite of the same
(variableDbId, version) preserves the originally published term. Before this
mission, it verified only HTTP 409. An implementation could respond 409
while silently changing a scale, method, provenance actor, or provenance digest.

## Change

- The initial publish captures a deep copy of the **submitted** original
  record, independent of server-returned conflict data.
- After the 409, the registered probe performs GET
  `/variable-terms/{variableDbId}?version={termVersion}`.
- The runner checks HTTP 200, a record mapping, and equality of every
  originally submitted top-level value, including nested provenance structures.
  Server-managed additional fields are not rejected.
- Manifest validation requires this assertion on the version-qualified GET
  **after** the conflict attempt.
- The `Scripts/test_variable_term_conflict_postcondition.py` mock-server
  regression suite checks valid extra metadata and failures for changed
  scale, method version, term identity, term version, nested actor/digest,
  omitted fields, malformed responses, unavailable records, and incorrect
  conflict status.
- The existing static workflow and its scope regression require this suite.

## Verification

```bash
python Scripts/test_variable_term_conflict_postcondition.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

The full hosted static and live conformance, independent runtime checks, and
generation workflow remain mandatory before merge.

## Boundaries

This verifies observable preservation of a synthetic term in the project's
in-memory reference implementation, not durable storage or distributed
transactions. It does not independently establish the biological accuracy
of the term, authoritativeness of the ontology, external vendor support or
BrAPI community acceptance. No scientific maturity promotion is claimed.
