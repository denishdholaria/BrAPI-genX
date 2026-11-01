# BrAPI GenX — FAIR Exchange Packages

A metadata envelope that makes payload sets citable: persistent identifiers,
an SPDX license, an access contract with embargo, and digest-bound payload
references. DOI minting, byte storage, and access approvals stay outside —
the package links to them.

- `POST /genx/v1/fair-packages` (`genxRegisterFairPackage`) registers a `FAIRPackage`
  (`Schemas/FAIRPackageNewRequest.yaml`). Same `packageDbId` + identical
  body replays; different body is rejected with `409`.
- `GET /genx/v1/fair-packages` (`genxListFairPackageMetadata`) lists metadata; `GET /genx/v1/fair-packages/{packageDbId}` (`genxGetFairPackageMetadata`) retrieves one package's metadata.
  Embargoed payloads are denied with `403` before `embargoUntil`.

Details and falsifiers: `../RFC-006-FAIR-Packages.md`.
