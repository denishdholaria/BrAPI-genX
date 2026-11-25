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

The authoritative [`probes.yaml`](./probes.yaml) currently registers **S-01
through S-21** and **L-01 through L-28**. Historical experimental branches
recorded results for an additional S-22 capability-mapping guard and L-29
advertisement check; neither identifier is registered in the present probe list.
Do not count them as active probes. The separately executed
`Scripts/test_capability_negotiation.py` and
`Scripts/test_endpoint_identity.py` exercise capability metadata and
deliberately invalid operation identities. Fixtures live in [`fixtures/`](./fixtures);
historical runs (not necessarily on the current commit) live in
[`RESULTS.md`](./RESULTS.md). Passing a historical run is not a substitute for
validating the current revision.

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
identity/operationId uniqueness/registered overlaps (S-21). Capability-to-operation
mapping is tested separately by `Scripts/test_capability_negotiation.py`; the
historical S-22 designation is **not** a registered probe.

Live: idempotent replay (L-01), key conflict (L-02), terminal-cancel rejection
(L-03), unknown job type (L-04), expiry (L-05), V2.1-only fallback negotiation
(L-06), provenance round-trip (L-07), term replay (L-08), term conflict (L-09),
ledger replay (L-10), ledger conflict (L-11), model replay (L-12), model
conflict (L-13), inference digest binding (L-14), unknown/revoked model
rejection (L-15), matrix replay (L-16), matrix conflict (L-17), package
replay (L-18), package conflict (L-19), embargo denial (L-20), telemetry
replay (L-21), telemetry conflict (L-22), aggregate recomputation (L-23),
concurrent-submit single effect (L-24), list envelopes (L-25), windowed
buckets (L-26), deprecated warning (L-27), and pagination slice (L-28).
Historical L-29 results describe a branch-specific experimental live
advertisement check, not a currently registered probe. Older static checks
have mutation evidence in `RESULTS.md` run 8. Endpoint-identity negative tests
run separately via `Scripts/test_endpoint_identity.py`.

## Status contract

Each probe reports `PASS`, `FAIL`, or `SKIP` (live without `--server` only).
Any `FAIL` exits non-zero. When `--only` is used, the runner now requires
exactly one registered probe identifier. An unknown, duplicate or malformed
selection fails; selecting a live probe without `--server` also fails rather
than silently reporting a skip. **Any explicitly selected probe that reports
`SKIP` now causes a non-zero process exit** (Mission 107), including L-05 when
`--expired-job` is omitted. An unfiltered static run still reports `SKIP`
for live probes when no server is provided. See the selection regression tests
in `Scripts/test_conformance_probe_selection.py` (Mission 103).
No probe may depend on another probe's side
effects; live probes that create server state use fresh idempotency keys.


## ServerInfoV3 capability audit

The experimental [capability registry](./capability-registry.json) maps every example capability to full GenX route templates, HTTP methods, and operation IDs. See [CAPABILITY-NEGOTIATION.md](../Core/ServerInfoV3/CAPABILITY-NEGOTIATION.md) for the findings and review questions. Run the dedicated mutation suite with:

```shell
python Scripts/test_capability_negotiation.py
```

The dedicated suite checks that duplicate/unregistered capability names, changed versions, false method summaries, stale routes or operation IDs, malformed job-type lists, and invalid scope/profile metadata fail closed. The historical S-22 and L-29 labels refer to experiments that are **not** registered in the current probe manifest. A passing metadata test does not prove authorization enforcement or production security.

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

## Hosted cross-runtime differential tier (Mission 100)

The conformance workflow runs an additional `independent-runtime-differential`
job that starts fresh Python and separately authored TypeScript/Bun reference
servers. The existing `Scripts/genx_differential_check.py` compares **nine**
RFC-001/RFC-004 subset requests, including job replay/conflict and model
registration/inference. It strips volatile timestamps and server names, and
allows a *subset* of advertised capabilities only when the remaining
server-info envelope matches. A mismatch or server-start failure fails the job.

These are **two project-owned reference implementations**, not independent
external-vendor servers. Passing the comparison is not a comprehensive GenX
interoperability certification, scientific validation, authorization proof
or production-readiness guarantee. Non-ASCII and numerical boundary digest
vectors are tested separately. See [Mission 100 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-100-CROSS-RUNTIME-DIFFERENTIAL-CI.md).

