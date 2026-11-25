#!/usr/bin/env python3
"""Mission 129: rejected matrix rewrite must leave the whole original record."""
from __future__ import annotations

import copy
from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class MatrixConflictWholeRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in source["probes"] if p["id"] == "L-17")

    def test_registered_conflict_then_readback(self):
        self.assertEqual(3, len(self.probe["calls"]))
        self.assertEqual("live_matrix_conflict",
                         self.probe["calls"][1]["body_fixture"])
        self.assertIs(True,
                      self.probe["calls"][2]["assert"]["unchanged_matrix_digest"])

    def exercise(self, mutate=None, get_status=200, conflict_status=409):
        calls = []
        submitted = {}

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", "/variantmatrices"), (method, path))
                submitted.update(copy.deepcopy(body))
                return 200, {"result": copy.deepcopy(body)}
            if len(calls) == 2:
                self.assertEqual(("POST", "/variantmatrices"), (method, path))
                self.assertEqual(submitted["matrixDbId"], body["matrixDbId"])
                self.assertNotEqual(submitted["fileDigest"], body["fileDigest"])
                return conflict_status, {}
            if len(calls) == 3:
                self.assertEqual(("GET", "/variantmatrices/" + submitted["matrixDbId"]),
                                 (method, path))
                stored = copy.deepcopy(submitted)
                if mutate:
                    stored = mutate(stored)
                return get_status, {"result": stored}
            self.fail("unexpected extra network call")

        outcome = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, None)
        return outcome.failures, calls

    def test_original_record_survives(self):
        self.assertEqual(0, self.exercise()[0])

    def test_extra_server_field_is_allowed(self):
        self.assertEqual(0, self.exercise(
            mutate=lambda record: {**record, "retrievedAt": "2026-11-25"})[0])

    def test_file_digest_mutation_fails(self):
        self.assertEqual(1, self.exercise(
            mutate=lambda record: {**record, "fileDigest": "f" * 64})[0])

    def test_wrong_record_identifier_fails(self):
        self.assertEqual(1, self.exercise(
            mutate=lambda record: {**record,
                                   "matrixDbId": "other:matrix:wrong"})[0])

    def test_changed_file_url_fails(self):
        self.assertEqual(1, self.exercise(
            mutate=lambda record: {**record, "fileURL": "drs://other"})[0])

    def test_changed_index_digest_fails(self):
        self.assertEqual(1, self.exercise(
            mutate=lambda record: {**record, "indexDigest": "f" * 64})[0])

    def test_changed_index_url_fails(self):
        self.assertEqual(1, self.exercise(
            mutate=lambda record: {**record, "indexURL": "https://wrong"})[0])

    def test_changed_access_service_endpoint_fails(self):
        def change(record):
            record["accessService"]["endpoint"] = "https://wrong"
            return record
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_changed_provenance_actor_fails(self):
        def change(record):
            record["provenance"]["actor"] = "actor:wrong"
            return record
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_changed_provenance_digest_fails(self):
        def change(record):
            record["provenance"]["inputsDigest"] = "f" * 64
            return record
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_missing_original_field_fails(self):
        def change(record):
            record.pop("variantSetDbId")
            return record
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_changed_variant_count_fails(self):
        self.assertEqual(1, self.exercise(
            mutate=lambda record: {**record, "variantCount": 999})[0])

    def test_missing_record_fails(self):
        self.assertEqual(1, self.exercise(mutate=lambda record: None)[0])

    def test_malformed_record_fails(self):
        self.assertEqual(1, self.exercise(mutate=lambda record: [record])[0])

    def test_readback_unavailable_fails(self):
        self.assertEqual(1, self.exercise(get_status=404)[0])

    def test_conflict_accepted_instead_of_rejected_fails(self):
        failed, calls = self.exercise(conflict_status=200)
        self.assertEqual(1, failed)
        self.assertEqual(2, len(calls))


if __name__ == "__main__":
    unittest.main()
