# BrAPI GenX — Conformance

Provides repeatable static and live checks for the GenX proposal's schemas,
endpoint identities, cross-generation route reuse, and behavior-level contracts.
A passing check proves only the tested claim; it does not make GenX normative or
establish production readiness.

## Two tiers

| Tier | Needs | Run |
|---|---|---|
| `static` (S-01…S-21) | this repo only | `python Scripts/checkGenXConformance.py` from the `BrAPI_genX` root |
| `live` (L-01…L-28) | a GenX test server | `python Scripts/checkGenXConformance.py --server https://host/genx/v1` |

Static probes run by default. Live probes `SKIP` without `--server` and fail
closed with it.

Note: `probes.yaml` currently registers S-01…S-21 only. References to an
"S-22" guardrail in this document and in `RESULTS.md` describe a proposed
capability-to-operation guardrail that is not yet a registered probe; this
discrepancy is tracked in the Phase 0 consistency register. Run the endpoint-identity negative tests separately with
`python Scripts/test_endpoint_identity.py`; these exercise deliberately broken
synthetic contracts to ensure identity errors fail closed. Both tiers are declared in [`probes.yaml`](./probes.yaml);
fixtures live in [`fixtures/`](./fixtures). The probe list is the authority —
the runner is one execution of it, replaceable by a future BRAVA harness.
Recorded runs live in [`RESULTS.md`](./RESULTS.md).

## Reference test servers

`Scripts/genx_test_server.py` (standard library only, in-memory, no
persistence, no authentication) implements the skeleton for live execution:

```shell
python Scripts/genx_test_server.py --port 8080 --profile genx &
python Scripts/checkGenXConformance.py \
  --server http://127.0.0.1:8080/genx/v1 --expired-job JOB_EXPIRED
```