## Differential status expectations (Mission 101)

The nine-request cross-runtime checker validates the HTTP status returned by
**each** reference implementation before comparing their normalized bodies.
The expected statuses are `200, 202, 200, 409, 400, 200, 200, 200, 202` for,
respectively, server information, initial job submission, exact replay,
changed-body replay conflict, invalid job type, expired job retrieval, model
registration, model replay and inference submission. Both servers agreeing on
a wrong status is **not** a pass. Negative mutations in
`Scripts/test_genx_differential_check.py` protect this check.

These are expectations for the current RFC-001/RFC-004 test sequence, not a
complete normative response code catalogue for all GenX operations.

## Independent TypeScript live probes (Mission 102)

In addition to the nine immediate-response differential comparisons, the
hosted cross-runtime job runs the **registered** live probes `L-14` and
`L-24` directly against the TypeScript/Bun reference server. `L-14`
registers a model, submits inference, awaits completion, and independently
recomputes `inputsDigest` from the test inputs. `L-24` tests eight
concurrent submissions with one idempotency key and checks that the server
creates exactly one job. Both run via the existing
`Scripts/checkGenXConformance.py --only` runner.

These are **two additional, subset-specific executions** of registered live
probes, not two newly registered probes, and do not validate the full GenX
operation catalogue, durable multi-instance idempotency, authorization, or
an external implementation. See [Mission 102 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-102-TYPESCRIPT-LIVE-PROBE-ASSURANCE.md).

## TypeScript model-identity and rejection probes (Mission 104)

The hosted TypeScript/Bun reference-server job now also executes existing
registered probes **L-12** (exact model-version replay), **L-13** (reject a
different artifact digest under the same published version), and **L-15**
(reject inference on unknown or revoked models). Together with Mission 102's
L-14/L-24 probes, these constrain the observable RFC-004 model/inference
subset without introducing any new wire contracts or probe identifiers.

Mission 104 originally verified only the L-13 conflict response. **Mission 105**
adds an explicit post-conflict retrieval and checks that the previously
submitted `modelDbId`, `modelVersion`, and `artifactDigest` remain unchanged.
This is an in-memory reference-server invariant, not a durability guarantee.
The models are in-memory reference stubs, not scientifically validated models.
See [Mission 104 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-104-TYPESCRIPT-MODEL-INTEGRITY-PROBES.md).

## Post-conflict model state verification (Mission 105)

The registered **L-13** model-conflict probe now fetches the exact version
after a rejected conflicting artifact registration and compares its model
identity, version and `artifactDigest` with the *original submitted request*.
The runner fails on an absent record, wrong status, changed digest, wrong
identity or incorrect version. Mutation tests model a server that returns the
expected conflict response but silently overwrites the stored artifact.

This checks an observable postcondition against both project-owned reference
servers when their normal hosted suites execute L-13. It does not establish
durable immutability, distributed race safety or production-grade authorization.
See [Mission 105 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-105-MODEL-CONFLICT-POSTCONDITION.md).

## Matrix and package post-conflict state verification (Mission 106)

Registered live probes **L-17** and **L-19** now perform a GET after a
conflicting registration is rejected, checking that the original matrix
`fileDigest` or package `license` remains associated with the original
resource identifier. Both compare against the initial submitted request, not
against a potentially altered second response. Mutation tests exercise
servers that reply `409` but silently change the stored record.

These checks run against the Python in-memory reference server. They do not
establish durable scientific-data integrity, real content-byte retrieval,
third-party interoperability, licensing authority or deployment security.
See [Mission 106 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-106-PUBLICATION-CONFLICT-POSTCONDITIONS.md).

## Explicit selection cannot succeed with skipped evidence (Mission 107)

The live L-05 expiry check needs a known expired job identifier supplied as
`--expired-job`. Before Mission 107, `--only L-05 --server …` without that
identifier exited successfully after reporting `SKIP`: an explicit request for
conformance evidence produced no evidence. The exit policy now treats any
`SKIP` from an explicitly selected probe as a failure, while retaining the
unfiltered runner's historical optional-fixture skip behavior. Regression
coverage is in `Scripts/test_conformance_probe_selection.py` and executes in
hosted static conformance. This change does not assert new scientific behavior
or amend the registered probe manifest.

