# Mission 113 — Validate executable live call directives and fixture names

**Date:** 2026-11-25. **Source parent:** Mission 112 review head `c2b6e443a9d11d28a150fc86118557445994085d`. **Integration dependency:** merge Mission 112 before retargeting this stacked change to `main`.

## Confirmed false-positive risk

The live conformance runner previously recognized particular `body_fixture` names through a chain of branches, but lacked a default error for unknown fixtures. A typo in a negative probe could cause a POST with no constructed request body; the server might reject it as malformed and accidentally satisfy a generic `rejected` or status assertion. Similarly, unknown top-level call directives and disabled Boolean capture flags were ignored.

## Bounded change

- Fail early on unknown call directive keys and fixture names, including null or disabled forms.
- Require POST calls to supply a registered fixture or intentional replay capture, forbid body fixtures on non-POST methods, ensure non-POST methods do not attempt capture/concurrent-post operations and require wait-for-terminal to be attached to job capture.
- Preserve existing 49 probe identities, fixtures and scientific meaning. Validate only already implemented execution vocabulary.
- Add fifteen mutation/command-line tests, execute the suite in the hosted static job, and guard that job step against removal.

## Falsifiers and gates

```sh
python Scripts/test_conformance_step_manifest.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

All must pass. A corrupted fixture name must cause non-zero exit before contacting a server. Require hosted static, Python live, TypeScript differential and version 2.1 fallback, plus specification generation at the exact review head before merging. Check integrated `main` separately.

**Limits:** This guards test correctness only. No real-world artifact-byte preimage, durable data integrity, scientific model validation, third-party certification, official Breeding Application Programming Interface (BrAPI) version 2.1 wire contract, GenX registry/schema, Request for Comments (RFC) maturity, or deferred geospatial decision is changed.
