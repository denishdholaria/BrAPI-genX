# RFC-004: Model Registry and Inference

- Status: **proposal** (not accepted, not normative, grants no implementation authority)
- Builds on: RFC-001 (Jobs, `ProvenanceEnvelope`, `409` evidence)
- Scope: registering model artifacts and running auditable inference through Jobs
- Non-scope: training pipelines, feature stores, model merging, online
  learning, hardware-specific serving — each needs its own RFC or stays out

## 1. Problem

Breeding decisions increasingly come from models (genomic selection,
phenomic classification, vision grading), but BrAPI has no model object. A
prediction value arriving without model identity, artifact digest, training
provenance, and uncertainty cannot be trusted, reproduced, or revoked: when a
model is found unsafe, there is no handle to deny its further use, and no way
to enumerate which past results it produced.

Reference experience (BijMantra polyglot cell, pre-production research, cited
as evidence only): the runtime owns all authority while isolated workers run
scoped contracts; every accepted dispatch recomputes a check value, commits
one result with tolerance and explicit uncertainty, and denies unknown
artifacts, stale results, and unsafe models. RFC-004 standardizes the wire
half: model identity with artifact digests, lifecycle including revocation,
and inference as a Job bound to a registered model version.

## 2. Object — ModelArtifact

Files: `Models/Schemas/ModelArtifact.yaml`,
`Models/Schemas/ModelArtifactNewRequest.yaml`,
`Models/Models_GET_POST.yaml`, `Models/Models_ModelDbId_GET.yaml`.

Purpose: give every model a namespaced identity, a content digest, training
provenance, and a revocable lifecycle.

Fields: `modelDbId` (`{authority}:model:{localId}`, required), `modelName`,
`modelVersion` (opaque string, required), `artifactDigest` (SHA-256 hex of the
model artifact bytes, required), `artifactURL?`, `trainingDataDigest?`
(SHA-256 hex over canonical training inputs), `metrics?` (open object —
evaluation scores with their own provenance in `provenance`), `framework?`
(e.g. `onnx-1.17`, `scikit-learn-1.5`), `status`
(`active`|`deprecated`|`revoked`), `supersededBy?`, `provenance?`
(`ProvenanceEnvelope` — who trained, on what, with which code version).

Responsibilities: model identity, artifact integrity, lifecycle.
Non-responsibilities: training execution; feature engineering; serving
topology; approval workflows (a `revoked` flag records decisions, it does not
make them).

Invariants:

1. Same `(modelDbId, modelVersion)` + identical body replays the existing
   record. Same pair + different body is rejected with `409`. In particular
   the `artifactDigest` of a published version never changes.
2. `revoked` is terminal and denies inference. `deprecated` warns (a
   `WARNING` status message on acceptance) but still serves.
3. Inference results always name their `(modelDbId, modelVersion)` and carry
   `inputsDigest` + `uncertainty`. A result without model identity is not a
   GenX inference result.

## 3. Inference as a Job

No new endpoint. Inference runs through RFC-001 Jobs with
`jobType: inference` and parameters `{modelDbId, modelVersion?, inputs}`:

- Unknown model, unknown version, or `revoked` status → submit rejected
  (`400`). `deprecated` → accepted with a `WARNING` status message.
- On `COMPLETED`, `result.data[0]` is the inference record
  `{modelDbId, modelVersion, inputsDigest, outputs, uncertainty}` where
  `inputsDigest` is SHA-256 over the canonical inputs and `outputs` is
  model-defined.
- Servers advertise supported inference kinds as `jobs` capabilities; the
  reference server implements one deterministic echo stub (`outputs.echo`)
  solely to prove digest binding — it is not a model.

## 4. Hypothesis, falsifier, verification

- Hypothesis: any consumer can verify what model produced a result, recompute
  its input binding, and be refused when the model is unknown or revoked.
- Falsifier: an inference result without model identity; a mutated artifact
  under a published version; a revoked model that still serves; an
  unverifiable `inputsDigest`.
- Verification: static probes S-13/S-14 plus live probes L-12–L-14 in
  `Conformance/probes.yaml` against the reference test server.

## 5. Explicit unknowns and requires-decision

1. `requires decision`: model approval/governance workflows behind
   `revoked` — the flag is a record, not a process.
2. `requires decision`: artifact transport (inline vs URL, chunking, signing)
   — only the digest is standardized here.
3. `assumption`: `metrics` semantics are model-defined; comparability across
   models is out of scope.
4. `unknown`: real serving topologies (batch, GPU pools, edge) — no wire
   impact is claimed.

## 6. File map

```text
Specification/BrAPI-GenX/
  RFC-004-Model-Registry.md   this document
  Models/README.md + GroupDescription.md
    + Schemas/ModelArtifact.yaml + Schemas/ModelArtifactNewRequest.yaml
    + Models_GET_POST.yaml + Models_ModelDbId_GET.yaml
```
