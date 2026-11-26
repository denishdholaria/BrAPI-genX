# Mission 180 — Terminal Job pre/post-DELETE schema integrity

**Status:** implemented; hosted checks required before merging.
**Dependency:** Mission 179, Pull Request #129.
**Scope:** registered L-03 terminal-state-retained assertion,
mandatory synthetic regression suite, conformance guide and probe expectation.

## Confirmed false-positive risk

L-03 originally checks exact terminal Job identity, status and result
preservation after rejecting DELETE. It did not validate the optional
progress or timestamp fields on the final returned Job. A malformed
post-DELETE record could pass if its original identity and completed
result remained intact. Synthetic L-03 tests stub terminal polling,
so the pre-DELETE baseline independently needs the same schema check.

## Bounded correction

- Require `valid_job_wire_fields` for both pre-DELETE baseline
  and post-DELETE stored Job, reusing the status, bounded optional
  progress and timezone-bearing optional timestamp validator.
- Preserve exact original `jobDbId`, original jobType/idempotencyKey,
  immutable terminal state and exact original result, including nested data.
- Permit optional server-managed progress and timestamps to legitimately
  differ between reads. No new immutability or ordering policy.
- Add negative regressions for malformed progress/timestamps on either
  side of the rejected DELETE, and a positive schema-valid change control.

## Verification

```sh
python Scripts/test_terminal_cancel_retained_state.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require hosted static conformance, live-reference conformance,
independent-runtime differential and specification generation before
merge. Observe post-merge main workflows separately.

## Boundaries

No official BrAPI (Breeding Application Programming Interface) v2.1
contract, new GenX wire field, lifecycle-transition rule, scientific
maturity or embargo policy change. This mission does not expand
record-immutability semantics beyond the identity, status and
completed-result guarantees already in L-03.