See [Mission 107 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-107-SELECTED-PROBE-SKIP-FAIL-CLOSED.md).

## Registered-probe completeness and execution guard (Mission 108)

The conformance runner validates its registry before dispatching any probe.
The existing **21 static** and **28 live** registered identifiers are the
minimum verification baseline. Missing identifiers, duplicates, a mismatched
identifier/tier, an unknown static checker or absent/invalid live call steps
now cause an error instead of allowing a reduced or zero-check run to pass.
Additional correctly formed probe registrations remain possible; this guard
does not ratify new probes or change existing scientific contracts.

The mutation suite is included in the already-required
`Scripts/test_conformance_probe_selection.py` hosted static step. See
[Mission 108 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-108-PROBE-MANIFEST-COMPLETENESS.md).

## Binary exact-byte digest test corpus (Mission 109)

The existing digest corpus tested the raw-byte category using only UTF-8
strings. Mission 109 adds two **synthetic binary payloads** encoded as
canonical Base64 in the test fixture (not to be confused with their hash
preimages). Independent Python and TypeScript/Bun verifiers decode those
fixtures to raw bytes before calculating SHA-256. The vectors include NUL
octets, bytes above 127, an archive-like header and significant trailing
zero bytes. Invalid Base64, absent or ambiguous byte sources, a changed digest
and removal of a required vector are mutation-tested in both runtimes.

This verifies the cross-runtime *hash of identical bytes*, **not** that a
particular model archive, variant matrix or package digest actually binds to
the authoritative production payload. File packaging, transport
representation, field scope, scientific authority and durability remain
outside this test. See [Mission 109 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-109-BINARY-EXACT-BYTE-VECTORS.md).

## Hosted TypeScript version 2.1-only fallback probe (Mission 110)

A third, separately started TypeScript/Bun reference process uses the existing
`--profile v21` mode. The hosted cross-runtime job executes registered live
probe **L-06** against that process on loopback port 18083, checking that its
legacy `calls` server-info shape is accepted without new GenX capabilities.
All three reference-server processes are readiness-checked, logged on failure
and stopped. Workflow mutations protect the startup and active L-06 execution.

This demonstrates compatibility of one project-owned version 2.1-only server
shape with the project's conformance runner, not comprehensive official BrAPI
2.1 interoperability or external-vendor certification. See
[Mission 110 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-110-TYPESCRIPT-V21-FALLBACK-HOSTED.md).

## Legacy fallback server-info shape verification (Mission 111)

The existing S-08 static fixture and L-06 live legacy-negotiation checks use
a shared minimal shape validator. An HTTP 200 response must contain a nonempty
`result.calls` array whose entries have a nonblank `service` and nonempty
string arrays for `versions` and `methods`. The former check for merely the
presence of the `calls` key incorrectly treated null, scalar or otherwise
unusable data as sufficient negotiation evidence.

Twelve mutation and execution-path regressions cover valid responses and
malformed envelopes. The test is a subset-specific compatibility check of
project-owned in-memory reference servers; it is not complete version 2.1
schema certification, authenticated authorization or external conformance.
See [Mission 111 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-111-V21-FALLBACK-SHAPE-VALIDATION.md).

## Fail-closed live assertion manifest validation (Mission 112)

The registered conformance runner previously tolerated unknown names in
`calls[].assert`. A typo such as `stauts: 409` could therefore disable a
negative check while the probe still reported success. Live assertion
validation now rejects unknown assertion keys, empty/invalid assertion maps
and non-executable values (including false values for affirmative Boolean
assertions). It also requires the existing job replay and concurrent-request
flags to carry their corresponding identity/effect assertions.

The mutation suite checks these failure modes, including a command-line
attempt to run a probe from a corrupted manifest without contacting a server.
The suite executes in hosted static conformance and is protected against
workflow removal. The registered probe list, proposed application programming
interface and scientific semantics remain unchanged. See
[Mission 112 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-112-ASSERTION-FAIL-CLOSED.md).

## Live call directives and body fixture integrity (Mission 113)

The conformance manifest now rejects unknown `calls[]` directives, misspelled
`body_fixture` values, disabled capture flags and POST calls that have
neither a recognized body fixture nor a replay payload. Previously, unknown
fixture names could fall through as an absent request body; a negative probe
might then receive the expected rejection for a malformed request rather than
for the specific scientific or lifecycle condition under test.

