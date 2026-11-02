# BrAPI-GenX — Pipeline Provenance (Genotyping)

Pipeline provenance records describe bioinformatics pipeline runs.
BrAPI v2.1 has no pipeline provenance record.

- `POST /genx/v1/pipeline-provenances` (`genxRegisterPipelineProvenance`) registers one
  `PipelineProvenance` (`Schemas/PipelineProvenanceNewRequest.yaml`). Same
  `pipelineProvenanceDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/pipeline-provenances` (`genxListPipelineProvenances`) lists records,
  optionally filtered by status.
- `GET /genx/v1/pipeline-provenances/{pipelineProvenanceDbId}`
  (`genxGetPipelineProvenance`) retrieves one record.

Details and falsifiers: `../RFC-116-Pipeline-Provenance.md`.