
# Mission 147 — Created job/model collection record integrity

**Status:** implemented; required hosted verification pending.
**Scope:** live L-25, its existing collection-assertion executor, synthetic regressions and documentation.
**Baseline:** `main` at `79a14c4114a09b6dacadcdb190c41f095a5345c3`.

## Confirmed false-positive risk

Mission 139 made L-25's first-page pagination envelope mathematically
consistent, but the collection assertion still accepted **any** row with
the accepted jobDbId or modelDbId/modelVersion tuple. A server could return
the correct count and one matching identifier while changing the original
job type, idempotency key, model artifact digest, metrics or nested
provenance. Duplicated identical created records could also pass if the
pagination counters were updated consistently.

## Correction

- Bind listed job identity to the accepted jobDbId and the original POST's
  jobType and idempotencyKey; require exactly one row with that jobDbId and
  exactly one row with the submitted idempotencyKey, and require they are
  the **same row**.
- Bind the accepted modelDbId/modelVersion to the original model submission,
  not merely the response or a collection entry.
- Require exactly one row with that model identifier/version pair and
  verify every original submitted model field, including nested values and
  provenance, is preserved. Additional server-managed fields are allowed.
- Preserve unrelated jobs, models and other versions as legitimate collection
  neighbors rather than assuming the entire collection contains only the
  probe's created record.
- Extend the existing mandatory `Scripts/test_collection_pagination_arithmetic.py`
  and `Scripts/test_collection_envelope_integrity.py` suites with duplicate,
  wrong-key, changed-model-field and accepted-identity mutation tests.
- Keep registered four-step L-25 procedure and its existing manifest guard.
  No new assertion vocabulary or hosted workflow wiring is necessary.

## Verification

```sh
python Scripts/test_collection_pagination_arithmetic.py
python Scripts/test_collection_envelope_integrity.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Require the hosted static, Python live-reference and independent runtime
conformance jobs, and specification generation, to pass before merging.

## Boundaries

No official Breeding Application Programming Interface (BrAPI) 2.1
contract, GenX wire schema, scientific maturity, or unresolved embargo
visibility policy is modified. This assures that the first page contains
the probe's original created records and does not establish complete
multi-page traversal for arbitrary large pre-populated collections,
cross-request snapshot isolation, or durable storage guarantees.
