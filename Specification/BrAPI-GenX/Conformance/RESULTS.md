# GenX Conformance Results

- Date (UTC): 2026-09-07
- Reference server: `Scripts/genx_test_server.py` (stdlib only, in-memory)
- Runner: `Scripts/checkGenXConformance.py`

## Historical-run scope

Runs 1–12 are recorded results for earlier proposal revisions. They include the former GenX term route `/genx/v1/variables`. During the endpoint-identity review, the proposed GenX term resource was renamed to `/genx/v1/variable-terms`, and its specification folder was renamed from `Ontology/` to `VariableTerms/`. Runs 1–12 do **not** validate the renamed route; Run 13 below records the first successful live check of `/genx/v1/variable-terms`. V2.1 contracts remain unchanged.

## Runs

```shell
python Scripts/checkGenXConformance.py
# 8 PASS, 0 FAIL, 7 SKIP (live tier needs --server)

python Scripts/genx_test_server.py --port 18080 --delay 0.4 &
python Scripts/checkGenXConformance.py \
  --server http://127.0.0.1:18080/genx/v1 --expired-job JOB_EXPIRED
# 15 PASS, 0 FAIL, 0 SKIP

python Scripts/genx_test_server.py --port 18081 --profile v21 &
python Scripts/checkGenXConformance.py \
  --server http://127.0.0.1:18081/brapi/v2 --only L-06
# PASS L-06 against the V2.1-only shape
```

## Run 2 — RFC-002 ontology terms (2026-09-07)

```shell
python Scripts/checkGenXConformance.py
# 10 PASS, 0 FAIL, 9 SKIP

python Scripts/genx_test_server.py --port 18080 --delay 0.4 &
python Scripts/checkGenXConformance.py \
  --server http://127.0.0.1:18080/genx/v1 --expired-job JOB_EXPIRED
# 19 PASS, 0 FAIL, 0 SKIP (L-08 term replay, L-09 term 409 conflict)

python Scripts/checkGenXConformance.py \
  --server http://127.0.0.1:18081/brapi/v2 --only L-06  # v21 profile
# PASS; v21 /variables -> 404, genx /variables -> 200
```

Collision found by S-01 and resolved: V2.1 Genotyping already defines
`OntologyTerm` (a GA4GH `{term, termURI?}` label), so the GenX object is named
`VariableTerm` / `VariableTermNewRequest` — zero shadowing exceptions.
Term conflicts reuse the `409` rule evidenced in run 1.

## Run 3 — RFC-003 seed-lot ledger (2026-09-07)

```shell
python Scripts/checkGenXConformance.py
# 12 PASS, 0 FAIL, 11 SKIP

python Scripts/genx_test_server.py --port 18080 --delay 0.4 &
python Scripts/checkGenXConformance.py \
  --server http://127.0.0.1:18080/genx/v1 --expired-job JOB_EXPIRED
# 23 PASS, 0 FAIL, 0 SKIP (L-10 ledger replay, L-11 ledger 409 conflict)
```

Defects found during the slice: a `: ` inside a plain-scalar description made
`Ledger_GET_POST.yaml` unparseable (S-01 now fails loudly on unparseable GenX
files instead of reporting dangling refs); quantity is a decimal string on the
wire while V2.1 `amount` stays a float (frozen, untouched).

## Run 4 — RFC-004 model registry and inference (2026-09-07)

```shell
python Scripts/checkGenXConformance.py
# 14 PASS, 0 FAIL, 15 SKIP

python Scripts/genx_test_server.py --port 18080 --delay 0.4 &
python Scripts/checkGenXConformance.py \
  --server http://127.0.0.1:18080/genx/v1 --expired-job JOB_EXPIRED
# 29 PASS, 0 FAIL, 0 SKIP (L-12 model replay, L-13 artifact 409,
# L-14 inference digest binding with recomputed SHA-256, L-15 unknown/revoked 400)
```

No new defects: the no-shadowing rule held for `ModelArtifact` on first pass.
The reference `outputs.echo` stub exists only to prove digest binding — it is
explicitly not a model.

