#!/usr/bin/env python3
"""Mutation tests for registry/source semantic-neighbor integrity."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "Scripts" / "auditEndpointRegistrySourceConsistency.py"
PYTHON = sys.executable


def run_strict(checkout: Path) -> int:
    result = subprocess.run(
        [PYTHON, str(AUDIT), "--root", str(checkout), "--strict"],
        cwd=checkout,
        capture_output=True,
        text=True,
    )
    return result.returncode


def copy_checkout(directory: Path) -> Path:
    checkout = directory / "repo"
    shutil.copytree(ROOT, checkout, ignore=shutil.ignore_patterns(".git", "__pycache__"))
    return checkout


class RegistrySourceConsistencyTests(unittest.TestCase):
    def test_current_registry_strict_passes(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            self.assertEqual(0, run_strict(checkout))

    def test_dangling_neighbor_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            reg_path = checkout / "Specification" / "ENDPOINT-REGISTRY.json"
            reg = json.loads(reg_path.read_text())
            target = next(e for e in reg["entries"]
                          if e["apiGeneration"] == "genx-v1"
                          and e.get("semanticNeighborIds"))
            target["semanticNeighborIds"] = list(target["semanticNeighborIds"]) + ["genxDoesNotExist"]
            reg_path.write_text(json.dumps(reg, indent=2) + "\n")
            self.assertNotEqual(0, run_strict(checkout))

    def test_unknown_governed_relationship_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            reg_path = checkout / "Specification" / "ENDPOINT-REGISTRY.json"
            reg = json.loads(reg_path.read_text())
            target = next(e for e in reg["entries"]
                          if e["apiGeneration"] == "genx-v1"
                          and e.get("semanticNeighborIds"))
            target["semanticNeighborIds"] = list(target["semanticNeighborIds"]) + ["SEM-99"]
            reg_path.write_text(json.dumps(reg, indent=2) + "\n")
            self.assertNotEqual(0, run_strict(checkout))

    def test_duplicate_neighbor_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            reg_path = checkout / "Specification" / "ENDPOINT-REGISTRY.json"
            reg = json.loads(reg_path.read_text())
            target = next(e for e in reg["entries"]
                          if e["apiGeneration"] == "genx-v1"
                          and e.get("semanticNeighborIds"))
            first = target["semanticNeighborIds"][0]
            target["semanticNeighborIds"] = list(target["semanticNeighborIds"]) + [first]
            reg_path.write_text(json.dumps(reg, indent=2) + "\n")
            self.assertNotEqual(0, run_strict(checkout))

    def test_malformed_neighbor_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            reg_path = checkout / "Specification" / "ENDPOINT-REGISTRY.json"
            reg = json.loads(reg_path.read_text())
            target = next(e for e in reg["entries"]
                          if e["apiGeneration"] == "genx-v1"
                          and e.get("semanticNeighborIds"))
            target["semanticNeighborIds"] = list(target["semanticNeighborIds"]) + [123]
            reg_path.write_text(json.dumps(reg, indent=2) + "\n")
            self.assertNotEqual(0, run_strict(checkout))

    def test_missing_source_neighbor_fails(self):
        import yaml
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            reg_path = checkout / "Specification" / "ENDPOINT-REGISTRY.json"
            reg = json.loads(reg_path.read_text())
            gov = {"OVERLAP-01","SEM-01","SEM-02","SEM-03","SEM-04","SEM-05","SEM-06","SEM-07"}
            # Find an entry with a source-declared neighbor present in registry.
            chosen = None
            chosen_neighbor = None
            for e in reg["entries"]:
                if e["apiGeneration"] != "genx-v1":
                    continue
                src_path = checkout / e["source"]["path"]
                doc = yaml.safe_load(src_path.read_text())
                op = doc["paths"][e["path"]][e["method"].lower()]
                src_neighbors = [n for n in (op.get("x-brapi-genx", {}) or {}).get("semanticNeighbors", [])
                                 if n not in gov]
                reg_neighbors = e.get("semanticNeighborIds", []) or []
                common = [n for n in src_neighbors if n in reg_neighbors]
                if common:
                    chosen = e
                    chosen_neighbor = common[0]
                    break
            self.assertIsNotNone(chosen)
            chosen["semanticNeighborIds"] = [n for n in chosen["semanticNeighborIds"] if n != chosen_neighbor]
            reg_path.write_text(json.dumps(reg, indent=2) + "\n")
            self.assertNotEqual(0, run_strict(checkout))

    def test_additional_verified_neighbor_passes(self):
        # Adding a valid GenX operation reference keeps strict passing.
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            reg_path = checkout / "Specification" / "ENDPOINT-REGISTRY.json"
            reg = json.loads(reg_path.read_text())
            target = next(e for e in reg["entries"]
                          if e["apiGeneration"] == "genx-v1"
                          and e.get("semanticNeighborIds"))
            # pick a valid operation id different from existing
            valid = next(op for op in
                         {e["recommendedOperationId"] for e in reg["entries"]
                          if e["apiGeneration"] == "genx-v1"}
                         if op not in target["semanticNeighborIds"])
            target["semanticNeighborIds"] = list(target["semanticNeighborIds"]) + [valid]
            reg_path.write_text(json.dumps(reg, indent=2) + "\n")
            self.assertEqual(0, run_strict(checkout))


if __name__ == "__main__":
    unittest.main()
