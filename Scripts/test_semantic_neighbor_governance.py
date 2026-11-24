#!/usr/bin/env python3
"""Mutation tests for semantic-neighbor governance validation."""
from __future__ import annotations

import copy
import json
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "Scripts" / "check_semantic_neighbor_governance.py"
PYTHON = sys.executable
LEDGER_REL = Path("Specification/BrAPI-GenX/Conformance/semantic-neighbor-review.yaml")
REGISTRY_REL = Path("Specification/ENDPOINT-REGISTRY.json")


def run_validator(checkout: Path, extra_args=None) -> int:
    cmd = [PYTHON, str(VALIDATOR), "--root", str(checkout)]
    if extra_args:
        cmd.extend(extra_args)
    result = subprocess.run(cmd, cwd=checkout, capture_output=True, text=True)
    return result.returncode


def run_validator_output(checkout: Path, extra_args=None) -> tuple[int, str]:
    cmd = [PYTHON, str(VALIDATOR), "--root", str(checkout)]
    if extra_args:
        cmd.extend(extra_args)
    result = subprocess.run(cmd, cwd=checkout, capture_output=True, text=True)
    return result.returncode, (result.stdout + "\n" + result.stderr)


def copy_checkout(directory: Path) -> Path:
    checkout = directory / "repo"
    shutil.copytree(ROOT, checkout, ignore=shutil.ignore_patterns(".git", "__pycache__"))
    return checkout


import yaml


