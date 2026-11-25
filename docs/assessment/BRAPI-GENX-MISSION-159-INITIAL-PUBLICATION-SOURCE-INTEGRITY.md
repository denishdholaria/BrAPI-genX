# Mission 159 — Original scientific fields in initial publication acknowledgments

**Status:** implemented; hosted checks pending.
**Dependency:** Mission 158, pull request #108.
**Scope:** first-response capture steps in variable terms, seed-lot
ledger, models, variant matrices and FAIR packages, plus existing
mandatory regression suites and documentation.

## Confirmed false-positive risk

The live capture steps accepted a successful initial publication response
and recorded the returned resource identity. They did not verify the rest
of the response contained the original submitted scientific fields. A
server could acknowledge a new publication with the correct identifier
but corrupted quantities, model digests, access services, source
provenance or package evidence while returning the correct record on
subsequent replay and GET. The registered replay and collection checks
would not catch the initial response corruption.

## Bounded correction

- Reuse the submitted-record comparison helper introduced by Mission 158,
  giving it the general `submitted_record_problem` name because it
  now checks both initial publication and identical replay responses.
- At each existing `capture_term`, `capture_ledger`, `capture_model`,
  `capture_matrix` and `capture_package` step, reject a response whose
  `result` object omits or changes any originally submitted field, nested
  provenance or evidence value.
- Permit additional server-managed fields and retain the existing
  accepted initial-response status semantics, identities and final
  readback assertions.
- Add first-response-only negative mutations and extra-field positive
  controls in the five already-mandatory replay suites.
- No new assertion vocabulary, registered probe call or workflow command.

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
independent runtime differential and specification generation before merge.

## Boundaries

This checks captured publication acknowledgments, not general derived
analysis results. No official Breeding Application Programming Interface
(BrAPI) version 2.1 contracts, GenX wire schemas, scientific maturity or
unresolved embargo metadata-visibility policy changes.
