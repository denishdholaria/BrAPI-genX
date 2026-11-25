# Mission 098 — Guard conformance triggers against scientific/governance input drift

**Date:** 2026-11-25  
**Inspected integrated main:** `4978ea5cdf294d9f35331e138aa87a214ebdeac1` (Mission 097).  
**Nature:** workflow assurance repair and mutation tests, not scientific ratification.

## Confirmed starting baseline

The final post-merge push workflows for Mission 097 completed successfully on the exact integrated `main` SHA:

- [Static and live GenX conformance](https://github.com/denishdholaria/BrAPI-genX/actions/runs/45462401700): success.
- [Specification/schema generation](https://github.com/denishdholaria/BrAPI-genX/actions/runs/45462401560): success.
- No open pull requests were found in the inspected baseline.

Documentation evidence remains **151 of 156** reviewed GroupDescriptions; five remain deliberately deferred, as detailed in [Mission 097](BRAPI-GENX-MISSION-097-FINAL-DEFERRED-MATURITY-RECONCILIATION.md). Successful conformance of the in-memory reference server does not establish scientific maturity or independent production interoperability.

## Defect and risk

`.github/workflows/genx-static-conformance.yml` executes guards and regressions that depend on `docs/governance/**` (including the RFC maturity register) and `docs/assessment/**` (including breeding decisions, spatial governance and recorded evidence). However, its `pull_request.paths` and `push.paths` originally listed only four specific assessment files and no general governance path. Some source-only changes therefore could avoid running the checks entirely.

The original path filter also enumerated individual scripts, allowing a newly added verifier or a previously unlisted script change to be omitted from workflow triggers until someone remembered to update both lists.

## Bounded repair

1. Include `docs/governance/**`, `docs/assessment/**` and `Scripts/**` in **both** path filters. Keep existing explicit entries unchanged to minimize churn; broader paths intentionally subsume existing individual script entries.
2. Extend `Scripts/test_conformance_workflow_scope.py` to require these paths and verify that removal of each watched path from either trigger is detected.
3. Protect four existing static-conformance commands: RFC governance checker and regression, documentation evidence report and regression. Mutations replacing each command with a no-op must fail the scope guard.
4. Keep other workflow steps, permissions, conformance probes, reference-server behavior, specification sources and decision statuses unchanged.

**Tradeoff:** Documentation or script edits not directly related to a normative contract may now initiate the full conformance workflow. That extra compute is intentional: silent bypass of decision-dependent verification is a greater risk for a foundational specification. If run cost becomes material, optimize job-level selectivity only with equivalent, tested dependency coverage.

## Verification, falsifiers and disposition

Run locally where a checked-out repository with Python and PyYAML is available:

```sh
python Scripts/test_conformance_workflow_scope.py
python Scripts/test_rfc_governance.py
python Scripts/test_genx_evidence_coverage.py
```

The change is **not verified** if removing a governance/assessment/script path from either trigger fails to produce a scope error, or if removing any protected maturity/evidence command is not detected. Confirm final results from hosted workflows at the pull request's exact head, then recheck the integrated `main` SHA after merge. Do not infer success from a previously green commit.

**Governance impact:** none. G-090-1/2/3 remain unratified; D-BP-08 and D-BP-11 remain approved deferrals. No claim of metadata-only ratification or executable geospatial service is introduced. No official BrAPI version 2.1 or GenX wire-contract change is proposed.
