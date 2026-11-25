#!/usr/bin/env python3
"""Mission 134: a rejected job conflict must not mutate stored job identities."""
from __future__ import annotations

import copy
from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class JobConflictCollectionUnchangedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        registry = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in registry["probes"] if p["id"] == "L-02")

    def test_registered_probe_compares_collections(self):
        self.assertEqual(4, len(self.probe["calls"]))
        self.assertIs(True, self.probe["calls"][1]["assert"]["capture_job_collection"])
        self.assertIs(True, self.probe["calls"][2]["assert"]["rejected"])
        self.assertIs(True, self.probe["calls"][3]["assert"]["job_conflict_collection_unchanged"])

    def exercise(self, before_rows=None, after_rows=None, before_page=None,
                 after_page=None, reject_status=409, get_before_status=200,
                 get_after_status=200, change_mutable_status=False):
        calls = []
        original = {}

        def envelope(rows, change_page=None):
            page = {"totalCount": len(rows) if isinstance(rows, list) else 1,
                    "pageSize": 1000, "totalPages": 1, "currentPage": 0}
            if change_page:
                page = change_page(page)
            return {"result": {"data": rows}, "metadata": {"pagination": page}}

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", "/jobs"), (method, path))
                original.update(copy.deepcopy(body))
                return 202, {"result": {
                    "jobDbId": "JOB_ONE",
                    "jobType": body["jobType"],
                    "idempotencyKey": body["idempotencyKey"], "status": "SUBMITTED"}}
            if len(calls) == 2:
                self.assertEqual(("GET", "/jobs"), (method, path))
                rows = [{"jobDbId": "JOB_ONE",
                         "jobType": original["jobType"],
                         "idempotencyKey": original["idempotencyKey"],
                         "status": "SUBMITTED"},
                        {"jobDbId": "JOB_UNRELATED",
                         "jobType": "analysis",
                         "idempotencyKey": "unrelated-key",
                         "status": "COMPLETED"}]
                if before_rows:
                    rows = before_rows(rows)
                return get_before_status, envelope(rows, before_page)
            if len(calls) == 3:
                self.assertEqual(("POST", "/jobs"), (method, path))
                self.assertEqual(body["idempotencyKey"], original["idempotencyKey"])
                self.assertNotEqual(body, original)
                return reject_status, {}
            if len(calls) == 4:
                self.assertEqual(("GET", "/jobs"), (method, path))
                rows = [{"jobDbId": "JOB_ONE",
                         "jobType": original["jobType"],
                         "idempotencyKey": original["idempotencyKey"],
                         "status": "SUBMITTED"},
                        {"jobDbId": "JOB_UNRELATED",
                         "jobType": "analysis",
                         "idempotencyKey": "unrelated-key",
                         "status": "COMPLETED"}]
                if change_mutable_status:
                    rows[0]["status"] = "COMPLETED"
                if after_rows:
                    rows = after_rows(rows)
                return get_after_status, envelope(rows, after_page)
            self.fail("unexpected extra HTTP call")

        outcome = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, None)
        return outcome.failures, calls

    def test_identical_immutable_collection_passes(self):
        self.assertEqual(0, self.exercise()[0])

    def test_mutable_job_status_can_progress(self):
        self.assertEqual(0, self.exercise(change_mutable_status=True)[0])

    def test_server_generated_new_job_fails(self):
        def change(rows):
            rows.append({"jobDbId": "JOB_HIDDEN", "jobType": "analysis",
                         "idempotencyKey": "another-key", "status": "SUBMITTED"})
            return rows
        self.assertEqual(1, self.exercise(after_rows=change)[0])

    def test_duplicate_job_identity_fails(self):
        self.assertEqual(1, self.exercise(
            after_rows=lambda rows: rows + [copy.deepcopy(rows[0])])[0])

    def test_original_job_removed_fails(self):
        self.assertEqual(1, self.exercise(after_rows=lambda rows: rows[1:])[0])

    def test_original_job_id_rewritten_fails(self):
        def change(rows):
            rows[0]["jobDbId"] = "JOB_REWRITTEN"
            return rows
        self.assertEqual(1, self.exercise(after_rows=change)[0])

    def test_original_job_type_rewritten_fails(self):
        def change(rows):
            rows[0]["jobType"] = "changed-type"
            return rows
        self.assertEqual(1, self.exercise(after_rows=change)[0])

    def test_original_idempotency_key_rewritten_fails(self):
        def change(rows):
            rows[0]["idempotencyKey"] = "changed-key"
            return rows
        self.assertEqual(1, self.exercise(after_rows=change)[0])

    def test_other_job_mutated_fails(self):
        def change(rows):
            rows[1]["jobType"] = "changed-type"
            return rows
        self.assertEqual(1, self.exercise(after_rows=change)[0])

    def test_missing_initial_original_fails(self):
        self.assertEqual(1, self.exercise(
            before_rows=lambda rows: rows[1:])[0])

    def test_initial_duplicate_job_id_fails(self):
        self.assertEqual(1, self.exercise(
            before_rows=lambda rows: rows + [copy.deepcopy(rows[0])])[0])

    def test_null_record_fails(self):
        self.assertEqual(1, self.exercise(
            after_rows=lambda rows: rows + [None])[0])

    def test_missing_collection_array_fails(self):
        self.assertEqual(1, self.exercise(
            after_rows=lambda rows: None)[0])

    def test_incomplete_initial_collection_fails(self):
        self.assertEqual(1, self.exercise(
            before_page=lambda p: {**p, "totalPages": 2})[0])

    def test_incomplete_final_collection_fails(self):
        self.assertEqual(1, self.exercise(
            after_page=lambda p: {**p, "totalPages": 2})[0])

    def test_hidden_initial_total_count_fails(self):
        self.assertEqual(1, self.exercise(
            before_page=lambda p: {**p, "totalCount": 99})[0])

    def test_hidden_final_total_count_fails(self):
        self.assertEqual(1, self.exercise(
            after_page=lambda p: {**p, "totalCount": 99})[0])

    def test_boolean_pagination_count_fails(self):
        self.assertEqual(1, self.exercise(
            after_page=lambda p: {**p, "totalCount": True})[0])

    def test_conflict_accepted_fails_before_final_collection(self):
        failures, calls = self.exercise(reject_status=202)
        self.assertEqual(1, failures)
        self.assertEqual(3, len(calls))

    def test_server_error_is_not_a_conflict_rejection(self):
        for code in (500, 503):
            with self.subTest(code=code):
                failures, calls = self.exercise(reject_status=code)
                self.assertEqual(1, failures)
                self.assertEqual(3, len(calls))

    def test_other_client_error_still_rejected_without_new_policy(self):
        # The exact conflict status remains open in RFC-001.
        self.assertEqual(0, self.exercise(reject_status=400)[0])

    def test_initial_collection_unavailable_fails(self):
        self.assertEqual(1, self.exercise(get_before_status=404)[0])

    def test_final_collection_unavailable_fails(self):
        self.assertEqual(1, self.exercise(get_after_status=404)[0])


if __name__ == "__main__":
    unittest.main()
