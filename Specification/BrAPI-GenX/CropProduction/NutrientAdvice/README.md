# BrAPI-GenX — NutrientAdvice

NutrientAdvice records describe NutrientAdvice entries.
BrAPI v2.1 has no NutrientAdvice record.

- `POST /genx/v1/nutrient-advices` (`genxRegisterNutrientAdvice`) registers one
  `NutrientAdvice` (`Schemas/NutrientAdviceNewRequest.yaml`). Same
  `nutrientAdviceDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/nutrient-advices` (`genxListNutrientAdvices`) lists records,
  optionally filtered by status.
- `GET /genx/v1/nutrient-advices/{nutrientAdviceDbId}`
  (`genxGetNutrientAdvice`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-132-NutrientAdvice.md`.