class SemanticNeighborGovernanceTests(unittest.TestCase):
    def test_current_ledger_passes(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            code, output = run_validator_output(checkout)
            self.assertEqual(0, code, output)

    def test_missing_entry_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            ledger_path = checkout / LEDGER_REL
            ledger = yaml.safe_load(ledger_path.read_text())
            removed_id = ledger["entries"][0]["id"]
            ledger["entries"].pop(0)
            ledger["entry_count"] = len(ledger["entries"])
            ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False))
            code, output = run_validator_output(checkout)
            self.assertNotEqual(0, code)
            self.assertIn(f"Missing retained semantic-neighbor relationship: {removed_id}", output)

    def test_paired_deletion_fails_with_missing_relationship_id(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            ledger_path = checkout / LEDGER_REL
            reg_path = checkout / REGISTRY_REL
            ledger = yaml.safe_load(ledger_path.read_text())
            reg = json.loads(reg_path.read_text())
            entry = ledger["entries"][0]
            rid = entry["id"]
            src_cat = entry["sourceCatalogId"]
            target_op = entry["targetOperationId"]
            # remove from registry neighbor list
            for e in reg["entries"]:
                if e.get("catalogId") == src_cat:
                    e["semanticNeighborIds"] = [n for n in e.get("semanticNeighborIds", []) if n != target_op]
            reg_path.write_text(json.dumps(reg, indent=2) + "\n")
            # remove from ledger
            ledger["entries"] = [e for e in ledger["entries"] if e["id"] != rid]
            ledger["entry_count"] = len(ledger["entries"])
            ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False))
            code, output = run_validator_output(checkout)
            self.assertNotEqual(0, code)
            self.assertIn(f"Missing retained semantic-neighbor relationship: {rid}", output)

    def test_duplicate_id_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            ledger_path = checkout / LEDGER_REL
            ledger = yaml.safe_load(ledger_path.read_text())
            dup = copy.deepcopy(ledger["entries"][0])
            ledger["entries"].append(dup)
            ledger["entry_count"] = len(ledger["entries"])
            ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False))
            code, output = run_validator_output(checkout)
            self.assertNotEqual(0, code)
            self.assertIn("Duplicate ledger entry id", output)

    def test_duplicate_pair_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            ledger_path = checkout / LEDGER_REL
            ledger = yaml.safe_load(ledger_path.read_text())
            dup = copy.deepcopy(ledger["entries"][0])
            dup["id"] = ledger["entries"][0]["id"] + "::duplicate"
            ledger["entries"].append(dup)
            ledger["entry_count"] = len(ledger["entries"])
            ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False))
            code, output = run_validator_output(checkout)
            self.assertNotEqual(0, code)
            self.assertTrue("Duplicate source-target relationship" in output or "Non-canonical" in output)

    def test_rewritten_id_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            ledger_path = checkout / LEDGER_REL
            ledger = yaml.safe_load(ledger_path.read_text())
            ledger["entries"][0]["id"] = "rewritten -> id"
            ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False))
            code, output = run_validator_output(checkout)
            self.assertNotEqual(0, code)
            self.assertIn("Non-canonical semantic-neighbor relationship id", output)

    def test_invalid_status_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            ledger_path = checkout / LEDGER_REL
            ledger = yaml.safe_load(ledger_path.read_text())
            ledger["entries"][0]["reviewStatus"] = "approved"
            ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False))
            code, output = run_validator_output(checkout)
            self.assertNotEqual(0, code)
            self.assertIn("invalid reviewStatus", output)

    def test_invalid_boundary_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            ledger_path = checkout / LEDGER_REL
            ledger = yaml.safe_load(ledger_path.read_text())
            ledger["entries"][0]["boundary"] = "within-module"
            ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False))
            code, output = run_validator_output(checkout)
            self.assertNotEqual(0, code)
            self.assertTrue("boundary" in output and "does not match" in output)

    def test_dangling_source_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            ledger_path = checkout / LEDGER_REL
            ledger = yaml.safe_load(ledger_path.read_text())
            ledger["entries"][0]["sourceCatalogId"] = "brapi-genx.genx.v1.does-not-exist"
            ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False))
            code, output = run_validator_output(checkout)
            self.assertNotEqual(0, code)
            self.assertIn("does not resolve to a registry entry", output)

    def test_dangling_target_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            ledger_path = checkout / LEDGER_REL
            ledger = yaml.safe_load(ledger_path.read_text())
            ledger["entries"][0]["targetOperationId"] = "genxDoesNotExist"
            ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False))
            code, output = run_validator_output(checkout)
            self.assertNotEqual(0, code)
            self.assertIn("does not resolve to an operation or governed relationship", output)

    def test_evidence_backed_missing_fields_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            ledger_path = checkout / LEDGER_REL
            ledger = yaml.safe_load(ledger_path.read_text())
            ledger["entries"][0]["reviewStatus"] = "evidence-backed-proposed"
            ledger["entries"][0]["rationale"] = ""
            ledger["entries"][0]["evidence"] = []
            ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False))
            code, output = run_validator_output(checkout)
            self.assertNotEqual(0, code)
            self.assertIn("requires non-empty", output.lower().replace("'", "") or "requires" in output)

    def test_forbidden_transition_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            ledger_path = checkout / LEDGER_REL
            ledger = yaml.safe_load(ledger_path.read_text())
            # comparison ledger: one entry advanced to evidence-backed-proposed
            comparison = copy.deepcopy(ledger)
            comparison["entries"][0]["reviewStatus"] = "evidence-backed-proposed"
            comparison["entries"][0]["rationale"] = "r"
            comparison["entries"][0]["evidence"] = ["RFC-002"]
            comparison["entries"][0]["reviewedBy"] = "reviewer"
            comparison["entries"][0]["reviewedAt"] = "2026-01-01"
            comp_path = Path(td) / "comparison.yaml"
            comp_path.write_text(yaml.safe_dump(comparison, sort_keys=False))
            # current: same entry back to inherited-unreviewed (forbidden)
            ledger["entries"][0]["reviewStatus"] = "inherited-unreviewed"
            ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False))
            code, output = run_validator_output(checkout, ["--comparison-ledger", str(comp_path)])
            self.assertNotEqual(0, code)
            self.assertIn("Forbidden semantic-neighbor status transition", output)

    def test_missing_authorization_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            ledger_path = checkout / LEDGER_REL
            ledger = yaml.safe_load(ledger_path.read_text())
            ledger["entries"][0]["reviewStatus"] = "rejected"
            ledger["entries"][0]["rationale"] = "r"
            ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False))
            code, output = run_validator_output(checkout)
            self.assertNotEqual(0, code)
            self.assertIn("authorizationReference", output)

    def test_missing_successor_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            ledger_path = checkout / LEDGER_REL
            ledger = yaml.safe_load(ledger_path.read_text())
            ledger["entries"][0]["reviewStatus"] = "superseded"
            ledger["entries"][0]["rationale"] = "r"
            ledger["entries"][0]["authorizationReference"] = "D-20"
            ledger["entries"][0]["supersededBy"] = "does-not-exist"
            ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False))
            code, output = run_validator_output(checkout)
            self.assertNotEqual(0, code)
            self.assertIn("supersededBy does not resolve", output)

    def test_valid_control_passes(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            ledger_path = checkout / LEDGER_REL
            ledger = yaml.safe_load(ledger_path.read_text())
            comparison = copy.deepcopy(ledger)
            comp_path = Path(td) / "comparison.yaml"
            comp_path.write_text(yaml.safe_dump(comparison, sort_keys=False))
            # advance one entry with full evidence
            ledger["entries"][0]["reviewStatus"] = "evidence-backed-proposed"
            ledger["entries"][0]["rationale"] = "r"
            ledger["entries"][0]["evidence"] = ["RFC-002"]
            ledger["entries"][0]["reviewedBy"] = "reviewer"
            ledger["entries"][0]["reviewedAt"] = "2026-01-01"
            ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False))
            code, output = run_validator_output(checkout, ["--comparison-ledger", str(comp_path)])
            self.assertEqual(0, code, output)

    def test_non_inherited_without_provenance_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            ledger_path = checkout / LEDGER_REL
            ledger = yaml.safe_load(ledger_path.read_text())
            new_entry = copy.deepcopy(ledger["entries"][0])
            new_entry["id"] = "brapi-genx.genx.v1.farms.list -> genxGetFarm"
            new_entry["sourceCatalogId"] = "brapi-genx.genx.v1.farms.list"
            new_entry["sourceOperationId"] = "genxListFarms"
            new_entry["targetOperationId"] = "genxGetFarm"
            new_entry["targetCatalogId"] = "brapi-genx.genx.v1.farms.get"
            new_entry["sourceModule"] = "Farm"
            new_entry["targetModule"] = "Farm"
            new_entry["boundary"] = "within-module"
            new_entry["provenance"] = "inherited-registry-only"
            new_entry["reviewStatus"] = "inherited-unreviewed"
            new_entry["rationale"] = ""
            new_entry["evidence"] = []
            ledger["entries"].append(new_entry)
            ledger["entry_count"] = len(ledger["entries"])
            ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False))
            code, output = run_validator_output(checkout)
            self.assertNotEqual(0, code)
            self.assertIn("inherited-registry-only", output)

    def test_entry_count_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            ledger_path = checkout / LEDGER_REL
            ledger = yaml.safe_load(ledger_path.read_text())
            ledger["entry_count"] = 999
            ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False))
            code, output = run_validator_output(checkout)
            self.assertNotEqual(0, code)
            self.assertIn("entry_count", output)



    def test_evidence_null_placeholder_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            ledger_path = checkout / LEDGER_REL
            ledger = yaml.safe_load(ledger_path.read_text())
            ledger["entries"][0]["reviewStatus"] = "evidence-backed-proposed"
            ledger["entries"][0]["rationale"] = "r"
            ledger["entries"][0]["evidence"] = [None]
            ledger["entries"][0]["reviewedBy"] = "reviewer"
            ledger["entries"][0]["reviewedAt"] = "2026-01-01"
            ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False))
            code, output = run_validator_output(checkout)
            self.assertNotEqual(0, code)
            self.assertIn("evidence entries must be non-empty strings", output)

    def test_whitespace_authorization_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            ledger_path = checkout / LEDGER_REL
            ledger = yaml.safe_load(ledger_path.read_text())
            ledger["entries"][0]["reviewStatus"] = "rejected"
            ledger["entries"][0]["rationale"] = "r"
            ledger["entries"][0]["authorizationReference"] = "   "
            ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False))
            code, output = run_validator_output(checkout)
            self.assertNotEqual(0, code)
            self.assertIn("authorizationReference", output)

    def test_self_supersession_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            ledger_path = checkout / LEDGER_REL
            ledger = yaml.safe_load(ledger_path.read_text())
            rid = ledger["entries"][0]["id"]
            ledger["entries"][0]["reviewStatus"] = "superseded"
            ledger["entries"][0]["rationale"] = "r"
            ledger["entries"][0]["authorizationReference"] = "D-20"
            ledger["entries"][0]["supersededBy"] = rid
            ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False))
            code, output = run_validator_output(checkout)
            self.assertNotEqual(0, code)
            self.assertIn("self-supersession is not allowed", output)

    def test_unreadable_comparison_ref_fails(self):
        # Use the real repository checkout (has .git) so the ref is resolved.
        code, output = run_validator_output(ROOT, ["--comparison-ref", "definitely-not-a-ref"])
        self.assertNotEqual(0, code)
        self.assertIn("Comparison ledger could not be loaded", output)


    def test_empty_comparison_ledger_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout = copy_checkout(Path(td))
            empty = Path(td) / "empty.yaml"
            empty.write_text("{}\n")
            code, output = run_validator_output(checkout, ["--comparison-ledger", str(empty)])
            self.assertNotEqual(0, code)
            self.assertIn("entries must be a list", output)

    def test_empty_comparison_ref_fails(self):
        code, output = run_validator_output(ROOT, ["--comparison-ref", ""])
        self.assertNotEqual(0, code)
        self.assertIn("comparison ref must not be empty", output)


    def _retirement_checkout(self, directory: Path, *, status: str | None, remove_edge: bool):
        """Construct a copied-repository mutation; never alter the real registry."""
        checkout = copy_checkout(directory)
        ledger_path = checkout / LEDGER_REL
        registry_path = checkout / REGISTRY_REL
        ledger = yaml.safe_load(ledger_path.read_text(encoding="utf-8"))
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        row = ledger["entries"][0]
        source = next(e for e in registry["entries"]
                      if e.get("catalogId") == row["sourceCatalogId"])
        self.assertIn(row["targetOperationId"], source["semanticNeighborIds"])

        comparison_path = directory / "comparison-before-retirement.yaml"
        comparison_path.write_text(yaml.safe_dump(ledger, sort_keys=False),
                                   encoding="utf-8")

        if status is not None:
            row["reviewStatus"] = status
            row["rationale"] = "Synthetic test-only terminal decision"
            # Existing validator checks whether the reference is followable.
            # This test token is NOT evidence of real maintainer approval.
            row["authorizationReference"] = "RFC-002"
            if status == "superseded":
                row["supersededBy"] = next(e["id"] for e in ledger["entries"]
                                            if e["id"] != row["id"])
            ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False),
                                   encoding="utf-8")
        if remove_edge:
            source["semanticNeighborIds"] = [
                n for n in source["semanticNeighborIds"]
                if n != row["targetOperationId"]
            ]
            registry_path.write_text(json.dumps(registry, indent=2) + "\n",
                                     encoding="utf-8")
        return checkout, comparison_path

    def test_terminal_rejected_neighbor_still_published_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout, baseline = self._retirement_checkout(
                Path(td), status="rejected", remove_edge=False)
            code, output = run_validator_output(
                checkout, ["--comparison-ledger", str(baseline)])
            self.assertNotEqual(0, code)
            self.assertIn("remains published in registry semanticNeighborIds", output)

    def test_consistent_terminal_removal_passes_structural_governance(self):
        with tempfile.TemporaryDirectory() as td:
            checkout, baseline = self._retirement_checkout(
                Path(td), status="rejected", remove_edge=True)
            code, output = run_validator_output(
                checkout, ["--comparison-ledger", str(baseline)])
            # Structural acceptance is not real scientific approval. The
            # synthetic authorization token cannot ratify a disposition.
            self.assertEqual(0, code, output)

    def test_registry_removal_without_terminal_disposition_fails(self):
        with tempfile.TemporaryDirectory() as td:
            checkout, baseline = self._retirement_checkout(
                Path(td), status=None, remove_edge=True)
            code, output = run_validator_output(
                checkout, ["--comparison-ledger", str(baseline)])
            self.assertNotEqual(0, code)
            self.assertIn("authorized terminal disposition", output)

if __name__ == "__main__":
    unittest.main()
