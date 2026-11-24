# Mission 071 — Official vendor-order overlap regression

**Parent inspected:** `8adcf1921f6755a4b7322cc7dbf018b1d78b6aad` (Mission 070), 2026-11-24.
**Intent:** Follow through on Mission 070's verified official BrAPI version 2.1 vendor-order overlap with a machine-checkable assurance gate. This is an additive review obligation, not a new wire contract or scientific equivalence.

## Source evidence

The official file `Specification/BrAPI-Genotyping/VendorSamples/Vendor_Orders_GET_POST.yaml` exposes both GET and POST operations at `/vendor/orders` (public BrAPI route `/brapi/v2/vendor/orders`). The candidate `Genotyping/VendorOrder/Schemas/VendorOrder.yaml` publishes `VendorOrderRecord`, whereas its filename does not equal its schema symbol; a false generic-path assumption would make this official overlap impossible to guard.

## Changes

- Add `Genotyping/VendorOrder` to the confirmed-overlap inventory, pinned to both official methods and an explicitly named candidate schema filename.
- Extend the overlap audit to resolve a schema filename independent of its type key; when the manifest explicitly declares required methods, fail closed if one disappears.
- Regression tests copy and mutate the official source, reject reintroduced false 'no vendor order' wording, and assert the expanded inventory count is six.
- Preserve all prior overlap records, all 33 currently observed unratified links and the original 156-module denominator.

## Boundary and validation

This guard proves source-file consistency and blocks known unsupported overlap claims. It does not prove `vendorOrderDbId` equivalence with official `orderId`, service implementation, authenticated result ingestion, independent conformance, or community adoption. Deferred vendor mapping and identifier decisions remain unresolved.

Execute `python3 Scripts/audit_genx_standards_overlap.py` and `python3 Scripts/test_genx_standards_overlap.py`; hosted workflow conclusions must be observed separately.
