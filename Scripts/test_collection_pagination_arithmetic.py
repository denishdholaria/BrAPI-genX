#!/usr/bin/env python3
"""Mission 139: L-25 pagination counts must match returned first-page rows."""
from __future__ import annotations

import copy
from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class CollectionPaginationArithmeticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        document = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in document["probes"] if p["id"] == "L-25")

    def test_registered_collections_are_both_required(self):
        self.assertEqual(4, len(self.probe["calls"]))
        self.assertEqual(
            ["jobs", "models"],
            [step["assert"]["collection_contains_created"]
             for step in self.probe["calls"][-2:]],
        )

    def exercise(self, modify=None, include_unrelated=False, status=200):
        requests = []
        submitted_model = {}
        job_body = {}

        def first_page(rows):
            page_size = max(len(rows), 1)
            return {
                "metadata": {"pagination": {
                    "totalCount": len(rows), "pageSize": page_size,
                    "totalPages": 1, "currentPage": 0,
                }},
                "result": {"data": rows},
            }

        def fake_http(_server, method, path, body=None, token=None):
            requests.append((method, path))
            if len(requests) == 1:
                self.assertEqual(("POST", "/jobs"), (method, path))
                job_body.update(copy.deepcopy(body))
                return 202, {"result": {"jobDbId": "JOB_PAGE"}}
            if len(requests) == 2:
                self.assertEqual(("POST", "/models"), (method, path))
                submitted_model.update(copy.deepcopy(body))
                return 200, {"result": copy.deepcopy(body)}
            if len(requests) == 3:
                self.assertEqual(("GET", "/jobs"), (method, path))
                rows = [{"jobDbId": "JOB_PAGE", "jobType": job_body["jobType"]}]
                if include_unrelated:
                    rows.append({"jobDbId": "OTHER", "jobType": "analysis"})
                value = first_page(rows)
                if modify:
                    value = modify("jobs", value)
                return status, value
            if len(requests) == 4:
                self.assertEqual(("GET", "/models"), (method, path))
                rows = [copy.deepcopy(submitted_model)]
                if include_unrelated:
                    rows.append({**copy.deepcopy(submitted_model),
                                 "modelDbId": "other:model:unrelated"})
                value = first_page(rows)
                if modify:
                    value = modify("models", value)
                return status, value
            self.fail("unexpected extra request")

        outcome = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, None
            )
        return outcome.failures, requests

    @staticmethod
    def mutate_page(kind, target, field, value):
        if kind == "jobs":
            target["metadata"]["pagination"][field] = value
        return target

    def test_exact_single_page_passes(self):
        self.assertEqual(0, self.exercise()[0])

    def test_unrelated_records_do_not_fail(self):
        self.assertEqual(0, self.exercise(include_unrelated=True)[0])

    def test_inflated_total_count_fails(self):
        self.assertEqual(1, self.exercise(
            modify=lambda k, p: self.mutate_page(k, p, "totalCount", 50))[0])

    def test_inflated_page_size_with_missing_rows_fails(self):
        # One returned row and totalCount=3 with pageSize=100 means a
        # nominally complete first page is underfilled.
        def change(kind, data):
            if kind == "jobs":
                data["metadata"]["pagination"].update(totalCount=3, pageSize=100)
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_incorrect_total_pages_fails(self):
        self.assertEqual(1, self.exercise(
            modify=lambda k, p: self.mutate_page(k, p, "totalPages", 2))[0])

    def test_wrong_current_page_fails(self):
        def change(kind, data):
            if kind == "jobs":
                data["metadata"]["pagination"].update(
                    totalCount=2, pageSize=1, totalPages=2, currentPage=1
                )
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_invalid_page_zero_count_fails(self):
        self.assertEqual(1, self.exercise(
            modify=lambda k, p: self.mutate_page(k, p, "totalCount", 0))[0])

    def test_zero_page_size_fails(self):
        self.assertEqual(1, self.exercise(
            modify=lambda k, p: self.mutate_page(k, p, "pageSize", 0))[0])

    def test_negative_count_fails(self):
        self.assertEqual(1, self.exercise(
            modify=lambda k, p: self.mutate_page(k, p, "totalCount", -1))[0])

    def test_bool_total_fails(self):
        self.assertEqual(1, self.exercise(
            modify=lambda k, p: self.mutate_page(k, p, "totalCount", True))[0])

    def test_missing_pagination_field_fails(self):
        def change(kind, data):
            if kind == "jobs":
                data["metadata"]["pagination"].pop("pageSize")
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_malformed_page_rows_fails(self):
        def change(kind, data):
            if kind == "jobs":
                data["result"]["data"].append(None)
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_extra_rows_beyond_page_size_fails(self):
        def change(kind, data):
            if kind == "jobs":
                data["result"]["data"].append({"jobDbId": "MORE"})
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_model_collection_inconsistent_totals_fails(self):
        def change(kind, data):
            if kind == "models":
                data["metadata"]["pagination"]["totalCount"] = 9
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_missing_created_model_fails(self):
        def change(kind, data):
            if kind == "models":
                data["result"]["data"][0]["modelDbId"] = "other:model:missing"
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_missing_created_job_fails(self):
        def change(kind, data):
            if kind == "jobs":
                data["result"]["data"][0]["jobDbId"] = "OTHER"
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_failed_collection_get_fails(self):
        self.assertEqual(1, self.exercise(status=500)[0])


if __name__ == "__main__":
    unittest.main()
