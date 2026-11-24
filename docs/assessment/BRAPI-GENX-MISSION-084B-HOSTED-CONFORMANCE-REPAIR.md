# Mission 084B — Hosted conformance failure triage and ImageMetadata decision trace

**Parent:** `188fd7e66731d9e8c24d3dd549f076c8aefceb61` (Mission 084, draft pull request #34), 2026-11-24.  
**Scope:** documentation evidence/verification only. No official BrAPI 2.1 contracts, GenX endpoint paths, operation identifiers, source wire schemas, endpoint registry, authority rules, scientific maturity status, or approved decisions are changed.

## Newly available hosted test evidence

GitHub Actions executed on the parent commit, contrary to the historical assumption that execution would remain unavailable:

- [GenX conformance (static and live), run 45432207752](https://github.com/denishdholaria/BrAPI-genX/actions/runs/45432207752): `live-reference-conformance` succeeded; `static-conformance` failed.
- [Specification/schema generation, run 45432179863](https://github.com/denishdholaria/BrAPI-genX/actions/runs/45432179863): succeeded.
- The static job's first blocking failure was **step 52, “Test group-description evidence guard”**. Its `Scripts/test_genx_group_descriptions.py` output was **68 tests, one failure**. The failure was in `test_image_phenology_and_vegetation_index_source_boundaries` (subtest `Phenotyping/ImageMetadata`): `AssertionError: 'D-93' not found` in its `GroupDescription.md`.
- The failure-only diagnostics executed additional checks despite the primary job's short-circuit. They reported `Scripts/test_conformance_workflow_scope.py` **5/5 passed**, `Scripts/test_genx_readme_routes.py` **8/8 passed**, strict vegetation-index README route audit **3 claims, zero mismatches, zero uncovered**, and `Scripts/check_genx_group_descriptions.py` **156 groups, 135 reviewed, 21 deferred**. The rest of the diagnostics did not report another nonzero exit code in the inspected log.

These results are **not** a successful overall static conformance run; normal steps after step 52 were skipped.

## Root cause and correction

The test in `Scripts/test_genx_group_descriptions.py` requires each newly reviewed ImageMetadata, PhenologyObservation and VegetationIndex description to identify its source-backed deferred decisions. ImageMetadata's schema/prose evidence was already present, but its description omitted the actual identifiers; this is an **evidence traceability omission**, not proof of an incorrect test or a wire-contract defect.

`Specification/BrAPI-GenX/RFCs/RFC-032-Image-Metadata.md` section 6 explicitly records:
- **D-93:** whether `imageDbId` should be required; current contract requires it.
- **D-94:** whether to link `PhenotypeCapture`; no `phenotypeCaptureDbId` field is modelled.
- **D-95:** whether `resolution` should be structured; current contract uses an unstructured string.

The revised ImageMetadata `GroupDescription.md` now spells out all three deferred questions while explicitly preserving their unapproved status. The existing test is retained **without relaxation**.

## Integration policy

- Keep the correction stacked on #34; do not modify `main`, promote drafts, merge dependent pull requests out of order, or assume readiness from green diagnostics alone.
- Before Mission 085's planned merge/baseline closure, require a **complete, successful static-conformance job** on this correction head, and retain the existing live-conformance and schema-generation gates.
- Compare the final cumulative diff against `main` to ensure only intended Markdown, assessment, assurance test scripts and workflow files changed.
- If subsequent hosted checks fail, record exact failures and repair them in a separate follow-up without weakening the checks.

**Status:** correction committed on a draft follow-up branch; complete hosted retest pending at time of authoring.
