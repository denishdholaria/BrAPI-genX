#!/usr/bin/env python3
"""Audit descriptive registry metadata against its authoritative GenX OpenAPI operations.

The registry remains authoritative for catalogue IDs, crosswalk metadata, and
implementation evidence. Source OpenAPI operation summaries/descriptions and
x-brapi-genx descriptive metadata are treated as the source of truth for the
fields compared here.

This audit is initially report-only. Pass --strict after existing drift has
been reconciled to make any mismatch fail the command.
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


def audit(strict: bool) -> int:
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
        for field in FIELD_MAP:
            expected = source_value(operation, entry, field)
            actual = entry.get(field)

            if field == "sourceDescription":
                # Registry descriptions may flatten YAML block-scalar newlines.
                # Compare semantic text, not formatting-only whitespace.
                if isinstance(expected, str):
                    expected = " ".join(expected.split())
                if isinstance(actual, str):
                    actual = " ".join(actual.split())

            if field == "semanticNeighborIds":
                # The registry may add explicitly governed relationship IDs
                # (for example SEM-*), beyond operation-level neighbors in YAML.
                actual = [value for value in (actual or []) if value not in relationship_ids]
                expected = expected or []

            if expected != actual:
                mismatches.append({
                    "catalogId": entry.get("catalogId"),
                    "module": entry.get("genxModule") or "Unclassified",
                    "field": field,
                    "registry": actual,
                    "source": expected,
                })

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

    if errors:
        print("Source errors (first 20):")
        for error in errors[:20]:
            print(f"  - {error}")

    if mismatches:
        print("Mismatch samples (first 20; source YAML is shown as the expected value):")
        for item in mismatches[:20]:
            registry_value = repr(item["registry"])
            source_value_text = repr(item["source"])
            if len(registry_value) > 180:
                registry_value = registry_value[:177] + "..."
            if len(source_value_text) > 180:
                source_value_text = source_value_text[:177] + "..."
            print(
                f"  - {item['catalogId']} [{item['field']}] "
                f"registry={registry_value}; source={source_value_text}"
            )

    if strict and (errors or mismatches):
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="return a failure status when source/registry drift is found",
    )
    args = parser.parse_args()
    try:
        return audit(strict=args.strict)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Cannot audit the endpoint registry: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
