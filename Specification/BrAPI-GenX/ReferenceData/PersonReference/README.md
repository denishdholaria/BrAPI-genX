# BrAPI-GenX — Person Reference (Reference Data)

Person reference entries describe people references for research.
Official BrAPI v2.1 already defines `People` resources and
`/brapi/v2/people` operations. The GenX proposal is a distinct candidate
record and does not assert that an optional person name or role is equivalent
to an official `personDbId`.

- `POST /genx/v1/person-references` (`genxRegisterPersonReference`) registers one
  `PersonReference` (`Schemas/PersonReferenceNewRequest.yaml`). Same
  `personReferenceDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/person-references` (`genxListPersonReferences`) lists entries,
  optionally filtered by status.
- `GET /genx/v1/person-references/{personReferenceDbId}`
  (`genxGetPersonReference`) retrieves one entry.

Details and falsifiers: `../../RFCs/RFC-097-Person-Reference.md`.
