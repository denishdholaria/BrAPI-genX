# Mission 109 — Cross-runtime binary exact-byte digest integrity vectors

**Date:** 2026-11-25. **Parent:** Mission 108 review head `4479bf587b5432937cebf1c998bcec99de756c83`. **Status:** stacked assurance candidate, dependent on integration of Missions 107–108.

## Evidence gap

The shared digest conformance corpus contained two `exactByteVectors` whose inputs were always `inputUtf8` strings. Those test bytes may detect whitespace or key-order changes but cannot exercise arbitrary binary content such as compressed variant matrices or serialized model artifacts with NUL or high-bit bytes. Without raw-binary vectors, successful exact-byte tests could be misconstrued as evidence for the broader byte domains.

The existing `DIGEST-SCOPE-INVENTORY.md` explicitly separates exact-file-byte hashes from structured JavaScript Object Notation canonicalization. Decision D-02 accepts JSON Canonicalization Scheme (JCS), Request for Comments (RFC) 8785, for generic canonical JSON, but does not define field-level artifact packaging or transport preimages.

## Bounded test improvement

- Add two synthetic binary byte vectors under the existing `exactByteVectors` corpus, using `inputBase64` only as a **transport representation for the test fixture**. Each has a known, independently calculated SHA-256 (Secure Hash Algorithm 256-bit) of the **decoded bytes**.
- Update Python and TypeScript/Bun digest verifiers to accept exactly one of `inputUtf8` or `inputBase64`, reject malformed or noncanonical Base64, then hash raw bytes.
- Require the new vector identifiers in both test implementations; extend the mutation suite with five cases for changed digest, invalid Base64, ambiguous input representation, missing input and removed vector. Existing five mutation cases remain.
- Correct an outdated TypeScript diagnostic that said D-02 was still open; do not change the ratified decision itself.
- Preserve all existing structured, rejection, legacy and UTF-8 exact-byte vectors.

## Expected hosted evidence

```sh
python Scripts/test_digest_vectors.py
cd Scripts/digest-conformance && bun run test
python Scripts/test_digest_vector_mutations.py
```

Both independently implemented digest verifiers and every mutation must pass/reject as appropriate. All three commands are already hosted in static conformance. Require complete hosted static, live, differential and specification generation workflows at the exact reviewed pull-request head before integration; verify the integrated `main`.

## Limits and governance

These are **synthetic vectors**, not downloaded real-world scientific files. Hash equality does not establish file provenance, scientific model validity, checksum authority, multi-file archive canonicalization, or the field-specific byte boundary for `ModelArtifact.artifactDigest`, `VariantMatrix.fileDigest` and `indexDigest`. This mission does **not** change BrAPI version 2.1 source, proposed GenX wire contracts, registry, RFC maturity, or deferred geospatial decisions.
