# RFC-073 — Vendor Order (Genomics)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-013 (Genomic Datasets), RFC-043 (VCF Import), `../CLASSIFICATION.md` (D3).

## 1. Problem

BrAPI v2.1 already includes `GET` and `POST /brapi/v2/vendor/orders`
and vendor order status, result and plate operations. GenX VendorOrderRecord
therefore overlaps an established vendor-facing workflow. A separate
candidate record may support internal audit or other needs, but the gap
and interoperable mapping have not been demonstrated. Absence of a
GenX-specific field is not evidence that BrAPI lacks vendor ordering.

## 2. Object

`VendorOrderRecord` — a candidate immutable metadata record describing
an asserted genotyping order, with optional vendor, platform, sample count
and ingestion timestamp; it does not prove actual submission or ingestion.

## 3. Endpoints

- `GET /genx/v1/vendor-orders` (`genxListVendorOrders`)
- `POST /genx/v1/vendor-orders` (`genxRegisterVendorOrder`)
- `GET /genx/v1/vendor-orders/{vendorOrderDbId}` (`genxGetVendorOrder`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Official BrAPI v2.1 vendor orders use `/brapi/v2/vendor/orders`,
  including an official `orderId`. The candidate `vendorOrderDbId`
  has no established equivalence or synchronization with that identifier.
- The candidate has no `sampleDbId`, `genomicDatasetDbId`, official
  `orderId` or `serviceIds` field. It does not reference BrAPI Sample or
  GenX GenomicDataset by identifier and is not a substitute for official
  vendor ordering.
- Result bytes are not transported by this proposal. Optional
  `resultIngestedAt` is a string claim, not independently verified ingestion
  or a link to retrieved data.

## 5. Invariants

- A published `vendorOrderDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional orders linked by `supersedes`.
- A record does not imply that the order was fulfilled, validated, or
  scientifically endorsed.
- `vendor` and `platform` are free-form identifiers; they are not BrAPI
  organizations or locations.

## 6. Deferred questions

- D-217: Should `sampleCount` be required? (Current: optional.)
- D-218: Should result ingestion require a GenX `GenomicDataset` reference?
  (Current: optional timestamp only.)
- D-219: Should vendor and platform be controlled GenX terminology instead of
  free-form strings? (Current: free-form strings.)

## 7. Classification

Primary domain: D3 — Genotyping and Molecular Genomics.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
