# BrAPI-GenX — Conservation Membership (Germplasm)

Conservation membership records describe conservation program memberships.
BrAPI v2.1 has no conservation membership record.

- `POST /genx/v1/conservation-memberships` (`genxRegisterConservationMembership`) registers one
  `ConservationMembership` (`Schemas/ConservationMembershipNewRequest.yaml`). Same
  `conservationMembershipDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/conservation-memberships` (`genxListConservationMemberships`) lists records,
  optionally filtered by status.
- `GET /genx/v1/conservation-memberships/{conservationMembershipDbId}`
  (`genxGetConservationMembership`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-102-Conservation-Membership.md`.
