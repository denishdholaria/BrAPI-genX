# BrAPI-GenX — Vendor Order (Genomics)

VendorOrderRecord is a proposed internal metadata register. Official BrAPI
version 2.1 already has `GET` and `POST /brapi/v2/vendor/orders`. This
candidate is not an equivalent substitute: its identity is distinct and its
schema has no official orderId, Sample or GenomicDataset identifier; an
ingestion timestamp alone does not verify results.

- `POST /genx/v1/vendor-orders` (`genxRegisterVendorOrder`) registers one
  `VendorOrderRecord` (`Schemas/VendorOrderNewRequest.yaml`). Same
  `vendorOrderDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/vendor-orders` (`genxListVendorOrders`) lists orders,
  optionally filtered by vendor or status.
- `GET /genx/v1/vendor-orders/{vendorOrderDbId}`
  (`genxGetVendorOrder`) retrieves one order.

Details and falsifiers: `../../RFCs/RFC-073-Vendor-Order.md`.
