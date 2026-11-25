#!/usr/bin/env python3
"""Mission 136: rejecting unknown jobType must leave no observable job record."""
from __future__ import annotations

import copy
from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class UnknownJobTypeNoStoredJobTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        doc = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in doc["probes"] if p["id"] == "L-04")

    def test_registered_rejection_checks_collection(self):
        self.assertEqual(2, len(self.probe["calls"]))
        self.assertEqual(400, self.probe["calls"][0]["assert"]["status"])
        self.assertIs(True, self.probe["calls"][1]["assert"]["unknown_job_type_not_stored"])

    def exercise(self, add_jobs=None, page_mutation=None,
                 rejection_status=400, get_status=200):
        original = {}
        calls = []

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", "/jobs"), (method, path))
                original.update(copy.deepcopy(body))
                self.assertEqual("this-door-does-not-exist", body["jobType"])
                return rejection_status, {}
            if len(calls) == 2:
                self.assertEqual(("GET", "/jobs"), (method, path))
                rows = [{"jobDbId": "JOB_UNRELATED",
                         "jobType": "analysis", "idempotencyKey": "other-key"}]
                if add_jobs is not None:
                    rows = add_jobs(rows, original)
                page = {"totalCount": len(rows) if isinstance(rows, list) else 1,
                        "pageSize": 1000, "totalPages": 1, "currentPage": 0}
                if page_mutation is not None:
                    page = page_mutation(page)
                return get_status, {"result": {"data": rows},
                                    "metadata": {"pagination": page}}
            self.fail("unexpected third request")

        outcome = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, None)
        return outcome.failures, calls

    def test_unrelated_job_allowed(self):
        self.assertEqual(0, self.exercise()[0])

    def test_empty_job_collection_allowed(self):
        self.assertEqual(0, self.exercise(add_jobs=lambda rows, req: [])[0])

    def test_same_rejected_key_with_unknown_type_fails(self):
        def change(rows, req):
            return rows + [{"jobDbId": "JOB_FORBIDDEN",
                            "jobType": req["jobType"],
                            "idempotencyKey": req["idempotencyKey"]}]
        self.assertEqual(1, self.exercise(add_jobs=change)[0])

    def test_same_rejected_key_with_changed_type_fails(self):
        def change(rows, req):
            return rows + [{"jobDbId": "JOB_FORBIDDEN",
                            "jobType": "analysis",
                            "idempotencyKey": req["idempotencyKey"]}]
        self.assertEqual(1, self.exercise(add_jobs=change)[0])

    def test_same_unknown_type_with_changed_key_fails(self):
        def change(rows, req):
            return rows + [{"jobDbId": "JOB_FORBIDDEN",
                            "jobType": req["jobType"],
                            "idempotencyKey": "server-generated-key"}]
        self.assertEqual(1, self.exercise(add_jobs=change)[0])

    def test_null_record_fails(self):
        self.assertEqual(1, self.exercise(
            add_jobs=lambda rows, req: [None])[0])

    def test_missing_collection_array_fails(self):
        self.assertEqual(1, self.exercise(
            add_jobs=lambda rows, req: None)[0])

    def test_truncated_total_count_fails(self):
        self.assertEqual(1, self.exercise(
            page_mutation=lambda p: {**p, "totalCount": 2})[0])

    def test_multi_page_collection_fails(self):
        self.assertEqual(1, self.exercise(
            page_mutation=lambda p: {**p, "totalPages": 2})[0])

    def test_wrong_current_page_fails(self):
        self.assertEqual(1, self.exercise(
            page_mutation=lambda p: {**p, "currentPage": 1})[0])

    def test_page_size_below_rows_fails(self):
        self.assertEqual(1, self.exercise(
            page_mutation=lambda p: {**p, "pageSize": 0})[0])

    def test_boolean_pagination_count_fails(self):
        self.assertEqual(1, self.exercise(
            page_mutation=lambda p: {**p, "totalCount": True})[0])

    def test_unavailable_readback_fails(self):
        self.assertEqual(1, self.exercise(get_status=404)[0])

    def test_unknown_job_type_accepted_fails_before_readback(self):
        failures, calls = self.exercise(rejection_status=202)
        self.assertEqual(1, failures)
        self.assertEqual(1, len(calls))


if __name__ == "__main__":
    unittest.main()
