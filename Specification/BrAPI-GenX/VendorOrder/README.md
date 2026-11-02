# BrAPI-GenX — Vendor Order (Genomics)

Vendor genotyping order records describe an order submitted to a genotyping
vendor, its platform, sample count, and result ingestion. BrAPI v2.1 has no
vendor order record.

- `POST /genx/v1/vendor-orders` (`genxRegisterVendorOrder`) registers one
  `VendorOrderRecord` (`Schemas/VendorOrderNewRequest.yaml`). Same
  `vendorOrderDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/vendor-orders` (`genxListVendorOrders`) lists orders,
  optionally filtered by vendor or status.
- `GET /genx/v1/vendor-orders/{vendorOrderDbId}`
  (`genxGetVendorOrder`) retrieves one order.

Details and falsifiers: `../RFC-073-Vendor-Order.md`.
