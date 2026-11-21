# RFC-073 — Vendor Order (Genomics)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-013 (Genomic Datasets), RFC-043 (VCF Import), `../CLASSIFICATION.md` (D3).

## 1. Problem

BrAPI v2.1 standardizes variants, call sets, and calls but has no place to
record a genotyping order submitted to a vendor, its platform, sample count,
and result ingestion. Vendor orders are the routine interface between a
breeding program and a genotyping service. Without an order record, results
arrive as unversioned files with no stated vendor, platform, or sample scope,
so they cannot be audited or reproduced.

## 2. Object

`VendorOrderRecord` — one immutable record of a genotyping order submitted to a
vendor, with its vendor, platform, sample count, status, and result ingestion.

## 3. Endpoints

- `GET /genx/v1/vendor-orders` (`genxListVendorOrders`)
- `POST /genx/v1/vendor-orders` (`genxRegisterVendorOrder`)
- `GET /genx/v1/vendor-orders/{vendorOrderDbId}` (`genxGetVendorOrder`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Vendor orders reference BrAPI `Sample` and GenX `GenomicDataset` by
  identifier; they do not duplicate those resources.
- A vendor order is not a BrAPI data resource and must not be treated as one.
- Result bytes are not transported by this API. The record names and verifies
  the ingestion; retrieval uses the referenced storage.

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
