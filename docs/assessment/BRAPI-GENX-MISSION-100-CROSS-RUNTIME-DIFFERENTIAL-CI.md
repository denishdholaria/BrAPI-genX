# Mission 100 — Restore cross-runtime behavioral differential verification

**Date:** 2026-11-25. **Inspected `main`:** `4bbb6c8171bbda9b9a89d207991ba0e9f3bd7fda` (Mission 099).

## Gap and purpose

The repository already contains a separately written TypeScript/Bun reference server for the RFC-001/RFC-004 subset and the nine-request `Scripts/genx_differential_check.py`. The hosted conformance workflow previously ran only the Python server for its 28 live probes. TypeScript exercised digest/canonicalization tests but not the behavioral differential sequence. Historical cross-runtime comparisons do not validate the latest commit.

## Bounded change

- Add a separate `independent-runtime-differential` hosted job; install the same pinned Python dependencies and the locked TypeScript canonicalization dependency.
- Launch the two in-memory servers independently, with explicit readiness checks on loopback ports 18080 and 18082.
- Run the existing nine-request differential check without changing its behavior; ensure the job fails on a nonzero exit or failed server readiness.
- Upload both server logs on failure and stop both processes unconditionally.
- Protect the job, live comparison command, TypeScript server startup and Bun setup with five negative workflow-scope regression tests.
- Clearly distinguish this cross-runtime evidence from the separate static and 28-probe Python live-reference checks.

## Falsifiers and limitations

The comparison covers only RFC-001/RFC-004's current common subset. Two project-owned implementations can agree on incorrect behavior; this is not external-vendor certification. It does not prove other GenX resources, every proposed operation, authorization, durable persistence, performance, scientific accuracy or production readiness. It does not advance any RFC maturity state.

Local regression: `python Scripts/test_conformance_workflow_scope.py`. The existing differential checker additionally requires two running servers. Full hosted static, live-reference, cross-runtime differential and specification-generation checks must pass at the exact pull-request commit before merge; recheck integrated `main`.

**Non-goals:** No released Breeding Application Programming Interface (BrAPI) version 2.1 contract, GenX wire schema, endpoint identity, registry, scientific maturity or pending spatial governance choice is altered.
