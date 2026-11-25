# Mission 107 — Explicit single-probe SKIP is never a passing verification

**Date:** 2026-11-25. **Inspected `main`:** `2725413449d4956853b4bd4ed316aacaec0a11a0` (Mission 106).

## Confirmed failure mode

Mission 103 rejected unknown selected probe IDs and selections of live probes without a server. A second bypass remained: registered live probe **L-05** requires the `--expired-job` fixture to exercise expiry. `python Scripts/checkGenXConformance.py --only L-05 --server http://127.0.0.1:1/genx/v1` without `--expired-job` reported `SKIP`, printed zero failures, and returned success despite never exercising the requested behavior.

The runner previously based exit status only on `Results.failures`; explicitly selected skipped probes were not considered failures.

## Bounded correction

- If `--only` is present, a reported `SKIP` produces a non-zero exit even with zero assertion failures. The original SKIP record remains visible; this changes the exit code, not the recorded probe result.
- An unfiltered static-only run preserves the established behavior of reporting live probes as `SKIP` while returning success when static assertions pass.
- Extend the existing selected-probe regression suite with deterministic command-line evidence for the L-05 missing-fixture case and outcome-policy cases for full-run versus selected-run behavior.
- The test suite is already required and protected in hosted static conformance; no new workflow commands are needed.

## Falsifiers

```sh
python Scripts/test_conformance_probe_selection.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py --only L-05 --server http://127.0.0.1:1/genx/v1
```

The first two commands must pass. The third must report `SKIP L-05`, explicitly explain missing `--expired-job`, and exit non-zero; it does not require a server to be running because it skips before issuing the expiry GET.

All normal hosted static, live-reference, cross-runtime and specification-generation workflows must pass on the exact pull-request head before integration. Verify integrated `main` separately.

**Non-goals:** No live probe additions, proposed GenX wire-schema changes, official Breeding Application Programming Interface (BrAPI) version 2.1 changes, scientific maturity promotion, or field-level artifact-byte digest decision. This is runner correctness, not evidence that an unavailable expiry fixture was actually verified.
