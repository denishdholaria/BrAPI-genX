#!/usr/bin/env python3
"""Check proposed GenX module classification against its human-readable mapping.

This validates classification identities, not the scientific correctness of an
unratified taxonomy. The YAML registry is authoritative for module assignments.
"""
from __future__ import annotations

import re
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
GENX_PATH = PurePosixPath("Specification/BrAPI-GenX")
GENX_ROOT = ROOT / GENX_PATH
CLASSIFICATION = GENX_ROOT / "Conformance/domain-classification.yaml"
DOCUMENT = GENX_ROOT / "CLASSIFICATION.md"
SUPPORT_DIRECTORIES = {"Conformance", "Inventory", "RFCs"}


def classification_errors(
    registry: dict[str, Any],
    document: str,
    endpoint_entries: list[dict[str, Any]],
    *,
    genx_root: Path | None = None,
) -> list[str]:
    """Return actionable errors; never auto-assign an unclassified module."""
    errors: list[str] = []
    domains = registry.get("domain_classes")
    capabilities = registry.get("cross_cutting_capabilities")
    modules = registry.get("modules")
    sections = registry.get("sections")
    if not isinstance(domains, dict) or not isinstance(capabilities, dict) or not isinstance(modules, list):
        return ["Classification registry requires domain_classes, cross_cutting_capabilities, and modules."]
    if not isinstance(sections, dict) or not sections or any(
        not isinstance(name, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", name)
        or name in SUPPORT_DIRECTORIES
        for name in sections
    ):
        return ["Classification registry requires valid, named specification sections."]

    by_module: dict[str, dict[str, Any]] = {}
    registered_paths: set[str] = set()
    for index, module in enumerate(modules, start=1):
        if not isinstance(module, dict):
            errors.append(f"Registry module #{index} is not an object.")
            continue
        path = module.get("path")
        if not isinstance(path, str) or not re.fullmatch(r"(?:[A-Za-z][A-Za-z0-9]*/){1,2}", path):
            errors.append(f"Registry module #{index} has an invalid path: {path!r}.")
            continue
        parts = PurePosixPath(path).parts
        if path != "Conformance/" and (len(parts) != 2 or parts[0] not in sections):
            errors.append(f"Registry module {path} must be under a declared specification section.")
            continue
        registered_paths.add(path)
        name = parts[-1]
        if name in by_module:
            errors.append(f"Duplicate registry classification for {path}.")
        by_module[name] = module
        primary = module.get("primary_class")
        facets = module.get("cross_cutting")
        if primary is not None and primary not in domains:
            errors.append(f"Registry {path} has unknown domain {primary!r}.")
        if not isinstance(facets, list) or not facets:
            errors.append(f"Registry {path} requires non-empty cross_cutting facets.")
        else:
            if len(facets) != len(set(facets)):
                errors.append(f"Registry {path} repeats cross-cutting facets.")
            for facet in facets:
                if facet not in capabilities:
                    errors.append(f"Registry {path} has unknown facet {facet!r}.")

    if genx_root is not None:
        errors.extend(layout_errors(genx_root, sections, registered_paths))

    section = document.split("## 4. Mapping current GenX modules", 1)
    if len(section) != 2 or "## 5." not in section[1]:
        return errors + ["CLASSIFICATION.md is missing the bounded module mapping table."]
    table = section[1].split("## 5.", 1)[0]
    seen: dict[str, int] = {}
    for lineno, line in enumerate(table.splitlines(), start=1):
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(cells) != 4 or cells[0] == "Current module/object":
            continue
        name = cells[0].split(" / ", 1)[0].strip()
        if name in seen:
            errors.append(f"CLASSIFICATION.md duplicates module {name} (mapping rows {seen[name]} and {lineno}).")
        seen[name] = lineno
        module = by_module.get(name)
        if module is None:
            errors.append(f"CLASSIFICATION.md names unknown module {name}.")
            continue
        primary_label = cells[1]
        primary: str | None = None
        implied_facets: set[str] = set()
        if re.fullmatch(r"D\d+", primary_label):
            primary = primary_label
        elif primary_label == "(none, cross-cutting)":
            pass
        elif re.fullmatch(r"Cross-cutting C\d+", primary_label):
            implied_facets.add(primary_label.split()[-1])
        elif re.fullmatch(r"No standalone domain class; C\d+", primary_label):
            implied_facets.add(primary_label.split()[-1])
        elif primary_label.startswith("Context-dependent:"):
            # The current telemetry proposal intentionally has no one primary
            # domain; mentioned D-codes describe contextual alternatives.
            for domain in re.findall(r"\bD\d+\b", primary_label):
                if domain not in domains:
                    errors.append(f"CLASSIFICATION.md {name} references unknown contextual domain {domain}.")
        else:
            errors.append(f"CLASSIFICATION.md {name} has unrecognized primary classification {primary_label!r}.")
            continue
        if primary is not None and primary not in domains:
            errors.append(f"CLASSIFICATION.md {name} uses unknown domain {primary}.")
        if primary != module.get("primary_class"):
            errors.append(f"Primary classification disagrees for {name}: document={primary!r}, registry={module.get('primary_class')!r}.")
        documented_facets = {part.strip() for part in cells[2].split(",") if part.strip()}
        all_facets = documented_facets | implied_facets
        for facet in all_facets:
            if facet not in capabilities:
                errors.append(f"CLASSIFICATION.md {name} uses unknown facet {facet!r}.")
        expected_facets = module.get("cross_cutting")
        if isinstance(expected_facets, list) and all_facets != set(expected_facets):
            errors.append(f"Cross-cutting facets disagree for {name}: document={sorted(all_facets)}, registry={sorted(expected_facets)}.")

    for name in sorted(by_module.keys() - seen.keys()):
        errors.append(f"CLASSIFICATION.md omits registry module {name}.")
    for entry in endpoint_entries:
        if entry.get("apiGeneration") != "genx-v1":
            continue
        name = entry.get("genxModule")
        module = by_module.get(name)
        if module is None:
            errors.append(f"Endpoint {entry.get('catalogId')} references unknown classification module {name!r}.")
            continue
        if (entry.get("classification") or {}).get("primaryDomain") != module.get("primary_class"):
            errors.append(f"Endpoint {entry.get('catalogId')} primaryDomain differs from module {name} classification.")
        source = entry.get("source")
        source_path = source.get("path") if isinstance(source, dict) else None
        module_path = GENX_PATH / module["path"]
        if (
            not isinstance(source_path, str)
            or ".." in PurePosixPath(source_path).parts
            or not PurePosixPath(source_path).is_relative_to(module_path)
        ):
            errors.append(f"Endpoint {entry.get('catalogId')} source must be under {module_path}/.")
    return errors


def layout_errors(
    root: Path, sections: dict[str, Any], registered_paths: set[str],
) -> list[str]:
    errors = []
    expected_top_level = set(sections) | SUPPORT_DIRECTORIES
    for child in sorted(root.iterdir()):
        if child.is_dir() and child.name not in expected_top_level:
            errors.append(f"Unexpected top-level GenX directory {child.name}/.")
        elif child.is_file() and child.name.startswith("RFC-") and child.suffix == ".md":
            errors.append(f"Place numbered RFC {child.name} in RFCs/.")
    for section in sections:
        section_path = root / section
        if not (section_path / "README.md").is_file():
            errors.append(f"Specification section {section}/ requires a README.md.")
            continue
        for child in sorted(section_path.iterdir()):
            if child.is_dir() and f"{section}/{child.name}/" not in registered_paths:
                errors.append(f"Unregistered specification module {section}/{child.name}/.")
    for path in sorted(registered_paths):
        if not (root / path / "README.md").is_file():
            errors.append(f"Registered module {path} is missing its README.md.")
    return errors


def check_classification(endpoint_entries: list[dict[str, Any]]) -> list[str]:
    try:
        registry = yaml.safe_load(CLASSIFICATION.read_text(encoding="utf-8"))
        document = DOCUMENT.read_text(encoding="utf-8")
    except (OSError, yaml.YAMLError) as exc:
        return [f"Cannot load classification documents: {exc}"]
    if not isinstance(registry, dict):
        return ["Classification registry must be a YAML mapping."]
    return classification_errors(registry, document, endpoint_entries, genx_root=GENX_ROOT)
