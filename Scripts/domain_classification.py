#!/usr/bin/env python3
"""Check proposed GenX module classification against its human-readable mapping.

This validates classification identities, not the scientific correctness of an
unratified taxonomy. The YAML registry is authoritative for module assignments.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CLASSIFICATION = ROOT / "Specification/BrAPI-GenX/Conformance/domain-classification.yaml"
DOCUMENT = ROOT / "Specification/BrAPI-GenX/CLASSIFICATION.md"


def classification_errors(
    registry: dict[str, Any],
    document: str,
    endpoint_entries: list[dict[str, Any]],
) -> list[str]:
    """Return actionable errors; never auto-assign an unclassified module."""
    errors: list[str] = []
    domains = registry.get("domain_classes")
    capabilities = registry.get("cross_cutting_capabilities")
    modules = registry.get("modules")
    if not isinstance(domains, dict) or not isinstance(capabilities, dict) or not isinstance(modules, list):
        return ["Classification registry requires domain_classes, cross_cutting_capabilities, and modules."]

    by_module: dict[str, dict[str, Any]] = {}
    for index, module in enumerate(modules, start=1):
        if not isinstance(module, dict):
            errors.append(f"Registry module #{index} is not an object.")
            continue
        path = module.get("path")
        if not isinstance(path, str) or not path.endswith("/") or not path[:-1]:
            errors.append(f"Registry module #{index} has an invalid path: {path!r}.")
            continue
        name = path[:-1]
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
        elif (entry.get("classification") or {}).get("primaryDomain") != module.get("primary_class"):
            errors.append(f"Endpoint {entry.get('catalogId')} primaryDomain differs from module {name} classification.")
    return errors


def check_classification(endpoint_entries: list[dict[str, Any]]) -> list[str]:
    try:
        registry = yaml.safe_load(CLASSIFICATION.read_text(encoding="utf-8"))
        document = DOCUMENT.read_text(encoding="utf-8")
    except (OSError, yaml.YAMLError) as exc:
        return [f"Cannot load classification documents: {exc}"]
    if not isinstance(registry, dict):
        return ["Classification registry must be a YAML mapping."]
    return classification_errors(registry, document, endpoint_entries)
