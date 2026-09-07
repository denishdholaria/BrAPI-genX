# BrAPI GenX — FAIR Exchange Packages

A metadata envelope that makes payload sets citable: persistent identifiers,
an SPDX license, an access contract with embargo, and digest-bound payload
references. DOI minting, byte storage, and access approvals stay outside —
the package links to them.

- `POST /fair-packages` registers a `FAIRPackage`
  (`Schemas/FAIRPackageNewRequest.yaml`). Same `packageDbId` + identical
  body replays; different body is rejected with `409`.
- `GET /fair-packages`, `GET /fair-packages/{packageDbId}` read metadata.
  Embargoed payloads are denied with `403` before `embargoUntil`.

Details and falsifiers: `../RFC-006-FAIR-Packages.md`.