## Run 5 — RFC-005 variant matrix references (2026-09-07)

```shell
python Scripts/checkGenXConformance.py
# 16 PASS, 0 FAIL, 17 SKIP

python Scripts/genx_test_server.py --port 18080 --delay 0.4 &
python Scripts/checkGenXConformance.py \
  --server http://127.0.0.1:18080/genx/v1 --expired-job JOB_EXPIRED
# 33 PASS, 0 FAIL, 0 SKIP (L-16 matrix replay, L-17 mutated-bytes 409)
```

External grounding: GA4GH htsget v1.3 (ticket-based subsection streaming),
GA4GH DRS v1.4 (logical-ID → bytes, checksums), VCF Zarr spec (GigaScience
2025, ~5X biobank storage reduction) — all referenced, none reinvented. No new
defects; no shadowing collisions for `VariantMatrix` on first pass.

## Run 6 — RFC-006 FAIR packages (2026-09-07)

```shell
python Scripts/checkGenXConformance.py
# 18 PASS, 0 FAIL, 20 SKIP

python Scripts/genx_test_server.py --port 18080 --delay 0.4 &
python Scripts/checkGenXConformance.py \
  --server http://127.0.0.1:18080/genx/v1 --expired-job JOB_EXPIRED
# 38 PASS, 0 FAIL, 0 SKIP (L-18 package replay, L-19 license 409,
# L-20 embargo 403 on far-future embargoUntil)
```

No new defects; no shadowing collisions for `FAIRPackage` on first pass. The
reference server denies the whole embargoed record (whole-record `403`) as a
stand-in for payload-level denial — recorded as requires-decision in
RFC-006 §5.

## Run 7 — RFC-007 telemetry streams (2026-09-07)

```shell
python Scripts/checkGenXConformance.py
# 20 PASS, 0 FAIL, 23 SKIP

python Scripts/genx_test_server.py --port 18080 --delay 0.4 &
python Scripts/checkGenXConformance.py \
  --server http://127.0.0.1:18080/genx/v1 --expired-job JOB_EXPIRED
# 43 PASS, 0 FAIL, 0 SKIP (L-21 batch replay counts, L-22 element-wise
# conflict, L-23 mean recomputation within 1e-9)
```

No new defects; no shadowing collisions for `TelemetryPoint` on first pass.
Float `value` is deliberate (measurements, not inventory) and documented
against the RFC-003 decimal-string rule.

## Run 8 — harness hardening (2026-09-07)

No new spec surface. Three verification upgrades:

1. Systematic mutation coverage: 9/9 targeted mutations fail closed across
   S-01 (dangling ref, shadowing), S-02, S-03, S-05, S-06, S-07, S-08, S-10.
   Together with the per-slice mutation tests (S-04, S-12, S-14, S-16, S-18,
   S-20), every static check function now has fail-closed evidence. (S-09,
   S-11, S-13, S-15, S-17 route through `required_fields`, proven via S-02.)
2. New live probe L-24: 8 threads POST one body+key; all 2xx with one
   distinct jobDbId. Stable over 3 runs; control run (8 distinct keys → 8
   jobs) proves the assertion discriminates.
3. Full suite re-run below.

```shell
python Scripts/checkGenXConformance.py
# 20 PASS, 0 FAIL, 24 SKIP

python Scripts/genx_test_server.py --port 18080 --delay 0.4 &
python Scripts/checkGenXConformance.py \
  --server http://127.0.0.1:18080/genx/v1 --expired-job JOB_EXPIRED
# 44 PASS, 0 FAIL, 0 SKIP
```

## Run 9 — second implementation, cross-runtime (2026-09-07)

A TypeScript/Bun server (`Scripts/genx_test_server_ts.ts`), written black-box
from the RFC text, implements the RFC-001 core + RFC-004 inference subset
(serverinfo both profiles, Jobs, minimal models). Result:

