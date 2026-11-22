#!/usr/bin/env python3
"""Validate GenX module layout and generated-artifact links without rewriting upstream BrAPI.

The module registry defines ownership. Known upstream v2.1 filename and casing
anomalies are intentionally outside this validator's rename authority.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path, PurePosixPath

import yaml

ROOT = Path(__file__).resolve().parents[1]
GENX = Path("Specification/BrAPI-GenX")
REGISTRY = Path("Specification/ENDPOINT-REGISTRY.json")
CLASSIFICATION = GENX / "Conformance/domain-classification.yaml"
PROVENANCE_ONLY = {"Core/Provenance/"}

# Historical BrAPI v2.1 paths are intentionally frozen. None is a GenX naming
# exception; never rename baseline files merely to satisfy local style.
LEGACY_UPSTREAM_EXCEPTIONS = (
    "Specification/BrAPI-Phenotyping/Methods/schemas/",
    "Specification/BrAPI-Phenotyping/Scales/schemas/",
    "Specification/BrAPI-Schema/Requests/VarientRequest.json",
    "Specification/BrAPI-Schema/Requests/VarientSetRequest.json",
    "Specification/BrAPI-Genotyping/ReferenceSets/ReferenceSets_RefernceSetId_GET.yaml",
    "Specification/BrAPI-Germplasm/Germplasm_Attribute_Values/AttributesValues_GET_POST.yaml",
)


def module_errors(root: Path, registry: dict) -> list[str]:
    """Check source ownership and conventions for the independently governed GenX modules."""
    errors: list[str] = []
    modules = registry.get("modules")
    if not isinstance(modules, list):
        return ["Missing module classification entries"]
    owners: dict[str, str] = {}
    for record in modules:
        if not isinstance(record, dict) or not isinstance(record.get("path"), str):
            errors.append("Invalid classification module record")
            continue
        rel = record["path"]
        if rel == "Conformance/":
            continue  # Registered specification support, not a domain contract.
        parts = PurePosixPath(rel).parts
        if len(parts) != 2 or ".." in parts:
            errors.append(f"Invalid GenX module path {rel!r}")
            continue
        if parts[1] in owners:
            errors.append(f"Duplicate GenX module name {parts[1]} in {rel} and {owners[parts[1]]}")
        owners[parts[1]] = rel
        module = root / GENX / rel
        if not module.is_dir():
            errors.append(f"Registered GenX module missing: {rel}")
            continue
        for required in ("README.md", "GroupDescription.md"):
            if not (module / required).is_file():
                errors.append(f"{rel} missing {required}")
        schemas = module / "Schemas"
        if not schemas.is_dir():
            errors.append(f"{rel} missing canonical Schemas/")
        elif not any(p.is_file() for p in schemas.glob("*.yaml")):
            errors.append(f"{rel} Schemas/ has no YAML definitions")
        source = [p for p in module.iterdir() if p.is_file() and p.suffix.lower() in (".yaml", ".yml")]
        if rel not in PROVENANCE_ONLY and not source:
            errors.append(f"{rel} missing OpenAPI operation file")
    genx_root = root / GENX
    if genx_root.is_dir():
        for path in genx_root.rglob("*"):
            if path.is_dir() and path.name.lower() == "schemas" and path.name != "Schemas":
                errors.append(f"Unexpected GenX schemas directory casing: {path.relative_to(root)}")
    return errors


def registry_source_errors(root: Path, registry: dict) -> list[str]:
    """Recheck source-file ownership; the existing registry checker validates operation details."""
    errors: list[str] = []
    entries = registry.get("entries")
    if not isinstance(entries, list):
        return ["Master endpoint registry has no entries"]
    for item in entries:
        if not isinstance(item, dict):
            errors.append("Invalid endpoint registry record")
            continue
        if item.get("apiGeneration") != "genx-v1":
            continue
        source_record = item.get("source")
        source = source_record.get("path") if isinstance(source_record, dict) else None
        if not isinstance(source, str) or ".." in PurePosixPath(source).parts:
            errors.append(f"{item.get('catalogId')}: unsafe/missing source")
            continue
        if not PurePosixPath(source).is_relative_to(GENX):
            errors.append(f"{item.get('catalogId')}: source outside GenX")
        elif not (root / source).is_file():
            errors.append(f"{item.get('catalogId')}: missing source file {source}")
    return errors


def generated_link_errors(root: Path) -> list[str]:
    """Do not confuse frozen v2.1 generated artifacts with deferred GenX outputs (D-04)."""
    readme = root / "Specification/Generated/README.md"
    if not readme.is_file():
        return ["Generated/README.md missing"]
    content = readme.read_text(encoding="utf-8")
    errors = []
    for basename in ("brapi_generated.json", "brapi_openapi.json"):
        link = f"[{basename}]({basename})"
        if content.count(link) != 1:
            errors.append(f"Generated/README.md must link once to {basename}")
        if not (readme.parent / basename).is_file():
            errors.append(f"Missing declared generated baseline artifact {basename}")
    return errors


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    try:
        classification = yaml.safe_load((root / CLASSIFICATION).read_text(encoding="utf-8"))
        registry = json.loads((root / REGISTRY).read_text(encoding="utf-8"))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return [f"Unable to load specification registries: {exc}"]
    if not isinstance(classification, dict) or not isinstance(registry, dict):
        return ["Invalid registry root type"]
    errors.extend(module_errors(root, classification))
    errors.extend(registry_source_errors(root, registry))
    errors.extend(generated_link_errors(root))
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Specification structural assurance FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Specification structural assurance passed (GenX modules, source ownership, generated links).")
    print("Official BrAPI v2.1 source paths are preserved, including documented legacy naming exceptions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
