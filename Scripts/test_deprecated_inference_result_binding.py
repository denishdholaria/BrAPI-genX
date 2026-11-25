#!/usr/bin/env python3
"""Mission 140: deprecated model inference completion must bind the original request."""
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


class DeprecatedInferenceResultBindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        document = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in document["probes"] if p["id"] == "L-27")

    def test_registered_warned_inference_completion(self):
        self.assertEqual(2, len(self.probe["calls"]))
        self.assertEqual("live_model_deprecated", self.probe["calls"][0]["body_fixture"])
        self.assertIs(True, self.probe["calls"][0]["capture_model_deprecated"])
        self.assertEqual("WARNING", self.probe["calls"][1]["assert"]["status_message"])
        self.assertIs(True,
                      self.probe["calls"][1]["assert"]["deprecated_inference_completed"])

    def exercise(self, mutate_terminal=None, mutate_warning=None, acceptance_status=202,
                 mutate_model=None, modify_request=None):
        calls = []
        original_model = {}
        submitted = {}

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", "/models"), (method, path))
                original_model.update(copy.deepcopy(body))
                response = copy.deepcopy(body)
                if mutate_model is not None:
                    response = mutate_model(response)
                return 200, {"result": response}
            if len(calls) == 2:
                self.assertEqual(("POST", "/jobs"), (method, path))
                submitted.update(copy.deepcopy(body))
                if modify_request is not None:
                    # For mismatched model captures, let the runner's own
                    # baseline preconditions determine the result.
                    modify_request(submitted)
                meta = {"status": [{"messageType": "WARNING",
                                    "message": "model deprecated"}]}
                if mutate_warning:
                    meta = mutate_warning(meta)
                return acceptance_status, {"result": {"jobDbId": "JOB_WARNED"},
                                           "metadata": meta["status"] and meta or meta}
            self.fail("unexpected request")

        def fake_wait(_server, job_id, _token):
            self.assertEqual("JOB_WARNED", job_id)
            inputs = submitted["parameters"]["inputs"]
            digest = hashlib.sha256(
                checker.canonical(inputs).encode("utf-8")).hexdigest()
            job = {
                "jobDbId": job_id, "status": "COMPLETED",
                "jobType": "inference",
                "idempotencyKey": submitted["idempotencyKey"],
                "result": {"data": [{
                    "modelDbId": original_model["modelDbId"],
                    "modelVersion": original_model["modelVersion"],
                    "inputsDigest": digest,
                }]},
            }
            if mutate_terminal is not None:
                job = mutate_terminal(job)
            return {"result": job}

        results = checker.Results()
        with (mock.patch.object(checker, "http_call", side_effect=fake_http),
              mock.patch.object(checker, "wait_terminal", side_effect=fake_wait)):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, results, None, None
            )
        return results.failures, calls

    def test_correct_completed_result_passes(self):
        self.assertEqual(0, self.exercise()[0])

    def test_completed_job_id_mutation_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_terminal=lambda j: {**j, "jobDbId": "JOB_WRONG"})[0])

    def test_non_completed_status_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_terminal=lambda j: {**j, "status": "FAILED"})[0])

    def test_changed_job_type_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_terminal=lambda j: {**j, "jobType": "analysis"})[0])

    def test_changed_idempotency_key_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_terminal=lambda j: {**j, "idempotencyKey": "wrong-key"})[0])

    def test_wrong_result_model_id_fails(self):
        def change(j):
            j["result"]["data"][0]["modelDbId"] = "other:model:wrong"
            return j
        self.assertEqual(1, self.exercise(mutate_terminal=change)[0])

    def test_wrong_result_model_version_fails(self):
        def change(j):
            j["result"]["data"][0]["modelVersion"] = "42"
            return j
        self.assertEqual(1, self.exercise(mutate_terminal=change)[0])

    def test_wrong_inputs_digest_fails(self):
        def change(j):
            j["result"]["data"][0]["inputsDigest"] = "f" * 64
            return j
        self.assertEqual(1, self.exercise(mutate_terminal=change)[0])

    def test_missing_result_record_fails(self):
        def change(j):
            j["result"]["data"] = []
            return j
        self.assertEqual(1, self.exercise(mutate_terminal=change)[0])

    def test_duplicate_result_record_fails(self):
        def change(j):
            j["result"]["data"].append(copy.deepcopy(j["result"]["data"][0]))
            return j
        self.assertEqual(1, self.exercise(mutate_terminal=change)[0])

    def test_malformed_result_record_fails(self):
        def change(j):
            j["result"]["data"][0] = None
            return j
        self.assertEqual(1, self.exercise(mutate_terminal=change)[0])

    def test_missing_result_data_fails(self):
        def change(j):
            j["result"].pop("data")
            return j
        self.assertEqual(1, self.exercise(mutate_terminal=change)[0])

    def test_missing_result_object_fails(self):
        def change(j):
            j.pop("result")
            return j
        self.assertEqual(1, self.exercise(mutate_terminal=change)[0])

    def test_deprecated_model_published_with_wrong_identity_fails(self):
        self.assertEqual(1, self.exercise(mutate_model=lambda body: {
            **body, "modelDbId": "other:model:wrong"})[0])

    def test_deprecated_model_published_with_wrong_version_fails(self):
        self.assertEqual(1, self.exercise(mutate_model=lambda body: {
            **body, "modelVersion": "different"})[0])

    def test_no_warning_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_warning=lambda m: {"status": []})[0])

    def test_accepted_inference_status_must_be_202(self):
        self.assertEqual(1, self.exercise(acceptance_status=200)[0])


if __name__ == "__main__":
    unittest.main()
