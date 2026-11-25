# Mission 138 — Embargo denial response confidentiality

**Status:** implemented; hosted verification required before integration.
**Scope:** registered L-20, HTTP error parsing and a negative regression suite.
**Scientific and wire-schema impact:** none.

## Confirmed false-positive risk

L-20 previously required only a 403 response after an embargoed package was
registered. A server could produce 403 while echoing the entire package
metadata or evidence digest in a JSON body or textual error, passing L-20.

The runner's generic HTTPError handler also discarded non-JSON error bodies,
so even a dedicated denial assertion would not have seen leaked text.

## Correction

- Capture the original package submission independently of server-returned
  response identifiers.
- Preserve plain-text HTTP error bodies as `{"error": "<body>"}` within
  the **local test runner**. This does not alter the wire contract or
  reference server's denial.
- Verify a 403 response and an object-shaped denial with no `result` or
  `data` envelope, no `payloadRefs`, and no exact submission-derived
  sensitive field strings: title, license, publisher, embargo timestamp,
  citation IDs, creators, evidence endpoints and digests.
- Keep the denial's package identifier and generic embargo message legal.
- Protect the registered L-20 submit → embargoed GET sequence in manifest
  validation. Require the `embargo_denial_no_payload` assertion.
- Add `Scripts/test_embargo_denial_no_payload.py` negative mutation tests
  for structured/serialized leaks, wrong status/identity, and error parser
  preservation. Register in the hosted static workflow.

## Policy boundary

RFC-006 §2 states metadata remains findable during embargo, while the
reference server's single-record GET currently denies the whole metadata
record. RFC-006 §5 leaves the precise embargo metadata visibility policy
**requires-decision**. The unfiltered collection endpoint currently exposes
metadata entries, including embargoed packages, without serving payload
bytes. This mission does **not** designate all such metadata as confidential,
redact the collection, add authorization, or settle that governance decision.

The content-leak assertion uses exact string matching against the submitted
fixture; it is not a substitute for payload-level access enforcement,
side-channel analysis, or robust third-party information-flow testing.

## Verification

```bash
python Scripts/test_embargo_denial_no_payload.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Mandatory hosted static, live-reference, independent runtime, and
specification-generation checks must pass before merge.
