#!/usr/bin/env python3
"""Prove deliberate corruption of the shared digest corpus fails in both runtimes."""
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "Specification/BrAPI-GenX/Conformance/digest-vectors.json"
PYTHON_RUNNER = ROOT / "Scripts/test_digest_vectors.py"
TS_RUNNER = ROOT / "Scripts/digest-conformance/test-digest-vectors.ts"


def run_case(name, mutate, runtimes, baseline):
    candidate = copy.deepcopy(baseline)
    mutate(candidate)
    with tempfile.TemporaryDirectory(prefix="brapi-genx-digest-mutation-") as folder:
        path = Path(folder) / "mutated-corpus.json"
        path.write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        for runtime_name, command in runtimes:
            completed = subprocess.run(
                command(path), cwd=ROOT, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
            )
            if completed.returncode == 0:
                print("FAIL mutation was accepted: " + name + " (" + runtime_name + ")")
                print(completed.stdout)
                return False
            print("PASS mutation rejected: " + name + " (" + runtime_name + ")")
    return True


def main():
    try:
        baseline = json.loads(CORPUS.read_text(encoding="utf-8"))
    except Exception as exc:
        print("FAIL cannot read baseline corpus: " + str(exc))
        return 2

    runtimes = [
        ("Python", lambda path: [sys.executable, str(PYTHON_RUNNER), "--corpus", str(path)]),
        ("TypeScript/Bun", lambda path: ["bun", str(TS_RUNNER), "--corpus=" + str(path)]),
    ]
    mutations = [
        (
            "wrong canonical UTF-8 bytes",
            lambda c: c["structuredJsonVectors"][0].update(expectedCanonicalUtf8="{}"),
        ),
        (
            "wrong structured digest",
            lambda c: c["structuredJsonVectors"][0].update(expectedSha256="0" * 64),
        ),
        (
            "wrong exact-byte digest",
            lambda c: c["exactByteVectors"][0].update(expectedSha256="0" * 64),
        ),
        (
            "binary digest modified",
            lambda c: next(v for v in c["exactByteVectors"]
                           if v["id"] == "binary-nul-high-bit-and-zip-header").update(
                               expectedSha256="0" * 64),
        ),
        (
            "binary base64 is invalid",
            lambda c: next(v for v in c["exactByteVectors"]
                           if v["id"] == "binary-nul-high-bit-and-zip-header").update(
                               inputBase64="not%base64=="),
        ),
        (
            "ambiguous binary and UTF-8 sources",
            lambda c: next(v for v in c["exactByteVectors"]
                           if v["id"] == "binary-nul-high-bit-and-zip-header").update(
                               inputUtf8="different bytes"),
        ),
        (
            "binary input bytes removed",
            lambda c: next(v for v in c["exactByteVectors"]
                           if v["id"] == "binary-nul-high-bit-and-zip-header").pop(
                               "inputBase64"),
        ),
        (
            "required binary vector removed",
            lambda c: c["exactByteVectors"].pop(next(
                i for i, v in enumerate(c["exactByteVectors"])
                if v["id"] == "binary-leading-and-trailing-zero-are-significant")),
        ),
        (
            "required edge vector removed",
            lambda c: c["rejectionVectors"].pop(
                next(i for i, v in enumerate(c["rejectionVectors"])
                     if v["id"] == "integer-outside-safe-interoperability-range")
            ),
        ),
        (
            "duplicate vector identity",
            lambda c: c["exactByteVectors"][1].update(id=c["exactByteVectors"][0]["id"]),
        ),
    ]

    failures = []
    for name, mutate in mutations:
        if not run_case(name, mutate, runtimes, baseline):
            failures.append(name)
    if failures:
        print("FAIL digest vector mutation suite: " + ", ".join(failures))
        return 1
    print(f"PASS digest vector mutation suite: {len(mutations)} mutations rejected by both runtimes ({2 * len(mutations)} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
