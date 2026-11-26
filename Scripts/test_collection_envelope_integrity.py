#!/usr/bin/env python3
"""L-25 must return paged collections containing the just-created records."""
from __future__ import annotations

import copy
from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class CollectionEnvelopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        document = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probes = document["probes"]
        cls.probe = next(p for p in cls.probes if p["id"] == "L-25")

    def test_registered_collection_assertions(self):
        self.assertEqual(
            ["jobs", "models"],
            [step["assert"]["collection_contains_created"]
             for step in self.probe["calls"][2:4]])
        self.assertIs(True, self.probe["calls"][4]["assert"][
            "filtered_expired_jobs_withheld"])
        self.assertIs(True, self.probe["calls"][5]["assert"][
            "filtered_expired_job_type_withheld"])

    def test_unknown_collection_selector_rejected(self):
        candidate = copy.deepcopy(self.probes)
        next(p for p in candidate if p["id"] == "L-25")["calls"][2][
            "assert"]["collection_contains_created"] = "unknown"
        with self.assertRaisesRegex(ValueError, "must be jobs or models"):
            checker.validate_probe_manifest(candidate)

    def exercise(self, mutate=None, bad_status=None, mutate_accepted_model=None):
        calls = []
        job_id = "JOB_COLLECTION_TEST"
        model = {}
        submitted_job = {}

        def paged(data):
            return {
                "metadata": {"pagination": {
                    "totalCount": len(data), "pageSize": max(len(data), 1),
                    "totalPages": 1, "currentPage": 0,
                }},
                "result": {"data": data},
            }

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", "/jobs"), (method, path))
                submitted_job.update(copy.deepcopy(body))
                return 202, {"result": {
                    "jobDbId": job_id, "jobType": body["jobType"],
                    "idempotencyKey": body["idempotencyKey"], "status": "SUBMITTED"}}
            if len(calls) == 2:
                self.assertEqual(("POST", "/models"), (method, path))
                model.update(copy.deepcopy(body))
                accepted = copy.deepcopy(body)
                if mutate_accepted_model is not None:
                    accepted = mutate_accepted_model(accepted)
                return 200, {"result": accepted}
            if len(calls) == 3:
                self.assertEqual(("GET", "/jobs"), (method, path))
                response = paged([{"jobDbId": job_id,
                                   "jobType": submitted_job["jobType"],
                                   "idempotencyKey": submitted_job["idempotencyKey"],
                                   "status": "SUBMITTED"}])
                return bad_status or 200, mutate("jobs", response) if mutate else response
            if len(calls) == 4:
                self.assertEqual(("GET", "/models"), (method, path))
                response = paged([copy.deepcopy(model)])
                return bad_status or 200, mutate("models", response) if mutate else response
            if len(calls) == 5:
                self.assertEqual(
                    ("GET", "/jobs?status=EXPIRED&page=0&pageSize=2"),
                    (method, path))
                response = paged([{"jobDbId": "JOB_EXPIRED",
                                   "jobType": "analysis",
                                   "status": "EXPIRED", "result": None}])
                response["metadata"]["pagination"]["pageSize"] = 2
                return bad_status or 200, (
                    mutate("filtered_jobs", response) if mutate else response)
            if len(calls) == 6:
                self.assertEqual(
                    ("GET", "/jobs?jobType=germplasm_search&status=EXPIRED&page=0&pageSize=2"),
                    (method, path))
                response = paged([{
                    "jobDbId": "JOB_EXPIRED_COMBINED",
                    "jobType": "germplasm_search",
                    "status": "EXPIRED", "result": None}])
                response["metadata"]["pagination"]["pageSize"] = 2
                return bad_status or 200, (
                    mutate("combined_jobs", response) if mutate else response)
            self.fail("unexpected extra live request")

        results = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, results, None, None)
        return results

    def test_valid_collections_pass(self):
        self.assertEqual(0, self.exercise().failures)

    def test_created_job_missing_status_rejected(self):
        def change(kind, payload):
            if kind == "jobs":
                payload["result"]["data"][0].pop("status")
            return payload
        self.assertEqual(1, self.exercise(change).failures)

    def test_created_job_invalid_status_rejected(self):
        def change(kind, payload):
            if kind == "jobs":
                payload["result"]["data"][0]["status"] = "QUEUED"
            return payload
        self.assertEqual(1, self.exercise(change).failures)

    def test_missing_data_rejected(self):
        def change(kind, payload):
            if kind == "jobs":
                payload["result"].pop("data")
            return payload
        self.assertEqual(1, self.exercise(change).failures)

    def test_missing_pagination_rejected(self):
        def change(kind, payload):
            if kind == "jobs":
                payload["metadata"].pop("pagination")
            return payload
        self.assertEqual(1, self.exercise(change).failures)

    def test_total_count_below_records_rejected(self):
        def change(kind, payload):
            if kind == "jobs":
                payload["metadata"]["pagination"]["totalCount"] = 0
            return payload
        self.assertEqual(1, self.exercise(change).failures)

    def test_zero_page_size_rejected(self):
        def change(kind, payload):
            if kind == "jobs":
                payload["metadata"]["pagination"]["pageSize"] = 0
            return payload
        self.assertEqual(1, self.exercise(change).failures)

    def test_out_of_bounds_page_number_rejected(self):
        def change(kind, payload):
            if kind == "jobs":
                payload["metadata"]["pagination"]["currentPage"] = 1
            return payload
        self.assertEqual(1, self.exercise(change).failures)

    def test_missing_created_job_rejected(self):
        def change(kind, payload):
            if kind == "jobs":
                payload["result"]["data"][0]["jobDbId"] = "OTHER"
            return payload
        self.assertEqual(1, self.exercise(change).failures)

    def test_wrong_model_version_rejected(self):
        def change(kind, payload):
            if kind == "models":
                payload["result"]["data"][0]["modelVersion"] = "WRONG"
            return payload
        self.assertEqual(1, self.exercise(change).failures)

    def test_malformed_collection_row_rejected(self):
        def change(kind, payload):
            if kind == "jobs":
                payload["result"]["data"] = [None]
            return payload
        self.assertEqual(1, self.exercise(change).failures)

    def test_non_success_http_rejected(self):
        self.assertEqual(1, self.exercise(bad_status=500).failures)


    def test_wrong_original_job_type_rejected(self):
        def change(kind, payload):
            if kind == "jobs":
                payload["result"]["data"][0]["jobType"] = "fabricated"
            return payload
        self.assertEqual(1, self.exercise(change).failures)

    def test_missing_original_idempotency_key_rejected(self):
        def change(kind, payload):
            if kind == "jobs":
                payload["result"]["data"][0].pop("idempotencyKey")
            return payload
        self.assertEqual(1, self.exercise(change).failures)

    def test_changed_model_training_digest_rejected(self):
        def change(kind, payload):
            if kind == "models":
                payload["result"]["data"][0]["trainingDataDigest"] = "f" * 64
            return payload
        self.assertEqual(1, self.exercise(change).failures)

    def test_changed_model_provenance_rejected(self):
        def change(kind, payload):
            if kind == "models":
                payload["result"]["data"][0]["provenance"]["recordedAt"] = "2026-01-01"
            return payload
        self.assertEqual(1, self.exercise(change).failures)


    def test_accepted_model_identifier_changed_rejected(self):
        self.assertEqual(1, self.exercise(
            mutate_accepted_model=lambda model: {
                **model, "modelDbId": "fabricated:model:other"}).failures)

    def test_accepted_model_version_changed_rejected(self):
        self.assertEqual(1, self.exercise(
            mutate_accepted_model=lambda model: {
                **model, "modelVersion": "999"}).failures)



if __name__ == "__main__":
    unittest.main()