The new regression suite covers these cases, along with the existing
replay/wait and capture constraints, and is enforced by the static workflow.
This protects the verification procedure; it does not modify production
wire contracts or certify an external service. See
[Mission 113 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-113-LIVE-STEP-FIXTURE-INTEGRITY.md).

## Post-conflict telemetry retained-value verification (Mission 114)

Registered live probe **L-22** already promised that a conflicting telemetry
value would be rejected without overwriting the original stored reading, but
previously stopped after checking the conflict response. It now performs a
follow-up GET filtered by the unique test device and sensor, checks an HTTP
200 response, and compares all three original device/sensor/timestamp keys
and their numeric values against the initially submitted batch. Missing,
duplicate or changed records fail.

The regression suite includes deliberate value mutation despite the expected
conflict response, and the check is mandatory in hosted Python live conformance.
The TypeScript reference deliberately does not implement telemetry; this
mission is not external production-data assurance. See
[Mission 114 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-114-TELEMETRY-POSTCONFLICT-INTEGRITY.md).

## Structural provenance round-trip verification (Mission 115)

Registered live probe **L-07** already requires provenance digests and
`evidenceLinks` to survive an analysis-job round trip. Previously the runner
passed when the original `inputsDigest` appeared *anywhere* in a serialized
response, without comparing the nested provenance or evidence links.

L-07 now compares the actual returned observation's full provenance mapping
to the submitted observation after confirming the expected completed job and
identity. Mock-server tests include changed digest values, missing evidence
links, changed actor, wrong job and injected unrelated copies of the original
digest. This is exact *structured round-trip equality* within a project-owned
reference server, **not** independent verification of the scientific source,
field-specific preimages or the provenance's truth. See
[Mission 115 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-115-PROVENANCE-STRUCTURAL-ROUNDTRIP.md).

## Created-resource collection and pagination evidence (Mission 116)

Registered **L-25** previously sent job and model collection GET requests but
asserted only HTTP 200, even though its stated expectation required
`result.data` arrays and pagination totals after creating both resources.
It now checks structured nonempty collections, basic integer pagination
metadata and the presence of the just-created job or model version. A success
response with unrelated data, malformed pagination or no records fails.

The negative regression suite is part of hosted static conformance. This
checks the current in-memory reference service's observable list behavior,
not a complete pagination protocol or third-party certification. See
[Mission 116 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-116-COLLECTION-ENVELOPE-EVIDENCE.md).

## Deprecated inference completion assurance (Mission 117)

Registered **L-27** already promised that inference with a deprecated model
would be accepted with a warning *and complete*. Previously its actual
assertions stopped at HTTP 202 and a warning status message. The runner now
also polls the accepted job and requires that the same job reaches
`COMPLETED`, rejecting failed, expired, running, missing or mismatched jobs.

The existing warning assertion is evaluated on the original submission
response before polling. Negative tests enforce both outcomes and run in
hosted static conformance. This is reference-server behavior evidence, not
scientific model validation, authentication, persistence or third-party
certification. See
[Mission 117 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-117-DEPRECATED-INFERENCE-COMPLETION.md).

## Telemetry window partition evidence (Mission 118)

Registered live **L-26** now checks that the three synthetic one-minute-apart
readings produce **three distinct 60-second mean buckets**, each with exactly
one sample and the corresponding original timestamp and mean value. Merely
returning three rows no longer passes. The assertion is required by the
manifest validator; malformed or weakened probe declarations fail before
running against a server.

The negative regression suite is `Scripts/test_telemetry_window_partition.py`;
it runs in hosted static conformance, and the registered L-26 live test runs
against the project-owned Python reference server. This check is restricted to
the fixture's minute-aligned readings and does not prove generalized temporal
window semantics, persistent data integrity or external interoperability. See
[Mission 118 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-118-TELEMETRY-WINDOW-PARTITIONS.md).

## Telemetry pagination slice evidence (Mission 119)

Registered live **L-28** now verifies that page zero of three synthetic
readings contains the first two timestamp-sorted records with their original
device, sensor, timestamp and value, rather than only checking row and total
counts. It also requires consistent first-page metadata (`currentPage: 0`,
`pageSize: 2`, `totalCount: 3`, `totalPages: 2`).