```shell
bun Scripts/genx_test_server_ts.ts --port 18082 --delay 0.4 &
python Scripts/checkGenXConformance.py --server http://127.0.0.1:18082/genx/v1 \
  --expired-job JOB_EXPIRED --only L-01   # ... L-02 L-03 L-04 L-05 L-06 L-07
                                          # L-12 L-13 L-14 L-15 L-24
# 13/13 PASS, including L-14 digest agreement across runtimes and L-24
```

Key evidence: L-14's `inputsDigest`, computed by Bun crypto over
TS-canonicalized JSON, matches the Python runner's independent recomputation —
sorted-keys + compact separators + UTF-8 agrees across runtimes for ASCII
payloads. Non-ASCII escaping differs (Python `ensure_ascii` vs raw UTF-8):
D-02's remaining boundary, now precisely located instead of open-ended.

Defect found by the exercise: two NUL bytes inside TS template literals broke
model lookup (L-14 submit → 400); fixed byte-precisely, suite re-run green.
No RFC text change was needed — the ambiguity was in my code, not the spec.

## Run 10 — differential + performance (2026-09-07)

```shell
python Scripts/genx_differential_check.py \
  --a http://127.0.0.1:18080/genx/v1 --b http://127.0.0.1:18082/genx/v1 \
  --expired-job JOB_EXPIRED
# differential: 9/9 steps agree (serverinfo agrees under subset-capability rule)
```

Indicative localhost numbers (debug servers, no production claims):

| Operation | Time |
|---|---|
| 1000-point telemetry batch ingest | 0.118 s |
| Range + mean over 1000 points | 0.027 s |
| Full 44-probe live suite (delay 0.4 s) | 6.6 s (polling-dominated) |

## Evidence for open RFC-001 decisions

- Conflict status: the reference server rejects same-key/different-body with
  `409` and a plain-text body. This is one implementation's evidence for
  `requires decision` #1, not the decision itself.
- Replay distinction: first submit returns `202`, identical replay returns
  `200` with the same `jobDbId` and zero new effects.
- Terminal-cancel, unknown-type (`400`), expiry-without-result, and
  V2.1-fallback negotiation all behave as the RFC specifies.

## Limits (not proven here)

No persistence (restart loses jobs), no authentication (Bearer accepted and
ignored), single process, expiry sweep untested beyond the pre-seeded
`JOB_EXPIRED`. Concurrency is proven for same-key submits (L-24) only;
mixed key/type races are untested. Production claims: none.

## Run 11 — coverage closure (2026-09-07)

Four previously unexercised behaviors get probes; no new spec surface:

```shell
python Scripts/checkGenXConformance.py --server http://127.0.0.1:18080/genx/v1 \
  --expired-job JOB_EXPIRED
# 48 PASS, 0 FAIL, 0 SKIP (L-25 list envelopes, L-26 windowed buckets,
# L-27 deprecated WARNING, L-28 pagination slice)
```

L-25 and L-27 also pass against the TypeScript server (subset surface).
Generic assert kinds added to the runner: `data_length`, `total_count`,
`status_message`.

## Run 12 — endpoint identity and semantic overlap guardrail (2026-10-14)

Feature branch: `work/endpoint-identity-clarity`  
Tested commit: `60df39bd43900674c6957b9c1427b8ba2a3d48fb`  
[GitHub Actions run](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38557019922)

The new endpoint-identity mutation tests and static conformance checks completed successfully in GitHub Actions:

- Endpoint identity mutation tests: **7 tests passed** (missing operation ID, duplicate operation ID, duplicate normalized route template, unregistered overlap, stale overlap entry, incomplete semantic-neighbor entry, and V2.1/GenX operation-ID collision all fail the checker; the valid control case passes).
- Static conformance: **21 probes passed, 0 failed**. This includes S-21, which checks stable GenX operation IDs and exact V2.1/GenX relative-path overlap registration.
- Live conformance probes: **skipped** in this static-only workflow because no `--server` was supplied. This run makes no new claim about reference-server behavior or production readiness.

