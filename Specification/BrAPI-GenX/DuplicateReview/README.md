# BrAPI-GenX — Duplicate Review (Germplasm)

Duplicate review records describe duplicate review decisions.
BrAPI v2.1 has no duplicate review record.

- `POST /genx/v1/duplicate-reviews` (`genxRegisterDuplicateReview`) registers one
  `DuplicateReview` (`Schemas/DuplicateReviewNewRequest.yaml`). Same
  `duplicateReviewDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/duplicate-reviews` (`genxListDuplicateReviews`) lists records,
  optionally filtered by status.
- `GET /genx/v1/duplicate-reviews/{duplicateReviewDbId}`
  (`genxGetDuplicateReview`) retrieves one record.

Details and falsifiers: `../RFC-104-Duplicate-Review.md`.
