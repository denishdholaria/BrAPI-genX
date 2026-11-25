# Mission 103 — Fail-closed explicit conformance probe selection

**Date:** 2026-11-25. **Starting `main`:** `bc1e9f40f2ac6fe7ff3b53db6e2ac250f3ff3b25` (Mission 102).  
**Nature:** conformance-runner correctness repair, not a scientific or normative specification change.

## Confirmed defect

The existing runner's `--only` implementation filtered the probe loop by identifier but did not establish that any probe matched. `--only L-999` therefore executed zero checks, printed `0 failures, 0 skipped` and exited successfully. In addition, `--only L-14` without `--server` reported a normal live SKIP and exited successfully, despite the caller explicitly requesting a live verification. This behavior could make an incorrectly named, removed or unconfigured guard appear green in continuous integration.

## Bounded correction

1. Require exactly one registered probe for an explicit `--only` selection. Reject missing, duplicate and unknown-tier matches.
2. Require `--server` for a selected live probe. Retain the established behavior of an **unfiltered** static-only run (live probes SKIP without a server).
3. Add ten regression cases spanning valid static/live selection, unknown/empty/duplicate/malformed cases, missing live-server configuration and actual command-line exit codes.
4. Execute the new tests in the hosted static-conformance job and protect that step against removal through the workflow-scope checker.

## Falsifiers

```sh
python Scripts/test_conformance_probe_selection.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py --only L-999
python Scripts/checkGenXConformance.py --only L-14
```

The first two commands must succeed; the last two **must fail with non-zero exit codes**. The full unfiltered runner must continue to report live SKIPs when no server is given. Require hosted static, live, differential and specification-generation checks at the exact review head, and verify integrated `main` separately.

**Scope limit:** No official Breeding Application Programming Interface (BrAPI) version 2.1 or GenX schema changes, operation/route identity changes, new registered probes, Request for Comments (RFC) maturity promotions, scientific claims or spatial-governance decisions.
