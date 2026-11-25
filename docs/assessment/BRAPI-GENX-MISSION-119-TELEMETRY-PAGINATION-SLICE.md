# Mission 119 — Telemetry pagination slice postcondition

**Scope:** existing live probe L-28 only; assurance change, no new probe ID.
**Dependency:** Mission 118 L-26 bucket assurance.
**Contract impact:** none to official BrAPI 2.1 or proposed GenX wire schemas.

## False-positive risk

L-28 promises that page zero of size two contains the correct slice of three
previously stored readings. Previously, `data_length: 2` and `total_count: 3`
allowed arbitrary or duplicated records to pass, and did not check page index,
declared page size or computed total pages.

## Enforcement

- Register `telemetry_page_slice: true` on the existing L-28 GET call.
- Compare its first two records against the timestamp-sorted original
  three-reading batch, checking device, sensor, timestamp, and numeric value.
  An unexpected or duplicate row fails even when the total and row count match.
- Require structured pagination with integer `currentPage: 0`,
  `pageSize: 2`, `totalCount: 3`, and `totalPages: 2`.
- Reject removal or disabling of L-28's new assertion in manifest validation.
- Add `Scripts/test_telemetry_pagination_slice.py` with positive and negative
  mocked-server cases and enforce its execution in the static workflow and
  workflow-scope regression.

## Verification commands

```bash
python Scripts/test_telemetry_pagination_slice.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

The registered L-28 also runs against the Python in-memory reference
server in hosted live conformance. Hosted outcomes must be verified before
integration.

## Limitations

This is exact evidence for the synthetic fixture on the first requested page.
It is not a general guarantee of stable multi-page cursors, concurrent
appends during pagination, large datasets, arbitrary sorting policies,
time-zone behavior, distributed persistence, access control, or third-party
interoperability. Scientific maturity and application contracts are unchanged.
