# Mission 110 — Run the version 2.1-only fallback probe on the TypeScript reference

**Date:** 2026-11-25. **Starting source:** Mission 109 review head `a01b88ef37136e50b370d45d3a03d32e20ac1252`. **Dependency:** integrate Mission 109 before retargeting to `main`.

## Gap

The TypeScript/Bun reference server includes a `--profile v21` mode with a legacy `calls` server-info array, but the hosted independent-runtime job started only its GenX profile. Existing registered live probe **L-06** checks that a version 2.1-only fallback negotiation succeeds. Historical support of the profile did not provide current hosted evidence of that behavior.

## Bounded change

- Start an additional in-memory TypeScript/Bun instance on loopback port 18083 under `--profile v21` alongside Python/GenX 18080 and TypeScript/GenX 18082.
- Extend readiness checks, failure-log collection, and unconditional cleanup to cover the third process.
- Run the unchanged registered L-06 against the legacy-only profile, and fail the job on a bad negotiation result or unavailable server.
- Protect the profile startup and active probe command with three workflow-scope mutation subcases.

## Verification

```sh
python Scripts/test_conformance_workflow_scope.py
bun Scripts/genx_test_server_ts.ts --port 18083 --profile v21
python Scripts/checkGenXConformance.py --server http://127.0.0.1:18083/genx/v1 --only L-06
```

The latter two commands require separate processes; hosted integration performs both. Require static, live-reference, cross-runtime (including the version 2.1-only check), and specification generation at the exact pull-request head before integration. Recheck integrated `main` separately.

**Evidence boundary:** This is a project-owned reference stub, not evidence of complete official Breeding Application Programming Interface (BrAPI) version 2.1 support, authorization, persistent state, scientific validity or external client certification. No official wire contract, GenX route, registry, Request for Comments (RFC) maturity or deferred spatial decision changes.
