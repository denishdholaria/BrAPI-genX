# Mission 158 — Source-field integrity of immutable publication replay replies

**Status:** implemented; hosted checks pending.
**Baseline:** `main` at `f8427a17f3b0eb0dfb405545da4b3aee5abbff0a`.
**Scope:** L-08, L-10, L-12, L-16 and L-18 conformance execution, five
mandatory replay regression suites, probe descriptions and conformance guide.

## Demonstrated false-positive risk

Each identical-publication replay verified response status 200 and the
original accepted resource identifier, followed by an unchanged stored
record readback. However, the replay response could use the right
identifier while modifying original submitted scientific fields,
measurements or nested provenance. Because only the identity was
inspected in the replay response, and storage was independently verified,
that replay-response corruption passed.

## Bounded correction

- Implement `replay_response_problem` for deep comparison of every
  submitted field, including nested values, against the reply's
  `result` record; require object-shaped result and source record.
- Use it inside existing `same_term`, `same_ledger`, `same_model`,
  `same_matrix` and `same_package` assertions, preserving existing
  resource identity, HTTP status, and stored-readback checks.
- Permit additional server-managed fields, rather than byte-for-byte
  equality or requiring the entire response body to match.
- Extend the already-mandatory synthetic replay tests for changed
  quantities, variable names, artifact and matrix digests, access URLs,
  package licenses, nested metrics, provenance and evidence, missing
  original fields, and benign extra metadata.
- Do not alter manifest vocabulary or hosted workflow wiring.

## Required verification

```sh
python Scripts/test_term_replay_version_uniqueness.py
python Scripts/test_ledger_replay_postcondition.py
python Scripts/test_model_replay_version_integrity.py
python Scripts/test_matrix_replay_stored_state.py
python Scripts/test_package_replay_stored_state.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require successful hosted static and live-reference conformance,
independent-runtime differential and specification generation before merge.

## Boundary

No official Breeding Application Programming Interface (BrAPI) version 2.1
contracts, GenX wire schema, maturity, or unresolved embargo visibility
policy changes. This verifies the original fields of an immutable
publication replay, not legitimately derived analytical results.
