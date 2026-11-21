# BrAPI-GenX — Genetic Gain (Scientific Compute)

Genetic gain records capture the estimated genetic improvement for a trait
over a period within a breeding program. BrAPI v2.1 has no genetic gain
record.

- `POST /genx/v1/genetic-gains` (`genxRecordGeneticGain`) registers one
  `GeneticGainRecord` (`Schemas/GeneticGainRecordNewRequest.yaml`). Same
  `geneticGainRecordDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/genetic-gains` (`genxListGeneticGains`) lists records,
  optionally filtered by program, trait, or period.
- `GET /genx/v1/genetic-gains/{geneticGainRecordDbId}`
  (`genxGetGeneticGain`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-046-Genetic-Gain.md`.