#!/usr/bin/env python3
"""Mission 133: returned replay identity is not proof of single stored effect."""
from __future__ import annotations

import copy
from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class JobReplaySingleStoredTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        manifest = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in manifest["probes"] if p["id"] == "L-01")

    def test_registered_probe_requires_readback_after_replay(self):
        self.assertEqual(3, len(self.probe["calls"]))
        self.assertIs(True, self.probe["calls"][1]["assert"]["same_jobDbId"])
        final = self.probe["calls"][2]
        self.assertEqual(("GET", "/jobs"), (final["method"], final["path"]))
        self.assertIs(True, final["assert"]["job_replay_single_stored"])

    def exercise(self, change_rows=None, change_page=None, read_status=200,
                 replay_id="JOB_ORIGINAL", unrelated=False):
        calls = []
        original = {}

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", "/jobs"), (method, path))
                original.update(copy.deepcopy(body))
                return 202, {"result": {
                    "jobDbId": "JOB_ORIGINAL", "jobType": body["jobType"],
                    "idempotencyKey": body["idempotencyKey"]}}
            if len(calls) == 2:
                self.assertEqual(("POST", "/jobs"), (method, path))
                self.assertEqual(original, body)
                return 200, {"result": {"jobDbId": replay_id,
                                         "jobType": body["jobType"]}}
            if len(calls) == 3:
                self.assertEqual(("GET", "/jobs"), (method, path))
                rows = [{"jobDbId": "JOB_ORIGINAL",
                         "jobType": original["jobType"],
                         "idempotencyKey": original["idempotencyKey"]}]
                if unrelated:
                    rows.append({"jobDbId": "JOB_UNRELATED",
                                 "jobType": "analysis",
                                 "idempotencyKey": "unrelated-key"})
                if change_rows is not None:
                    rows = change_rows(copy.deepcopy(rows))
                pagination = {
                    "totalCount": len(rows) if isinstance(rows, list) else 1,
                    "pageSize": 1000, "totalPages": 1, "currentPage": 0,
                }
                if change_page is not None:
                    pagination = change_page(pagination)
                return read_status, {"result": {"data": rows},
                                     "metadata": {"pagination": pagination}}
            self.fail("unexpected extra request")

        outcome = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, None)
        return outcome.failures, calls

    def test_single_original_job_passes(self):
        self.assertEqual(0, self.exercise()[0])

    def test_unrelated_historical_job_allowed(self):
        self.assertEqual(0, self.exercise(unrelated=True)[0])

    def test_duplicate_key_with_different_id_fails(self):
        def change(rows):
            rows.append({**rows[0], "jobDbId": "JOB_HIDDEN"})
            return rows
        self.assertEqual(1, self.exercise(change_rows=change)[0])

    def test_duplicate_same_id_and_key_fails(self):
        self.assertEqual(1, self.exercise(
            change_rows=lambda rows: rows + [copy.deepcopy(rows[0])])[0])

    def test_missing_stored_job_fails(self):
        self.assertEqual(1, self.exercise(change_rows=lambda rows: [])[0])

    def test_wrong_job_identifier_fails(self):
        def change(rows):
            rows[0]["jobDbId"] = "JOB_OTHER"
            return rows
        self.assertEqual(1, self.exercise(change_rows=change)[0])

    def test_wrong_idempotency_key_fails(self):
        def change(rows):
            rows[0]["idempotencyKey"] = "other-key"
            return rows
        self.assertEqual(1, self.exercise(change_rows=change)[0])

    def test_changed_job_type_fails(self):
        def change(rows):
            rows[0]["jobType"] = "different-type"
            return rows
        self.assertEqual(1, self.exercise(change_rows=change)[0])

    def test_extra_job_with_same_identifier_fails(self):
        def change(rows):
            rows.append({**rows[0], "idempotencyKey": "different-key"})
            return rows
        self.assertEqual(1, self.exercise(change_rows=change)[0])

    def test_malformed_collection_row_fails(self):
        self.assertEqual(1, self.exercise(change_rows=lambda rows: [None])[0])

    def test_missing_collection_array_fails(self):
        self.assertEqual(1, self.exercise(change_rows=lambda rows: None)[0])

    def test_unseen_second_page_fails(self):
        self.assertEqual(1, self.exercise(
            change_page=lambda p: {**p, "totalPages": 2})[0])

    def test_hidden_total_count_fails(self):
        self.assertEqual(1, self.exercise(
            change_page=lambda p: {**p, "totalCount": 2})[0])

    def test_boolean_count_fails(self):
        self.assertEqual(1, self.exercise(
            change_page=lambda p: {**p, "totalCount": True})[0])

    def test_wrong_page_index_fails(self):
        self.assertEqual(1, self.exercise(
            change_page=lambda p: {**p, "currentPage": 1})[0])

    def test_page_size_less_than_rows_fails(self):
        self.assertEqual(1, self.exercise(
            unrelated=True,
            change_page=lambda p: {**p, "pageSize": 1})[0])

    def test_readback_unavailable_fails(self):
        self.assertEqual(1, self.exercise(read_status=404)[0])

    def test_replay_returns_wrong_identifier_fails_before_get(self):
        failures, calls = self.exercise(replay_id="JOB_WRONG")
        self.assertEqual(1, failures)
        self.assertEqual(2, len(calls))


if __name__ == "__main__":
    unittest.main()
