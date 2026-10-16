#!/usr/bin/env python3
"""Cross-language digest-vector checks; RFC 8785 remains an unselected candidate."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import sys

try:
    import rfc8785
except ImportError:
    raise SystemExit("Missing test dependency: python -m pip install rfc8785==0.1.4")

ROOT = Path(__file__).resolve().parents[1]
CORPUS_PATH = ROOT / "Specification/BrAPI-GenX/Conformance/digest-vectors.json"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_VECTOR_IDS = {
    "structuredJsonVectors": {
        "object-key-order-and-whitespace",
        "unicode-escaped-input-canonical-unescaped-output",
        "nested-objects-arrays-null-booleans",
        "string-escaping",
        "utf16-property-order",
        "number-serialization-and-negative-zero",
        "exact-scientific-decimal-represented-as-string",
        "unicode-composed-form-preserved",
        "unicode-decomposed-form-preserved-without-normalization",
        "empty-object",
        "empty-array",
        "safe-integer-interoperability-boundary",
    },
    "exactByteVectors": {"http-body-whitespace-preserved", "http-body-key-order-preserved"},
    "rejectionVectors": {
        "duplicate-property-name",
        "duplicate-property-name-after-unescaping",
        "non-json-nan-token",
        "lone-unicode-surrogate",
        "integer-outside-safe-interoperability-range",
    },
    "legacyDiagnostics": {"non-ascii-escaping", "unicode-property-order"},
}

class DuplicatePropertyName(ValueError):
    pass

def unique_object_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicatePropertyName("duplicate JSON property after escape decoding: " + repr(key))
        result[key] = value
    return result

def reject_non_json_constant(token):
    raise ValueError("non-JSON constant: " + token)

def parse_strict(raw):
    return json.loads(raw, object_pairs_hook=unique_object_pairs, parse_constant=reject_non_json_constant)

def reject_lone_surrogates(value):
    if isinstance(value, str):
        for char in value:
            if 0xD800 <= ord(char) <= 0xDFFF:
                raise ValueError("lone Unicode surrogate")
    elif isinstance(value, list):
        for item in value:
            reject_lone_surrogates(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            reject_lone_surrogates(key)
            reject_lone_surrogates(item)

def legacy_python_canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=CORPUS_PATH,
                        help="alternate corpus JSON path (used by mutation tests)")
    args = parser.parse_args()
    try:
        corpus = json.loads(args.corpus.read_text(encoding="utf-8"))
    except Exception as exc:
        print("FAIL digest interoperability vectors: cannot read corpus: " + str(exc))
        return 2

    failures = []
    observed_ids = []
    for section, required_ids in REQUIRED_VECTOR_IDS.items():
        vectors = corpus.get(section)
        if not isinstance(vectors, list):
            failures.append(section + ": missing or non-array section")
            continue
        ids = [item.get("id") for item in vectors if isinstance(item, dict)]
        observed_ids.extend(ids)
        missing = sorted(required_ids - set(ids))
        if missing:
            failures.append(section + ": missing required vectors: " + ", ".join(missing))
        if len(ids) != len(set(ids)):
            failures.append(section + ": duplicate vector IDs")
    if len(observed_ids) != len(set(observed_ids)):
        failures.append("vector IDs must be unique across the whole corpus")
    for vector in corpus.get("rejectionVectors", []):
        if vector.get("reasonClass") not in {"jcs-input-constraint", "invalid-json-syntax", "candidate-profile-hardening"}:
            failures.append(str(vector.get("id")) + ": unknown rejection reasonClass")
        if not isinstance(vector.get("reason"), str) or not vector["reason"].strip():
            failures.append(str(vector.get("id")) + ": missing rejection rationale")

    for section in ("structuredJsonVectors", "exactByteVectors"):
        for vector in corpus.get(section, []):
            digest = vector.get("expectedSha256") if isinstance(vector, dict) else None
            if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
                failures.append(section + ": invalid lowercase SHA-256 value for " +
                                str(vector.get("id") if isinstance(vector, dict) else "<non-object>"))
    if failures:
        print("FAIL digest interoperability vectors")
        for item in failures:
            print(" - " + item)
        return 1

    failures = []
    structured_count = exact_count = rejection_count = legacy_count = 0

    for vector in corpus["structuredJsonVectors"]:
        try:
            value = parse_strict(vector["inputJson"])
            reject_lone_surrogates(value)
            canonical_bytes = rfc8785.dumps(value)
            canonical_text = canonical_bytes.decode("utf-8")
            digest = hashlib.sha256(canonical_bytes).hexdigest()
            if canonical_text != vector["expectedCanonicalUtf8"]:
                failures.append(vector["id"] + ": canonical UTF-8 differs")
            if digest != vector["expectedSha256"]:
                failures.append(vector["id"] + ": SHA-256 differs (" + digest + ")")
            structured_count += 1
        except Exception as exc:
            failures.append(vector["id"] + ": unexpected rejection/error: " + str(exc))

    for vector in corpus["exactByteVectors"]:
        digest = hashlib.sha256(vector["inputUtf8"].encode("utf-8")).hexdigest()
        if digest != vector["expectedSha256"]:
            failures.append(vector["id"] + ": exact-byte SHA-256 differs (" + digest + ")")
        exact_count += 1

    for vector in corpus["rejectionVectors"]:
        try:
            value = parse_strict(vector["inputJson"])
            reject_lone_surrogates(value)
            rfc8785.dumps(value)
        except Exception:
            rejection_count += 1
        else:
            failures.append(vector["id"] + ": rejection-policy input was accepted")

    for vector in corpus["legacyDiagnostics"]:
        try:
            value = parse_strict(vector["inputJson"])
            actual = legacy_python_canonical(value)
            if actual != vector["pythonLegacyCanonicalUtf8"]:
                failures.append(vector["id"] + ": Python legacy diagnostic changed: " + repr(actual))
            if actual == vector["typescriptLegacyCanonicalUtf8"]:
                failures.append(vector["id"] + ": expected Python/TypeScript legacy divergence disappeared")
            legacy_count += 1
        except Exception as exc:
            failures.append(vector["id"] + ": legacy diagnostic error: " + str(exc))

    if failures:
        print("FAIL digest interoperability vectors")
        for item in failures:
            print(" - " + item)
        return 1
    print("PASS digest interoperability vectors: " + str(structured_count) + " structured JCS candidates, " +
          str(exact_count) + " exact-byte cases, " + str(rejection_count) + " rejection-policy cases, " +
          str(legacy_count) + " known legacy divergences")
    print("NOTE: RFC 8785 is evaluated as a candidate only; BrAPI decision D-02 remains open.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
