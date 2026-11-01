#!/usr/bin/env python3
"""
Differential check: run an identical GenX sequence against two servers and
compare normalized responses. Catches semantic drift between implementations.

Volatile fields (timestamps, server name) are stripped before comparison;
job/model/counter ids align because both servers start fresh. Digests,
statuses, envelopes, and conflict behavior must agree byte-for-byte.

Usage:
    python Scripts/genx_differential_check.py \
      --a http://127.0.0.1:18080/genx/v1 \
      --b http://127.0.0.1:18082/genx/v1 \
      --expired-job JOB_EXPIRED
"""

import argparse
import copy
import json
import sys
import uuid

from urllib import request as urlrequest
from urllib.error import HTTPError

VOLATILE = {"createdAt", "updatedAt", "expiresAt", "serverName"}


def http_call(server, method, path, body=None):
    url = server.rstrip("/") + path
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urlrequest.Request(url, data=data, method=method)
    req.add_header("Accept", "application/json")
    if body is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urlrequest.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8") or "{}")
    except HTTPError as exc:
        try:
            return exc.code, json.loads(exc.read().decode("utf-8") or "{}")
        except Exception:
            return exc.code, {}


def normalize(doc):
    if isinstance(doc, dict):
        return {k: normalize(v) for k, v in doc.items() if k not in VOLATILE}
    if isinstance(doc, list):
        return [normalize(v) for v in doc]
    return doc


def main():
    parser = argparse.ArgumentParser(description="GenX differential check")
    parser.add_argument("--a", required=True)
    parser.add_argument("--b", required=True)
    parser.add_argument("--expired-job", default="JOB_EXPIRED")
    args = parser.parse_args()

    key = str(uuid.uuid4())
    model_id = f"test-authority:model:{uuid.uuid4().hex[:8]}"
    submit = {
        "jobType": "germplasm_search",
        "parameters": {"germplasmNames": ["Germ 01"]},
        "idempotencyKey": key,
    }
    conflict = dict(submit)
    conflict["parameters"] = {"germplasmNames": ["Germ 02"]}
    model = {
        "modelDbId": model_id,
        "modelName": "Differential probe model",
        "modelVersion": "1",
        "artifactDigest": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
        "status": "active",
    }
    inference = {
        "jobType": "inference",
        "parameters": {"modelDbId": model_id, "modelVersion": "1",
                       "inputs": {"x": [1.5, 2.5]}},
        "idempotencyKey": str(uuid.uuid4()),
    }
    steps = [
        ("GET", "/serverinfo", None),
        ("POST", "/jobs", submit),
        ("POST", "/jobs", copy.deepcopy(submit)),
        ("POST", "/jobs", conflict),
        ("POST", "/jobs", {"jobType": "nope"}),
        ("GET", f"/jobs/{args.expired_job}", None),
        ("POST", "/models", model),
        ("POST", "/models", copy.deepcopy(model)),
        ("POST", "/jobs", inference),
    ]

    failures = 0
    for method, path, body in steps:
        left = http_call(args.a, method, path, body=copy.deepcopy(body) if body else None)
        right = http_call(args.b, method, path, body=copy.deepcopy(body) if body else None)
        if path == "/serverinfo" and left[0] == right[0] == 200:
            # Capability lists legitimately differ by implementation scope:
            # the smaller set must be a subset, everything else byte-equal.
            left_names = {c["name"] for c in left[1]["result"].get("capabilities", [])}
            right_names = {c["name"] for c in right[1]["result"].get("capabilities", [])}
            smaller, larger = sorted([left_names, right_names], key=len)
            rest_left = {k: v for k, v in normalize(left[1]).items()}
            rest_right = {k: v for k, v in normalize(right[1]).items()}
            for doc in (rest_left, rest_right):
                doc["result"].pop("capabilities", None)
                doc["result"].pop("authProfiles", None)
            if smaller <= larger and rest_left == rest_right:
                print(f"AGREE  {method} {path} -> 200 (subset capabilities)")
                continue
            failures += 1
            print(f"DIVERGE {method} {path}: capability sets {sorted(left_names)} vs {sorted(right_names)}")
            continue
        if left[0] != right[0] or normalize(left[1]) != normalize(right[1]):
            failures += 1
            print(f"DIVERGE {method} {path}: status {left[0]} vs {right[0]}")
            left_doc, right_doc = normalize(left[1]), normalize(right[1])
            if left_doc != right_doc:
                print(f"  A: {json.dumps(left_doc)[:400]}")
                print(f"  B: {json.dumps(right_doc)[:400]}")
        else:
            print(f"AGREE  {method} {path} -> {left[0]}")
    print(f"differential: {len(steps) - failures}/{len(steps)} steps agree")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
