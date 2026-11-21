#!/usr/bin/env python3
"""Mutation-based regression tests for domain classification reconciliation."""
from __future__ import annotations

import copy
from pathlib import Path
import tempfile
import unittest

from domain_classification import classification_errors

REGISTRY = {
    "sections": {"Breeding": "Breeding", "Core": "Core", "Instrumentation": "Instrumentation"},
    "domain_classes": {"D2": {"name": "Breeding"}, "D4": {"name": "Phenotyping"}},
    "cross_cutting_capabilities": {"C1": "Identity", "C7": "Telemetry"},
    "modules": [
        {"path": "Breeding/BreedingPipeline/", "primary_class": "D2", "cross_cutting": ["C1"]},
        {"path": "Core/ServerInfoV3/", "primary_class": None, "cross_cutting": ["C1"]},
        {"path": "Instrumentation/Telemetry/", "primary_class": None, "cross_cutting": ["C1", "C7"]},
    ],
}
DOCUMENT = """# Classification
## 4. Mapping current GenX modules
| Current module/object | Primary classification | Cross-cutting facets | Important boundary |
|---|---|---|---|
| BreedingPipeline / BreedingPipeline | D2 | C1 | Breeding contract |
| ServerInfoV3 | Cross-cutting C1 | | Server metadata |
| Telemetry / TelemetryPoint | Context-dependent: D4 | C1, C7 | Context-specific |
## 5. Relationship to published standard
"""
ENDPOINTS = [{"apiGeneration": "genx-v1", "genxModule": "BreedingPipeline",
              "catalogId": "pipeline.get", "classification": {"primaryDomain": "D2"},
              "source": {"path": "Specification/BrAPI-GenX/Breeding/BreedingPipeline/Pipeline.yaml"}}]


class ClassificationRegression(unittest.TestCase):
    def audit(self, registry=None, document=None, endpoints=None, *, genx_root=None):
        return classification_errors(registry if registry is not None else copy.deepcopy(REGISTRY),
                                     document if document is not None else DOCUMENT,
                                     endpoints if endpoints is not None else copy.deepcopy(ENDPOINTS),
                                     genx_root=genx_root)

    def test_valid_scientific_and_cross_cutting_entries(self):
        self.assertEqual([], self.audit())

    def test_duplicate_document_row_is_rejected(self):
        row = "| BreedingPipeline / BreedingPipeline | D2 | C1 | Breeding contract |"
        errors = self.audit(document=DOCUMENT.replace(row, row + "\n" + row))
        self.assertTrue(any("duplicates module BreedingPipeline" in error for error in errors), errors)

    def test_conflicting_primary_class_is_rejected(self):
        errors = self.audit(document=DOCUMENT.replace("| D2 | C1 |", "| D4 | C1 |"))
        self.assertTrue(any("Primary classification disagrees" in error for error in errors), errors)

    def test_unknown_domain_and_facet_are_rejected(self):
        errors = self.audit(document=DOCUMENT.replace("| D2 | C1 |", "| D99 | C99 |"))
        self.assertTrue(any("unknown domain D99" in error for error in errors), errors)
        self.assertTrue(any("unknown facet 'C99'" in error for error in errors), errors)

    def test_missing_document_module_is_rejected(self):
        row = "| BreedingPipeline / BreedingPipeline | D2 | C1 | Breeding contract |\n"
        errors = self.audit(document=DOCUMENT.replace(row, ""))
        self.assertTrue(any("omits registry module BreedingPipeline" in error for error in errors), errors)

    def test_operation_primary_domain_drift_is_rejected(self):
        entries = copy.deepcopy(ENDPOINTS)
        entries[0]["classification"]["primaryDomain"] = "D4"
        errors = self.audit(endpoints=entries)
        self.assertTrue(any("primaryDomain differs from module" in error for error in errors), errors)

    def test_duplicate_registry_module_is_rejected(self):
        registry = copy.deepcopy(REGISTRY)
        registry["modules"].append(dict(registry["modules"][0], path="Core/BreedingPipeline/"))
        errors = self.audit(registry=registry)
        self.assertTrue(any("Duplicate registry classification" in error for error in errors), errors)

    def test_flat_or_undeclared_module_path_is_rejected(self):
        for path in ("BreedingPipeline/", "Unknown/BreedingPipeline/", "Breeding/../BreedingPipeline/"):
            with self.subTest(path=path):
                registry = copy.deepcopy(REGISTRY)
                registry["modules"][0]["path"] = path
                errors = self.audit(registry=registry)
                self.assertTrue(any("Registry module" in error for error in errors), errors)

    def test_operation_source_cannot_point_to_a_different_module(self):
        entries = copy.deepcopy(ENDPOINTS)
        entries[0]["source"]["path"] = "Specification/BrAPI-GenX/Core/ServerInfoV3/ServerInfo.yaml"
        errors = self.audit(endpoints=entries)
        self.assertTrue(any("source must be under" in error for error in errors), errors)

    def test_layout_detects_missing_unregistered_and_flat_modules(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for module in REGISTRY["modules"]:
                path = root / module["path"]
                path.mkdir(parents=True)
                (path / "README.md").touch()
                (path.parent / "README.md").touch()
            self.assertEqual([], self.audit(genx_root=root))
            (root / "Core" / "Unlisted").mkdir()
            (root / "FlatModule").mkdir()
            (root / "RFC-000-Misplaced.md").touch()
            (root / "Breeding" / "BreedingPipeline").rename(root / "BreedingPipeline")
            errors = self.audit(genx_root=root)
            for message in ("Core/Unlisted/", "FlatModule/", "RFC-000-Misplaced.md",
                            "Breeding/BreedingPipeline/ is missing"):
                self.assertTrue(any(message in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
