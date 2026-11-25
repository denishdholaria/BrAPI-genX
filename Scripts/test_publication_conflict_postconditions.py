#!/usr/bin/env python3
"""Mutation tests for registered L-17/L-19 post-conflict GET invariants."""
from __future__ import annotations

from pathlib import Path
from unittest import mock
import copy
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class PublicationConflictTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        document = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probes = {p["id"]: p for p in document["probes"] if p["id"] in ("L-17", "L-19")}

    def test_registered_postconditions_include_get(self):
        expected = {
            "L-17": ("GET", "/variantmatrices/{matrixDbId}", "unchanged_matrix_digest"),
            "L-19": ("GET", "/fair-packages/{packageDbId}", "unchanged_package_license"),
        }
        for key, (method, path, assertion) in expected.items():
            with self.subTest(probe=key):
                self.assertEqual(3, len(self.probes[key]["calls"]))
                final = self.probes[key]["calls"][-1]
                self.assertEqual((method, path), (final["method"], final["path"]))
                self.assertTrue(final["assert"][assertion])

    def run_conflict(self, probe_id, mutate=None, get_status=200):
        resource = {"L-17": "/variantmatrices", "L-19": "/fair-packages"}[probe_id]
        id_field = {"L-17": "matrixDbId", "L-19": "packageDbId"}[probe_id]
        conflict_field = {"L-17": "fileDigest", "L-19": "license"}[probe_id]
        original = {}
        calls = []

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", resource), (method, path))
                original.update(copy.deepcopy(body))
                return 200, {"result": copy.deepcopy(body)}
            if len(calls) == 2:
                self.assertEqual(("POST", resource), (method, path))
                self.assertEqual(body[id_field], original[id_field])
                self.assertNotEqual(body[conflict_field], original[conflict_field])
                return 409, {}
            if len(calls) == 3:
                self.assertEqual(("GET", f"{resource}/{original[id_field]}"), (method, path))
                saved = copy.deepcopy(original)
                if mutate is not None:
                    saved = mutate(saved)
                return get_status, {"result": saved}
            self.fail("unexpected extra HTTP request")

        outcome = checker.Results()
        ctx = {"conformance_dir": str(CONF)}
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe("http://example.test/genx/v1", self.probes[probe_id],
                                   ctx, outcome, None, None)
        self.assertEqual(3, len(calls))
        return outcome

    def test_matrix_digest_unchanged_passes(self):
        self.assertEqual(0, self.run_conflict("L-17").failures)

    def test_matrix_digest_corruption_fails(self):
        result = self.run_conflict("L-17", lambda r: {**r, "fileDigest": "f" * 64})
        self.assertEqual(1, result.failures)

    def test_matrix_wrong_identity_fails(self):
        result = self.run_conflict(
            "L-17", lambda r: {**r, "matrixDbId": "test-authority:matrix:other"})
        self.assertEqual(1, result.failures)

    def test_matrix_missing_payload_fails(self):
        self.assertEqual(1, self.run_conflict("L-17", get_status=404).failures)

    def test_package_license_unchanged_passes(self):
        self.assertEqual(0, self.run_conflict("L-19").failures)

    def test_package_license_corruption_fails(self):
        result = self.run_conflict("L-19", lambda r: {**r, "license": "replaced-license"})
        self.assertEqual(1, result.failures)

    def test_package_wrong_identity_fails(self):
        result = self.run_conflict(
            "L-19", lambda r: {**r, "packageDbId": "test-authority:package:other"})
        self.assertEqual(1, result.failures)

    def test_package_missing_record_fails(self):
        self.assertEqual(1, self.run_conflict("L-19", get_status=404).failures)


if __name__ == "__main__":
    unittest.main()
