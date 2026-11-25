
# Mission 154 — Identical publication replay status assurance

**Status:** implemented; hosted verification required.
**Dependency:** Mission 153, pull request #103.
**Scope:** registered L-08, L-10, L-12, L-16 and L-18,
their fail-closed manifest guards, existing synthetic regression suites
and conformance documentation.

## Confirmed false-positive risk

The registered expectations for identical variable-term, ledger, model,
matrix and FAIR package publication replays each explicitly state the
second POST must return HTTP 200 and the original resource identity.
The runner tested only the identity and eventual collection state,
and did not test the status. An implementation could report 202 Accepted,
incorrectly treating the same version as a new write, while reusing
the old identifier and pass. A 5xx response with a copied identifier
could also be falsely accepted by the identity-only assertion.

## Bounded correction

- Register `status: 200` alongside each existing `same_term`,
  `same_ledger`, `same_model`, `same_matrix` and `same_package`
  assertion on the second POST.
- Require the specific HTTP 200 assertion in the established
  manifest guards for L-08, L-10, L-12, L-16 and L-18.
- Extend five existing mandatory synthetic regression suites to reject
  replay 202 and 500 even when the response identity is unchanged.
- Preserve all existing immutable-source, version-uniqueness, and
  readback postconditions.
- Do not change L-01, whose asynchronous job replay explicitly allows
  either 200 or 202.
- Do not introduce any new assertion vocabulary, schema or workflow step.

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
independent runtime differential and specification generation before
merging.

## Boundaries

These are already-documented reference publication replay expectations;
no new normative replay policy is inferred for other operations.
No official Breeding Application Programming Interface (BrAPI)
version 2.1 contract, GenX wire schema, scientific maturity or
embargo metadata-visibility policy changes.
