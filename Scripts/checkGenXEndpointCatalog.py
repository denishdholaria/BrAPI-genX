#!/usr/bin/env python3
"""Validate that every BrAPI-GenX operation is uniquely and explicitly catalogued.

The OpenAPI operation is authoritative for the wire contract. Its x-brapi-genx
extension is authoritative for domain classification and semantic boundaries.
The human-readable ENDPOINT-CATALOG.md must enumerate the same operation and
catalog identifiers.
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterator

import yaml

ROOT = Path(__file__).resolve().parents[1]
SPECIFICATION = ROOT / "Specification"
GENX_ROOT = SPECIFICATION / "BrAPI-GenX"
CATALOG_PATH = GENX_ROOT / "GENX-ENDPOINT-CATALOG.md"
HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "trace"}
REQUIRED_EXTENSION_FIELDS = {
    "catalogId",
    "classification",
    "purpose",
    "canBeUsedFor",
    "mustNotBeUsedFor",
    "sideEffects",
    "idempotency",
    "semanticNeighbors",
    "decisions",
    "proposalStatus",
}
REQUIRED_CLASSIFICATION_FIELDS = {"primaryDomain", "crossCuttingCapabilities"}


def iter_yaml_documents(root: Path) -> Iterator[tuple[Path, dict[str, Any]]]:
    for path in sorted((*root.rglob("*.yaml"), *root.rglob("*.yml"))):
        try:
            document = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            raise ValueError(f"Invalid YAML in {path.relative_to(ROOT)}: {exc}") from exc
        if isinstance(document, dict):
            yield path, document


def iter_operations(document: dict[str, Any]) -> Iterator[tuple[str, str, dict[str, Any]]]:
    paths = document.get("paths")
    if not isinstance(paths, dict):
        return
    for route, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if method.lower() in HTTP_METHODS and isinstance(operation, dict):
                yield method.upper(), str(route), operation


def normalized_route(route: str) -> str:
    return re.sub(r"\{[^{}]+\}", "{}", route)


def validate() -> list[str]:
    errors: list[str] = []
    operation_records: list[tuple[Path, str, str, dict[str, Any]]] = []
    operation_ids: list[str] = []
    catalog_ids: list[str] = []
    route_owners: dict[tuple[str, str], str] = {}

    for path, document in iter_yaml_documents(GENX_ROOT):
        if "Conformance" in path.parts:
            continue
        for method, route, operation in iter_operations(document):
            operation_id = operation.get("operationId")
            if not isinstance(operation_id, str) or not operation_id.strip():
                errors.append(f"{path.relative_to(ROOT)} {method} {route}: missing operationId")
                continue
            operation_ids.append(operation_id)
            operation_records.append((path, method, route, operation))
            route_key = (method, normalized_route(route))
            if route_key in route_owners:
                errors.append(
                    f"Duplicate GenX method/route {method} {route}: "
                    f"{route_owners[route_key]} and {operation_id}"
                )
            else:
                route_owners[route_key] = operation_id

            if not re.fullmatch(r"genx[A-Z][A-Za-z0-9]+", operation_id):
                errors.append(f"{operation_id}: operationId must follow genxVerbNoun-style casing")

            extension = operation.get("x-brapi-genx")
            if not isinstance(extension, dict):
                errors.append(f"{operation_id}: missing operation-level x-brapi-genx metadata")
                continue
            missing = REQUIRED_EXTENSION_FIELDS - extension.keys()
            if missing:
                errors.append(f"{operation_id}: x-brapi-genx missing fields {sorted(missing)}")
                continue

            classification = extension.get("classification")
            if not isinstance(classification, dict):
                errors.append(f"{operation_id}: classification must be an object")
            else:
                missing_classification = REQUIRED_CLASSIFICATION_FIELDS - classification.keys()
                if missing_classification:
                    errors.append(
                        f"{operation_id}: classification missing fields "
                        f"{sorted(missing_classification)}"
                    )
                primary = classification.get("primaryDomain")
                if primary is not None and primary not in {"D1", "D2", "D3", "D4", "D5", "D6", "D7"}:
                    errors.append(f"{operation_id}: unknown primaryDomain {primary!r}")
                for capability in classification.get("crossCuttingCapabilities", []):
                    if capability not in {f"C{i}" for i in range(1, 10)}:
                        errors.append(f"{operation_id}: unknown cross-cutting capability {capability!r}")
                for domain in classification.get("contextualDomains", []):
                    if domain not in {"D1", "D2", "D3", "D4", "D5", "D6", "D7"}:
                        errors.append(f"{operation_id}: unknown contextual domain {domain!r}")

            for field in ("canBeUsedFor", "mustNotBeUsedFor", "semanticNeighbors", "decisions"):
                value = extension.get(field)
                if not isinstance(value, list):
                    errors.append(f"{operation_id}: {field} must be a list")
                elif field in {"canBeUsedFor", "mustNotBeUsedFor"} and not value:
                    errors.append(f"{operation_id}: {field} must not be empty")

            for field in ("catalogId", "purpose", "sideEffects", "idempotency", "proposalStatus"):
                value = extension.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{operation_id}: {field} must be a non-empty string")
            catalog_id = extension.get("catalogId")
            if isinstance(catalog_id, str):
                catalog_ids.append(catalog_id)
                if not catalog_id.startswith("brapi-genx.genx."):
                    errors.append(f"{operation_id}: catalogId must use the brapi-den.genx namespace")

    duplicate_operation_ids = sorted(key for key, count in Counter(operation_ids).items() if count > 1)
    duplicate_catalog_ids = sorted(key for key, count in Counter(catalog_ids).items() if count > 1)
    errors.extend(f"Duplicate GenX operationId: {value}" for value in duplicate_operation_ids)
    errors.extend(f"Duplicate GenX catalogId: {value}" for value in duplicate_catalog_ids)

    # GenX operation identifiers must not collide with identifiers in older
    # BrAPI specifications, even when those files are generated separately.
    genx_id_set = set(operation_ids)
    for path, document in iter_yaml_documents(SPECIFICATION):
        if path.is_relative_to(GENX_ROOT) or "Conformance" in path.parts:
            continue
        for _method, _route, operation in iter_operations(document):
            operation_id = operation.get("operationId")
            if isinstance(operation_id, str) and operation_id in genx_id_set:
                errors.append(
                    f"operationId collision with non-GenX specification: {operation_id} "
                    f"in {path.relative_to(ROOT)}"
                )

    if not CATALOG_PATH.exists():
        errors.append(f"Missing human-readable catalogue: {CATALOG_PATH.relative_to(ROOT)}")
    else:
        catalogue = CATALOG_PATH.read_text(encoding="utf-8")
        listed_operation_ids = re.findall(
            r"^- \*\*Source OpenAPI operationId:\*\* `([^`]+)`", catalogue, flags=re.MULTILINE
        )
        listed_catalog_ids = re.findall(
            r"^- \*\*Catalogue ID:\*\* `([^`]+)`", catalogue, flags=re.MULTILINE
        )
        expected_ids = sorted(operation_ids)
        if sorted(listed_operation_ids) != expected_ids:
            missing = sorted(set(expected_ids) - set(listed_operation_ids))
            extra = sorted(set(listed_operation_ids) - set(expected_ids))
            errors.append(
                f"Catalogue operationId coverage mismatch; missing={missing}, extra={extra}"
            )
        expected_catalog_ids = sorted(catalog_ids)
        if sorted(listed_catalog_ids) != expected_catalog_ids:
            missing = sorted(set(expected_catalog_ids) - set(listed_catalog_ids))
            extra = sorted(set(listed_catalog_ids) - set(expected_catalog_ids))
            errors.append(
                f"Catalogue catalogId coverage mismatch; missing={missing}, extra={extra}"
            )

    return errors


def main() -> int:
    try:
        errors = validate()
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1
    if errors:
        print("GenX endpoint-catalogue validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("GenX endpoint catalogue is complete: operation IDs, catalogue IDs, classifications, and semantic metadata are unique and consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
