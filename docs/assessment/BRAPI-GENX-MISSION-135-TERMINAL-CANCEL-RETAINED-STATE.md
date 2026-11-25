# Mission 135 — Rejected terminal cancellation retained-state assurance

**Status:** implemented; required hosted verification pending.  
**Scope:** registered L-03 conformance probe and regression test.  
**Dependency:** Mission 134. No official BrAPI 2.1 or GenX schema change.

## Gap

L-03 claimed that cancelling a terminal job is rejected and its terminal
state remains unchanged. Previously the executable probe stopped after
observing a rejected DELETE without reading back the original job.

## Postcondition

L-03 now submits a synthetic job, polls for terminal state, attempts a
DELETE against the captured jobDbId, and re-GETs the same job. The runner
captures the baseline job identity and status from the terminal poll result.

The `terminal_state_unchanged` assertion requires:

- A valid captured baseline jobDbId matching the submitted job.
- One of the terminal statuses COMPLETED, FAILED, CANCELLED or EXPIRED.
- HTTP 200 for the GET, the same jobDbId, and exactly the original
  terminal status after cancellation was rejected.

The manifest guard requires this three-step procedure including the
`wait_terminal` directive and the terminal-state GET check. The dedicated
`Scripts/test_terminal_cancel_retained_state.py` regression suite tests
all four valid terminal statuses plus changed/missing state, unavailable
records, invalid baseline and an accidentally accepted DELETE. Hosted
static conformance and the workflow-scope guard require the regression.

## Verification commands

```bash
python Scripts/test_terminal_cancel_retained_state.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Required hosted static, live-reference, independent runtime and generation
checks must pass before merging.

## Boundaries

This is observable state verification in a synthetic in-memory reference
server. It does not prove durability, crash/restart behavior, distributed
job cancellation, external side effects, or third-party conformance.
