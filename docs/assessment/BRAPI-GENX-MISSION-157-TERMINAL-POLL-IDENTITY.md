# Mission 157 — Terminal polling must return the requested job

**Status:** implemented; hosted verification pending.
**Dependency:** Mission 156, pull request #106.
**Scope:** the shared live-conformance terminal-polling helper and the
already mandatory terminal-cancellation regression suite.

## Confirmed false-positive risk

The shared `wait_terminal` helper polled a specific
`GET /jobs/{jobDbId}` path, but returned as soon as the response
reported a terminal status. It did not verify the response's
`result.jobDbId` matched the originally requested job. A server
returning another job's terminal-looking payload could satisfy the
wait and contaminate downstream assumptions. Mission 156 corrected
the separate transport-status omission; status 200 alone is still
insufficient proof of the requested job's identity.

## Narrow correction

- Require each successful polling response to contain a dictionary
  `result` with `jobDbId` exactly matching the requested identifier.
- Fail immediately with a descriptive validation error on an absent,
  malformed or mismatched job identity, even if the reported state is
  already terminal or still nonterminal.
- Retain the 200-only transport check and normal terminal-status and
  30-second timeout behavior for correctly identified jobs.
- Extend the existing mandatory
  `Scripts/test_terminal_cancel_retained_state.py` synthetic suite
  with wrong and missing terminal identifiers, malformed result objects,
  and wrong nonterminal identifiers.
- No new assertion vocabulary or workflow command needed.

## Required verification

```sh
python Scripts/test_terminal_cancel_retained_state.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require successful hosted static, live-reference, independent-runtime
conformance and specification generation before merging.

## Boundaries

This only verifies requested job identity in existing terminal polling.
No official Breeding Application Programming Interface (BrAPI)
version 2.1 contracts, GenX wire schema, scientific maturity, or
unresolved embargo metadata policy changes.
