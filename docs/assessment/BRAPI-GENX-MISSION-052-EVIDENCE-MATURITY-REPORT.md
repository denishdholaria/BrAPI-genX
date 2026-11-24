# Mission 052 — Read-only group evidence and candidate RFC maturity reporting

**Date:** 2026-11-24
**Prepared parent:** `81de352a1ccde6d93fa16e5d8deb18949f0a9b21`

## Purpose

The repository contains **156** GenX group description files, of which **42** have source-backed protected descriptions and **114** remain evidence-deferred after Missions 043–049b. The Request for Comments (RFC) maturity register is a separate, independently governed source of proposal states (e.g. STRUCTURAL_DRAFT, DEFERRED, CONTRACT_VALIDATED, SEMANTICALLY_REVIEWED).

`Scripts/report_genx_evidence_coverage.py` now emits a reproducible per-module JSON and console inventory of both dimensions: documentation evidence and the RFC maturity identifiers cited by each module overview. It does **not** aggregate these into a production-ready score, claim scientific adoption, or infer independent service conformance.

An RFC is included only if the module README explicitly cites its RFC identifier; no source match is invented. If an identifier is absent from the maturity register it is labelled `UNVERIFIED_RFC_REFERENCE` rather than being promoted. Missing maturity register, duplicate/unknown statuses, missing module README, and failures in the original evidence-backed group checker fail closed.

The static workflow runs the read-only check and six mutation tests; script changes are included in path filters. No GenX specification, RFC maturity record, group-description contents, registered scientific relationship, or external service has been changed.

## Acceptance

Run `python Scripts/report_genx_evidence_coverage.py --check` and `python Scripts/test_genx_evidence_coverage.py`, followed by the complete hosted static/live and specification-generation workflows on the integrated HEAD. Report exact observed counts; do not treat source review as proof of independent conformance.