The registered assertion is fail-closed in manifest validation. Its negative
tests in `Scripts/test_telemetry_pagination_slice.py` are required by hosted
static conformance; the Python reference server exercises L-28 live. This
does not certify snapshot isolation or arbitrary pagination policies. See
[Mission 119 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-119-TELEMETRY-PAGINATION-SLICE.md).

## Replay retained-state verification (Mission 120)

Registered **L-21** checks the first telemetry append and exact replay response
counts, then reads back the same device/sensor readings and confirms that
exactly the original three timestamp/value records survive, with no duplicated
natural key. The existing `telemetry_original_intact` assertion is reused;
the manifest validator requires the L-21 readback, so removing it fails closed.

The regression suite at `Scripts/test_telemetry_replay_postcondition.py`
simulates replay responses with correct reported counts but duplicate, missing,
or mutated stored records. It is mandatory in hosted static conformance,
while registered L-21 executes against the in-memory Python reference server.
This does not establish durability, multi-server idempotency, or third-party
interoperability. See [Mission 120 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-120-TELEMETRY-REPLAY-READBACK.md).

## Concurrent job stored-effect verification (Mission 121)

Registered **L-24** now fetches the complete jobs collection after eight
identical concurrent submissions. Besides asserting one returned job identifier,
the runner checks that exactly one stored job has the original unique
idempotency key and that its identifier and job type match the submitted
request. It rejects truncated collection evidence, malformed pagination, and
duplicate or missing stored records; unrelated historical jobs may coexist.

The manifest validator requires both the eight-way submission and its GET
postcondition. The mutation suite at `Scripts/test_concurrent_job_stored_effect.py`
is mandatory in hosted static conformance; L-24 executes against the Python
and independent TypeScript/Bun in-memory reference servers. This is **not**
a durable, distributed, or third-party exactly-once guarantee. See
[Mission 121 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-121-CONCURRENT-JOB-STORED-EFFECT.md).

## Variable-term publication conflict postcondition (Mission 122)

Registered **L-09** now performs a version-qualified GET after a conflicting
variable-term publication is rejected with 409. The runner compares all
submitted original fields, including nested provenance, against the stored
published version; matching only the resource identifiers is insufficient.
The manifest validator requires this readback after the conflict POST.

Mock-server mutations in `Scripts/test_variable_term_conflict_postcondition.py`
verify that server responses cannot conceal changed scales, versions, actors,
digests, omitted fields or unavailable published records. The suite executes
in hosted static conformance and registered L-09 runs against the project's
Python reference server. This does not establish external scientific truth,
transaction durability or third-party interoperability. See
[Mission 122 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-122-VARIABLE-TERM-CONFLICT-READBACK.md).

## Ledger conflict retained-value verification (Mission 123)

Registered **L-11** already rejected a conflicting ledger append and checked
that its collection still had one entry, but this could pass after the
original entry was silently rewritten. It now checks the stored entry's
identity and **all originally submitted fields**, including its fixed-scale
quantity, actor, locations, idempotency key, and nested provenance. Readback
pagination must prove exactly one entry is visible.

The manifest validator requires the L-11 GET assertion after the conflict;
the mutation suite `Scripts/test_ledger_conflict_postcondition.py` is
mandatory in hosted static conformance. The registered probe executes
against the project's Python reference server. This is not external scientific
or database durability certification. See
[Mission 123 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-123-LEDGER-CONFLICT-READBACK.md).

## Ledger replay retained-value verification (Mission 124)

Registered **L-10** now validates the original stored ledger entry after
an identical replay in addition to checking the response's identifier and
record count. It reuses the full `ledger_original_intact` assertion from
Mission 123, including the original quantity, actor, provenance, idempotency
key, entry identity and complete collection pagination.

Its manifest guard rejects losing the L-10 readback, and the dedicated
`Scripts/test_ledger_replay_postcondition.py` mutation suite is mandatory
in hosted static conformance. The project-owned Python server exercises L-10
live. This is observable in-memory behavior, not a durability or scientific
certification. See
[Mission 124 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-124-LEDGER-REPLAY-READBACK.md).

## Variable-term replay uniqueness (Mission 125)

