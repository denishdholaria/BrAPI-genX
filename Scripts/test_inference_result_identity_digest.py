#!/usr/bin/env python3
"""Mission 141: inference result must bind exact completed job and model version."""
from __future__ import annotations

import copy
import hashlib
from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class InferenceResultIdentityDigestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        doc = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in doc["probes"] if p["id"] == "L-14")

    def test_registered_probe_checks_inference_readback(self):
        self.assertEqual(3, len(self.probe["calls"]))
        self.assertIs(True, self.probe["calls"][1]["wait_terminal"])
        self.assertIs(True, self.probe["calls"][2]["assert"]["inference_intact"])

    def exercise(self, mutate=None, status=200, mutate_model_response=None,
                 mutate_submit_response=None):
        calls = []
        published = {}
        submitted = {}

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", "/models"), (method, path))
                published.update(copy.deepcopy(body))
                result = copy.deepcopy(body)
                if mutate_model_response:
                    result = mutate_model_response(result)
                return 200, {"result": result}
            if len(calls) == 2:
                self.assertEqual(("POST", "/jobs"), (method, path))
                submitted.update(copy.deepcopy(body))
                result = {"jobDbId": "JOB_INFERENCE"}
                if mutate_submit_response:
                    result = mutate_submit_response(result)
                return 202, {"result": result}
            if len(calls) == 3:
                self.assertEqual(("GET", "/jobs/JOB_INFERENCE"), (method, path))
                digest = hashlib.sha256(checker.canonical(
                    submitted["parameters"]["inputs"]).encode("utf-8")).hexdigest()
                job = {
                    "jobDbId": "JOB_INFERENCE",
                    "status": "COMPLETED",
                    "jobType": "inference",
                    "idempotencyKey": submitted["idempotencyKey"],
                    "result": {"data": [{
                        "modelDbId": published["modelDbId"],
                        "modelVersion": published["modelVersion"],
                        "inputsDigest": digest,
                    }]},
                }
                if mutate:
                    job = mutate(job)
                return status, {"result": job}
            self.fail("unexpected request")

        outcome = checker.Results()
        with (mock.patch.object(checker, "http_call", side_effect=fake_http),
              mock.patch.object(checker, "wait_terminal",
                                return_value={"result": {
                                    "jobDbId": "JOB_INFERENCE",
                                    "status": "COMPLETED"}})):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, None
            )
        return outcome.failures, calls

    def test_original_job_and_result_pass(self):
        self.assertEqual(0, self.exercise()[0])

    def test_missing_stored_job_fails(self):
        self.assertEqual(1, self.exercise(mutate=lambda j: None)[0])

    def test_malformed_stored_job_fails(self):
        self.assertEqual(1, self.exercise(mutate=lambda j: [j])[0])

    def test_wrong_completed_job_identifier_fails(self):
        self.assertEqual(1, self.exercise(
            mutate=lambda j: {**j, "jobDbId": "JOB_WRONG"})[0])

    def test_nonterminal_status_fails(self):
        self.assertEqual(1, self.exercise(
            mutate=lambda j: {**j, "status": "RUNNING"})[0])

    def test_changed_job_type_fails(self):
        self.assertEqual(1, self.exercise(
            mutate=lambda j: {**j, "jobType": "analysis"})[0])

    def test_changed_idempotency_key_fails(self):
        self.assertEqual(1, self.exercise(
            mutate=lambda j: {**j, "idempotencyKey": "wrong-key"})[0])

    def test_wrong_model_id_fails(self):
        def change(j):
            j["result"]["data"][0]["modelDbId"] = "other:model:wrong"
            return j
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_wrong_model_version_fails(self):
        def change(j):
            j["result"]["data"][0]["modelVersion"] = "other-version"
            return j
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_wrong_input_digest_fails(self):
        def change(j):
            j["result"]["data"][0]["inputsDigest"] = "f" * 64
            return j
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_missing_inference_data_fails(self):
        def change(j):
            j["result"].pop("data")
            return j
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_duplicate_inference_rows_fail(self):
        def change(j):
            j["result"]["data"].append(copy.deepcopy(j["result"]["data"][0]))
            return j
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_null_inference_row_fails(self):
        def change(j):
            j["result"]["data"] = [None]
            return j
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_wrong_model_registration_response_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_model_response=lambda m: {**m, "modelVersion": "WRONG"})[0])

    def test_accepted_job_identity_mismatch_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_submit_response=lambda j: {"jobDbId": "JOB_WRONG"})[0])

    def test_readback_http_error_fails(self):
        self.assertEqual(1, self.exercise(status=404)[0])


if __name__ == "__main__":
    unittest.main()