This result applies to the recorded feature-branch commit only; it is not a merge or standards-ratification event.

## Run 13 — endpoint identity and renamed variable-term route (2026-10-14)

Feature branch: `work/endpoint-identity-clarity`  
Tested commit: `884420e0b095e4613fc83d40d797cf73d9f95807`  
[GitHub Actions run](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38559182512)

- Endpoint-identity mutation tests: **10 passed**, including the valid control case and negative cases for missing/duplicate operation IDs, duplicate normalized route templates, stale or missing overlap entries, incomplete semantic-neighbor metadata, V2.1 identifier collisions, and endpoint-catalogue drift.
- Static conformance: **21 passed, 0 failed**. S-21 found **21 named GenX operations** and **one registered cross-generation relative-path overlap**: `GET /serverinfo`.
- Live reference-server conformance: **28 passed, 0 failed, 0 skipped**, including L-08/L-09 against the renamed `/genx/v1/variable-terms` route.
- The reference server is in-memory and does not provide durable persistence or effective authentication. This run validates the exercised proposal behavior, not production readiness, security posture, performance, or interoperability with an independent third-party implementation.

V2.1 endpoint files were not changed. This is a feature-branch engineering result, not a standards-ratification event.

## Run 14 — explicit endpoint meaning and non-equivalence boundaries (2026-10-14)

Feature branch: `work/endpoint-identity-clarity`  
Tested commit: `b551142357047dd9c82cedcc207588324190730d`  
[GitHub Actions conformance run](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38560252431)

- Endpoint-identity mutation tests: **12 passed**. Negative tests include missing/duplicate operation IDs, duplicated normalized route templates, absent/stale overlap records, malformed semantic-neighbor records, cross-generation operation-ID collisions, endpoint-catalogue drift, and missing meaning/boundary text. The valid synthetic control passes.
- Static conformance: **21 passed, 0 failed**. S-21 verified 21 named GenX operations and one registered cross-generation relative-path overlap, `GET /serverinfo`.
- Live reference-server conformance: **28 passed, 0 failed, 0 skipped**. These include the renamed `/genx/v1/variable-terms` replay/conflict behaviors and unrelated existing capability probes.
- The live target is an in-memory Python reference server. This is evidence for the tested behavior and conformance tooling only; it does not prove durable persistence, effective authentication, production security, third-party interoperability, or standard acceptance.

The separate schema-generation/build workflow also passed on this tested commit: [GitHub Actions run 38560252360](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38560252360). The conformance and schema-generation workflows therefore both pass for the commit cited above. No V2.1 contract file was edited.


## Run 15 — ServerInfoV3 capability-to-operation contract (2026-10-15)

Feature branch: `work/std-04-capability-negotiation`  
Tested commit: `e6784a56052373709aeee4c4369df06d634b90a1`  
[GitHub Actions conformance run](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38688671323)

- Dedicated capability-negotiation mutation suite: **15 tests passed**. Negative cases include duplicate/unregistered capability names, missing capabilities, duplicate or unregistered versions, false method summaries, stale routes and operation IDs, missing mappings, duplicated operation references, malformed/duplicate scopes, duplicate auth-profile names, and duplicate OpenAPI operation IDs.
- Existing endpoint-identity mutation tests: **12 passed**.
- Static conformance: **22 probes passed, 0 failed**, including S-22, which cross-checks exact full route templates, methods, and stable operation IDs against the actual GenX OpenAPI definitions.
- Live reference-server conformance: **29 probes passed, 0 failed, 0 skipped**, including L-29, which checks live ServerInfoV3 advertisements against the same registry.
- The separate schema/specification build workflow for this commit passed: [run 38688671310](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38688671310).

The new `operations[]` property is explicitly optional and experimental in the schema. The registry and tests define the current proposal profile, not an accepted BrAPI requirement. D-21 (operation mapping/version tokens) and D-22 (authorization scopes/auth profiles) remain open for implementer and community review. In particular, the reference server is in-memory and does not implement authentication or authorization; passing tests is not evidence of production security or enforcement. No BrAPI V2.1 contract file was modified.


