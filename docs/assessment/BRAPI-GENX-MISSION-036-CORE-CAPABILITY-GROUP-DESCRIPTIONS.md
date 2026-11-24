# Mission 036 — Evidence-gated Core capability group descriptions

**Date:** 2026-11-24
**Starting `main`:** `f761046a9f23b2cf52613a1abdf86e7972edf827`
**Scope:** Core/CapabilityMetadata, Core/CapabilityNegotiation and Core/ServerInfoV3 group descriptions, pinned description guard and one pinning regression test.

## Source evidence

- CapabilityMetadata: local README, record/request OpenAPI schemas, GET/POST operation, RFC-099; the maturity register labels RFC-099 `STRUCTURAL_DRAFT`. Deferred decisions D-295–D-297 remain open.
- CapabilityNegotiation: local README, record/request schemas, GET/POST operation, RFC-153; maturity register explicitly marks RFC-153 `DEFERRED`. Nothing here ratifies the negotiation protocol or closes RFC-153-Q1–Q3.
- ServerInfoV3: local README, proposed GET operation, schema and CAPABILITY-NEGOTIATION.md audit. D-21, D-22 and D-23 remain open. The draft `3.0-draft` string is not an official BrAPI release.

## Change

Three heading-only group descriptions now explain their limited source-backed scope, unresolved questions, and non-ownership boundaries. The project keeps separate (a) metadata records, (b) deferred negotiation records, and (c) a candidate read-only capability advertisement. None is evidence of production service health, authentication enforcement or official BrAPI release status.

The pinned `REVIEWED` set grows from **9 to 12** of the unchanged **156** groups; **144 remain deferred for evidence review**. A focused unit test protects all twelve pinned review identities. Existing generic mutation tests protect required source links, maturity disclaimers and non-placeholder content for every pinned description.

## Verification and limits

Pre-commit checks against the inspected repository tree confirmed all cited direct local source paths exist; each new description satisfies the checker prerequisites. The connected GitHub workflow must independently execute the full repository regression suite; **do not record hosted PASS until a completed runner confirms it**.

No operation, OpenAPI schema, generated catalogue, endpoint registry, scientific relationship, terminal decision, maturity classification, or official BrAPI contract was changed. Group prose is not a normative acceptance or independent service conformance claim.
