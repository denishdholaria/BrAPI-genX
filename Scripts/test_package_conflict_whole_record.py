#!/usr/bin/env python3
"""Mission 130: package conflict must retain the original complete record."""
from __future__ import annotations

import copy
from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class PackageConflictWholeRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        doc = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in doc["probes"] if p["id"] == "L-19")

    def test_registered_procedure(self):
        self.assertEqual(3, len(self.probe["calls"]))
        self.assertEqual("live_package_conflict",
                         self.probe["calls"][1]["body_fixture"])
        self.assertIs(True, self.probe["calls"][2]["assert"]["unchanged_package_license"])

    def exercise(self, mutation=None, status=200, conflict_status=409):
        calls = []
        original = {}

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", "/fair-packages"), (method, path))
                original.update(copy.deepcopy(body))
                return 200, {"result": copy.deepcopy(body)}
            if len(calls) == 2:
                self.assertEqual(("POST", "/fair-packages"), (method, path))
                self.assertEqual(original["packageDbId"], body["packageDbId"])
                self.assertNotEqual(original["license"], body["license"])
                return conflict_status, {}
            if len(calls) == 3:
                self.assertEqual(("GET", "/fair-packages/" + original["packageDbId"]),
                                 (method, path))
                stored = copy.deepcopy(original)
                if mutation is not None:
                    stored = mutation(stored)
                return status, {"result": stored}
            self.fail("unexpected extra network request")

        outcome = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, None)
        return outcome.failures, calls

    def test_original_package_intact_passes(self):
        self.assertEqual(0, self.exercise()[0])

    def test_additional_server_field_allowed(self):
        self.assertEqual(0, self.exercise(
            mutation=lambda record: {**record, "reviewed": True})[0])

    def test_altered_license_fails(self):
        self.assertEqual(1, self.exercise(
            mutation=lambda record: {**record, "license": "other"})[0])

    def test_wrong_package_identity_fails(self):
        self.assertEqual(1, self.exercise(
            mutation=lambda record: {**record,
                                     "packageDbId": "other:package:wrong"})[0])

    def test_altered_access_rights_fails(self):
        self.assertEqual(1, self.exercise(
            mutation=lambda record: {**record, "accessRights": "restricted"})[0])

    def test_altered_title_fails(self):
        self.assertEqual(1, self.exercise(
            mutation=lambda record: {**record, "title": "Modified title"})[0])

    def test_altered_identifier_fails(self):
        def change(record):
            record["identifiers"][0]["value"] = "10.1234/WRONG"
            return record
        self.assertEqual(1, self.exercise(mutation=change)[0])

    def test_altered_evidence_digest_fails(self):
        def change(record):
            record["payloadRefs"][0]["responseDigest"] = "f" * 64
            return record
        self.assertEqual(1, self.exercise(mutation=change)[0])

    def test_altered_evidence_query_digest_fails(self):
        def change(record):
            record["payloadRefs"][0]["queryDigest"] = "f" * 64
            return record
        self.assertEqual(1, self.exercise(mutation=change)[0])

    def test_altered_provenance_actor_fails(self):
        def change(record):
            record["provenance"]["actor"] = "actor:wrong"
            return record
        self.assertEqual(1, self.exercise(mutation=change)[0])

    def test_altered_provenance_digest_fails(self):
        def change(record):
            record["provenance"]["inputsDigest"] = "f" * 64
            return record
        self.assertEqual(1, self.exercise(mutation=change)[0])

    def test_missing_original_evidence_fails(self):
        def change(record):
            record.pop("payloadRefs")
            return record
        self.assertEqual(1, self.exercise(mutation=change)[0])

    def test_missing_original_provenance_fails(self):
        def change(record):
            record.pop("provenance")
            return record
        self.assertEqual(1, self.exercise(mutation=change)[0])

    def test_absent_result_fails(self):
        self.assertEqual(1, self.exercise(mutation=lambda record: None)[0])

    def test_malformed_result_fails(self):
        self.assertEqual(1, self.exercise(mutation=lambda record: [record])[0])

    def test_unavailable_readback_fails(self):
        self.assertEqual(1, self.exercise(status=404)[0])

    def test_conflicting_submit_accepted_fails(self):
        failures, calls = self.exercise(conflict_status=200)
        self.assertEqual(1, failures)
        self.assertEqual(2, len(calls))


if __name__ == "__main__":
    unittest.main()
