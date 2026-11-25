# Mission 101 — Reject shared wrong HTTP statuses in cross-runtime conformance

**Date:** 2026-11-25. **Starting source:** Mission 100 review head `b917477253fbee985a50ffd25fe9a0b9de0def03`. **Review base:** integrated `main` at `07e8dada4efb6d56701a5711fafc81600c7b0c60`. **Status:** implementation under verification; not merged or ratified by this assessment.

## Confirmed weakness

The nine-request `Scripts/genx_differential_check.py` compared response status codes and normalized bodies for agreement. In the general comparison path, both implementations returning a matching but **incorrect** status (for example `200` for a changed-body idempotency conflict that must return `409`, or matching `500` errors) could count as agreement. Agreement of two implementations is necessary but not sufficient for a contract claim.

## Bounded change

Each existing request now has an explicit expected status, in order: `200, 202, 200, 409, 400, 200, 200, 200, 202`. The checker rejects a mismatch from **either** server before its existing response-body comparison and capability-subset logic.

The new `Scripts/test_genx_differential_check.py` uses controlled, paired HTTP responses to establish (1) nine expected statuses pass, (2) two matching but incorrect conflict statuses fail, (3) one-sided wrong replay status fails and (4) matching internal-server errors fail. Hosted cross-runtime execution runs this suite as an explicit step, protected by the workflow-scope regression checker.

## Verification and scientific boundary

```sh
python Scripts/test_genx_differential_check.py
python Scripts/test_conformance_workflow_scope.py
```

Require hosted static, live-reference, cross-runtime differential and specification-generation checks on the exact review head, then check `main` separately after integration. The expected statuses are grounded in the current project-owned RFC-001/RFC-004 reference implementation sequence; no claim is made that these nine status choices define every future GenX API or guarantee independent-vendor interoperability.

**No normative promotion:** No released Breeding Application Programming Interface (BrAPI) version 2.1 source contract, GenX wire schema, endpoint registry, Request for Comments (RFC) maturity, governance decision, or protected GroupDescription is changed.