Registered **L-08** now reads the collection filtered by its freshly
generated variable-term identifier after an identical publication replay.
It verifies a complete one-version collection and compares the stored
record with all fields of the original submitted version, including nested
provenance. Merely returning identical (variableDbId, version) identifiers
no longer passes if another version was created.

The `term_replay_single_version` assertion is required by the manifest
validator, and the `Scripts/test_term_replay_version_uniqueness.py`
mutation suite runs in hosted static conformance. The existing Python
reference server executes the L-08 live probe. This remains a synthetic,
in-memory assurance test, not production durability or certification. See
[Mission 125 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-125-TERM-REPLAY-UNIQUENESS.md).

## Variant-matrix replay stored-state evidence (Mission 126)

Registered **L-16** now reads the complete `/variantmatrices` collection
after identical registration replay. It verifies a single stored occurrence
of the freshly submitted matrix identifier and compares **all originally
submitted attributes**, including file and index digests, remote access
metadata, and nested provenance. Unrelated matrices may coexist.

A malformed, incomplete or multipage collection fails closed rather than
being treated as evidence that no duplicate exists. The mandatory assertion
is checked by the manifest validator and its negative regression suite at
`Scripts/test_matrix_replay_stored_state.py` runs in hosted static
conformance. See [Mission 126 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-126-MATRIX-REPLAY-STORED-STATE.md).

## Package replay stored-state assurance (Mission 127)

Registered **L-18** now reads the complete `/fair-packages` collection
after identical registration replay. It checks exactly one occurrence of
the original package identifier and all originally submitted attributes,
including license, access rights, nested payload references/digests and
provenance. Unrelated packages may coexist; incomplete pagination fails
closed.

The runner shares its collection integrity helper with L-16 rather than
duplicating the same validation logic. Manifest guards require this L-18
readback, and the `Scripts/test_package_replay_stored_state.py`
regression suite executes in hosted static conformance. See
[Mission 127 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-127-PACKAGE-REPLAY-STORED-STATE.md).

## Model replay version integrity (Mission 128)

Registered **L-12** now performs a GET on the model collection filtered by
its fresh `modelDbId` after replay. The test verifies a single original
`modelVersion`, unchanged artifact and training digests, framework metrics,
and nested provenance. Incomplete pagination, duplicate model versions,
missing records and mutated metadata fail closed.

This check shares the replay collection helper with Missions 126–127 and
requires `model_replay_single_version` in the registered manifest. The
negative regression suite `Scripts/test_model_replay_version_integrity.py`
runs in hosted static conformance. See
[Mission 128 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-128-MODEL-REPLAY-VERSION-INTEGRITY.md).

## Matrix conflict full-record verification (Mission 129)

Registered **L-17** has been strengthened from checking only the original
matrix identifier and file digest to checking **all submitted fields** on its
versioned record GET following a 409 conflict response. This includes
`fileURL`, index digest, access service and nested provenance; additional
server-managed fields are allowed.

The runner-local `published_record_problem` helper carries the full
record comparison for conflict readbacks without duplicating logic. The
manifest validator requires the existing L-17 three-step sequence; the
`Scripts/test_matrix_conflict_whole_record.py` mutation suite is mandatory
in hosted static conformance. See
[Mission 129 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-129-MATRIX-CONFLICT-WHOLE-RECORD.md).

## FAIR package conflict whole-record verification (Mission 130)

Registered **L-19** is strengthened from license-only post-conflict
readback to a complete comparison with all originally submitted package
fields, including nested evidence links and provenance. The existing
`unchanged_package_license` assertion now uses the same runner-local
`published_record_problem` helper introduced for matrices in Mission 129.

The manifest validator requires the three-step publish → conflicting POST
→ readback sequence. The `Scripts/test_package_conflict_whole_record.py`
regressions run in the mandatory hosted static conformance workflow. See
[Mission 130 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-130-PACKAGE-CONFLICT-WHOLE-RECORD.md).

## Model conflict whole-record verification (Mission 131)

Registered **L-13** now checks all originally submitted model fields after
rejecting a conflicting version with 409, not only the `artifactDigest`.
The existing `unchanged_model_digest` assertion reuses the runner-local
`published_record_problem` helper for versioned model identity, artifact
and training-data metadata, metrics, framework and nested provenance.

