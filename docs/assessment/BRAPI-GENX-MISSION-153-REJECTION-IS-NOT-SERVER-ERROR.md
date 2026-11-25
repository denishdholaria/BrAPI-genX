
# Mission 153 — Server failures are not valid rejection evidence

**Status:** implemented; hosted verification pending.
**Dependency:** Mission 152, pull request #102.
**Scope:** the already registered `rejected` live assertion used in L-02
and L-03, existing mandatory negative regression suites and documentation.

## Confirmed false-positive risk

The conformance executor implemented `rejected: true` as HTTP status
greater than or equal to 400. This wrongly accepted 500 Internal Server Error
and 503 Service Unavailable as valid conflict/terminal-cancel rejections.
A broken server could fail the request due to internal errors and still
pass the behavioral probe if preexisting stored state survived the error.

## Narrow correction

- Require a real integer HTTP status in the 400–499 client-error range.
- Do not accept server-error HTTP 5xx, successful 2xx or redirect 3xx statuses.
- Preserve the existing job collection and terminal-state readbacks.
- Add negative cases for 500/503 to the mandatory
  `Scripts/test_job_conflict_collection_unchanged.py` and
  `Scripts/test_terminal_cancel_retained_state.py` suites.
- Keep valid client errors accepted without selecting an exact code;
  the original RFC-001 conflict-status policy remains unresolved.

## Verification

```sh
python Scripts/test_job_conflict_collection_unchanged.py
python Scripts/test_terminal_cancel_retained_state.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require hosted static, live-reference, independent runtime conformance
and specification generation before merging.

## Boundaries

This prevents internal server failure from being mistaken for evidence of
rejection. It does not prove that every client-error status necessarily
represents the intended domain-level conflict; that stronger contract
requires a separate governance decision. No published Breeding Application
Programming Interface (BrAPI) version 2.1 contracts, GenX wire schema,
scientific maturity or embargo metadata visibility policy is changed.
