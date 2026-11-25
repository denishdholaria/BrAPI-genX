#!/usr/bin/env python3
"""Falsify L-13: HTTP 409 is insufficient without an unchanged model GET."""
from __future__ import annotations

from pathlib import Path
from unittest import mock
import copy
import unittest

import yaml

import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class ModelConflictPostconditionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        manifest = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in manifest["probes"] if p["id"] == "L-13")

    def test_registered_probe_includes_verified_retrieval(self):
        calls = self.probe["calls"]
        self.assertEqual(3, len(calls))
        self.assertEqual("GET", calls[2]["method"])
        self.assertEqual("/models/{modelDbId}?version={modelVersion}", calls[2]["path"])
        self.assertTrue(calls[2]["assert"]["unchanged_model_digest"])

    def exercise(self, mutate=None, read_status=200):
        calls = []
        submitted = {}

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", "/models"), (method, path))
                submitted.update(copy.deepcopy(body))
                return 200, {"result": copy.deepcopy(body)}
            if len(calls) == 2:
                self.assertEqual(("POST", "/models"), (method, path))
                self.assertEqual(submitted["modelDbId"], body["modelDbId"])
                self.assertEqual(submitted["modelVersion"], body["modelVersion"])
                self.assertNotEqual(submitted["artifactDigest"], body["artifactDigest"])
                return 409, {}
            if len(calls) == 3:
                self.assertEqual(
                    ("GET", f"/models/{submitted['modelDbId']}?version={submitted['modelVersion']}"),
                    (method, path),
                )
                result = copy.deepcopy(submitted)
                if mutate:
                    result = mutate(result)
                return read_status, {"result": result}
            self.fail("unexpected extra HTTP request")

        ctx = {"conformance_dir": str(CONF)}
        outcome = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe("http://example.test/genx/v1", self.probe,
                                   ctx, outcome, None, None)
        self.assertEqual(3, len(calls))
        return outcome

    def test_unchanged_registered_version_passes(self):
        self.assertEqual(0, self.exercise().failures)

    def test_changed_digest_after_conflict_fails(self):
        outcome = self.exercise(
            lambda record: {**record, "artifactDigest": "f" * 64})
        self.assertEqual(1, outcome.failures)

    def test_changed_model_identity_after_conflict_fails(self):
        outcome = self.exercise(
            lambda record: {**record, "modelDbId": "test-authority:model:other"})
        self.assertEqual(1, outcome.failures)

    def test_changed_model_version_after_conflict_fails(self):
        outcome = self.exercise(
            lambda record: {**record, "modelVersion": "unrequested-version"})
        self.assertEqual(1, outcome.failures)

    def test_missing_artifact_digest_fails(self):
        def remove_digest(record):
            del record["artifactDigest"]
            return record
        self.assertEqual(1, self.exercise(remove_digest).failures)

    def test_unavailable_registered_version_fails(self):
        self.assertEqual(1, self.exercise(read_status=404).failures)


if __name__ == "__main__":
    unittest.main()
