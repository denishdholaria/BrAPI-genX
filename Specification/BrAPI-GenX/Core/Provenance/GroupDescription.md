# Group Provenance

**Status:** BrAPI-GenX proposed shared schema, not a finalized scientific provenance standard and not an official BrAPI version 2.1 endpoint.

This group contains the optional embedded `ProvenanceEnvelope` schema for describing how a computed result was produced. It can record method and algorithm versions, source-record identities, creation time, assumptions, quantified uncertainty, and links to retrievable evidence. This module defines **no independent operations**; a host record chooses whether and how to embed provenance.

**Boundaries:** Missing provenance is explicitly permitted by this candidate schema and must not be misrepresented as proof that a result is scientifically validated. Digest fields in the draft schema must not be used to assert a universally accepted digest algorithm or canonical preimage. The accepted project decision D-02 separates raw-byte, canonical data and domain-specific semantic fingerprints; remaining domain-specific digest choices require their own evidence. This module does not decide licensing, embargo, ontology governance or data-access authority.

**Sources:** [Local module scope](./README.md), [ProvenanceEnvelope schema](./Schemas/ProvenanceEnvelope.yaml), and [accepted D-02 boundary](../../DECISIONS.md).
