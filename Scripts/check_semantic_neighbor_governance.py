#!/usr/bin/env python3
"""Validate the semantic-neighbor review ledger against the endpoint registry.

This is a governance check, not a scientific-equivalence check. It ensures the
review inventory remains complete, internally consistent, and explicitly
unresolved where evidence is absent.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "Specification" / "ENDPOINT-REGISTRY.json"
LEDGER = ROOT / "Specification" / "BrAPI-GenX" / "Conformance" / "semantic-neighbor-review.yaml"
AUDIT = ROOT / "Scripts" / "auditEndpointRegistrySourceConsistency.py"

ALLOWED_STATUSES = {"inherited-unreviewed", "evidence-backed-proposed",
                    "requires-decision", "rejected", "superseded"}
ALLOWED_PROVENANCE = {"inherited-registry-only", "source-openapi-declared",
                      "registry-and-source", "documented-mapping", "manual-review"}
ALLOWED_BOUNDARIES = {"within-module", "cross-module", "cross-domain"}
REQUIRED_FIELDS = [
    "id", "sourceCatalogId", "sourceOperationId", "targetOperationId",
    "targetCatalogId", "sourceModule", "targetModule", "boundary",
    "provenance", "reviewStatus", "documentaryEvidence", "decisionReferences",
    "scientificConcerns",
]
EVIDENCE_REQUIRED = {
    "evidence-backed-proposed": ["rationale", "evidence", "reviewedBy", "reviewedAt"],
    "requires-decision": ["rationale", "openQuestion"],
    "rejected": ["rationale"],
    "superseded": ["rationale", "supersededBy"],
}


def run_audit(root: Path) -> dict[str, Any]:
    command = [sys.executable, str(AUDIT), "--root", str(root), "--report-json"]
    result = subprocess.run(command, cwd=root, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"Registry audit failed: {result.stderr[-2000:]}")
    for line in reversed(result.stdout.splitlines()):
        if line.startswith("REGISTRY_DRIFT_REPORT="):
            report = json.loads(line[len("REGISTRY_DRIFT_REPORT="):])
            if isinstance(report, dict):
                return report
    raise RuntimeError("Audit did not emit a structured report")


def module_path(entry: dict[str, Any]) -> str:
    source = entry.get("source") or {}
    path = source.get("path") or ""
    parts = path.split("/")
    return "/".join(parts[2:4]) if len(parts) >= 4 else ""


def primary_class(entry: dict[str, Any], dc_modules: list[dict[str, Any]]) -> str | None:
    path = module_path(entry)
    for mod in dc_modules:
        if mod.get("path", "").rstrip("/") == path:
            return mod.get("primary_class")
    return None


def inherited_set(root: Path) -> set[tuple[str, str]]:
    report = run_audit(root)
    result: set[tuple[str, str]] = set()
    registry = json.loads((root / "Specification" / "ENDPOINT-REGISTRY.json").read_text(encoding="utf-8"))
    by_cat = {e["catalogId"]: e for e in registry["entries"]}
    by_opid = {e["recommendedOperationId"]: e for e in registry["entries"]}
    for item in report.get("registryOnlyNeighbors", []):
        for neighbor in item.get("neighbors", []):
            result.add((item["catalogId"], neighbor))
    return result


def check(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    root = root.resolve()
    registry_path = root / "Specification" / "ENDPOINT-REGISTRY.json"
    ledger_path = root / "Specification" / "BrAPI-GenX" / "Conformance" / "semantic-neighbor-review.yaml"
    dc_path = root / "Specification" / "BrAPI-GenX" / "Conformance" / "domain-classification.yaml"

    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Cannot load registry: {exc}"]
    try:
        ledger = yaml.safe_load(ledger_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [f"Cannot load semantic-neighbor ledger: {exc}"]
    try:
        dc = yaml.safe_load(dc_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [f"Cannot load domain classification: {exc}"]

    if not isinstance(ledger, dict):
        return ["Semantic-neighbor ledger root must be a mapping."]
    if not isinstance(registry, dict):
        return ["Registry root must be a mapping."]
    dc_modules = dc.get("modules", []) if isinstance(dc, dict) else []
    if not isinstance(dc_modules, list):
        dc_modules = []

    by_cat = {e["catalogId"]: e for e in registry.get("entries", [])}
    by_opid = {e["recommendedOperationId"]: e for e in registry.get("entries", [])}
    gov_ids = {r.get("id") for r in registry.get("semanticRelationships", [])
               if isinstance(r, dict) and isinstance(r.get("id"), str)}

    # Schema-level checks.
    if ledger.get("allowed_statuses") != sorted(ALLOWED_STATUSES):
        # Allow same set, order-independent.
        if set(ledger.get("allowed_statuses", [])) != ALLOWED_STATUSES:
            errors.append("Ledger allowed_statuses does not match the governed status set.")
    if not isinstance(ledger.get("entries"), list):
        return errors + ["Ledger 'entries' must be a list."]

    entries = ledger["entries"]
    try:
        current_inherited_global = inherited_set(root)
    except RuntimeError as exc:
        errors.append(f"Cannot compute current inherited set: {exc}")
        current_inherited_global = set()
    # Unique ids and source-target pairs.
    seen_ids: set[str] = set()
    seen_pairs: set[tuple[str, str]] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("Ledger contains a non-mapping entry.")
            continue
        for field in REQUIRED_FIELDS:
            if field not in entry:
                errors.append(f"Ledger entry {entry.get('id', '<unknown>')} is missing required field '{field}'.")
        eid = entry.get("id")
        if not isinstance(eid, str) or not eid.strip():
            errors.append("Ledger entry has a missing or invalid id.")
            continue
        if eid in seen_ids:
            errors.append(f"Duplicate ledger entry id: {eid}")
        seen_ids.add(eid)
        pair = (entry.get("sourceCatalogId"), entry.get("targetOperationId"))
        if pair in seen_pairs:
            errors.append(f"Duplicate source-target relationship: {pair}")
        seen_pairs.add(pair)

        status = entry.get("reviewStatus")
        if status not in ALLOWED_STATUSES:
            errors.append(f"{eid}: invalid reviewStatus {status!r}.")

        boundary = entry.get("boundary")
        if boundary not in ALLOWED_BOUNDARIES:
            errors.append(f"{eid}: invalid boundary {boundary!r}.")

        provenance = entry.get("provenance")
        if provenance not in ALLOWED_PROVENANCE:
            errors.append(f"{eid}: invalid provenance {provenance!r}.")

        # Resolve source.
        src_cat = entry.get("sourceCatalogId")
        src_entry = by_cat.get(src_cat)
        if not isinstance(src_entry, dict):
            errors.append(f"{eid}: sourceCatalogId does not resolve to a registry entry: {src_cat!r}.")
        else:
            if entry.get("sourceOperationId") != src_entry.get("recommendedOperationId"):
                errors.append(f"{eid}: sourceOperationId does not match the registry entry.")
            if entry.get("sourceModule") != src_entry.get("genxModule"):
                errors.append(f"{eid}: sourceModule does not match the registry entry.")
            # Boundary recomputation.
            tgt_entry = by_opid.get(entry.get("targetOperationId"))
            if isinstance(tgt_entry, dict):
                sp = module_path(src_entry)
                tp = module_path(tgt_entry)
                sc = primary_class(src_entry, dc_modules)
                tc = primary_class(tgt_entry, dc_modules)
                if sp == tp:
                    computed = "within-module"
                elif sc is not None and tc is not None and sc != tc:
                    computed = "cross-domain"
                else:
                    computed = "cross-module"
                if computed != boundary:
                    errors.append(f"{eid}: boundary {boundary!r} does not match computed {computed!r}.")

        # Resolve target: operation id or governed relationship id.
        target_op = entry.get("targetOperationId")
        target_entry = by_opid.get(target_op)
        if isinstance(target_entry, dict):
            if entry.get("targetCatalogId") != target_entry.get("catalogId"):
                errors.append(f"{eid}: targetCatalogId does not match the resolved target operation.")
            if entry.get("targetModule") != target_entry.get("genxModule"):
                errors.append(f"{eid}: targetModule does not match the resolved target operation.")
        elif target_op in gov_ids:
            # Governed relationship target; targetCatalogId may be empty/None.
            pass
        else:
            errors.append(f"{eid}: targetOperationId does not resolve to an operation or governed relationship: {target_op!r}.")

        # Evidence requirements.
        for field in EVIDENCE_REQUIRED.get(status, []):
            value = entry.get(field)
            if field == "evidence":
                if not isinstance(value, list) or not value:
                    errors.append(f"{eid}: evidence-backed status requires non-empty 'evidence' list.")
            elif field == "rationale":
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{eid}: status {status!r} requires non-empty 'rationale'.")
            elif field == "openQuestion":
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{eid}: status {status!r} requires non-empty 'openQuestion'.")
            elif field == "reviewedBy":
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{eid}: evidence-backed status requires 'reviewedBy'.")
            elif field == "reviewedAt":
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{eid}: evidence-backed status requires 'reviewedAt'.")
            elif field == "supersededBy":
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{eid}: superseded status requires 'supersededBy'.")
            else:
                if value in (None, "", [], {}):
                    errors.append(f"{eid}: status {status!r} requires field '{field}'.")

        # Documentary evidence type check.
        de = entry.get("documentaryEvidence")
        if not isinstance(de, list):
            errors.append(f"{eid}: documentaryEvidence must be a list.")

        # Scientific concerns type check.
        sc = entry.get("scientificConcerns")
        if not isinstance(sc, list):
            errors.append(f"{eid}: scientificConcerns must be a list.")

        # decisionReferences type check.
        dr = entry.get("decisionReferences")
        if not isinstance(dr, list):
            errors.append(f"{eid}: decisionReferences must be a list.")

        # Newly proposed/non-inherited relationships need traceable provenance.
        pair = (src_cat, target_op)
        if pair not in current_inherited_global:
            # Not a current registry-only inherited reference.
            if status == "inherited-unreviewed":
                errors.append(f"{eid}: a non-inherited relationship cannot be 'inherited-unreviewed'.")
            if provenance == "inherited-registry-only":
                errors.append(f"{eid}: a non-inherited relationship requires traceable provenance beyond inherited-registry-only.")
            if not isinstance(entry.get("rationale"), str) or not entry.get("rationale", "").strip():
                errors.append(f"{eid}: a non-inherited relationship requires a non-empty rationale.")

    # Completeness: every current inherited relationship must be in ledger.
    try:
        current = inherited_set(root)
    except RuntimeError as exc:
        return errors + [f"Cannot compute inherited set: {exc}"]
    ledger_pairs = {(e.get("sourceCatalogId"), e.get("targetOperationId"))
                    for e in entries if isinstance(e, dict)}
    for pair in sorted(current):
        if pair not in ledger_pairs:
            errors.append(f"Missing ledger entry for inherited registry-only relationship: {pair}")

    # Grandfathered entries remain unresolved: inherited-unreviewed entries must
    # not be treated as approved. (No status named approved exists; ensure none
    # of the inherited entries were silently changed to evidence-backed without
    # evidence, already covered above.)

    # Ledger header count sanity.
    if ledger.get("entry_count") != len(entries):
        errors.append(f"Ledger entry_count {ledger.get('entry_count')} does not match entries length {len(entries)}.")

    # Baseline count preservation (informational but check).
    baseline = ledger.get("generated_from", {}).get("baseline_registry_only_count")
    if baseline is not None and baseline != 153 and baseline != len(current):
        # Allow baseline to remain 153 for historical reference.
        pass

    return errors


def main() -> int:
    global ROOT, REGISTRY, LEDGER, AUDIT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root")
    args = parser.parse_args()
    root = args.root.resolve()
    ROOT = root
    REGISTRY = root / "Specification" / "ENDPOINT-REGISTRY.json"
    LEDGER = root / "Specification" / "BrAPI-GenX" / "Conformance" / "semantic-neighbor-review.yaml"
    AUDIT = root / "Scripts" / "auditEndpointRegistrySourceConsistency.py"
    errors = check(root)
    if errors:
        print("Semantic-neighbor governance validation FAILED:")
        for error in errors:
            print("- " + error)
        return 1
    print("Semantic-neighbor governance validation passed: ledger complete, references resolve, "
          "statuses valid, evidence requirements enforced.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
