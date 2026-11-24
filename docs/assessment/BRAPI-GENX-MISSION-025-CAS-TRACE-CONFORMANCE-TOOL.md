# Mission 025 — Portable BreedingPipeline CAS Trace Verifier (Phase 1)

**Date:** 2026-11-24  
**Baseline `main`:** `6a901323deab73a41cb01e310f1e61552bd7c457`  
**Status:** implementation-independent **offline trace verifier** for
CAS-01 through CAS-04; not an independent service execution.

## Purpose and ratified boundary

D-BP-14 ratifies the *candidate* Compare-and-Set (CAS) profile for
BreedingPipeline immutable current-revision concurrency. The executable
behavioral plan
`docs/assessment/BRAPI-GENX-BREEDING-PIPELINE-CAS-BEHAVIORAL-TEST-PLAN.md`
requires a real independent service, two concurrent authenticated clients,
a synchronization barrier, durable readback and side-effect inspection.
Neither static fixture validators nor this offline trace checker can
alone establish those properties.

## Deliverables

- `Scripts/verify_breeding_pipeline_cas_trace.py`: a read-only JavaScript
  Object Notation (JSON) trace checker for four scenarios:
  - **CAS-01:** stale precondition returns HTTP (Hypertext Transfer Protocol)
    409 with `current-version-precondition-failed`; no changed pointer,
    revision or lifecycle event.
  - **CAS-02:** two distinct writers race on the same baseline. Exactly one
    succeeds and becomes the published current revision; the loser gets
    precondition conflict, contributes no revision or side effect, and the
    old immutable history stays unchanged.
  - **CAS-03:** identical same-version retry succeeds before now-stale
    pointer evaluation and creates no additional revision or effect.
  - **CAS-04:** a reused immutable version ID with different fingerprint
    conflicts with `version-content-conflict` and leaves storage unchanged.
- `Scripts/test_breeding_pipeline_cas_trace.py`: **21 local positive and
  negative tests**, including reversed winning client, double success,
  wrong conflict code, changed historical fingerprints, missing barrier,
  leaked losing revision/side effects, draft winner, and replay side effects.
- Static conformance workflow integration for the synthetic verifier
  tests. The script remains opt-in for independently captured traces.

## Trace format (synthetic example, CAS-01)

```json
{
  "scenario": "CAS-01",
  "before": {
    "currentVersionId": "V3",
    "revisions": {
      "V3": {"fingerprint": "digest3", "publicationState": "published"}
    },
    "effects": {"e3": "V3"}
  },
  "requests": [{
    "client": "A", "versionId": "V4",
    "fingerprint": "digest4", "expectedCurrentVersionId": "V2"
  }],
  "responses": [{
    "client": "A", "status": 409,
    "errorCode": "current-version-precondition-failed"
  }],
  "after": {
    "currentVersionId": "V3",
    "revisions": {
      "V3": {"fingerprint": "digest3", "publicationState": "published"}
    },
    "effects": {"e3": "V3"}
  }
}
```

The `fingerprint` is a comparison token captured by an external
test harness. This script **does not compute or prescribe a cryptographic
digest algorithm**; the project's canonicalization and digest decisions
govern that choice separately.

Invoke the trace checker:

```sh
python Scripts/verify_breeding_pipeline_cas_trace.py \
  --trace PATH_TO_OBSERVED_TRACE.json
```

The required `effects` snapshot maps lifecycle event identity to affected
revision identity. Empty maps may be used only where the independent harness
can genuinely observe and attest absence of such events. The verifier
cannot itself prove event visibility, durable commit or real concurrency.

## Local verification and limits

```sh
cd /mnt/data/brapigenx_mission025
python -m unittest -v test_breeding_pipeline_cas_trace.py
python -m py_compile verify_breeding_pipeline_cas_trace.py test_breeding_pipeline_cas_trace.py
```

**21/21 synthetic tests passed.** Exact tested Git object hashes:

- verifier: `38c1b7cadebd13c0255eaac12f475b09429a50bb`;
- tests: `67a90c621d38cc4ac6c454f706a52dc89bee3866`.

Only trace-shape and selected state-invariant checks have been run;
**no real concurrent service run was performed**. A complete
implementation-independent conformance result still needs CAS-05..CAS-16,
independent authenticated clients, durable before/after readback and
transaction failure injection, followed by negative authority tests.

No RFC (Request for Comments) 154 maturity change, public application
programming interface (API) change, official Breeding API (BrAPI) version
2.1 source alteration, or new production implementation was made.
