# GenX Conformance Results

- Date (UTC): 2026-09-07
- Reference server: `Scripts/genx_test_server.py` (stdlib only, in-memory)
- Runner: `Scripts/checkGenXConformance.py`

## Runs

```shell
python Scripts/checkGenXConformance.py
# 8 PASS, 0 FAIL, 7 SKIP (live tier needs --server)

python Scripts/genx_test_server.py --port 18080 --delay 0.4 &
python Scripts/checkGenXConformance.py \
  --server http://127.0.0.1:18080/brapi/v3 --expired-job JOB_EXPIRED
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
  --server http://127.0.0.1:18080/brapi/v3 --expired-job JOB_EXPIRED
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
  --server http://127.0.0.1:18080/brapi/v3 --expired-job JOB_EXPIRED
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
  --server http://127.0.0.1:18080/brapi/v3 --expired-job JOB_EXPIRED
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
  --server http://127.0.0.1:18080/brapi/v3 --expired-job JOB_EXPIRED
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
  --server http://127.0.0.1:18080/brapi/v3 --expired-job JOB_EXPIRED
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
  --server http://127.0.0.1:18080/brapi/v3 --expired-job JOB_EXPIRED
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
  --server http://127.0.0.1:18080/brapi/v3 --expired-job JOB_EXPIRED
# 44 PASS, 0 FAIL, 0 SKIP
```

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
`JOB_EXPIRED`, no concurrent-key race test. Production claims: none.
