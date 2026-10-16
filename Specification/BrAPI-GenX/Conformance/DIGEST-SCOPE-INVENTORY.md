# Digest scope inventory (engineering review; non-normative)

**Status:** observed draft contracts and unresolved questions, not a decision on RFC-001 D-02. This inventory is intentionally descriptive where current wording is ambiguous.

## Existing digest-bearing fields

| Field | Current draft wording / byte or value scope | Canonicalization class | Unresolved contract questions |
|---|---|---|---|
| ProvenanceEnvelope.inputsDigest | SHA-256 over the canonical inputs that produced a result | Structured JSON | What exact object is “inputs” for each job type? Are defaults, omitted values, schema identifiers, version, ordered arrays, and preprocessing included? Which canonicalization profile/version produces the bytes? |
| EvidenceLink.responseDigest | SHA-256 over the canonical evidence response | Structured JSON | Is the target the complete standard BrAPI response envelope, only result data, or the source payload bytes? How are pagination, metadata, datafiles, content negotiation, redaction, and source version treated? |
| EvidenceLink.queryDigest | SHA-256 binding the query, identity, and evidence when applicable | Context/query binding | There is no complete byte-level formula in the current draft. Which query fields, identity context, evidence digests, order, and response state are included? How are authorization-sensitive identifiers represented without leaking them? |
| ModelArtifact.trainingDataDigest | SHA-256 over canonical training inputs | Structured JSON or dataset manifest — unresolved | Is this an exact source dataset, a selected row/feature matrix, or a post-preprocessing training representation? What binds sample order, feature order, missing-value rules, data schema, and preprocessing version? |
| ModelArtifact.artifactDigest | SHA-256 over the model artifact bytes | Exact bytes | Current wording is stronger than “canonical inputs,” but packaged models may contain multiple files. Must the digest cover the exact downloadable archive, a manifest plus component bytes, or a resolved object? Transport/content-encoding semantics need precision. |
| VariantMatrix.fileDigest | SHA-256 over the matrix bytes | Exact bytes | Which byte representation is covered: stored object bytes or bytes after HTTP content decoding/decompression? How are multi-file formats or manifests represented? |
| VariantMatrix.indexDigest | SHA-256 over the index bytes | Exact bytes | Same transport and exact-byte boundary as fileDigest; index-to-matrix association also needs explicit identity. |
| FAIRPackage.payloadRefs[].responseDigest | Reuses EvidenceLink.responseDigest | Structured JSON | Inherits the responseDigest scope ambiguity above. A FAIR package does not itself make the referenced response bytes available or immutable. |
| FAIRPackage.payloadRefs[].queryDigest | Reuses EvidenceLink.queryDigest | Context/query binding | Inherits queryDigest construction ambiguity above. |

The search was limited to the current GenX draft schemas and RFC text on the feature branch; it is not a claim that every future digest-bearing field has already been enumerated.

## Cross-cutting observations

1. The draft uses one wire shape — lowercase SHA-256 hexadecimal — for distinct concepts: canonicalized JSON values, exact file bytes, and query/evidence bindings. The algorithm encoding alone does not identify the hashed input.
2. RFC-001 D-02 currently leaves the canonical form unresolved. The schema wording for inputsDigest, responseDigest, and trainingDataDigest therefore must not be treated as a fully interoperable byte-level rule yet.
3. Exact-byte digests do not need JSON canonicalization. Their contract should name the exact byte domain, including any transformations or packaging layer.
4. Structured-JSON digests need an explicit canonicalization profile and version, parser acceptance rules, and a defined object boundary before implementations can promise interoperability.
5. A query/evidence binding digest needs a separately specified, versioned input envelope or construction algorithm. Calling it “a digest of the query” is not enough to reconstruct the same preimage.
6. Examples repeated in schemas and fixtures are shape examples, not checksums of actual model, matrix, or source payload files. They must not be used as integrity evidence for real payloads.
7. SHA-256 output is a fingerprint of its preimage, not a digital signature, identity proof, authorization result, or evidence that a producer was trustworthy. The expected digest must itself be bound to a trusted source or protected through an appropriate signature/trust mechanism.

## Candidate implications

[RFC 8785 — JSON Canonicalization Scheme (JCS)](https://www.rfc-editor.org/rfc/rfc8785.html) is being evaluated for the structured-JSON cases only. It does not define the content scope of these BrAPI fields or the preimage of queryDigest. It also uses the I-JSON / IEEE 754 binary64 model, requires unique object names and valid Unicode, and does not normalize Unicode strings. Exact scientific decimal quantities and large identifiers may need string representations if exactness matters.

The experimental [golden corpus](./digest-vectors.json) is tested independently by Python and TypeScript/Bun: 12 structured-JSON vectors, 2 exact-byte cases, 5 rejection-policy cases (four JCS/JSON input constraints and one conservative numeric policy), and 2 known legacy serializer divergence diagnostics passed in [CI run 38687419662](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38687419662). Five deliberate corpus mutations are rejected by both runtimes (10 mutation checks). Passing the corpus is evidence for that candidate profile only; it does not settle field scope or ratify D-02.

## Decisions still required

- Select a structured-JSON digest profile (or document why no candidate fits), assign an explicit profile/version identifier, and define its accepted input subset.
- Define the exact preimage for inputsDigest, responseDigest, trainingDataDigest, and queryDigest independently rather than assuming their scopes are equivalent.
- Confirm exact byte boundaries for artifactDigest, fileDigest, and indexDigest, including content encodings and multi-file artifacts.
- Specify how canonicalization/profile migrations work without silently changing existing digest meaning.
- Decide which identifiers or provenance fields must be included in digest bindings, and how to avoid exposing restricted or sensitive context.
- Require third-party implementations to run the corpus and field-level conformance tests before the proposal advances beyond experimental status.
