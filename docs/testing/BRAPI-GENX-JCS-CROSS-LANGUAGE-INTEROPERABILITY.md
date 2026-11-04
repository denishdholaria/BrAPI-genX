# BrAPI-GenX — JCS Cross-Language Interoperability

## 1. Scope

Phase 1B.2 establishes that independent implementations in Python and
TypeScript (Bun) produce exactly the same canonical JSON bytes (RFC 8785
JCS) and SHA-256 digest bytes for the same permitted JSON input.

In scope:

- Shared language-independent JCS vector corpus.
- Python canonicalizer revalidation.
- TypeScript/Bun canonicalizer implementation.
- Cross-language canonical-byte comparison.
- Cross-language SHA-256 comparison.
- Negative-case (rejection) agreement.
- CI integration and reproduction instructions.

Out of scope (explicitly excluded): public digest envelopes/encoding,
request fingerprint changes, idempotency, persistence, reference-server
migration, scientific semantic fingerprints.

## 2. Supported implementation languages

| Language | Runtime | Module |
|---|---|---|
| Python | CPython 3.13 | `src/brapi_genx/canonicalization.py` |
| TypeScript | Bun 1.4.2 | `Scripts/jcs-canonicalization/jcs.ts` |

## 3. JCS library and versions

| Implementation | Library | Version | License |
|---|---|---|---|
| Python | `rfc8785` | 0.1.4 | (see package) |
| TypeScript/Bun | `canonicalize` (erdtman) | 5.1.0 | Apache-2.0 |

Both libraries implement RFC 8785 JCS. BrAPI-GenX strict input validation
(duplicate properties, lone surrogates, safe integers, non-finite numbers)
is layered on top of the library in both implementations.

## 4. Shared fixture location

`Specification/BrAPI-GenX/Conformance/digest-vectors.json`

Provenance: official RFC 8785 examples adapted, plus independently derived
GenX vectors. See vector `id` and corpus metadata.

## 5. Vector categories

- Category A — Official JCS vectors (RFC 8785 examples).
- Category B — Basic JSON (empty object/array, strings, ints, decimals, bools, null, nested).
- Category C — Property ordering (reversed, nested, ASCII, Unicode, UTF-16 edge cases).
- Category D — Numbers (boundaries, floats, decimals, exponentials, negative zero, large, invalid).
- Category E — Unicode (non-ASCII, multilingual, escapes, combining, supplementary).
- Category F — Invalid inputs (duplicate props, nested duplicates, malformed JSON, non-finite, unsafe integers, invalid encoding, unpaired surrogates).
- Category G — Raw-byte digest (exact bytes).
- Category H — Canonical JSON SHA-256.

## 6. Canonical-byte comparison strategy

For every valid vector:

1. Supply identical input bytes to Python (`jcs_canonicalize`).
2. Supply identical input bytes to TypeScript/Bun (`jcsCanonicalize` via CLI).
3. Obtain canonical output bytes from both.
4. Compare exact byte sequences (not parsed objects).
5. Compare against independently recorded expected output.

Harness: `Scripts/test_cross_language_jcs.py`.

## 7. SHA-256 comparison strategy

After canonical-byte agreement:

1. Hash canonical output with SHA-256 in Python.
2. Hash same canonical output in TypeScript/Bun.
3. Compare raw digest bytes (hex).
4. Compare against recorded expected SHA-256.

Raw-byte digest path (Category G) hashes input bytes directly without
canonicalization, tested separately.

## 8. Duplicate-property handling

Both implementations detect duplicate JSON object property names at every
nesting level BEFORE conversion to language objects (which would collapse
duplicates). Detection occurs after JSON string-escape decoding, so
`"a"` and `"\u0061"` are both decoded to `"a"` and treated as duplicates.

Rejection vectors: `duplicate-property-name`,
`duplicate-property-name-after-unescaping`.

## 9. Numeric policy

- JCS number serialization (IEEE 754 shortest form) via the underlying
  library.
- Non-finite values (NaN, Infinity, -Infinity) rejected (not valid JSON).
- Plain integer tokens outside IEEE 754 safe range
  [-(2^53-1), 2^53-1] rejected (GenX strict input policy).
- Exponential/decimal numbers are treated as floats and are not subject to
  the safe-integer range check (mirroring Python's `isinstance(int)`).
- Scientific decimal values requiring exact precision must be encoded as
  JSON strings; generic JCS does not preserve numeric precision beyond
  binary64.

## 10. Unicode policy

- No Unicode normalization (NFC/NFD preserved).
- Lone/unpaired surrogates rejected.
- Property key ordering by UTF-16 code units (JCS requirement), verified
  with supplementary-plane edge cases.
- Strings preserved verbatim.

## 11. Invalid-input behaviour

Both implementations reject the same violations:
- Duplicate property names (top-level and nested).
- Malformed JSON.
- Non-finite numbers.
- Lone surrogates.
- Unsafe integers (plain tokens).
- Invalid UTF-8.

Error messages need not be byte-identical; error categories are consistent
where practical.

## 12. Actual test results

| Test category | Python | TypeScript/Bun | Cross-language |
|---|---|---|---|
| Official JCS vectors | pass | pass | pass |
| Basic JSON | pass | pass | pass |
| Property ordering | pass | pass | pass |
| Numeric edge cases | pass | pass | pass |
| Unicode | pass | pass | pass |
| Duplicate properties | pass | pass | pass |
| Invalid inputs | pass | pass | pass |
| Canonical byte equality | pass | pass | pass |
| SHA-256 equality | pass | pass | pass |

Quantitative:
- Python: 56 tests passed (`tests/test_jcs_canonicalization.py`).
- TypeScript/Bun: 12 structured + 5 rejection vectors passed.
- Cross-language harness: 12 structured, 2 exact-byte, 5 rejection vectors agreed.

## 13. Known limitations

- The `canonicalize` (TS) and `rfc8785` (Python) libraries are independent
  implementations; agreement is verified on the corpus, not by construction.
- External digest encoding remains unresolved (intentionally).
- Request fingerprint construction in `digest.py` still uses a legacy
  sort_keys path; migration deferred.
- Reference servers still use legacy canonicalizers (see migration inventory).

## 14. Reproduction instructions

Python tests:
```
cd brapi-genx
python -m pytest tests/test_jcs_canonicalization.py -v
```

TypeScript/Bun tests:
```
cd brapi-genx/Scripts/jcs-canonicalization
bun install
bun run test
```

Cross-language harness:
```
cd brapi-genx
python Scripts/test_cross_language_jcs.py
```

Existing digest conformance (both runtimes):
```
cd brapi-genx/Scripts/digest-conformance && bun install && bun run test
python Scripts/test_digest_vectors.py
```

## 15. CI integration

The existing workflow `.github/workflows/genx-static-conformance.yml` runs
Python and Bun digest tests. The new cross-language harness and TS JCS tests
should be added to the workflow paths and steps. Minimal additions:

- Install deps in `Scripts/jcs-canonicalization`.
- Run `bun run test` there.
- Run `python Scripts/test_cross_language_jcs.py`.

## 16. Reference-server migration status

Migration has NOT occurred. See migration inventory (Stage G) for legacy
consumers. Reference servers continue to use legacy canonicalizers; migration
is a separate bounded task.
EOF
