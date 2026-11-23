# Group ModelArtifact

Models get identities, artifact digests, training provenance, and a revocable lifecycle. Inference runs as a Job bound to a registered model version, so every result names its model and binds its inputs by digest. Unknown or revoked models are rejected at submit.
