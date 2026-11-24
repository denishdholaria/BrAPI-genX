# Mission 011 — Reviewed Semantic-Neighbor State Compatibility

**Date:** 2026-11-24  
**Baseline:** `52f3237d77572896b6571dd37db6996233304f31`  
**Scope:** non-normative regression gate only.

## Defect

The Mission 009 scientific source-contract checker required six previously
reviewed source/target groups to remain in the exact `requires-decision`
status. But the canonical neighbor governance state machine explicitly permits
subsequent `requires-decision → evidence-backed-proposed` and
`requires-decision → rejected/superseded` transitions subject to its own
requirements. Consequently, a valid maintainer-authorized disposition would
have been incorrectly blocked by a second, overly strict evidence guard.

## Correction

The source-evidence guard now recognizes these four *reviewed* states:
`requires-decision`, `evidence-backed-proposed`, `rejected`, and
`superseded`. It still rejects a regression to `inherited-unreviewed`
or an unknown status and preserves assessment citation, module pair and
three-identity checks. This guard does **not** approve terminal transitions
or override the canonical governance validator, which retains decision
authorization, allowed-transition, and status-evidence enforcement.

Three mutation/positive tests were added to the original twelve, covering
proposed advancement, terminal reviewed states and unknown-status rejection.
No relationship status or source schema was changed by Mission 011.

## Verification

Using the locally available isolated test copies under
`/mnt/data/brapigenx_mission011`:

```sh
python -m unittest -v test_scientific_contract_boundaries.py
python -m py_compile check_scientific_contract_boundaries.py test_scientific_contract_boundaries.py
```

**15/15 tests passed** and compilation succeeded. Git blob hashes for the
locally executed files (to compare with the subsequent repository commit):

- checker: `2ebe01427776451eb7698598952407749e1de35b`
- test: `74cfb1a71fe109eca8bea229331b3e2d258363bb`

This isolated verification is not the complete checked-out repository's
conformance suite. The existing GitHub Actions checks will execute after
the maintainer-reported monthly minutes budget becomes available.
