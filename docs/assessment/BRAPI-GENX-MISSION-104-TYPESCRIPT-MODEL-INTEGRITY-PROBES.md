# Mission 104 — Host negative and replay model-integrity probes against TypeScript

**Date:** 2026-11-25. **Starting source:** Mission 103 review head `04a968e456a35139ebdd9f45ba1302f9cef98f42`. **Integration dependency:** Mission 103, which fixes selected-probe fail-open behavior. The Mission 104 branch is stacked and must be retargeted to integrated `main` when Mission 103 is merged.

## Evidence gap

The hosted cross-runtime job already compares nine immediate responses and runs the existing L-14 inference-digest and L-24 concurrent-idempotency probes against the separately written TypeScript/Bun reference server. But it has no mandatory current-run test of the TypeScript implementation's model version replay and model authority denials.

The registered probe manifest already supplies the relevant behaviors:
- **L-12:** identical `ModelArtifact` registration must replay the same version instead of creating another;
- **L-13:** a different artifact digest under the same model version must be rejected with `409`;
- **L-15:** inference with an unknown or revoked model must be rejected at submission.

These checks cover additional negative integrity and authority cases but do not introduce normative meanings.

## Bounded implementation

1. Execute `L-12`, `L-13` and `L-15` using the existing `checkGenXConformance.py --only` runner against the existing TypeScript loopback server in the hosted `independent-runtime-differential` job.
2. Require each command in the workflow scope validator, and add six mutation subcases across the three probes (removal or demotion to failure-only diagnostics must fail).
3. Keep the registered probe manifest, official BrAPI version 2.1 contracts, proposed GenX schemas, registry and reference implementations unchanged.

## Evidence limits and falsifiers

Run `python Scripts/test_conformance_workflow_scope.py`, and run each of the three live probes against a started TypeScript reference server. The hosted job must fail if an explicit probe is unavailable, skipped, or produces a failed assertion.

**Important limitation:** L-13 currently asserts a conflict status but has no post-conflict re-GET verifying that the original digest remains stored. No claim of independently validated immutable storage follows from this mission. L-15 is authorization-independent domain refusal by an in-memory mock, not authentication or tenant isolation. Project-owned reference servers are not independent external-vendor conformance evidence.

Require successful hosted static, Python live, TypeScript differential/model probes and specification-generation workflows at the exact pull-request head before merging. Recheck integrated `main` thereafter.

**Scientific/governance boundary:** No Request for Comments (RFC) maturity change, group-description evidence count change, or unresolved spatial decision promotion.
