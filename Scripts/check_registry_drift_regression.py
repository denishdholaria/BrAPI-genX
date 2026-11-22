#!/usr/bin/env python3
"""Prevent new source/registry drift relative to the pinned pre-refactor baseline.

This is a transition gate, NOT a waiver declaring existing drift correct.
Removing baseline discrepancies improves conformance. Any new or changed
discrepancy fails until the source/registry relationship is reconciled.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "Scripts/auditEndpointRegistrySourceConsistency.py"
BASELINE_REF = "d9259dca0bab21a131fa1f6a20e7643eadd6f3d7"
MARKER = "REGISTRY_DRIFT_REPORT="


def run_audit(checkout: Path) -> dict:
    command = [sys.executable, str(AUDIT), "--root", str(checkout), "--report-json"]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"Registry audit failed for {checkout}: {result.stderr[-2500:]}")
    for line in reversed(result.stdout.splitlines()):
        if line.startswith(MARKER):
            report = json.loads(line[len(MARKER):])
            if not isinstance(report, dict):
                raise RuntimeError("Audit report is not a mapping")
            return report
    raise RuntimeError(f"Audit did not emit a structured report: {result.stdout[-2500:]}")


def normalized_records(records: list) -> Counter:
    return Counter(json.dumps(item, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
                   for item in records)


def regression_errors(baseline: dict, current: dict) -> list[str]:
    errors: list[str] = []
    # Any current source load error fails immediately, whether or not old.
    for message in current.get("errors", []):
        errors.append(f"Source audit error: {message}")
    for field in ("mismatches", "registryOnlyNeighbors"):
        old = normalized_records(baseline.get(field, []))
        new = normalized_records(current.get(field, []))
        for representation, count in sorted((new - old).items()):
            errors.append(f"New or changed {field} ({count}): {representation[:450]}")
    return errors


def verify(ref: str = BASELINE_REF) -> int:
    current = run_audit(ROOT)
    with tempfile.TemporaryDirectory(prefix="genx-registry-baseline-") as directory:
        command = ["git", "worktree", "add", "--detach", "--quiet", directory, ref]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        if result.returncode:
            print(f"Cannot restore frozen baseline {ref}: {result.stderr}", file=sys.stderr)
            return 1
        try:
            baseline = run_audit(Path(directory))
        finally:
            subprocess.run(["git", "worktree", "remove", "--force", directory],
                           cwd=ROOT, check=True, capture_output=True, text=True)
    errors = regression_errors(baseline, current)
    print(f"Registry drift baseline: {ref}")
    for label in ("mismatches", "registryOnlyNeighbors"):
        print(f"{label}: baseline={len(baseline.get(label, []))}, current={len(current.get(label, []))}")
    print(f"Current source audit errors: {len(current.get('errors', []))}")
    if errors:
        print("Registry drift regression gate FAILED:")
        for item in errors[:30]:
            print(f"- {item}")
        return 1
    if current.get("mismatches") or current.get("registryOnlyNeighbors"):
        print("PASS: no new drift. Historic descriptive differences remain non-normative debt; "
              "strict zero-drift mode must not be claimed yet.")
    else:
        print("PASS: zero drift against source operations.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-ref", default=BASELINE_REF,
                        help="immutable pre-assurance baseline commit")
    args = parser.parse_args()
    try:
        return verify(args.baseline_ref)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"Registry drift check failed closed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
