# Adopting BrAPI GenX on a V2.1 Server

Non-normative guide. GenX is a proposal (see `DECISIONS.md`); this document
describes how a V2.1 server would adopt it incrementally if accepted. Each
step is independently shippable and leaves V2.1 behavior byte-identical.

## Order

1. **ServerInfoV3** (`ServerInfoV3/`). Serve `GET /brapi/v3/serverinfo`
   (`genxGetServerInfoV3`) alongside the untouched V2.1 endpoint
   `GET /brapi/v2/serverinfo`. Zero behavior change;
   unlocks negotiation for everything below.
2. **ProvenanceEnvelope** (`Provenance/`). Embed optional `provenance` on
   observations and results first — highest value per line changed, no
   endpoints.
3. **Jobs** (`Jobs/`). Submit work via `POST /brapi/v3/jobs`
   (`genxSubmitAsyncJob`), poll via `GET /brapi/v3/jobs/{jobDbId}`
   (`genxGetAsyncJobById`), and request cancellation via `DELETE
   /brapi/v3/jobs/{jobDbId}` (`genxRequestAsyncJobCancellation`). Existing
   BrAPI V2.1 `/brapi/v2/search/*` contracts remain unchanged; Jobs are not a
   retroactive replacement for them.
4. **Domain objects in any order**: `VariableTerm` via `/brapi/v3/variable-terms`, `LotLedgerEntry` via `/brapi/v3/seedlots/{seedLotDbId}/ledger`,
   `ModelArtifact` + inference, `VariantMatrix`, `FAIRPackage`,
   `TelemetryPoint`. Each is additive; implement what your users need.

## Compatibility rules (from RFC-001 §3)

V2.1 frozen; `/brapi/v3/` base; standard envelope unchanged; no shadowing of
V2.1 component names (run S-01). Until D-01 (conflict status) resolves,
servers SHOULD use `409` and clients MUST treat any `4xx` on a keyed write as
a possible conflict and re-read before retrying.

## Conformance for adopters

```shell
# Static tier on every change (no server needed)
python Scripts/checkGenXConformance.py

# Live tier against staging
python Scripts/genx_test_server.py --port 8080 --profile genx &  # reference behavior
python Scripts/checkGenXConformance.py --server https://staging/brapi/v3 --expired-job JOB_EXPIRED

# With two implementations, differential-test them
python Scripts/genx_differential_check.py --a URL_A --b URL_B --expired-job JOB_EXPIRED
```

Reference behaviors: `Scripts/genx_test_server.py` (full surface, Python),
`Scripts/genx_test_server_ts.ts` (RFC-001 core + inference, Bun) — 13/13
shared probes agree, 9/9 differential steps agree (run 9/10).

## Anti-patterns (from evidence)

- One service/cell/deployment per module or per entity — GenX objects are
  capability packs, not services.
- Silent overwrites on conflicting writes — replay or reject, never merge.
- Float quantities for inventory — decimal strings (RFC-003).
- Assuming global ordering across lots, servers, or event streams.
- Minting identifiers you cannot resolve; asserting provenance you cannot recompute.
