# BrAPI-GenX — PublicationReview

PublicationReview records describe PublicationReview entries.
BrAPI v2.1 has no PublicationReview record.

- `POST /genx/v1/publication-reviews` (`genxRegisterPublicationReview`) registers one
  `PublicationReview` (`Schemas/PublicationReviewNewRequest.yaml`). Same
  `publicationReviewDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/publication-reviews` (`genxListPublicationReviews`) lists records,
  optionally filtered by status.
- `GET /genx/v1/publication-reviews/{publicationReviewDbId}`
  (`genxGetPublicationReview`) retrieves one record.

Details and falsifiers: `../RFC-120-PublicationReview.md`.
