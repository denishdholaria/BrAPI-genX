# Mission 043 — Reproducible BrAPI standards-overlap evidence gate

**Date:** 2026-11-24
**Starting main:** `e4f61d5ee1ec9be82c4ea0f7fd73f25a672e5b74`
**Scope:** reproducible bounded standards-overlap and typed-link source audit, mutation tests, continuous integration (CI) gate. No candidate/open standard contract change.

## Problem

Missions 040–042 corrected documentation that incorrectly described official BrAPI v2.1 Scales, Methods, Lists, common crop names and People as absent, and fixed prose claiming typed links that actual GenX candidate schemas lacked. A one-off editorial audit will not prevent those same discrepancies recurring.

## Evidence and enforcement

`docs/assessment/BRAPI-GENX-STANDARDS-OVERLAP-EVIDENCE.json` lists five **explicitly inspected** GenX modules and their corresponding official operation source and route. `Scripts/audit_genx_standards_overlap.py` verifies actual official OpenAPI source operations, candidate resource schema presence and explicit official route acknowledgments in each module README, GroupDescription and candidate RFC.

Five missing/unratified typed-reference observations are separately anchored to actual candidate schema source and their unresolved decision IDs. The gate fails if the audited candidate later gains an apparently linked target without re-review or if the RFC loses its unresolved decision. This does not assert that external relations are scientifically meaningful.

**Provenance categories:** overlap ≠ semantic identity; absence of typed link ≠ rejection of a future mapping; draft route ≠ independently implemented service conformance. Not-listed modules remain unreviewed. No automatic normalization, similarity algorithm or mass-generated normative proposals.

## Regression and workflow

The mutation suite exercises missing incumbent routes, missing acknowledgments, newly asserted unratified typed links, fabricated reviewed modules, missing manifest, and missing RFC decision. Both push and pull request workflow path filters include the new scripts. Static conformance executes the audit and mutations; diagnostics collect them on failure.

## Acceptance

Run `python Scripts/audit_genx_standards_overlap.py` and `python Scripts/test_genx_standards_overlap.py`; then the existing full static/live workflow and separate specification generation. Hosted results must be reported separately. No official BrAPI source, GenX OpenAPI contract, generated catalogue, terminal scientific decision or RFC maturity was altered.
