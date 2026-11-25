# Mission 173 — Replay and concurrent Job acknowledgment status integrity

**Status:** implemented; verify hosted checks before merge.
**Dependency:** Mission 172, Pull Request #122.
**Scope:** registered L-01 identical replay acknowledgment and L-24
eight-way concurrent Job acknowledgments, existing mandatory
regression suites, conformance documentation.

## Confirmed gap

Job.status is a required enumerated field of the published GenX Job
schema. Mission 172 verifies the field in initial Job acceptance and
warned-inference acceptance. Identical replay and eight concurrent
responses were still accepted based only on successful HTTP statuses,
matching identifiers, type and idempotency key. Malformed Job status
could therefore escape the runner despite correct stored state.

## Bounded correction

- Reuse the shared `valid_job_lifecycle_status` helper from Mission
  172 for identical replay and **every** concurrent response.
- Preserve L-01's HTTP 200/202 replay policy and L-24's existing
  success-status policy and complete stored-effect readback.
- Permit independently changing valid lifecycle states across
  concurrent responses rather than requiring identical statuses.
- Add negative mutations for missing, unsupported and nonstring
  statuses in the replay or only one of eight acknowledgments;
  verify failure before collection readback.
- Add positive RUNNING replay and mixed SUBMITTED/RUNNING concurrent
  controls. Retain positive extra-server-metadata behavior.

## Verification

```sh
python Scripts/test_job_replay_single_stored.py
python Scripts/test_concurrent_job_stored_effect.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require hosted static conformance, live-reference conformance,
independent-runtime differential and specification generation before
merge. Inspect post-merge main workflows separately.

## Boundaries

No official BrAPI (Breeding Application Programming Interface)
version 2.1 source contract, proposed GenX Job wire schema,
scientific maturity, lifecycle transition policy or unresolved
embargo visibility policy changes.
