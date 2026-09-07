# BrAPI GenX — Model Registry and Inference

Models get identities, artifact digests, training provenance, and a revocable
lifecycle. Inference runs as a Job bound to a registered model version, so
every result names its model and binds its inputs by digest.

- `POST /models` registers a `ModelArtifact`
  (`Schemas/ModelArtifactNewRequest.yaml`). Same `(modelDbId, modelVersion)` +
  identical body replays; different body is rejected with `409`.
- `GET /models`, `GET /models/{modelDbId}` read terms (latest created when
  `version` is omitted).
- Inference: Jobs with `jobType: inference`,
  `parameters: {modelDbId, modelVersion?, inputs}`. Unknown or revoked models
  are rejected at submit; `deprecated` serves with a `WARNING`.

Details and falsifiers: `../RFC-004-Model-Registry.md`.
