# Mission 115 — Validate the actual nested provenance and evidence links

**Date:** 2026-11-25. **Starting source:** Mission 114 review head `ff53a2981a0f82c07ee487e146b88f444275b5e0`. **Dependencies:** integrate Missions 112–114 in order before retargeting.

## Confirmed false-green risk

Registered **L-07** promises that the provenance `inputsDigest` and `evidenceLinks` of a submitted observation survive a completed analysis-job round trip. The existing assertion implementation searched for the original `inputsDigest` as a substring of `json.dumps(payload)`. It did not verify the correct response location, the actual provenance object, evidence link identity or query and response digests. An unrelated copy of the old digest elsewhere in the response could make a corrupted provenance record appear conformant.

## Bounded correction

- Compare the full provenance mapping on the returned observation to the provenance of the *actual submitted request* held in the runner's live context.
- Require HTTP 200, expected job identity, terminal `COMPLETED` status and one structured returned observation before comparing provenance.
- Add eleven deterministic mocked-response tests for exact round trip, changed input/response/query digests, evidence-link deletion, changed actor, wrong job identity or status, missing observations and bad transport status.
- Run the test suite as an enforced hosted static-conformance step. Preserve registered probe L-07, proposed GenX schemas, operation identity, reference servers and scientific policy.

## Falsifiers and limits

```sh
python Scripts/test_provenance_roundtrip_integrity.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py --server http://127.0.0.1:18080/genx/v1 --only L-07
```

The live command requires the project-owned Python reference server to be started separately. Require complete static, Python live, TypeScript differential/legacy and specification generation at the exact pull-request head before merge, then recheck integrated `main`.

**Evidence boundary:** Structural equality proves only that one submitted provenance mapping was echoed unchanged by the in-memory reference server; it does not validate provenance truth, recorded actor identity, scientific model correctness, underlying evidence payload bytes, field-specific digest preimages, cryptographic signatures, durable persistence, or external-vendor conformance. No official Breeding Application Programming Interface (BrAPI) version 2.1 source, GenX wire contract, Request for Comments (RFC) maturity or pending spatial-governance decision is changed.
