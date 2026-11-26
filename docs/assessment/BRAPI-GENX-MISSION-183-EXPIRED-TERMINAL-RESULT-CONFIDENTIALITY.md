# Mission 183 — Expired terminal Job result confidentiality

**Status:** implemented; hosted verification required before merge.
**Baseline:** `ae6b5d478133d0edb173f04e7e5e2af73f4ddaf0`.
**Scope:** existing L-03, L-05 and the shared terminal polling
validator; no Job schema or expiry policy changes.

## Confirmed false-positive

Registered L-05 already rejects an `EXPIRED` Job whose `result`
field contains non-null data. After Missions 179–182, the
`wait_terminal` helper and L-03 terminal-cancellation readback
validated the Job schema and original identity but did not apply
the L-05 result-withholding policy.

An `EXPIRED` job with result data could terminate polling.
More seriously, L-03's pre-DELETE baseline and post-DELETE
readback could both contain the **same leaked result**, passing
its unchanged-result comparison. Result preservation does not
prove confidentiality.

## Bounded correction

- Implement one `expired_job_result_withheld` predicate:
  an EXPIRED Job may omit `result` or supply explicit null;
  any other value is rejected.
- Apply it in `wait_terminal` before returning the EXPIRED
  terminal response, and in L-03 to **both** pre- and post-DELETE
  terminal records when status is EXPIRED.
- Reuse the same predicate for L-05's existing expired-result
  assertion rather than maintaining a separate, drifting rule.
- Add negative regressions for leaked result payloads, including
  the decisive case of equal leakage in both L-03 snapshots and
  non-null falsy values. Add positive controls for absent and
  explicit-null withheld results.
- Preserve the valid EXPIRED state, original job identity,
  request binding, required wire fields, terminal-state immutability
  and the completed-result preservation requirements.

## Verification

```sh
python Scripts/test_terminal_cancel_retained_state.py
python Scripts/test_expired_job_result_withheld.py
python Scripts/test_deprecated_inference_completion.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require hosted static conformance, live-reference conformance,
independent-runtime differential and specification generation
on the exact pull-request head before merge. Observe post-merge
main workflows separately.

## Boundaries

The existing result-withholding rule is reused, not broadened.
No official BrAPI (Breeding Application Programming Interface)
version 2.1 contract, new GenX schema field, lifecycle transition,
expiry time, scientific maturity or embargo metadata visibility
decision is introduced.
