# Mission 125 — Variable-term replay version uniqueness

**Status:** implemented, pending mandatory hosted checks.  
**Scope:** existing registered live probe L-08; no new scientific or wire
contracts. **Dependency:** Mission 124.

## Existing false-positive risk

L-08 republishes the exact same variable-term version and checks that both
responses identify the same (variableDbId, version). The expected reply can
coexist with a hidden extra stored version, duplicate record, or changed
original version. Previously the test did not inspect the collection.

## New observed postcondition

After the identical replay, the runner queries:
`GET /variable-terms?variableDbId={variableDbId}`.

The `term_replay_single_version: true` assertion verifies:

- HTTP 200, exactly one structured returned record, and complete pagination
  reporting one total record on the sole page.
- The returned record's variableDbId and version match the original submitted
  version and the identifiers captured from the initial publish.
- Every originally submitted field remains unchanged, including the
  scientific term definitions and nested provenance. Extra server-managed
  properties are permitted.

The manifest validator now requires the replay and its follow-up check.
The new `Scripts/test_term_replay_version_uniqueness.py` regression suite
tests duplicate and extra versions, missing/modified records, altered
scientific attributes, malformed pagination and incorrect replay replies.

## Verification

```bash
python Scripts/test_term_replay_version_uniqueness.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

The hosted static, Python live reference, independent cross-runtime, and
specification generation workflows are required merge gates.

## Boundaries

This verifies a single visible version for a fresh synthetic term on the
project's in-memory server. It does not establish persistent uniqueness
constraints, transactional semantics, complete historical version policies,
scientific validity of ontology assertions, authorization, or third-party
interoperability. Official BrAPI 2.1 and proposed GenX schemas are unchanged.