## Run 16 — capability registry source-of-truth hardening (2026-10-15)

Feature branch: `work/std-04-capability-negotiation`  
Tested commit: `444d1e7303e482067e3e06f80e6ad3c499868d21`  
[GitHub Actions conformance run](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38688966139)  
[GitHub Actions schema/specification build](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38688966287)

- Capability-negotiation mutation suite: **21 tests passed**. It includes mutations to the advertised document and the registry itself, malformed and duplicate tokens, unsupported routes/methods, incorrect/missing operation identities, and malformed scope/auth-profile shapes.
- Endpoint-identity mutation suite: **12 tests passed**.
- Static conformance: **22 probes passed, 0 failed**, including S-22 mapping every advertised capability operation to the checked-in OpenAPI route, method, and operation ID.
- Live reference-server conformance: **29 probes passed, 0 failed, 0 skipped**, including L-29 comparing the runtime ServerInfoV3 response against the same capability registry.
- Schema/specification build and generation: **passed**.

The new `operations[]` property and registry remain experimental proposal material. These tests prevent metadata drift; they do not prove client interoperability with an independent implementation or authorize a normative change. D-21 (capability-operation mapping and version semantics) and D-22 (scope/auth-profile semantics and enforcement) remain open. The in-memory server still does not implement authentication/authorization, and no BrAPI V2.1 contract files were changed.


## Run 17 — supported job-type advertisement and runtime drift guard (2026-10-15)

Feature branch: `work/std-04-capability-negotiation`  
Tested commit: `e8f9e106402c5fe3fbb1f395dea20f81b3721006`  
[GitHub Actions conformance run](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38689928375)  
[Schema/specification build](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38689928312)

- Capability-negotiation mutation suite: **29 tests passed**. The suite now detects absent, duplicate, malformed, or registry-divergent `jobTypes[]` values, jobTypes attached to non-jobs capabilities, and divergence between the capability registry and the actual `SUPPORTED_JOB_TYPES` constant in the submission validator.
- Endpoint-identity mutation suite: **12 tests passed**.
- Static conformance: **22 probes passed, 0 failed**, including S-22's exact operation map and job-type drift check.
- Live reference-server conformance: **29 probes passed, 0 failed, 0 skipped**, including L-29 validating the live ServerInfoV3 data against the registry.
- The job-type advertisement now agrees with the current prototype's accepted type tokens: `germplasm_search`, `analysis`, and `inference`; `export` is not advertised by this prototype.

The `jobTypes[]` property is optional and experimental in the schema. Whether a future GenX contract requires it, how older servers are handled, and how job-type names are versioned/deprecated remain open under D-23. These tests verify internal agreement and fail-closed metadata validation; they do not prove third-party interoperability or ratify a standard. D-21 and D-22 also remain open. No V2.1 contract files changed, and the in-memory reference server still has no effective authentication/authorization or durable persistence.

## Run 18 — digest interoperability candidate corpus (2026-10-15)

Feature branch: `work/std-01-digest-vectors`  
Tested commit: `86fec6494ee95773d8993d7d69cbcc060793cfa1`  
[GitHub Actions run](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38686137872)

- Shared structured-JSON candidate vectors: **11 passed** independently in Python (`rfc8785==0.1.4`) and TypeScript/Bun (`canonicalize==5.1.0`).
- Exact-byte digest vectors: **2 passed** in both runtimes.
- Invalid-input rejection vectors: **4 passed** in both runtimes, including duplicate property names after escape decoding, non-JSON constants, and lone surrogate values.
- Legacy divergence diagnostics: **2 passed** in both runtimes, confirming different current serializer behavior for non-ASCII text and Unicode property ordering.
- Endpoint-identity mutation suite: **12 passed**; static GenX conformance: **21 passed, 0 failed**; live reference-server conformance: **28 passed, 0 failed, 0 skipped**.

