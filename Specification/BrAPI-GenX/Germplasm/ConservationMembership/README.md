# BrAPI-GenX — Conservation Membership (Germplasm)

Conservation membership records describe conservation program memberships.
Official BrAPI Germplasm and MCPD records already describe accession and institute context. A conservation-program membership may be a distinct workflow, but this draft currently stores only optional `memberDbId` and free-form `program` strings, without typed identity, consent, custody, or a verified conservation obligation.

- `POST /genx/v1/conservation-memberships` (`genxRegisterConservationMembership`) registers one
  `ConservationMembership` (`Schemas/ConservationMembershipNewRequest.yaml`). Same
  `conservationMembershipDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/conservation-memberships` (`genxListConservationMemberships`) lists records,
  optionally filtered by status.
- `GET /genx/v1/conservation-memberships/{conservationMembershipDbId}`
  (`genxGetConservationMembership`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-102-Conservation-Membership.md`.
