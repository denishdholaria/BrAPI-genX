# Mission 037 — Evidence-gated interoperability group descriptions

**Date:** 2026-11-24
**Starting `main`:** `c3a1823d457f9d2ef67a447bb98cf872267e7bfb`
**Scope:** three previously heading-only interoperability modules; no operation or wire-contract change.

## Source-based disposition

- `Interoperability/ConformanceProbe`: RFC-155 is explicitly **DEFERRED**. Proposed record fields and operation descriptions do not prove that a probe was executed. The `actualResponse` record field is not in the registration request; do not infer observation or collection mechanics.
- `Interoperability/Crosswalk`: RFC-105 is a **STRUCTURAL_DRAFT**. The present `source` and `target` fields identify systems as plain strings; they are not a validated entity-level identity crosswalk. D-313–D-315 remain open.
- `Interoperability/SchemaMapping`: RFC-152 is **DEFERRED**. `mappingRules` is optional string content, with no certified executable transformation semantics. D-457–D-459 remain open.

Three source-linked group descriptions distinguish proposals from runtime conformance, ontology equivalence and official BrAPI v2.1 behavior. The pinned reviewed-description set is extended from 12 to **15** of 156; **141** remain evidence-deferred. The existing guard checks every reviewed description for a substantive scope, explicit maturity qualifier and direct local source links; a new test pins the three reviewed identities.

## Verification and limitations

The three prose files were checked against their corresponding README, record/request schemas, operation drafts, RFCs and maturity register. All direct Markdown evidence links were resolved against the inspected repository tree before commit. Full hosted conformance is tracked separately and must not be represented as passing until completed.

There are **no** new standards claims, accepted science/identity relationships, conformance declarations, endpoint/registry modifications or changes to official BrAPI v2.1 files.
