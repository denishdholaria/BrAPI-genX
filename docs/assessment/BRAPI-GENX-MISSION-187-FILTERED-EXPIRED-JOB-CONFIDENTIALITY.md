# Mission 187 — EXPIRED-filtered Job collection confidentiality

**Status:** implemented; required hosted verification before merge.
**Dependency:** Mission 186 (Pull Request #136).
**Scope:** mandatory L-25 filtered collection readback, reference-server query handling, and existing mandatory conformance mutation suites.

## Confirmed false-positive

Mission 186 traverses each advertised page of the **unfiltered** `GET /jobs`
collection, but does not inspect `GET /jobs?status=EXPIRED`. Both reference
servers previously ignored the `status` query parameter altogether. An
implementation could return a valid unfiltered collection while returning
a different, leaking, status-filtered collection and still pass L-25.
The published Jobs endpoint already advertises lifecycle-status filtering.

## Bounded correction

- Add a mandatory fifth L-25 request to
  `/jobs?status=EXPIRED&page=0&pageSize=2` after the original Job and
  model readbacks.
- Require HTTP 200, a properly typed collection envelope, nonnegative
  count, positive exact requested page size, and coherent pagination.
  An empty result is legitimate (with `totalPages` either 0 or 1) but
  establishes only shape/filter evidence, not nonvacuous confidentiality.
- Follow **every** advertised page using the same status filter and
  page size; reject missing pages, inconsistent counters, truncated
  slices and repeated identities.
- Every row must carry a valid nonempty Job ID and type, exact
  `EXPIRED` lifecycle status, valid optional Job fields, a typed optional
  idempotency key, and an absent or null `result`. Even non-null empty
  objects and falsy values fail.
- Update the Python and TypeScript reference servers to honor existing
  `jobType`, `status`, `page` and `pageSize` query parameters on
  `GET /jobs`. Unfiltered behavior remains equivalent.
- Lock the fifth request and its assertion into the conformance
  manifest validator, and include positive/negative mutations in
  mandatory existing L-25 suites.

## Verification

```sh
python Scripts/test_collection_envelope_integrity.py
python Scripts/test_collection_pagination_arithmetic.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

GitHub-hosted static, live-reference, cross-runtime and generated
specification checks must all pass before merging.

## Boundaries and residual risk

- No changes to official BrAPI (Breeding Application Programming
  Interface) version 2.1 or to the published GenX Job wire schema.
- No new expiry timing, lifecycle transitions, storage, authorization or
  scientific maturity policy.
- L-25 checks filtered confidentiality for the response data a test
  server actually exposes. An **empty** filtered result cannot establish
  that a previously existing expired Job was discoverable: separate
  known-expired L-05 evidence covers direct resource retrieval.
- Offset pagination is not snapshot-consistent under concurrent
  mutation. A moving collection may fail closed rather than produce
  a false pass.
