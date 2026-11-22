#!/usr/bin/env python3
"""Audit descriptive registry metadata against its authoritative GenX OpenAPI operations.

The registry remains authoritative for catalogue IDs, crosswalk metadata, and
implementation evidence. Source OpenAPI operation summaries/descriptions and
x-brapi-genx descriptive metadata are treated as the source of truth for the
fields compared here.

The default command is report-only. Pass --strict to reject source/registry
disagreements and invalid references while permitting verified additional
registry-only relationships. The baseline regression gate separately rejects
new unreviewed additional relationships. --report-json emits the complete
deterministic discrepancy set; reference validation does not establish scientific
equivalence or interoperability.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "Specification" / "ENDPOINT-REGISTRY.json"

# Deliberately allowed human-readable labels for the frozen BrAPI v2.1
# baseline; a generic "V2.1 " prefix must not bypass referential validation.
LEGACY_V21_NEIGHBOR_LABELS = frozenset({
    "V2.1 GET /brapi/v2/serverinfo",
    "V2.1 /brapi/v2/variables",
    "V2.1 OntologyTerm schema",
})

FIELD_MAP = {
    "operationName": ("summary", None),
    "sourceDescription": ("description", None),
    "canBeUsedFor": ("x-brapi-genx", "canBeUsedFor"),
    "mustNotBeUsedFor": ("x-brapi-genx", "mustNotBeUsedFor"),
    "semanticNeighborIds": ("x-brapi-genx", "semanticNeighbors"),
    "decisionReferences": ("x-brapi-genx", "decisions"),
}


def load_registry() -> dict[str, Any]:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def load_source_documents(entries: list[dict[str, Any]]) -> tuple[dict[str, Any], list[str]]:
    documents: dict[str, Any] = {}
    errors: list[str] = []
    for entry in entries:
        source = entry.get("source") or {}
        source_path = source.get("path")
        if not isinstance(source_path, str) or not source_path:
            errors.append(f"{entry.get('catalogId')}: missing source.path")
            continue
        if source_path in documents:
            continue
        path = ROOT / source_path
        if not path.is_file():
            errors.append(f"{entry.get('catalogId')}: source file does not exist: {source_path}")
            continue
        try:
            documents[source_path] = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{entry.get('catalogId')}: cannot parse {source_path}: {exc}")
    return documents, errors


def source_value(operation: dict[str, Any], entry: dict[str, Any], field: str) -> Any:
    source_key, extension_key = FIELD_MAP[field]
    if extension_key is None:
        return operation.get(source_key)
    extension = operation.get(source_key)
    if not isinstance(extension, dict):
        return None
    return extension.get(extension_key)


def audit(strict: bool, plan_json: bool, report_json: bool = False) -> int:
    registry = load_registry()
    entries = [e for e in registry.get("entries", []) if e.get("apiGeneration") == "genx-v1"]
    documents, errors = load_source_documents(entries)
    mismatches: list[dict[str, Any]] = []
    examined = 0
    relationship_ids = {
        relation.get("id")
        for relation in registry.get("semanticRelationships", [])
        if isinstance(relation, dict) and isinstance(relation.get("id"), str)
    }
    sync_plan: dict[str, dict[str, Any]] = {}
    registry_only_neighbors: list[dict[str, Any]] = []

    for entry in entries:
        source = entry.get("source") or {}
        source_path = source.get("path")
        document = documents.get(source_path)
        if not isinstance(document, dict):
            continue
        path_item = (document.get("paths") or {}).get(entry.get("path"))
        method = str(entry.get("method", "")).lower()
        operation = path_item.get(method) if isinstance(path_item, dict) else None
        if not isinstance(operation, dict):
            errors.append(
                f"{entry.get('catalogId')}: no source operation for "
                f"{method.upper()} {entry.get('path')} in {source_path}"
            )
            continue

        examined += 1
        catalog_id = entry.get("catalogId")
        sync_fields = sync_plan.setdefault(catalog_id, {})

        for field in FIELD_MAP:
            expected = source_value(operation, entry, field)
            actual = entry.get(field)

            if field == "sourceDescription":
                # Registry descriptions may flatten YAML block-scalar newlines.
                # Compare and store semantic text, not formatting-only whitespace.
                if isinstance(expected, str):
                    expected = " ".join(expected.split())
                if isinstance(actual, str):
                    actual = " ".join(actual.split())

            if field == "semanticNeighborIds":
                # Source-declared operation neighbours must be present. Keep
                # additional registry links (including governed SEM-* links)
                # until they receive their own explicit semantic review.
                source_neighbors = list(expected or [])
                registry_neighbors = list(actual or [])

                # Validate registry-declared references: malformed, duplicate,
                # unknown governed relationships and dangling operation ids are
                # hard errors. Additional (registry-only) relationships are
                # still reported separately; they pass only when verified.
                seen_registry: set[str] = set()
                for ref in registry_neighbors:
                    if not isinstance(ref, str) or not ref.strip():
                        errors.append(
                            f"{catalog_id}: malformed semanticNeighborIds entry {ref!r}"
                        )
                        continue
                    if ref in seen_registry:
                        errors.append(
                            f"{catalog_id}: duplicate semanticNeighborIds entry {ref}"
                        )
                        continue
                    seen_registry.add(ref)
                    if ref.startswith(("SEM-", "OVERLAP-")):
                        if ref not in relationship_ids:
                            errors.append(
                                f"{catalog_id}: unknown governed semantic relationship {ref}"
                            )
                    elif ref.startswith("V2.1 "):
                        if ref not in LEGACY_V21_NEIGHBOR_LABELS:
                            errors.append(f"{catalog_id}: unregistered historical BrAPI v2.1 label {ref}")
                    else:
                        genx_operation_ids = {
                            item.get("recommendedOperationId")
                            for item in entries
                            if item.get("apiGeneration") == "genx-v1"
                        }
                        v21_operation_ids = {
                            item.get("recommendedOperationId")
                            for item in entries
                            if item.get("apiGeneration") == "brapi-v2.1"
                        }
                        if ref not in genx_operation_ids and ref not in v21_operation_ids:
                            errors.append(
                                f"{catalog_id}: dangling semantic neighbor reference {ref}"
                            )

                # Validate source-declared references similarly.
                seen_source: set[str] = set()
                for ref in source_neighbors:
                    if not isinstance(ref, str) or not ref.strip():
                        errors.append(
                            f"{catalog_id}: malformed source semanticNeighbors entry {ref!r}"
                        )
                        continue
                    if ref in seen_source:
                        errors.append(
                            f"{catalog_id}: duplicate source semanticNeighbors entry {ref}"
                        )
                        continue
                    seen_source.add(ref)
                    if ref.startswith(("SEM-", "OVERLAP-")):
                        if ref not in relationship_ids:
                            errors.append(
                                f"{catalog_id}: unknown governed semantic relationship {ref} in source"
                            )
                    elif ref.startswith("V2.1 "):
                        if ref not in LEGACY_V21_NEIGHBOR_LABELS:
                            errors.append(f"{catalog_id}: unregistered historical BrAPI v2.1 source label {ref}")
                    else:
                        genx_operation_ids = {
                            item.get("recommendedOperationId")
                            for item in entries
                            if item.get("apiGeneration") == "genx-v1"
                        }
                        v21_operation_ids = {
                            item.get("recommendedOperationId")
                            for item in entries
                            if item.get("apiGeneration") == "brapi-v2.1"
                        }
                        if ref not in genx_operation_ids and ref not in v21_operation_ids:
                            errors.append(
                                f"{catalog_id}: dangling source semantic neighbor reference {ref}"
                            )

                source_operation_neighbors = [
                    value for value in source_neighbors if value not in relationship_ids
                ]
                registry_operation_neighbors = [
                    value for value in registry_neighbors if value not in relationship_ids
                ]
                # All source-declared relationships, including governed
                # SEM-/OVERLAP- identifiers, must be mirrored in the registry.
                missing = [
                    value for value in source_neighbors
                    if value not in registry_neighbors
                ]
                extra = [
                    value for value in registry_operation_neighbors
                    if value not in source_operation_neighbors
                ]
                if missing:
                    mismatches.append({
                        "catalogId": catalog_id,
                        "module": entry.get("genxModule") or "Unclassified",
                        "field": field,
                        "registry": registry_neighbors,
                        "source": source_operation_neighbors,
                        "missing": missing,
                    })
                if extra:
                    registry_only_neighbors.append({
                        "catalogId": catalog_id,
                        "module": entry.get("genxModule") or "Unclassified",
                        "neighbors": extra,
                    })
                continue

            if expected != actual:
                mismatches.append({
                    "catalogId": catalog_id,
                    "module": entry.get("genxModule") or "Unclassified",
                    "field": field,
                    "registry": actual,
                    "source": expected,
                })
                if expected is not None:
                    sync_fields[field] = expected

        if not sync_fields:
            sync_plan.pop(catalog_id, None)

    counts = Counter(item["field"] for item in mismatches)
    modules: dict[str, set[str]] = defaultdict(set)
    for item in mismatches:
        modules[item["field"]].add(item["module"])

    print("GenX registry/source descriptive-metadata audit")
    print(f"Registry entries: {len(entries)}")
    print(f"Source operations examined: {examined}")
    print(f"Source loading/lookup errors: {len(errors)}")
    print(f"Field mismatches: {len(mismatches)}")

    if counts:
        print("Mismatch counts by field:")
        for field in FIELD_MAP:
            if counts[field]:
                print(
                    f"  {field}: {counts[field]} operation(s) across "
                    f"{len(modules[field])} module(s)"
                )
    else:
        print("All audited descriptive fields match their source OpenAPI operations.")

    if registry_only_neighbors:
        by_module = defaultdict(int)
        for item in registry_only_neighbors:
            by_module[item["module"]] += len(item["neighbors"])
        print(
            f"Registry-only operation-neighbor references: "
            f"{sum(len(item['neighbors']) for item in registry_only_neighbors)} "
            f"across {len(registry_only_neighbors)} operations and {len(by_module)} modules"
        )

    if errors:
        print("Source errors (first 20):")
        for error in errors[:20]:
            print(f"  - {error}")

    if mismatches:
        print("Mismatch samples (up to 4 per field; source YAML is the expected value):")
        for field in FIELD_MAP:
            samples = [item for item in mismatches if item["field"] == field][:4]
            for item in samples:
                registry_value = repr(item.get("registry"))
                source_value_text = repr(item.get("source"))
                if len(registry_value) > 180:
                    registry_value = registry_value[:177] + "..."
                if len(source_value_text) > 180:
                    source_value_text = source_value_text[:177] + "..."
                detail = f"; missing={item['missing']!r}" if item.get("missing") else ""
                print(
                    f"  - {item['catalogId']} [{field}] "
                    f"registry={registry_value}; source={source_value_text}{detail}"
                )

    if plan_json:
        plan = [
            {"catalogId": catalog_id, "fields": fields}
            for catalog_id, fields in sorted(sync_plan.items())
        ]
        print("REGISTRY_SOURCE_SYNC_PLAN=" + json.dumps(plan, separators=(",", ":")))

    if report_json:
        print("REGISTRY_DRIFT_REPORT=" + json.dumps({
            "errors": errors,
            "mismatches": mismatches,
            "registryOnlyNeighbors": registry_only_neighbors,
            "sourceOperationsExamined": examined,
        }, sort_keys=True, separators=(",", ":")))

    if strict and (errors or mismatches):
        return 1
    return 0


def main() -> int:
    global ROOT, REGISTRY
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="return a failure status when source/registry drift is found",
    )
    parser.add_argument(
        "--plan-json",
        action="store_true",
        help="emit a machine-readable metadata reconciliation plan",
    )
    parser.add_argument(
        "--report-json",
        action="store_true",
        help="emit complete machine-readable discrepancies for deterministic review",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="repository checkout to audit (defaults to this script's checkout)",
    )
    args = parser.parse_args()
    ROOT = args.root.resolve()
    REGISTRY = ROOT / "Specification/ENDPOINT-REGISTRY.json"
    try:
        return audit(strict=args.strict, plan_json=args.plan_json, report_json=args.report_json)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Cannot audit the endpoint registry: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
