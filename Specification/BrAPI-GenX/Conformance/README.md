# BrAPI GenX — Conformance

Proves the RFC-001 hypothesis before any fourth object is designed:

> the three objects can be adopted independently by two interoperating
> implementations with zero changes to their V2.1 paths.

## Two tiers

| Tier | Needs | Run |
|---|---|---|
| `static` (S-01…S-08) | this repo only | `python Scripts/checkGenXConformance.py` from the `BrAPI_genX` root |
| `live` (L-01…L-07) | a GenX test server | `python Scripts/checkGenXConformance.py --server https://host/brapi/v3` |

Static probes run by default. Live probes `SKIP` without `--server` and fail
closed with it. Both tiers are declared in [`probes.yaml`](./probes.yaml);
fixtures live in [`fixtures/`](./fixtures). The probe list is the authority —
the runner is one execution of it, replaceable by a future BRAVA harness.
Recorded runs live in [`RESULTS.md`](./RESULTS.md).

## Reference test server

`Scripts/genx_test_server.py` (standard library only, in-memory, no
persistence, no authentication) implements the skeleton for live execution:

```shell
python Scripts/genx_test_server.py --port 8080 --profile genx &
python Scripts/checkGenXConformance.py \
  --server http://127.0.0.1:8080/brapi/v3 --expired-job JOB_EXPIRED
```

`--profile v21` serves the V2.1-only shape for probe L-06. Supported job
types: `germplasm_search`, `analysis` (echoes `parameters.observation` for
L-07). `JOB_EXPIRED` is pre-seeded for L-05. Same-key/different-body is
rejected with `409` (evidence for RFC-001 §8 decision #1). Term versions live
under `/variables` with RFC-002 replay/conflict semantics for L-08/L-09. Lot
ledger entries live under `/seedlots/{seedLotDbId}/ledger` with RFC-003
append/replay/conflict semantics for L-10/L-11 (lots auto-provisioned).
Models live under `/models` with RFC-004 replay/conflict semantics for
L-12/L-13; `inference` jobs bind to registered models for L-14/L-15 (the
reference `outputs.echo` stub exists only to prove digest binding).

## Probe index

Static: `$ref` resolution (S-01), fixture shape (S-02, S-09, S-11), enums (S-03),
digest format (S-04), date-time format (S-05), replay/conflict fixture
relations (S-06), capability advertisement grounding (S-07), V2.1 fallback
shape (S-08), namespaced term identifiers (S-10), decimal-string quantities
(S-12), model artifact shape (S-13, S-14).

Live: idempotent replay (L-01), key conflict (L-02), terminal-cancel rejection
(L-03), unknown job type (L-04), expiry (L-05), V2.1-only fallback negotiation
(L-06), provenance round-trip (L-07), term replay (L-08), term conflict (L-09),
ledger replay (L-10), ledger conflict (L-11), model replay (L-12), model
conflict (L-13), inference digest binding (L-14), unknown/revoked model
rejection (L-15).

## Status contract

Each probe reports `PASS`, `FAIL`, or `SKIP` (live without `--server` only).
Any `FAIL` exits non-zero. No probe may depend on another probe's side
effects; live probes that create server state use fresh idempotency keys.