`--profile v21` serves the V2.1-only shape for probe L-06. Supported job
types: `germplasm_search`, `analysis` (echoes `parameters.observation` for
L-07). `JOB_EXPIRED` is pre-seeded for L-05. Same-key/different-body is
rejected with `409` (evidence for RFC-001 §8 decision #1). Versioned `VariableTerm` records are exposed under `/genx/v1/variable-terms`:
`genxListVariableTermVersions` lists, `genxPublishVariableTermVersion` publishes
one immutable version, and `genxGetVariableTermVersion` retrieves one. These
are not the V2.1 `ObservationVariable` contract: the routes are intentionally distinct, `/brapi/v2/variables` versus `/genx/v1/variable-terms`.
See [`ENDPOINT-IDENTITY.md`](../ENDPOINT-IDENTITY.md). Lot
ledger entries use `/genx/v1/seedlots/{seedLotDbId}/ledger` with RFC-003
append/replay/conflict semantics for L-10/L-11 (lots auto-provisioned).
Models live under `/genx/v1/models` with RFC-004 replay/conflict semantics for
L-12/L-13; `inference` jobs bind to registered models for L-14/L-15 (the
reference `outputs.echo` stub exists only to prove digest binding). Matrix
references live under `/genx/v1/variantmatrices` with RFC-005 replay/conflict
semantics for L-16/L-17. Packages live under `/genx/v1/fair-packages` with RFC-006
replay/conflict/embargo semantics for L-18–L-20. Samples live under
`/genx/v1/telemetry` with RFC-007 batch/replay/conflict/aggregate semantics for
L-21–L-23.

A second, black-box TypeScript/Bun server
(`Scripts/genx_test_server_ts.ts`, run with `bun`) implements the RFC-001
core + RFC-004 inference subset to prove cross-runtime interop (RESULTS.md
run 9). Canonical JSON there is sorted-keys + compact separators + UTF-8;
digest agreement with Python holds for ASCII payloads.

## Probe index

Static: `$ref` resolution (S-01), fixture shape (S-02, S-09, S-11), enums (S-03),
digest format (S-04), date-time format (S-05), replay/conflict fixture
relations (S-06), capability advertisement grounding (S-07), V2.1 fallback
shape (S-08), namespaced term identifiers (S-10), decimal-string quantities
(S-12), model artifact shape (S-13, S-14), matrix reference shape (S-15, S-16),
package envelope shape (S-17, S-18), telemetry point shape (S-19, S-20), endpoint
identity/operationId uniqueness/registered overlaps (S-21), and capability-to-operation
mapping plus advertised job-type validation against the experimental ServerInfoV3
registry (S-22). S-22 is a review guardrail for this proposal profile, not an accepted
BrAPI requirement.

Live: idempotent replay (L-01), key conflict (L-02), terminal-cancel rejection
(L-03), unknown job type (L-04), expiry (L-05), V2.1-only fallback negotiation
(L-06), provenance round-trip (L-07), term replay (L-08), term conflict (L-09),
ledger replay (L-10), ledger conflict (L-11), model replay (L-12), model
conflict (L-13), inference digest binding (L-14), unknown/revoked model
rejection (L-15), matrix replay (L-16), matrix conflict (L-17), package
replay (L-18), package conflict (L-19), embargo denial (L-20), telemetry
replay (L-21), telemetry conflict (L-22), aggregate recomputation (L-23),
concurrent-submit single effect (L-24), list envelopes (L-25), windowed
buckets (L-26), deprecated warning (L-27), pagination slice (L-28), and live
capability-advertisement/route-registry agreement including supported job types (L-29). Older static checks have historical mutation evidence in RESULTS.md run 8. The endpoint-identity guardrail has dedicated synthetic negative tests in `Scripts/test_endpoint_identity.py`.

## Status contract

Each probe reports `PASS`, `FAIL`, or `SKIP` (live without `--server` only).
Any `FAIL` exits non-zero. No probe may depend on another probe's side
effects; live probes that create server state use fresh idempotency keys.


## ServerInfoV3 capability audit

The experimental [capability registry](./capability-registry.json) maps every example capability to full GenX route templates, HTTP methods, and operation IDs. See [CAPABILITY-NEGOTIATION.md](../Core/ServerInfoV3/CAPABILITY-NEGOTIATION.md) for the findings and review questions. Run the dedicated mutation suite with:

```shell
python Scripts/test_capability_negotiation.py
```

The suite proves that duplicate/unregistered capability names, duplicate or changed versions, false method summaries, stale routes/operation IDs, missing maps, wrong/missing/duplicate/malformed job type lists, job-type/runtime drift, malformed scope lists, duplicate auth profiles, and duplicated operation references fail closed. S-22 validates the checked-in fixture against the registry/OpenAPI files; L-29 checks the in-memory reference server’s live advertisement against the same registry. Neither probe treats scopes or auth-profile names as proof of access-control enforcement.

D-21 (operation mapping and version-token semantics), D-22 (scope/auth-profile semantics), and D-23 (job-type advertisement and compatibility) remain deferred. In particular, the reference server accepts and ignores bearer tokens; it is an in-memory conformance prototype, not a secured deployment.

## Digest interoperability candidate (experimental)

The shared vector corpus at [digest-vectors.json](./digest-vectors.json) distinguishes structured-JSON canonicalization from exact-byte integrity digests. Run both independent candidate implementations with:

```shell
python -m pip install 'rfc8785==0.1.4'
python Scripts/test_digest_vectors.py
cd Scripts/digest-conformance && bun install && bun run test
```

The corpus includes Unicode, UTF-16 property ordering, number formatting, duplicate-key rejection, exact-byte hashes, and known disagreement between the two existing reference-server legacy serializers. D-02 now accepts RFC 8785 (JCS) as BrAPI-GenX's `JCS-RFC8785` method for generic canonical JSON; this is not an accepted BrAPI community standard. See [DIGEST-INTEROPERABILITY.md](./DIGEST-INTEROPERABILITY.md). The current reference servers have **not** been migrated by this documentation change.

The [digest-scope inventory](./DIGEST-SCOPE-INVENTORY.md) records the current per-field preimage ambiguity. Passing the candidate vectors is not sufficient to resolve D-02: field meaning, exact input scope, and migration/versioning must also be specified.

The [digest decision brief](./DIGEST-DECISION-BRIEF.md) preserves the historical comparison of the legacy serializer, JCS, a custom canonicalizer, and exact-byte hashing, and identifies field-level implementation work still requiring review.

## BreedingPipeline and BreedingScheme candidate gates

The approved-candidate breeding contract has two additional static gates:

- `python Scripts/validate_breeding_pipeline_candidate_fixtures.py` validates the historical design-evidence corpus.
- `python Scripts/validate_breeding_pipeline_contract_fixtures.py` validates the approved-candidate fixtures for immutable identity, embedded scheme-version equality, stage/transition/task integrity, target-context rules, authority-qualified references, and exact execution contexts.
- `python Scripts/check_breeding_pipeline_api_contract.py` checks the actual OpenAPI schema composition and source-server filter pairs against the endpoint registry.

The corresponding fixtures are in `docs/assessment/BRAPI-GENX-BREEDING-PIPELINE-CANDIDATE-FIXTURES.json` and `docs/assessment/BRAPI-GENX-BREEDING-PIPELINE-CONTRACT-FIXTURES.json`. These gates are implementation-independent static checks; they do not prove production runtime behavior or promote RFC-154 from candidate status.
