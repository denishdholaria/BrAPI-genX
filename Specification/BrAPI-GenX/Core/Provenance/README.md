# BrAPI GenX — Provenance

Embedded, optional provenance for any computed result. No endpoints.

The `ProvenanceEnvelope` (`Schemas/ProvenanceEnvelope.yaml`) records how a
value was produced: method/algorithm version, inputs digest, assumptions,
uncertainty, actor, sources, and evidence links. Host objects embed it as an
optional `provenance` field; absence means "unprovenanced", never an error.

Not covered here: licensing/DOI/embargo (future FAIR wrapper RFC), ontology
versioning and conflict policy (future ontology RFC), file payloads (use the
standard `metadata.datafiles` array).
