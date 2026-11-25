#!/usr/bin/env python3
"""L-27 must observe a completed job after accepting deprecated inference."""
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


class DeprecatedInferenceCompletionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        doc = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in doc["probes"] if p["id"] == "L-27")

    def test_registered_probe_requires_completion_and_warning(self):
        assertion = self.probe["calls"][1]["assert"]
        self.assertIs(True, assertion["deprecated_inference_completed"])
        self.assertEqual("WARNING", assertion["status_message"])

    def exercise(self, *, terminal_status="COMPLETED", terminal_id=None,
                 submit_status=202, include_warning=True, include_id=True,
                 missing_terminal=False, ack_mutate=None,
                 reject_before_poll=False):
        calls = []
        accepted_id = "JOB_DEPRECATED_TEST"
        model = {}
        submitted_inference = {}

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", "/models"), (method, path))
                model.update(copy.deepcopy(body))
                self.assertEqual("deprecated", model["status"])
                return 200, {"result": copy.deepcopy(body)}
            if len(calls) == 2:
                self.assertEqual(("POST", "/jobs"), (method, path))
                self.assertEqual(model["modelDbId"],
                                 body["parameters"]["modelDbId"])
                submitted_inference.update(copy.deepcopy(body))
                accepted = {
                    "jobDbId": accepted_id, "jobType": body["jobType"],
                    "idempotencyKey": body["idempotencyKey"],
                }
                if not include_id:
                    accepted.pop("jobDbId")
                if ack_mutate is not None:
                    accepted = ack_mutate(accepted)
                return submit_status, {
                    "result": accepted,
                    "metadata": {"status": (
                        [{"messageType": "WARNING", "message": "deprecated"}]
                        if include_warning else []
                    )},
                }
            self.fail("unexpected HTTP request")

        def fake_wait(_server, job_id, token):
            self.assertEqual(accepted_id, job_id)
            if missing_terminal:
                return {"result": {}}
            inputs = submitted_inference["parameters"]["inputs"]
            digest = hashlib.sha256(
                checker.canonical(inputs).encode("utf-8")).hexdigest()
            return {"result": {
                "jobDbId": terminal_id if terminal_id is not None else accepted_id,
                "status": terminal_status,
                "jobType": "inference",
                "idempotencyKey": submitted_inference["idempotencyKey"],
                "result": {"data": [{
                    "modelDbId": model["modelDbId"],
                    "modelVersion": model["modelVersion"],
                    "inputsDigest": digest,
                }]},
            }}

        outcome = checker.Results()
        with (mock.patch.object(checker, "http_call", side_effect=fake_http),
              mock.patch.object(checker, "wait_terminal", side_effect=fake_wait)
              as wait_mock):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, None)
        if reject_before_poll:
            wait_mock.assert_not_called()
        self.assertEqual(2, len(calls))
        return outcome

    def test_completed_deprecated_inference_with_warning_passes(self):
        self.assertEqual(0, self.exercise().failures)

    def test_running_job_fails(self):
        self.assertEqual(1, self.exercise(terminal_status="RUNNING").failures)

    def test_failed_job_fails(self):
        self.assertEqual(1, self.exercise(terminal_status="FAILED").failures)

    def test_expired_job_fails(self):
        self.assertEqual(1, self.exercise(terminal_status="EXPIRED").failures)

    def test_wrong_terminal_job_identity_fails(self):
        self.assertEqual(1, self.exercise(terminal_id="JOB_OTHER").failures)

    def test_terminal_job_missing_fails(self):
        self.assertEqual(1, self.exercise(missing_terminal=True).failures)

    def test_acceptance_missing_job_identifier_fails(self):
        self.assertEqual(1, self.exercise(include_id=False).failures)

    def test_initial_ack_missing_job_type_fails_before_poll(self):
        def change(accepted):
            accepted.pop("jobType")
            return accepted
        self.assertEqual(1, self.exercise(
            ack_mutate=change, reject_before_poll=True).failures)

    def test_initial_ack_wrong_job_type_fails_before_poll(self):
        self.assertEqual(1, self.exercise(
            ack_mutate=lambda a: {**a, "jobType": "analysis"},
            reject_before_poll=True).failures)

    def test_initial_ack_missing_key_fails_before_poll(self):
        def change(accepted):
            accepted.pop("idempotencyKey")
            return accepted
        self.assertEqual(1, self.exercise(
            ack_mutate=change, reject_before_poll=True).failures)

    def test_initial_ack_wrong_key_fails_before_poll(self):
        self.assertEqual(1, self.exercise(
            ack_mutate=lambda a: {**a, "idempotencyKey": "other-key"},
            reject_before_poll=True).failures)

    def test_initial_ack_nonstring_key_fails_before_poll(self):
        self.assertEqual(1, self.exercise(
            ack_mutate=lambda a: {**a, "idempotencyKey": False},
            reject_before_poll=True).failures)

    def test_initial_ack_malformed_result_fails_before_poll(self):
        self.assertEqual(1, self.exercise(
            ack_mutate=lambda a: None, reject_before_poll=True).failures)

    def test_initial_ack_additional_server_metadata_allowed(self):
        self.assertEqual(0, self.exercise(
            ack_mutate=lambda a: {**a, "createdAt": "2026-11-25T00:00:00Z"}
        ).failures)

    def test_accepted_without_warning_fails(self):
        self.assertEqual(1, self.exercise(include_warning=False).failures)

    def test_wrong_submit_status_fails(self):
        self.assertEqual(1, self.exercise(submit_status=200).failures)


if __name__ == "__main__":
    unittest.main()
