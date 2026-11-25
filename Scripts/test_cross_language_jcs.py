#!/usr/bin/env python3
"""Cross-language JCS canonicalization interoperability test.

Runs the Python and TypeScript/Bun canonicalizers on the SAME shared input
bytes and compares canonical UTF-8 bytes and SHA-256 digest bytes.

Usage:
    python Scripts/test_cross_language_jcs.py
    python Scripts/test_cross_language_jcs.py --corpus PATH
"""
import argparse
import base64
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS = ROOT / "Specification/BrAPI-GenX/Conformance/digest-vectors.json"
TS_CLI = ROOT / "Scripts/jcs-canonicalization/cli.ts"

sys.path.insert(0, str(ROOT / "src"))
from brapi_genx.canonicalization import jcs_canonicalize, JCSError
from brapi_genx.digest import raw_byte_digest


def run_ts(input_bytes: bytes, raw: bool = False) -> dict:
    cmd = ["bun", str(TS_CLI)]
    if raw:
        cmd.append("--raw")
    proc = subprocess.run(
        cmd, input=input_bytes, capture_output=True,
    )
    # stdout is JSON
    try:
        out = json.loads(proc.stdout.decode("utf-8"))
    except Exception as exc:
        return {"ok": False, "error": f"bad ts output: {exc} :: {proc.stderr.decode('utf-8', 'replace')}", "returncode": proc.returncode}
    out["returncode"] = proc.returncode
    return out


def exact_vector_bytes(vector: dict) -> bytes:
    """Resolve test-fixture byte representation; never hash base64 text."""
    has_utf8 = isinstance(vector.get("inputUtf8"), str)
    has_base64 = isinstance(vector.get("inputBase64"), str)
    if has_utf8 == has_base64:
        raise ValueError("expected exactly one of inputUtf8 or inputBase64")
    if has_utf8:
        return vector["inputUtf8"].encode("utf-8")
    encoded = vector["inputBase64"]
    raw = base64.b64decode(encoded, validate=True)
    if base64.b64encode(raw).decode("ascii") != encoded:
        raise ValueError("noncanonical base64 representation")
    return raw


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", default=str(DEFAULT_CORPUS))
    args = parser.parse_args()

    corpus = json.loads(Path(args.corpus).read_text(encoding="utf-8"))

    failures = []
    structured = 0
    exact = 0
    rejected = 0

    # Structured JSON vectors: canonical bytes + SHA-256 must agree.
    for v in corpus.get("structuredJsonVectors", []):
        vid = v["id"]
        input_bytes = v["inputJson"].encode("utf-8")

        # Python side
        try:
            py_canonical = jcs_canonicalize(input_bytes)
            py_ok = True
            py_err = None
        except JCSError as e:
            py_ok = False
            py_err = str(e)
        # TS side
        ts = run_ts(input_bytes)
        ts_ok = bool(ts.get("ok"))

        if not (py_ok and ts_ok):
            if not py_ok and not ts_ok:
                # both rejected; for structured vectors this is a failure
                failures.append(f"{vid}: both rejected (py={py_err}, ts={ts.get('error')})")
                continue
            failures.append(f"{vid}: acceptance mismatch py_ok={py_ok} ts_ok={ts_ok} py_err={py_err} ts_err={ts.get('error')}")
            continue

        ts_canonical = base64.b64decode(ts["canonicalBase64"])
        if py_canonical != ts_canonical:
            failures.append(f"{vid}: canonical bytes differ\n  py={py_canonical!r}\n  ts={ts_canonical!r}")
            continue
        # compare to independently recorded expected
        expected_canonical = v["expectedCanonicalUtf8"].encode("utf-8")
        if py_canonical != expected_canonical:
            failures.append(f"{vid}: canonical differs from recorded expected")
            continue
        py_sha = hashlib.sha256(py_canonical).hexdigest()
        ts_sha = ts["sha256"]
        if py_sha != ts_sha:
            failures.append(f"{vid}: sha256 differs py={py_sha} ts={ts_sha}")
            continue
        if py_sha != v["expectedSha256"]:
            failures.append(f"{vid}: sha256 differs from recorded expected")
            continue
        structured += 1

    # Exact-byte vectors: raw-byte digest (SHA-256 of input bytes).
    for v in corpus.get("exactByteVectors", []):
        vid = v["id"]
        try:
            input_bytes = exact_vector_bytes(v)
        except Exception as exc:
            failures.append(f"{vid}: invalid exact-byte input: {exc}")
            continue
        py_res = raw_byte_digest(input_bytes)
        ts = run_ts(input_bytes, raw=True)
        if not ts.get("ok"):
            failures.append(f"{vid}: ts raw digest failed: {ts.get('error')}")
            continue
        if py_res.hex() != ts["sha256"]:
            failures.append(f"{vid}: raw sha256 differs py={py_res.hex()} ts={ts['sha256']}")
            continue
        if py_res.hex() != v["expectedSha256"]:
            failures.append(f"{vid}: raw sha256 differs from recorded expected")
            continue
        exact += 1

    # Rejection vectors: both must reject.
    for v in corpus.get("rejectionVectors", []):
        vid = v["id"]
        input_bytes = v["inputJson"].encode("utf-8")
        py_rejected = False
        try:
            jcs_canonicalize(input_bytes)
        except JCSError:
            py_rejected = True
        ts = run_ts(input_bytes)
        ts_rejected = not bool(ts.get("ok"))
        if not (py_rejected and ts_rejected):
            failures.append(f"{vid}: rejection mismatch py_rejected={py_rejected} ts_rejected={ts_rejected}")
            continue
        rejected += 1

    print(f"Cross-language JCS: {structured} structured, {exact} exact-byte, {rejected} rejection vectors agreed.")
    if failures:
        print("FAILURES:")
        for f in failures:
            print(" - " + f)
        return 1
    print("PASS cross-language JCS interoperability")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
