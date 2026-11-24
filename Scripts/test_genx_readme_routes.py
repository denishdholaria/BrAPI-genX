#!/usr/bin/env python3
"""Mutation tests for non-normative GenX README route claims."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from audit_genx_readme_routes import audit

HERE = Path(__file__).resolve().parent
MODULE = "Geospatial/VegetationIndex"
DOC = "Specification/BrAPI-GenX/" + MODULE + "/README.md"
SOURCE = "Specification/BrAPI-GenX/" + MODULE + "/VegetationIndex_GET_POST.yaml"
RECORDS = [
    {"apiGeneration": "genx-v1", "catalogId": "genx.vi.list",
     "method": "GET", "path": "/vegetation-indexes",
     "operationIdInSource": "genxListVegetationIndexes", "source": {"path": SOURCE}},
    {"apiGeneration": "genx-v1", "catalogId": "genx.vi.record",
     "method": "POST", "path": "/vegetation-indexes",
     "operationIdInSource": "genxRegisterVegetationIndex", "source": {"path": SOURCE}},
]
GOOD = ("- `GET /genx/v1/vegetation-indexes` "
        "(`genxListVegetationIndexes`) lists records.\n"
        "- `POST /genx/v1/vegetation-indexes` "
        "(`genxRegisterVegetationIndex`) registers a record.\n")


class ReadmeRouteAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        registry = self.root / "Specification/ENDPOINT-REGISTRY.json"
        registry.parent.mkdir(parents=True)
        registry.write_text(json.dumps({"entries": RECORDS}), encoding="utf-8")
        self.readme = self.root / DOC
        self.readme.parent.mkdir(parents=True)
        self.readme.write_text(GOOD, encoding="utf-8")

    def test_correct_claims_match_exact_registered_operations(self):
        result = audit(self.root, [MODULE])
        self.assertEqual(2, result["claimsChecked"])
        self.assertEqual([], result["errors"])
        self.assertEqual([], result["mismatches"])
        self.assertEqual([], result["uncovered"])

    def test_singular_legacy_route_is_rejected(self):
        self.readme.write_text(GOOD.replace("/vegetation-indexes", "/vegetation-index"))
        result = audit(self.root, [MODULE])
        self.assertEqual(2, len(result["mismatches"]))
        self.assertEqual(2, len(result["uncovered"]))

    def test_wrong_operation_identity_is_rejected(self):
        self.readme.write_text(GOOD.replace("genxListVegetationIndexes",
                                            "genxListVegetationIndex"))
        result = audit(self.root, [MODULE])
        self.assertEqual(1, len(result["mismatches"]))
        self.assertEqual([], result["errors"])

    def test_missing_readme_claim_is_advisory_coverage_gap(self):
        self.readme.write_text(GOOD.splitlines(keepends=True)[0])
        result = audit(self.root, [MODULE])
        self.assertEqual([], result["mismatches"])
        self.assertEqual(1, len(result["uncovered"]))

    def test_unknown_module_is_rejected(self):
        self.assertTrue(audit(self.root, ["Unknown/Module"])["errors"])
        self.assertTrue(audit(self.root, ["../unsafe"])["errors"])

    def test_source_path_escape_is_rejected(self):
        registry = self.root / "Specification/ENDPOINT-REGISTRY.json"
        data = json.loads(registry.read_text())
        data["entries"][0]["source"]["path"] = "../../outside.yaml"
        registry.write_text(json.dumps(data))
        result = audit(self.root, [MODULE])
        self.assertTrue(any("unsafe source" in x for x in result["errors"]))

    def test_cli_strict_fails_for_incorrect_claim(self):
        self.readme.write_text(GOOD.replace("/vegetation-indexes", "/vegetation-index"))
        command = [sys.executable, str(HERE / "audit_genx_readme_routes.py"),
                   "--root", str(self.root), "--module", MODULE]
        report_only = subprocess.run(command, capture_output=True, text=True)
        strict = subprocess.run(command + ["--strict"], capture_output=True, text=True)
        self.assertEqual(0, report_only.returncode, report_only.stdout)
        self.assertEqual(1, strict.returncode, strict.stdout)


if __name__ == "__main__":
    unittest.main()