This verifies two independent implementations against an experimental candidate corpus. It does not migrate either reference server to JCS, resolve D-02, or adopt RFC 8785 for BrAPI. Scientific quantities requiring exact decimal or integer precision must not be silently converted to binary64 JSON numbers. No BrAPI V2.1 contract files changed; the in-memory reference server still has no effective authentication, and no production-readiness claim is made.


## Run 19 — digest numeric-boundary hardening (2026-10-15)

Feature branch: `work/std-01-digest-vectors`  
Tested commit: `3f4518e97eefebf9c8045ef83c789f2142e753ec`  
[GitHub Actions run](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38686741683)

- Structured JSON candidate corpus: **12 passed** independently in Python and TypeScript/Bun, including the largest interoperable safe integer boundary.
- Exact-byte digest cases: **2 passed** in both runtimes.
- Rejection-policy cases: **5 passed** in both runtimes — four JSON/JCS input-constraint cases and one deliberately stricter profile rule that rejects an unsafe integer token before JavaScript can silently round it. The numeric rule is a candidate-profile safeguard, not a claim that the token is invalid JSON.
- Known legacy serializer divergence diagnostics: **2 passed** in both runtimes.
- Endpoint-identity mutation tests: **12 passed**; static GenX conformance: **21 passed, 0 failed**; live reference-server conformance: **28 passed, 0 failed, 0 skipped**.

The strict parser is a conformance-test guard, not a production parser or a normative BrAPI rule. RFC 8785/JCS remains an experimental candidate. The currently deployed-in-repository reference-server canonicalization helpers have not been migrated; D-02 remains unresolved pending field-scope, scientific numeric semantics, migration/versioning, and implementer/community review. V2.1 contracts remain unchanged.


## Run 20 — digest corpus completeness and mutation resistance (2026-10-15)

Feature branch: `work/std-01-digest-vectors`  
Tested commit: `7542db0248f21182c5ce95d6146aee2a89880580`  
[GitHub Actions run](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38687016131)

- Python and TypeScript/Bun independently passed the shared digest corpus: **12 structured JSON vectors, 2 exact-byte cases, 5 rejection-policy cases (four JCS/JSON input constraints plus one conservative numeric hardening rule), and 2 known legacy divergence diagnostics**.
- Digest corpus mutation tests: **5 deliberate corruptions rejected by both runtimes (10 checks)** — wrong canonical bytes, wrong structured digest, wrong exact-byte digest, removed required edge vector, and duplicate vector identity.
- Endpoint-identity mutation tests: **12 passed**; static GenX conformance: **21 passed, 0 failed**; live reference-server conformance: **28 passed, 0 failed, 0 skipped**.

This adds evidence that the tests themselves detect deliberate corruption and missing edge-case coverage. The shared corpus still evaluates RFC 8785/JCS as a candidate only; D-02 remains open. Neither current reference-server canonicalization helper has been migrated, and V2.1 contracts remain unchanged. Reference-server constraints continue to apply: no durable persistence or effective authentication.


## Run 21 — make strict-profile rejection semantics explicit (2026-10-15)

Feature branch: `work/std-01-digest-vectors`  
Tested commit: `1fcf062c65faf2ec797899070f9da386011aead5`  
[GitHub Actions run](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38687419662)

- Python and TypeScript/Bun passed the same corpus: **12 structured JSON vectors, 2 exact-byte cases, 5 rejection-policy cases, and 2 legacy divergence diagnostics**.
- The rejection vectors now name their rationale and distinguish four JSON/JCS input constraints from the stricter unsafe-integer guard. That guard is an explicit exploratory candidate-profile policy, not a blanket claim that large integers are invalid JSON or a requirement imposed by RFC 8785.
- Five intentional mutations were rejected by each implementation (10 checks). The run also passed 12 endpoint-identity mutation tests, 21 static GenX probes, and 28 live reference-server probes; no skips or failures.

D-02 remains open. The current Python and TypeScript/Bun reference-server canonicalizers remain unchanged. This run supports the test harness and candidate comparison only; it does not establish third-party agreement or standards acceptance.
