# Mission 099 — Least-privilege schema-generation workflow

**Date:** 2026-11-25. **Starting baseline:** `7b4867d65d634dca9400f8045c7db95add318892` (Mission 098).

## Confirmed source defect

The 127-line `.github/workflows/generate-schema.yml` granted its jobs `contents: write` even though no active step commits, pushes or creates pull requests. It validates and generates artifacts locally. A source comment claiming a guarded release-branch commit was stale.

## Change

- Set top-level `contents: read` and correct the stale comment, leaving existing artifact-generation steps intact.
- Add a Python/PyYAML regression guard that detects the original permission mistake, a job-level override and common Git commit/push commands. This is a configuration guard, not an adversarial shell-security guarantee.
- Execute that guard inside static conformance; watch the generator workflow source on both pull-request and push events and protect the new test command in workflow-scope checks.
- Leave the existing release-branch conditional outputs in place; separately consider their cleanup if warranted.

## Falsifiers and verification

```sh
python Scripts/test_generation_workflow_permissions.py
python Scripts/test_conformance_workflow_scope.py
```

Require hosted static/live conformance and specification generation on the exact pull-request head. Reject if generator steps require write access in practice. After merging, inspect the integrated `main` checks.

**Decision boundary:** No official Breeding Application Programming Interface (BrAPI) 2.1 contract, GenX wire schema, operation, registry, Request for Comments (RFC) maturity, or evidence-reviewed module is changed. Reintroduction of repository publishing requires separately approved permissions and verification.
