# Digest interoperability — decision brief for review

**Historical status:** engineering recommendation for authorized review, not a BrAPI decision.

> **Ratification update (2026-11-03):** The BrAPI-GenX project maintainer accepted D-02 internally: generic canonical JSON uses unmodified JCS/RFC 8785 (`JCS-RFC8785`), while raw-byte and optional scientific semantic fingerprints remain distinct. This historical brief still accurately records evidence limitations; it does not prove implementation, field-level preimage definition, production conformance, or official BrAPI endorsement.

## Recommendation in one sentence

Do not standardize “SHA-256 of canonical JSON” as a universal digest rule; define the exact preimage and purpose of each digest field first, then use a versioned canonicalization profile only for fields whose preimage is a structured JSON value.

## Why the current description is insufficient

A lowercase 64-character SHA-256 value communicates an algorithm and encoding, but not what was hashed. The current GenX drafts use that same shape for at least three fundamentally different purposes:

1. **Content-byte integrity** — the exact bytes of a matrix, index, model artifact, or other payload.
2. **Structured-value identity** — JSON inputs or a canonical evidence response.
3. **Query/evidence binding** — a relationship among a request, identity context, and evidence, for which a precise preimage formula is not yet written.

A canonicalization scheme only addresses deterministic serialization of accepted JSON values. It does not decide whether the provenance input means the submitted request, normalized/defaulted parameters, preprocessed model input, or a broader execution context. It also cannot define which HTTP representation, archive, or bytes a file digest covers.

See the [digest-scope inventory](./DIGEST-SCOPE-INVENTORY.md) for the currently observed fields and gaps.

## Option assessment

| Option | Strength | Material limitation | Engineering judgement |
|---|---|---|---|
| Keep the current Python/Bun canonicalizers | Small change; already works for the tested ASCII subset | They demonstrably diverge for non-ASCII escaping and Unicode key ordering. No complete shared contract. | Not acceptable as a cross-runtime contract. Retain only as legacy diagnostics, not as the long-term rule. |
| Select RFC 8785 JSON Canonicalization Scheme (JCS) for structured JSON | Published byte-level algorithm; shared corpus evidence; avoids a bespoke serializer | Its input model is constrained by Internet JSON and IEEE 754 binary64 behavior; no Unicode normalization; does not define GenX field scope. Existing digests may change. | Accepted internally for generic canonical JSON as `JCS-RFC8785`; not automatically applicable to exact-byte fields or query-binding semantics. |
| Invent a GenX-specific canonicalizer | Could be tailored to domain-specific number requirements | Creates a permanent custom conformance and maintenance burden; likely reproduces edge-case disagreement between languages. | Avoid unless evidence demonstrates that mature candidates cannot satisfy a real requirement. Any custom profile would require a complete specification and multi-runtime vectors. |
| Hash original JSON request/response bytes | Excellent for exact byte-integrity or transport evidence | Whitespace, property order and equivalent spellings change the digest; does not identify a logical JSON value independent of serialization. | Use where exact byte identity is the goal, but name the byte domain clearly. Do not present it as a canonical structured-value digest. |

## Proposed digest classes for the design review

These are conceptual classes for discussion, not final wire-field names.

### A. Exact payload bytes

Use for model artifact bytes, matrix bytes, and index bytes. The contract must identify the byte domain (for example, the exact stored object representation) and any packaging/manifest rule for multi-file artifacts. It must say whether content-decoding, decompression, repacking, or format normalization happens before hashing. The hash is computed over the defined octet sequence, without JSON parsing or canonicalization.

The service should validate digest syntax and, when it has the payload bytes, recompute the digest. A URL and a digest alone do not prove the bytes are available or that the URL is authorized.

### B. Canonical structured JSON

Use only where the logical object boundary is precisely specified. Define:
- The exact field-level preimage object and its schema/version.
- The canonicalization profile and version.
- Accepted input constraints, including duplicate property names, Unicode validity, numeric range/precision, and parser behavior.
- UTF-8 as the encoding of the resulting canonical bytes before SHA-256.
- Version/migration rules so existing digests do not silently change meaning.

RFC 8785/JCS is the approved generic canonical JSON rule within BrAPI-GenX. Scientific quantities requiring exact decimal fidelity should be represented using the appropriate schema semantics—often decimal strings—not silently rounded through JSON binary64 number handling.

### C. Query/evidence binding

Do not define this merely as “hash the query.” Specify a versioned, typed preimage or construction that identifies the query, relevant identity/authorization context, and the exact evidence items/digests it binds. Distinguish set semantics from order semantics. Avoid embedding secrets or low-entropy sensitive values in a public, unsalted hash where an observer could guess them. State how the binding behaves when evidence is unavailable, changed, redacted, reordered, or no longer resolvable.

It may be safer to identify a complete canonical binding envelope and hash that envelope than to concatenate values with an undocumented delimiter. If a construction is retained, define unambiguous encoding and escaping for every component.

## Compatibility and migration

1. Leave BrAPI V2.1 and its existing digest-free/legacy semantics untouched.
2. Do not change actual GenX reference-server digest computation merely because the candidate-vector suite passes.
3. Define an explicit digest profile/version boundary before migration. If legacy values have already been persisted or exchanged, do not reinterpret them as JCS values; preserve a legacy profile identifier or issue new versioned records/digests as appropriate.
4. Where a digest is part of an immutable model/matrix identity, profile migration may require a new digest field/version, re-registration, or a controlled alias mapping; do not overwrite a published digest in place.
5. Golden vectors should be mandatory conformance evidence for independent implementations, but not the only acceptance criterion. Implementers must also agree on field-level preimages and domain behavior.
6. Keep tests for canonicalized structured JSON separate from exact-byte integrity tests and from any query/evidence binding test.

## Evidence and current limits

The candidate corpus is in [digest-vectors.json](./digest-vectors.json). GitHub Actions run [38687419662](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38687419662) passed 12 structured-JCS candidate vectors, 2 exact-byte cases, 5 rejection-policy cases (four JCS/JSON input constraints plus one conservative numeric guard), and 2 known legacy divergence diagnostics in both runtimes. The digest corpus mutation suite also rejected five deliberate corruptions in each runtime (10 checks total), while 12 endpoint-identity mutation tests, 21 static probes, and 28 live reference-server probes passed. These are candidate and prototype results only; they do not prove third-party agreement or standards acceptance.

Not established: digest scope agreement with third parties; deployment interoperability; production server behavior; effective authentication; durable state; or standards acceptance.

## Questions that require implementer/community review

- Is JCS acceptable for all structured JSON digest use cases, or only certain field classes?
- Should a digest object expose its algorithm/profile/version explicitly, or should the profile be fixed by a versioned contract where every field uses it?
- What is the exact preimage for each inputsDigest, responseDigest, trainingDataDigest, and queryDigest?
- How should multiple files, archives, generated indices, and HTTP content coding affect exact payload hashes?
- Which source/context identifiers belong in provenance bindings, and what privacy safeguards are required?
- How should previously generated digest values be migrated or marked without corrupting immutable artifact identities?
- Which independent language/runtime implementations and real scientific payloads must pass before an implementation can claim conformance?

## Decision boundary

Engineering can expose mismatches, publish test vectors, and show migration consequences. The BrAPI-GenX maintainer accepted the architectural rule; engineering alone still cannot claim official BrAPI ratification or implementation/conformance completion. Field-level semantics remain work to specify and verify.
