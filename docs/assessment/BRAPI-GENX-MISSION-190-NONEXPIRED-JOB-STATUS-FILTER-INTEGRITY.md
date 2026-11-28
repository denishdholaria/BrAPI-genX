# Mission 190 — Non-EXPIRED lifecycle-status Job filter integrity

**Status:** implemented; hosted checks required before integration.
**Baseline:** `7c750672b2bf36569d50c47368a71e4276d550e1`.
**Dependency:** Mission 189, Pull Request #139.
**Scope:** registered L-25 live evidence, manifest integrity, and existing mandatory collection mutation suites.

## Confirmed false-positive

The published `GET /jobs` contract advertises six status values:
`SUBMITTED`, `RUNNING`, `COMPLETED`, `FAILED`,
`CANCELLED`, and `EXPIRED`.

Missions 187–189 verify `status=EXPIRED` (alone and combined with
`jobType`), `jobType` alone, and unfiltered collections. L-25
previously never requested any of the **five remaining** status
filters. A server could ignore `status=COMPLETED`, return unrelated
lifecycle states under `status=FAILED`, or truncate a
`status=RUNNING` tail page while passing every registered status
filter probe.

## Bounded correction

- Register a mandatory L-25 first-page request for each of the five
  remaining statuses, each with `page=0&pageSize=2`.
- Introduce one `filtered_job_status_integrity` assertion whose
  value must be a supported non-`EXPIRED` status and whose request
  path must match that value exactly.
- Dispatch all five assertions through the **existing**
  `filtered_job_collection_problem` validator. For each filtered
  response, enforce the requested status on **every** row and
  **every** advertised page, with stable pagination counters,
  complete page slices, unique nonempty Job identities, required
  job types, and schema-valid optional fields.
- Continue existing expired-result confidentiality checks on
  `EXPIRED` records wherever they appear, including unfiltered,
  type-only and previously registered filtered lists.
- Do **not** introduce an invented rule that all nonexpired Jobs
  expose results. A `COMPLETED` Job's result may be present,
  null or omitted as permitted by the current wire schema.
- Treat an empty filtered list as valid structural evidence only;
  it does not prove completeness or discoverability of an
  independently known Job.
- Fail closed on missing later pages, wrong lifecycle states,
  inconsistent metadata, duplicate identities or malformed rows.
- Protect every one of the five mandatory request/expected-status
  pairs against removal, substitution, path drift or misspelling.
- Extend mandatory collection regression suites with
  valid nonexpired result visibility, null/absent results,
  status mismatch on first and later pages, missing pages,
  duplicates, invalid fields, malformed page metadata and
  complete pagination.

## Verification

```sh
python Scripts/test_collection_envelope_integrity.py
python Scripts/test_collection_pagination_arithmetic.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Required hosted static conformance, live-reference,
independent-runtime differential and specification generation
must pass before merging.

## Boundaries

No published GenX Job wire schema or official BrAPI
(Breeding Application Programming Interface) version 2.1
contract changes. No added lifecycle timing, result-availability,
access-control or expiry policy. The Python and TypeScript reference
servers already support these lifecycle-status filters;
no server implementation change is needed.

The probe proves that returned pages are internally consistent
and satisfy the requested status. It does not establish global
record completeness for empty filters or provide a
snapshot-consistent pagination guarantee under concurrent mutation.
