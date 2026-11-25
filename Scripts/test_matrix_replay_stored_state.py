#!/usr/bin/env python3
"""Mission 126: matrix replay must retain one original stored reference."""
from __future__ import annotations

import copy
from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class MatrixReplayStoredStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        document = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in document["probes"] if p["id"] == "L-16")

    def test_registered_probe_requires_readback(self):
        self.assertEqual(3, len(self.probe["calls"]))
        self.assertIs(True, self.probe["calls"][1]["assert"]["same_matrix"])
        final = self.probe["calls"][2]
        self.assertEqual(("GET", "/variantmatrices"), (final["method"], final["path"]))
        self.assertIs(True, final["assert"]["matrix_replay_single_record"])

    def exercise(self, mutate_rows=None, mutate_page=None, read_status=200,
                 replay_identifier=None, unrelated=False):
        calls = []
        original = {}

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", "/variantmatrices"), (method, path))
                original.update(copy.deepcopy(body))
                return 200, {"result": copy.deepcopy(body)}
            if len(calls) == 2:
                self.assertEqual(("POST", "/variantmatrices"), (method, path))
                self.assertEqual(original, body)
                returned = copy.deepcopy(body)
                if replay_identifier is not None:
                    returned["matrixDbId"] = replay_identifier
                return 200, {"result": returned}
            if len(calls) == 3:
                self.assertEqual(("GET", "/variantmatrices"), (method, path))
                rows = [copy.deepcopy(original)]
                if unrelated:
                    rows.append({**copy.deepcopy(original),
                                 "matrixDbId": "external:matrix:unrelated"})
                if mutate_rows is not None:
                    rows = mutate_rows(rows)
                page = {"totalCount": len(rows) if isinstance(rows, list) else 1,
                        "pageSize": 1000, "totalPages": 1, "currentPage": 0}
                if mutate_page is not None:
                    page = mutate_page(page)
                return read_status, {
                    "result": {"data": rows}, "metadata": {"pagination": page}
                }
            self.fail("unexpected extra network request")

        outcome = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, None)
        return outcome.failures, calls

    def test_unchanged_single_matrix_passes(self):
        self.assertEqual(0, self.exercise()[0])

    def test_unrelated_matrix_can_coexist(self):
        self.assertEqual(0, self.exercise(unrelated=True)[0])

    def test_additional_server_metadata_is_allowed(self):
        self.assertEqual(0, self.exercise(
            mutate_rows=lambda rows: [{**rows[0], "auditStatus": "seen"}])[0])

    def test_duplicate_matrix_identity_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_rows=lambda rows: rows + [copy.deepcopy(rows[0])])[0])

    def test_original_matrix_missing_fails(self):
        self.assertEqual(1, self.exercise(mutate_rows=lambda rows: [])[0])

    def test_wrong_matrix_identity_fails(self):
        def modify(rows):
            rows[0]["matrixDbId"] = "other:matrix:wrong"
            return rows
        self.assertEqual(1, self.exercise(mutate_rows=modify)[0])

    def test_changed_file_digest_fails(self):
        def modify(rows):
            rows[0]["fileDigest"] = "f" * 64
            return rows
        self.assertEqual(1, self.exercise(mutate_rows=modify)[0])

    def test_changed_index_digest_fails(self):
        def modify(rows):
            rows[0]["indexDigest"] = "f" * 64
            return rows
        self.assertEqual(1, self.exercise(mutate_rows=modify)[0])

    def test_changed_access_endpoint_fails(self):
        def modify(rows):
            rows[0]["accessService"]["endpoint"] = "https://wrong.example"
            return rows
        self.assertEqual(1, self.exercise(mutate_rows=modify)[0])

    def test_changed_nested_provenance_fails(self):
        def modify(rows):
            rows[0]["provenance"]["actor"] = "actor:unexpected"
            return rows
        self.assertEqual(1, self.exercise(mutate_rows=modify)[0])

    def test_missing_original_field_fails(self):
        def modify(rows):
            rows[0].pop("indexURL")
            return rows
        self.assertEqual(1, self.exercise(mutate_rows=modify)[0])

    def test_malformed_collection_row_fails(self):
        self.assertEqual(1, self.exercise(mutate_rows=lambda rows: [None])[0])

    def test_missing_collection_array_fails(self):
        self.assertEqual(1, self.exercise(mutate_rows=lambda rows: None)[0])

    def test_incomplete_second_page_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_page=lambda page: {**page, "totalPages": 2})[0])

    def test_hidden_total_count_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_page=lambda page: {**page, "totalCount": 2})[0])

    def test_boolean_total_count_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_page=lambda page: {**page, "totalCount": True})[0])

    def test_bad_page_index_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_page=lambda page: {**page, "currentPage": 1})[0])

    def test_unavailable_read_fails(self):
        self.assertEqual(1, self.exercise(read_status=404)[0])

    def test_wrong_replay_identifier_fails_before_readback(self):
        failures, calls = self.exercise(replay_identifier="other:matrix:wrong")
        self.assertEqual(1, failures)
        self.assertEqual(2, len(calls))


if __name__ == "__main__":
    unittest.main()
