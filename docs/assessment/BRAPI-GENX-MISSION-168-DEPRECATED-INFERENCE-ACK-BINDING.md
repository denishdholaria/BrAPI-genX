# Mission 168 — Deprecated inference initial acknowledgment binding

**Status:** implementation proposed for hosted verification.
**Dependency:** Mission 167 (L-25 model identities).
**Scope:** registered L-27 deprecated-model inference job acceptance,
its mandatory synthetic regressions and conformance documentation.

## Confirmed false-positive risk

L-27 submitted inference naming a deprecated model and captured only
the initial `jobDbId`. It then waited for a terminal readback,
which validated the correct `jobType` and `idempotencyKey`.
A corrupted **initial acknowledgment** that omitted or changed the
submitted type/key could pass when the later terminal job was correct.

## Bounded correction

- After HTTP 202, require a nonempty accepted job identifier and
  an acknowledgment echoing the original `jobType` and
  `idempotencyKey`.
- Check these fields **before** polling; keep terminal response and
  canonical input digest checks intact.
- Permit additional server-managed acknowledgment metadata.
- Add mandatory regressions for dropped/changed/nonstring
  acknowledgment fields and malformed result objects, asserting that
  invalid acknowledgments cause no polling, plus a positive extra-field
  control.

## Verification

```sh
python Scripts/test_deprecated_inference_completion.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require GitHub-hosted static, live-reference, independent-runtime
and specification-generation checks before merge.

## Boundaries

No official BrAPI (Breeding Application Programming Interface) v2.1
source contract or GenX wire schema changes. Deprecated model policy,
scientific maturity, and unresolved embargo policies remain unchanged.
