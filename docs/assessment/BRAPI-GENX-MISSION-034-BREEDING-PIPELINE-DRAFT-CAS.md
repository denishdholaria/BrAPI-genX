# Mission 034 — D-BP-14 first publication and draft trace invariants

**Date:** 2026-11-24. **Starting `main`:** `4b9287e099536c94331e83ad4d60f6f765321d0d`.

## Coverage extension

The offline BreedingPipeline Compare-and-Set (CAS) verifier now
supports three additional scenarios from the accepted **candidate**
D-BP-14 behavioral plan:

- **CAS-07** — an *existing* pipeline with no published-current version
  accepts a new published revision only with an explicit null
  `expectedCurrentVersionId`. A missing field is not equivalent.
- **CAS-08** — appending a draft based on the current published revision
  preserves the published pointer and uses a preparation baseline,
  not a `supersedes`/`corrects` published-successor claim.
- **CAS-09** — two concurrent drafts may both append from the same
  published baseline without moving the current pointer. The trace must
  record a barrier and show both immutable drafts and successful results.

The existing common verifier retains immutable-history and prior
lifecycle-event checks. An additional pure helper checks requested
publication intent, exact fingerprints and revision state,
returned version identity, expected baseline, pointer transitions,
the absence of unrelated extra revisions or lifecycle effects,
and the CAS-09 race barrier.

## Recorded trace conventions

The trace file remains a **separately captured**, untrusted JavaScript
Object Notation (JSON) observation, not a live test driver.
`requestedPublicationState` and `basedOnVersionId` are observation
fields extracted from the submitted request. For CAS-07 the external
harness must record `pipelineExistsBefore: true`; the checker cannot
independently prove logical pipeline existence.

## Verification

- **16/16** isolated positive/mutation tests passed locally in
  `/mnt/data/genx_mission034`.
- Syntax compilation passed.
- Tested Git object hashes:
  `d0adf1e316ab27e9a52ede9f9bdc4faebf319f15` (helper),
  `5e5de80e2e034b20d028d939e4ec17338e73a312` (tests).
- Three main-verifier integration tests were added, bringing its
  previous 27 tests to **30**; full suite and generated artifacts
  require confirmation from GitHub Actions.

**No independent authenticated service was exercised.**
The trace tests are synthetic; CAS-05 and CAS-10..14,
security scenarios AUTH-01..05, persistence rollback and external
effect observation remain work requiring a real test target.
No official BrAPI version 2.1 source, public GenX route or scientific
decision was changed.
