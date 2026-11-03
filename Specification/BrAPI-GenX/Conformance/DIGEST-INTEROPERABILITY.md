# Digest interoperability corpus (experimental)

**Status:** exploratory engineering evidence only. This file does not prove implementation or conformance and is not a normative BrAPI rule.

> **Ratification update (2026-11-03):** The BrAPI-GenX maintainer accepted JCS/RFC 8785 as the `JCS-RFC8785` method for generic canonical JSON under D-02. The results below remain historical candidate-evaluation evidence; they do not show the reference servers have been migrated or imply official BrAPI endorsement.

## Why the corpus exists

The current reference servers do not serialize the same logical JSON value into the same bytes for every input. Python's default JSON dumper escapes non-ASCII characters and sorts property names by Unicode code point; the TypeScript/Bun implementation uses ECMAScript string serialization and UTF-16 code-unit ordering. These choices can produce different digests for identical logical JSON.

The shared machine-readable vectors are in [digest-vectors.json](./digest-vectors.json). Two separate modes are tested:

- **Structured JSON digest candidate:** parse a valid JSON value, serialize it according to the candidate profile, encode the result as UTF-8, then compute SHA-256 over those canonical bytes.
- **Exact-byte digest:** compute SHA-256 over the exact supplied bytes. Do not parse, normalize, reorder, or reserialize them. Whitespace and key order therefore matter.

These two digest types are not interchangeable. Any future field or specification must state which input and bytes it binds to.

## Historical candidate evaluation: RFC 8785 JCS

[RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html) defines the JSON Canonicalization Scheme (JCS). It is the accepted BrAPI-GenX generic canonical JSON method (`JCS-RFC8785`); this historical evidence does not itself implement it or adopt it on behalf of the BrAPI community.

Important constraints and review questions:

- JCS requires an Internet JSON (I-JSON) compatible value, including no duplicate property names and numbers that interoperate as IEEE 754 binary64 values.
- Exact decimal quantities and integers that require precision beyond binary64 should generally be represented as strings with a separately defined semantic schema, not silently rounded JSON numbers.
- Unicode is preserved as supplied; JCS does not normalize composed and decomposed Unicode strings.
- JCS canonical bytes are not a digest of the original HTTP body. Exact-body integrity uses the exact bytes instead.
- A bare SHA-256 digest is not a signature, proof of authorization, proof of origin, or protection against a malicious producer.

The vector runners reject duplicate names (including names equal only after JSON escape decoding), non-JSON constants, and lone surrogate values. They also apply one deliberately stricter candidate-profile safeguard: reject a plain integer token outside the JavaScript safe-integer range before parsing can silently round it. This is not a claim that large integer tokens are invalid JSON or that RFC 8785 mandates blanket rejection; RFC 7493 says such values are not guaranteed to be treated exactly and recommends strings when exact interchange is required. The two language-specific test runners consume this same corpus and compare exact UTF-8 canonical bytes and digest outputs.

## Current result boundary

The legacyDiagnostics section records known disagreement in the existing reference-server algorithms. The tests intentionally keep those diagnostics visible while separately verifying the historical JCS candidate corpus. They do **not** claim the current reference-server behavior has been migrated.

The approved architecture still requires implementation evidence for scientific-data implications, parser behavior in supported languages, query/source digest scope, schema version, and missing/changed/redacted-source behavior. BrAPI V2.1 remains unchanged, and no official BrAPI standards acceptance is claimed.

## Field-level scope inventory

The [digest-scope inventory](./DIGEST-SCOPE-INVENTORY.md) catalogs each digest field currently found in the draft contracts and distinguishes structured-JSON digests, exact-byte payload digests, and the underspecified query/evidence binding digest. The canonicalization algorithm alone cannot define any of these fields' exact preimage. D-02 is approved architecturally; field-by-field scope remains implementation/specification work.

The design recommendation is captured separately in [DIGEST-DECISION-BRIEF.md](./DIGEST-DECISION-BRIEF.md). The [digest-scope inventory](./DIGEST-SCOPE-INVENTORY.md) should be reviewed alongside it: selecting JCS alone cannot resolve which values or bytes the field names actually bind.
