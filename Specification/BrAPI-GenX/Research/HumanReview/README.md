# BrAPI-GenX — HumanReview

HumanReview records describe HumanReview entries.
BrAPI v2.1 has no HumanReview record.

- `POST /genx/v1/human-reviews` (`genxRegisterHumanReview`) registers one
  `HumanReview` (`Schemas/HumanReviewNewRequest.yaml`). Same
  `humanReviewDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/human-reviews` (`genxListHumanReviews`) lists records,
  optionally filtered by status.
- `GET /genx/v1/human-reviews/{humanReviewDbId}`
  (`genxGetHumanReview`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-136-HumanReview.md`.
