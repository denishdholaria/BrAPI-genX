# Mission 178 — Schema-valid expired Job readback

**Status:** implemented; hosted checks required before merge.
**Dependency:** Mission 177, Pull Request #127.
**Scope:** registered L-05 direct GET of an expired Job,
its mandatory synthetic regression suite and conformance guidance.

## Confirmed false-positive risk

The published `Job` schema requires `jobDbId`, `jobType`,
and enumerated `status`. Optional `progress` is a bounded number,
timestamps require timezone-aware date-time encoding, and
`idempotencyKey` is a string when present. Before this mission,
L-05 accepted a GET response with the right expired identifier and
`EXPIRED` status and no exposed result even if `jobType`
was missing or the optional fields were malformed.

## Bounded correction

- Keep L-05's original known expired-job identity,
  `EXPIRED` state, and withheld-result assertions.
- Require a nonempty string `jobType` in the returned record.
- Reuse `valid_job_wire_fields` for required state, optional
  bounded progress and optional timezone-bearing timestamps.
- Require string-typed `idempotencyKey` when present.
- Allow both absent result and explicit null result; reject any
  other returned result value.
- Extend the existing mandatory expired-result regression suite
  with missing/blank/nonstring job types, invalid optional fields,
  positive valid progress and timestamp controls, while preserving
  every existing confidentiality regression.

## Verification

```sh
python Scripts/test_expired_job_result_withheld.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require hosted static conformance, live-reference conformance,
independent-runtime differential and specification generation
before merging. Confirm post-merge main workflows separately.

## Boundaries

No official BrAPI (Breeding Application Programming Interface)
version 2.1 contracts, proposed GenX wire schemas, expiry timing
policy, Job transition semantics, scientific maturity decisions
or embargo-visibility policy change. Broader terminal polling
schema enforcement is a distinct potential future audit.
