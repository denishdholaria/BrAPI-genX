#!/usr/bin/env python3
"""Mission 131: reject model conflicts without rewriting any original field."""
from __future__ import annotations

import copy
from pathlib import Path
from unittest import mock
import unittest
from urllib.parse import quote

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class ModelConflictWholeRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        document = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in document["probes"] if p["id"] == "L-13")

    def test_registered_conflict_then_versioned_readback(self):
        self.assertEqual(3, len(self.probe["calls"]))
        self.assertEqual("live_model_conflict", self.probe["calls"][1]["body_fixture"])
        self.assertEqual(409, self.probe["calls"][1]["assert"]["status"])
        self.assertIs(True, self.probe["calls"][2]["assert"]["unchanged_model_digest"])

    def exercise(self, mutate=None, read_status=200, conflict_status=409):
        calls = []
        original = {}

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", "/models"), (method, path))
                original.update(copy.deepcopy(body))
                return 200, {"result": copy.deepcopy(body)}
            if len(calls) == 2:
                self.assertEqual(("POST", "/models"), (method, path))
                self.assertEqual(original["modelDbId"], body["modelDbId"])
                self.assertEqual(original["modelVersion"], body["modelVersion"])
                self.assertNotEqual(original["artifactDigest"], body["artifactDigest"])
                return conflict_status, {}
            if len(calls) == 3:
                uri = ("/models/" + quote(original["modelDbId"], safe=":")
                       + "?version=" + quote(original["modelVersion"], safe=""))
                self.assertEqual(("GET", uri), (method, path))
                stored = copy.deepcopy(original)
                if mutate is not None:
                    stored = mutate(stored)
                return read_status, {"result": stored}
            self.fail("unexpected extra HTTP call")

        outcome = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, None)
        return outcome.failures, calls

    def test_unchanged_model_passes(self):
        self.assertEqual(0, self.exercise()[0])

    def test_extra_server_field_is_allowed(self):
        self.assertEqual(0, self.exercise(
            mutate=lambda record: {**record, "auditLabel": "readback"})[0])

    def test_changed_artifact_digest_fails(self):
        self.assertEqual(1, self.exercise(
            mutate=lambda record: {**record, "artifactDigest": "f" * 64})[0])

    def test_changed_training_data_digest_fails(self):
        self.assertEqual(1, self.exercise(
            mutate=lambda record: {**record, "trainingDataDigest": "f" * 64})[0])

    def test_changed_artifact_url_fails(self):
        self.assertEqual(1, self.exercise(
            mutate=lambda record: {**record, "artifactURL": "https://other.example"})[0])

    def test_changed_framework_fails(self):
        self.assertEqual(1, self.exercise(
            mutate=lambda record: {**record, "framework": "other-framework"})[0])

    def test_changed_metrics_fails(self):
        def mutation(record):
            record["metrics"]["rmse"] = 99.0
            return record
        self.assertEqual(1, self.exercise(mutation)[0])

    def test_changed_provenance_actor_fails(self):
        def mutation(record):
            record["provenance"]["actor"] = "actor:unauthorized"
            return record
        self.assertEqual(1, self.exercise(mutation)[0])

    def test_changed_provenance_digest_fails(self):
        def mutation(record):
            record["provenance"]["inputsDigest"] = "f" * 64
            return record
        self.assertEqual(1, self.exercise(mutation)[0])

    def test_changed_model_status_fails(self):
        self.assertEqual(1, self.exercise(
            mutate=lambda record: {**record, "status": "revoked"})[0])

    def test_changed_model_identity_fails(self):
        self.assertEqual(1, self.exercise(
            mutate=lambda record: {**record, "modelDbId": "other:model:wrong"})[0])

    def test_changed_model_version_fails(self):
        self.assertEqual(1, self.exercise(
            mutate=lambda record: {**record, "modelVersion": "99"})[0])

    def test_missing_original_field_fails(self):
        def mutation(record):
            record.pop("trainingDataDigest")
            return record
        self.assertEqual(1, self.exercise(mutation)[0])

    def test_missing_provenance_fails(self):
        def mutation(record):
            record.pop("provenance")
            return record
        self.assertEqual(1, self.exercise(mutation)[0])

    def test_absent_result_fails(self):
        self.assertEqual(1, self.exercise(mutate=lambda record: None)[0])

    def test_malformed_result_fails(self):
        self.assertEqual(1, self.exercise(mutate=lambda record: [record])[0])

    def test_unavailable_readback_fails(self):
        self.assertEqual(1, self.exercise(read_status=404)[0])

    def test_conflicting_write_accepted_fails_before_readback(self):
        failures, calls = self.exercise(conflict_status=200)
        self.assertEqual(1, failures)
        self.assertEqual(2, len(calls))


if __name__ == "__main__":
    unittest.main()
