#!/usr/bin/env python3
"""L-07 must compare the actual nested provenance, not a digest substring."""
from __future__ import annotations

import copy
from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class ProvenanceRoundtripTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        doc = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in doc["probes"] if p["id"] == "L-07")

    def exercise(self, mutate=None, status=200):
        calls = []
        submission = {}

        def completed_job():
            observation = copy.deepcopy(submission["parameters"]["observation"])
            job = {
                "jobDbId": "JOB_PROVENANCE_TEST",
                "jobType": submission["jobType"],
                "idempotencyKey": submission["idempotencyKey"],
                "status": "COMPLETED",
                "result": {"data": [observation]},
            }
            response = {"result": job}
            if mutate is not None:
                response = mutate(response)
            return response

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", "/jobs"), (method, path))
                submission.update(copy.deepcopy(body))
                return 202, {"result": {
                    "jobDbId": "JOB_PROVENANCE_TEST", "status": "SUBMITTED",
                    "jobType": body["jobType"],
                    "idempotencyKey": body["idempotencyKey"]}}
            if len(calls) == 2:
                self.assertEqual(("GET", "/jobs/JOB_PROVENANCE_TEST"), (method, path))
                return status, completed_job()
            self.fail("unexpected extra HTTP request")

        results = checker.Results()
        with (mock.patch.object(checker, "http_call", side_effect=fake_http),
              mock.patch.object(checker, "wait_terminal",
                                side_effect=lambda *args: completed_job())):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, results, None, None)
        self.assertEqual(2, len(calls))
        return results

    def test_original_provenance_passes(self):
        self.assertEqual(0, self.exercise().failures)

    def test_changed_inputs_digest_fails_despite_digest_elsewhere(self):
        def mutate(resp):
            obs = resp["result"]["result"]["data"][0]
            original = obs["provenance"]["inputsDigest"]
            obs["provenance"]["inputsDigest"] = "f" * 64
            resp["metadata"] = {"echoedDigest": original}
            return resp
        self.assertEqual(1, self.exercise(mutate).failures)

    def test_dropped_evidence_links_fails(self):
        def mutate(resp):
            resp["result"]["result"]["data"][0]["provenance"].pop("evidenceLinks")
            return resp
        self.assertEqual(1, self.exercise(mutate).failures)

    def test_changed_evidence_response_digest_fails(self):
        def mutate(resp):
            links = resp["result"]["result"]["data"][0]["provenance"]["evidenceLinks"]
            links[0]["responseDigest"] = "0" * 64
            return resp
        self.assertEqual(1, self.exercise(mutate).failures)

    def test_changed_evidence_query_digest_fails(self):
        def mutate(resp):
            links = resp["result"]["result"]["data"][0]["provenance"]["evidenceLinks"]
            links[0]["queryDigest"] = "0" * 64
            return resp
        self.assertEqual(1, self.exercise(mutate).failures)

    def test_changed_actor_fails(self):
        def mutate(resp):
            resp["result"]["result"]["data"][0]["provenance"]["actor"] = "actor:other"
            return resp
        self.assertEqual(1, self.exercise(mutate).failures)

    def test_removed_nested_provenance_fails(self):
        def mutate(resp):
            resp["result"]["result"]["data"][0].pop("provenance")
            return resp
        self.assertEqual(1, self.exercise(mutate).failures)

    def test_wrong_job_identity_fails(self):
        def mutate(resp):
            resp["result"]["jobDbId"] = "JOB_OTHER"
            return resp
        self.assertEqual(1, self.exercise(mutate).failures)

    def test_noncompleted_job_fails(self):
        def mutate(resp):
            resp["result"]["status"] = "RUNNING"
            return resp
        self.assertEqual(1, self.exercise(mutate).failures)

    def test_missing_observation_fails(self):
        def mutate(resp):
            resp["result"]["result"]["data"] = []
            return resp
        self.assertEqual(1, self.exercise(mutate).failures)

    def test_failed_http_response_fails(self):
        self.assertEqual(1, self.exercise(status=404).failures)


    def test_changed_observation_value_fails_with_intact_provenance(self):
        def mutate(resp):
            resp["result"]["result"]["data"][0]["value"] = "99.9"
            return resp
        self.assertEqual(1, self.exercise(mutate).failures)

    def test_changed_observation_unit_fails_with_intact_provenance(self):
        def mutate(resp):
            resp["result"]["result"]["data"][0]["observationUnitDbId"] = "OU_OTHER"
            return resp
        self.assertEqual(1, self.exercise(mutate).failures)

    def test_changed_observation_variable_fails_with_intact_provenance(self):
        def mutate(resp):
            resp["result"]["result"]["data"][0]["observationVariableDbId"] = "CO_OTHER"
            return resp
        self.assertEqual(1, self.exercise(mutate).failures)

    def test_changed_observation_identity_fails_with_intact_provenance(self):
        def mutate(resp):
            resp["result"]["result"]["data"][0]["observationDbId"] = "OBS_OTHER"
            return resp
        self.assertEqual(1, self.exercise(mutate).failures)

    def test_missing_observation_value_fails_with_intact_provenance(self):
        def mutate(resp):
            resp["result"]["result"]["data"][0].pop("value")
            return resp
        self.assertEqual(1, self.exercise(mutate).failures)

    def test_nonstring_numeric_observation_value_fails(self):
        def mutate(resp):
            resp["result"]["result"]["data"][0]["value"] = 4.2
            return resp
        self.assertEqual(1, self.exercise(mutate).failures)

    def test_wrong_completed_job_type_fails(self):
        def mutate(resp):
            resp["result"]["jobType"] = "germplasm_search"
            return resp
        self.assertEqual(1, self.exercise(mutate).failures)

    def test_wrong_completed_idempotency_key_fails(self):
        def mutate(resp):
            resp["result"]["idempotencyKey"] = "unrelated-request"
            return resp
        self.assertEqual(1, self.exercise(mutate).failures)

    def test_missing_completed_idempotency_key_fails(self):
        def mutate(resp):
            resp["result"].pop("idempotencyKey")
            return resp
        self.assertEqual(1, self.exercise(mutate).failures)

    def test_extra_server_generated_observation_field_allowed(self):
        def mutate(resp):
            resp["result"]["result"]["data"][0]["ingestedAt"] = "2026-11-25T00:00:00Z"
            return resp
        self.assertEqual(0, self.exercise(mutate).failures)

    def test_extra_returned_observation_fails(self):
        def mutate(resp):
            rows = resp["result"]["result"]["data"]
            rows.append(copy.deepcopy(rows[0]))
            return resp
        self.assertEqual(1, self.exercise(mutate).failures)



if __name__ == "__main__":
    unittest.main()