The manifest validator requires the exact submit, conflict and versioned
GET procedure. The dedicated negative regression suite
`Scripts/test_model_conflict_whole_record.py` is mandatory in hosted
static conformance; prior model-conflict tests remain active. See
[Mission 131 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-131-MODEL-CONFLICT-WHOLE-RECORD.md).

## Rejected inference has no stored job (Mission 132)

Registered **L-15** now follows HTTP 400 responses for unknown and revoked
model inference with a complete jobs-collection readback. The original
inference idempotency keys and model identifiers are recorded before
submission and must be absent from the stored job records.

The `rejected_inference_not_stored` assertion fails on incomplete or
multipage collection evidence and is mandatory in the manifest. Regression
suite `Scripts/test_rejected_inference_no_stored_job.py` runs in hosted
static conformance. This proves no **observable stored job**, not that no
unobservable side effect or processing ever occurred. See
[Mission 132 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-132-REJECTED-INFERENCE-NO-STORED-JOB.md).

## Job replay single stored-effect assurance (Mission 133)

Registered **L-01** now reads the complete jobs collection after replay,
rather than relying on the two equal job identifiers returned by POST.
It requires exactly one stored job matching the original idempotency key
and returned identifier, with an unchanged job type; unrelated jobs can
coexist. A truncated or malformed collection fails closed.

The `job_replay_single_stored` assertion is required on a GET after the
original captured POST and identical replay. The mandatory regression
suite `Scripts/test_job_replay_single_stored.py` tests falsifying
duplicate/missing records, mismatched identity and incomplete pagination.
See [Mission 133 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-133-JOB-REPLAY-SINGLE-STORED.md).

## Job conflict immutable collection snapshot (Mission 134)

Registered **L-02** now reads GET /jobs **before and after** a conflicting
submission. A complete pre-conflict snapshot must contain the initially
submitted job with its original identifier, job type and idempotency key.
After a rejection, the full collection must contain exactly the same
immutable identities, allowing legitimate changes in mutable job status.

This also detects a hidden second job with an unrelated server-generated key.
The dedicated regression suite
`Scripts/test_job_conflict_collection_unchanged.py` is mandatory in hosted
static conformance, and the manifest validator enforces the four-step
procedure. See [Mission 134 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-134-JOB-CONFLICT-COLLECTION-UNCHANGED.md).

## Rejected terminal-job cancellation readback (Mission 135)

Registered **L-03** now captures the terminal job's identifier and status
from the poll result before attempting cancellation. After the DELETE is
rejected, the runner requires a GET of the same job and verifies that the
terminal status is unchanged. An unobserved or nonterminal baseline fails.

The manifest validator requires the captured terminal wait, rejected DELETE,
and readback assertion. The regression suite
`Scripts/test_terminal_cancel_retained_state.py` runs in hosted static
conformance. See [Mission 135 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-135-TERMINAL-CANCEL-RETAINED-STATE.md).

## Unknown job type leaves no stored job (Mission 136)

Registered **L-04** now reads GET /jobs after rejecting an unknown job
type with HTTP 400. It captures the originally submitted idempotency key
and invalid jobType and requires the full collection to contain neither
a job with that key nor a job with that unadvertised type.

The `unknown_job_type_not_stored` assertion fails on incomplete
pagination or malformed responses and is mandatory on the L-04 GET step.
The negative regression suite `Scripts/test_unknown_jobtype_no_stored_job.py`
runs in hosted static conformance. See
[Mission 136 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-136-UNKNOWN-JOBTYPE-NO-STORED-JOB.md).

## Expired job result withholding (Mission 137)

Registered **L-05** now asserts that a known expired job reports
`EXPIRED` while omitting the actual job `result` field (or returning
null), and that the returned identity matches the requested expired job.
Reporting the correct status while leaking result data fails closed.

The `expired_result_withheld` assertion is protected by the registered
manifest and tested by `Scripts/test_expired_job_result_withheld.py` in
hosted static conformance. Full live execution of L-05 still requires a
known-expired identifier supplied using `--expired-job`; otherwise
the live runner marks L-05 **SKIP**. See
[Mission 137 assessment](../../../docs/assessment/BRAPI-GENX-MISSION-137-EXPIRED-JOB-RESULT-WITHHELD.md).
