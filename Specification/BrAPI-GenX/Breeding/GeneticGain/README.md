# BrAPI-GenX — Genetic Gain (Scientific Compute)

GeneticGainRecord proposes a numerical estimate of genetic improvement,
not a verified program-level rate or response to selection. The `gainValue`,
program and trait identifiers are required, but `unit`, `period`, `method`,
and provenance are optional. No required baseline, annualization method,
variance component or statistical uncertainty is specified.

Official BrAPI version 2.1 Program and Trait resources remain authoritative;
the candidate's string identifiers do not by themselves prove valid joins.

- `POST /genx/v1/genetic-gains` (`genxRecordGeneticGain`) registers one
  `GeneticGainRecord` (`Schemas/GeneticGainRecordNewRequest.yaml`). Same
  `geneticGainRecordDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/genetic-gains` (`genxListGeneticGains`) lists records,
  optionally filtered by program, trait, or period.
- `GET /genx/v1/genetic-gains/{geneticGainRecordDbId}`
  (`genxGetGeneticGain`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-046-Genetic-Gain.md`.