#!/usr/bin/env python3
"""Mutation tests for contract-preserving GenX specification structure rules."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from specification_structure import generated_link_errors, module_errors, registry_source_errors


class StructureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.genx = self.root / "Specification/BrAPI-GenX"
        self.module = self.genx / "Core/Jobs"
        (self.module / "Schemas").mkdir(parents=True)
        (self.module / "README.md").write_text("# Jobs\n")
        (self.module / "GroupDescription.md").write_text("# Jobs\n")
        (self.module / "Schemas/Job.yaml").write_text("components:\n  schemas:\n    Job: {}\n")
        (self.module / "Jobs_GET_POST.yaml").write_text("paths: {}\n")
        self.classification = {"modules": [{"path": "Core/Jobs/"}]}
        self.registry = {"entries": [
            {"apiGeneration": "genx-v1", "catalogId": "jobs.list",
             "source": {"path": "Specification/BrAPI-GenX/Core/Jobs/Jobs_GET_POST.yaml"}}
        ]}

    def test_valid_module_and_source(self):
        self.assertEqual([], module_errors(self.root, self.classification))
        self.assertEqual([], registry_source_errors(self.root, self.registry))

    def test_missing_operation_or_schema_fails_closed(self):
        (self.module / "Jobs_GET_POST.yaml").unlink()
        (self.module / "Schemas/Job.yaml").unlink()
        errors = module_errors(self.root, self.classification)
        self.assertTrue(any("missing OpenAPI operation" in x for x in errors), errors)
        self.assertTrue(any("has no YAML definitions" in x for x in errors), errors)

    def test_lowercase_schema_directory_rejected(self):
        (self.module / "Schemas").rename(self.module / "schemas")
        errors = module_errors(self.root, self.classification)
        self.assertTrue(any("missing canonical Schemas/" in x for x in errors), errors)
        self.assertTrue(any("schemas directory casing" in x for x in errors), errors)

    def test_unregistered_source_and_traversal_rejected(self):
        self.registry["entries"][0]["source"]["path"] = "Specification/BrAPI-GenX/../escape.yaml"
        errors = registry_source_errors(self.root, self.registry)
        self.assertTrue(any("unsafe/missing source" in x for x in errors), errors)
        self.registry["entries"][0]["source"]["path"] = "Specification/BrAPI-GenX/Core/Jobs/missing.yaml"
        self.assertTrue(any("missing source file" in x for x in registry_source_errors(self.root, self.registry)))

    def test_embedded_provenance_is_exempt_from_endpoint_requirement(self):
        path = self.genx / "Core/Provenance"
        (path / "Schemas").mkdir(parents=True)
        (path / "Schemas/ProvenanceEnvelope.yaml").write_text("components: {}\n")
        (path / "README.md").write_text("# Provenance\n")
        (path / "GroupDescription.md").write_text("# Provenance\n")
        classification = {"modules": self.classification["modules"] + [{"path": "Core/Provenance/"}]}
        self.assertEqual([], module_errors(self.root, classification))

    def test_missing_generated_file_or_link_rejected(self):
        dest = self.root / "Specification/Generated"
        dest.mkdir(parents=True)
        (dest / "brapi_generated.json").write_text("{}\n")
        (dest / "brapi_openapi.json").write_text("{}\n")
        (dest / "README.md").write_text(
            "[brapi_generated.json](brapi_generated.json)\n"
            "[brapi_openapi.json](brapi_openapi.json)\n"
        )
        self.assertEqual([], generated_link_errors(self.root))
        (dest / "brapi_openapi.json").unlink()
        self.assertTrue(any("Missing declared generated" in x for x in generated_link_errors(self.root)))


if __name__ == "__main__":
    unittest.main()
