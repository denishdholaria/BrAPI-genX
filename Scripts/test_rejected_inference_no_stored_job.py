#!/usr/bin/env python3
"""Mission 132: rejected unknown/revoked model inference stores no job."""
from __future__ import annotations

import copy
from pathlib import Path
from urllib.parse import quote
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class RejectedInferenceNoStoredJobTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        manifest = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in manifest["probes"] if p["id"] == "L-15")

    def test_registered_readback_after_both_rejections(self):
        self.assertEqual(5, len(self.probe["calls"]))
        self.assertEqual(400, self.probe["calls"][0]["assert"]["status"])
        self.assertEqual(400, self.probe["calls"][3]["assert"]["status"])
        stored = self.probe["calls"][2]
        self.assertEqual("GET", stored["method"])
        self.assertEqual(
            "/models/{revokedModelDbId}?version={revokedModelVersion}",
            stored["path"])
        self.assertIs(True, stored["assert"]["revoked_model_persisted"])
        final = self.probe["calls"][4]
        self.assertEqual(("GET", "/jobs"), (final["method"], final["path"]))
        self.assertIs(True, final["assert"]["rejected_inference_not_stored"])

    def exercise(self, create_job=None, mutate_page=None, read_status=200,
                 unknown_status=400, revoked_status=400,
                 mutate_revoked_ack=None, mutate_stored_revoked=None,
                 stored_model_status=200):
        calls = []
        rejected = []
        accepted_revoked = []

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", "/jobs"), (method, path))
                rejected.append(copy.deepcopy(body))
                self.assertEqual("inference", body["jobType"])
                return unknown_status, {}
            if len(calls) == 2:
                self.assertEqual(("POST", "/models"), (method, path))
                self.assertEqual("revoked", body["status"])
                accepted_revoked.append(copy.deepcopy(body))
                acknowledged = copy.deepcopy(body)
                if mutate_revoked_ack is not None:
                    acknowledged = mutate_revoked_ack(acknowledged)
                return 200, {"result": acknowledged}
            if len(calls) == 3:
                original = accepted_revoked[0]
                expected_path = (
                    "/models/" + quote(original["modelDbId"], safe=":")
                    + "?version=" + quote(original["modelVersion"], safe=""))
                self.assertEqual(("GET", expected_path), (method, path))
                stored = copy.deepcopy(original)
                if mutate_stored_revoked is not None:
                    stored = mutate_stored_revoked(stored)
                return stored_model_status, {"result": stored}
            if len(calls) == 4:
                self.assertEqual(("POST", "/jobs"), (method, path))
                rejected.append(copy.deepcopy(body))
                self.assertEqual(accepted_revoked[0]["modelDbId"],
                                 body["parameters"]["modelDbId"])
                self.assertNotEqual(rejected[0]["idempotencyKey"],
                                    rejected[1]["idempotencyKey"])
                return revoked_status, {}
            if len(calls) == 5:
                self.assertEqual(("GET", "/jobs"), (method, path))
                rows = [{
                    "jobDbId": "JOB_UNRELATED",
                    "jobType": "analysis",
                    "idempotencyKey": "unrelated-key",
                    "status": "COMPLETED",
                    "parameters": {"data": "unrelated"},
                }]
                if create_job is not None:
                    rows = create_job(rows, rejected)
                page = {
                    "totalCount": len(rows) if isinstance(rows, list) else 1,
                    "pageSize": 1000, "totalPages": 1, "currentPage": 0,
                }
                if mutate_page is not None:
                    page = mutate_page(page)
                return read_status, {
                    "result": {"data": rows},
                    "metadata": {"pagination": page},
                }
            self.fail("unexpected extra HTTP request")

        outcome = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, None)
        return outcome.failures, calls

    def test_both_rejections_with_no_stored_jobs_pass(self):
        failures, calls = self.exercise()
        self.assertEqual(0, failures)
        self.assertEqual(5, len(calls))

    def test_revoked_ack_changed_status_rejected_before_inference(self):
        failures, calls = self.exercise(
            mutate_revoked_ack=lambda model: {**model, "status": "active"})
        self.assertEqual((1, 2), (failures, len(calls)))

    def test_revoked_ack_changed_artifact_rejected_before_inference(self):
        failures, calls = self.exercise(
            mutate_revoked_ack=lambda model: {
                **model, "artifactDigest": "f" * 64})
        self.assertEqual((1, 2), (failures, len(calls)))

    def test_revoked_ack_dropped_field_rejected_before_inference(self):
        def change(model):
            del model["modelVersion"]
            return model
        failures, calls = self.exercise(mutate_revoked_ack=change)
        self.assertEqual((1, 2), (failures, len(calls)))

    def test_revoked_ack_nested_provenance_rejected_before_inference(self):
        def change(model):
            model["provenance"]["actor"] = "actor:other"
            return model
        failures, calls = self.exercise(mutate_revoked_ack=change)
        self.assertEqual((1, 2), (failures, len(calls)))

    def test_revoked_ack_null_result_rejected_before_inference(self):
        failures, calls = self.exercise(mutate_revoked_ack=lambda model: None)
        self.assertEqual((1, 2), (failures, len(calls)))

    def test_revoked_ack_extra_server_metadata_allowed(self):
        failures, calls = self.exercise(
            mutate_revoked_ack=lambda model: {
                **model, "serverReviewedAt": "2026-11-25T00:00:00Z"})
        self.assertEqual((0, 5), (failures, len(calls)))

    def test_revoked_model_not_persisted_fails_before_rejected_submit(self):
        failures, calls = self.exercise(stored_model_status=404)
        self.assertEqual((1, 3), (failures, len(calls)))

    def test_revoked_model_wrong_stored_status_fails_before_submit(self):
        failures, calls = self.exercise(
            mutate_stored_revoked=lambda m: {**m, "status": "active"})
        self.assertEqual((1, 3), (failures, len(calls)))

    def test_revoked_model_changed_stored_digest_fails_before_submit(self):
        failures, calls = self.exercise(
            mutate_stored_revoked=lambda m: {
                **m, "artifactDigest": "f" * 64})
        self.assertEqual((1, 3), (failures, len(calls)))

    def test_revoked_model_wrong_stored_version_fails_before_submit(self):
        failures, calls = self.exercise(
            mutate_stored_revoked=lambda m: {**m, "modelVersion": "other"})
        self.assertEqual((1, 3), (failures, len(calls)))

    def test_revoked_model_missing_stored_provenance_fails_before_submit(self):
        def change(model):
            del model["provenance"]
            return model
        failures, calls = self.exercise(mutate_stored_revoked=change)
        self.assertEqual((1, 3), (failures, len(calls)))

    def test_revoked_model_malformed_stored_result_fails_before_submit(self):
        failures, calls = self.exercise(
            mutate_stored_revoked=lambda m: None)
        self.assertEqual((1, 3), (failures, len(calls)))

    def test_revoked_model_extra_readback_metadata_allowed(self):
        failures, calls = self.exercise(
            mutate_stored_revoked=lambda m: {
                **m, "serverReadAt": "2026-11-25T00:00:00Z"})
        self.assertEqual((0, 5), (failures, len(calls)))

    def test_unrelated_stored_job_missing_status_fails(self):
        def change(rows, denied):
            rows[0].pop("status")
            return rows
        self.assertEqual(1, self.exercise(create_job=change)[0])

    def test_unrelated_stored_job_unknown_status_fails(self):
        def change(rows, denied):
            rows[0]["status"] = "QUEUED"
            return rows
        self.assertEqual(1, self.exercise(create_job=change)[0])

    def test_empty_job_collection_allowed(self):
        self.assertEqual(0, self.exercise(create_job=lambda rows, denied: [])[0])

    def test_unknown_model_job_key_is_rejected(self):
        def create(rows, denied):
            return rows + [{"jobDbId": "JOB_FORBIDDEN",
                            "jobType": "inference",
                            "idempotencyKey": denied[0]["idempotencyKey"],
                            "parameters": denied[0]["parameters"]}]
        self.assertEqual(1, self.exercise(create_job=create)[0])

    def test_revoked_model_job_key_is_rejected(self):
        def create(rows, denied):
            return rows + [{"jobDbId": "JOB_FORBIDDEN",
                            "jobType": "inference",
                            "idempotencyKey": denied[1]["idempotencyKey"],
                            "parameters": denied[1]["parameters"]}]
        self.assertEqual(1, self.exercise(create_job=create)[0])

    def test_unknown_model_job_with_different_key_is_rejected(self):
        def create(rows, denied):
            return rows + [{"jobDbId": "JOB_FORBIDDEN",
                            "jobType": "inference",
                            "idempotencyKey": "changed-server-key",
                            "parameters": denied[0]["parameters"]}]
        self.assertEqual(1, self.exercise(create_job=create)[0])

    def test_revoked_model_job_with_different_key_is_rejected(self):
        def create(rows, denied):
            return rows + [{"jobDbId": "JOB_FORBIDDEN",
                            "jobType": "inference",
                            "idempotencyKey": "changed-server-key",
                            "parameters": denied[1]["parameters"]}]
        self.assertEqual(1, self.exercise(create_job=create)[0])

    def test_job_of_other_type_with_rejected_key_is_rejected(self):
        def create(rows, denied):
            return rows + [{"jobDbId": "JOB_FORBIDDEN",
                            "jobType": "analysis",
                            "idempotencyKey": denied[1]["idempotencyKey"],
                            "parameters": {}}]
        self.assertEqual(1, self.exercise(create_job=create)[0])

    def test_unrelated_inference_job_is_allowed(self):
        def create(rows, denied):
            return rows + [{"jobDbId": "JOB_OTHER",
                            "jobType": "inference",
                            "idempotencyKey": "unrelated-key-2",
                            "status": "SUBMITTED",
                            "parameters": {"modelDbId": "different:model:allowed"}}]
        self.assertEqual(0, self.exercise(create_job=create)[0])

    def test_null_row_rejected(self):
        self.assertEqual(1, self.exercise(
            create_job=lambda rows, denied: rows + [None])[0])

    def test_missing_array_fails(self):
        self.assertEqual(1, self.exercise(
            create_job=lambda rows, denied: None)[0])

    def test_unseen_second_page_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_page=lambda p: {**p, "totalPages": 2})[0])

    def test_hidden_total_count_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_page=lambda p: {**p, "totalCount": 2})[0])

    def test_boolean_pagination_count_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_page=lambda p: {**p, "totalCount": True})[0])

    def test_wrong_page_index_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_page=lambda p: {**p, "currentPage": 1})[0])

    def test_page_too_small_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_page=lambda p: {**p, "pageSize": 0})[0])

    def test_failed_collection_get_fails(self):
        self.assertEqual(1, self.exercise(read_status=404)[0])

    def test_unknown_model_inference_accepted_fails_before_readback(self):
        failures, calls = self.exercise(unknown_status=202)
        self.assertEqual(1, failures)
        self.assertEqual(1, len(calls))

    def test_revoked_model_inference_accepted_fails_before_readback(self):
        failures, calls = self.exercise(revoked_status=202)
        self.assertEqual(1, failures)
        self.assertEqual(4, len(calls))


    def test_duplicate_unrelated_job_identifiers_fail(self):
        def change(rows, denied):
            return rows + [
                {"jobDbId": "JOB_OTHER", "jobType": "analysis",
                 "idempotencyKey": "other-2"},
                {"jobDbId": "JOB_OTHER", "jobType": "analysis",
                 "idempotencyKey": "other-3"},
            ]
        self.assertEqual(1, self.exercise(create_job=change)[0])

    def test_missing_unrelated_job_id_fails(self):
        def change(rows, denied):
            rows[0].pop("jobDbId")
            return rows
        self.assertEqual(1, self.exercise(create_job=change)[0])

    def test_blank_unrelated_job_id_fails(self):
        def change(rows, denied):
            rows[0]["jobDbId"] = ""
            return rows
        self.assertEqual(1, self.exercise(create_job=change)[0])

    def test_unrelated_job_missing_type_fails(self):
        def change(rows, denied):
            rows[0].pop("jobType")
            return rows
        self.assertEqual(1, self.exercise(create_job=change)[0])

    def test_unrelated_job_boolean_idempotency_key_fails(self):
        def change(rows, denied):
            rows[0]["idempotencyKey"] = False
            return rows
        self.assertEqual(1, self.exercise(create_job=change)[0])

    def test_unrelated_job_with_optional_missing_key_allowed(self):
        def change(rows, denied):
            rows[0].pop("idempotencyKey")
            return rows
        self.assertEqual(0, self.exercise(create_job=change)[0])

    def test_unrelated_distinct_valid_job_allowed(self):
        def change(rows, denied):
            rows.append({"jobDbId": "JOB_OTHER", "jobType": "analysis",
                         "idempotencyKey": "other-key-2", "status": "RUNNING"})
            return rows
        self.assertEqual(0, self.exercise(create_job=change)[0])



if __name__ == "__main__":
    unittest.main()
