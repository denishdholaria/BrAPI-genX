#!/usr/bin/env python3
"""Mutation tests for the experimental ServerInfoV3 capability contract."""

import copy
import json
import tempfile
import unittest
from pathlib import Path

import yaml

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
import importlib.util

SPEC = importlib.util.spec_from_file_location(
    "genx_capability_conformance_checker",
    SCRIPT_ROOT / "Scripts" / "checkGenXConformance.py",
)
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


def operation(method, route, operation_id):
    return {"method": method, "route": route, "operationId": operation_id}


def capability(name, methods, operations, scopes=None):
    item = {
        "name": name,
        "kind": "endpoint-family" if name == "jobs" else "embedded-contract",
        "meaning": "Test capability " + name,
        "boundary": "A synthetic fixture only.",
        "versions": ["1.0"],
        "methods": methods,
        "operations": copy.deepcopy(operations),
        "scopes": [] if scopes is None else scopes,
    }
    if name == "jobs":
        item["jobTypes"] = ["germplasm_search", "analysis"]
    return item


def baseline():
    jobs_ops = [
        operation("GET", "/genx/v1/jobs", "genxListJobs"),
        operation("POST", "/genx/v1/jobs", "genxSubmitAsyncJob"),
    ]
    embedded_ops = [operation("POST", "/genx/v1/jobs", "genxSubmitAsyncJob")]
    caps = [
        capability("jobs", ["GET", "POST"], jobs_ops, ["jobs.read", "jobs.submit"]),
        capability("provenanceEnvelope", ["POST"], embedded_ops, []),
    ]
    registry = {
        "schemaVersion": 1,
        "status": "experimental-review-only",
        "sourceOfTruth": "Specification/BrAPI-GenX/Conformance/capability-registry.json",
        "baseRoute": "/genx/v1",
        "versionPolicy": "Exact opaque tokens.",
        "methodPolicy": "Union of methods from operations.",
        "operationPolicy": "Experimental explicit route map.",
        "securityPolicy": "Scopes remain under review.",
        "capabilities": copy.deepcopy(caps),
    }
    fixture = {
        "metadata": {"pagination": {}, "status": [], "datafiles": []},
        "result": {
            "serverName": "Synthetic test server",
            "calls": [],
            "brapiVersions": ["2.1", "3.0-draft"],
            "capabilities": [
                {key: value for key, value in item.items() if key in {
                    "name", "versions", "methods", "operations", "scopes", "jobTypes"
                }}
                for item in caps
            ],
            "authProfiles": [{"name": "none", "scopes": []}],
        },
    }
    openapi = {
        "openapi": "3.0.0",
        "paths": {
            "/jobs": {
                "get": {"operationId": "genxListJobs"},
                "post": {"operationId": "genxSubmitAsyncJob"},
            }
        },
    }
    return fixture, registry, openapi


class CapabilityNegotiationGuardrailTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.genx = self.root / "Specification" / "BrAPI-GenX"
        self.conf = self.genx / "Conformance"
        (self.conf / "fixtures").mkdir(parents=True)
        (self.genx / "Jobs").mkdir(parents=True)
        (self.root / "Scripts").mkdir(parents=True)
        self.fixture, self.registry, self.openapi = baseline()
        self._write()

    def tearDown(self):
        self.temp.cleanup()

    def _write(self):
        (self.conf / "fixtures" / "serverinfov3.json").write_text(
            json.dumps(self.fixture, indent=2) + "\n", encoding="utf-8"
        )
        (self.conf / "capability-registry.json").write_text(
            json.dumps(self.registry, indent=2) + "\n", encoding="utf-8"
        )
        (self.genx / "Jobs" / "Jobs.yaml").write_text(
            yaml.safe_dump(self.openapi, sort_keys=False), encoding="utf-8"
        )
        (self.root / "Scripts" / "genx_test_server.py").write_text(
            "SUPPORTED_JOB_TYPES = ('germplasm_search', 'analysis')\n", encoding="utf-8"
        )

    def _problems(self):
        self._write()
        return CHECKER.capability_contract_problems(
            str(self.root),
            self.fixture,
            str(self.conf / "capability-registry.json"),
        )

    def test_valid_registry_and_routes_pass(self):
        self.assertEqual(self._problems(), [])

    def test_duplicate_advertised_capability_name_fails(self):
        self.fixture["result"]["capabilities"][1]["name"] = "jobs"
        self.assertTrue(self._problems())

    def test_unregistered_advertised_capability_fails(self):
        self.fixture["result"]["capabilities"].append(
            capability("mysteryCapability", ["GET"], [
                operation("GET", "/genx/v1/jobs", "genxListJobs")
            ])
        )
        self.assertTrue(self._problems())

    def test_registered_capability_missing_from_advertisement_fails(self):
        self.fixture["result"]["capabilities"].pop()
        self.assertTrue(self._problems())

    def test_duplicate_registry_capability_name_fails(self):
        self.registry["capabilities"][1]["name"] = "jobs"
        self.assertTrue(self._problems())

    def test_duplicate_registry_version_fails(self):
        self.registry["capabilities"][0]["versions"] = ["1.0", "1.0"]
        self.assertTrue(self._problems())

    def test_duplicate_capability_version_fails(self):
        self.fixture["result"]["capabilities"][0]["versions"] = ["1.0", "1.0"]
        self.assertTrue(self._problems())

    def test_malformed_version_value_fails_closed(self):
        self.fixture["result"]["capabilities"][0]["versions"] = [[]]
        self.assertTrue(self._problems())

    def test_duplicate_brapi_version_token_fails(self):
        self.fixture["result"]["brapiVersions"] = ["2.1", "2.1"]
        self.assertTrue(self._problems())

    def test_unknown_capability_version_fails(self):
        self.fixture["result"]["capabilities"][0]["versions"] = ["2.0"]
        self.assertTrue(self._problems())

    def test_missing_job_types_fails(self):
        self.fixture["result"]["capabilities"][0].pop("jobTypes")
        self.assertTrue(self._problems())

    def test_duplicate_job_types_fail(self):
        self.fixture["result"]["capabilities"][0]["jobTypes"] = ["analysis", "analysis"]
        self.assertTrue(self._problems())

    def test_malformed_job_type_fails_closed(self):
        self.fixture["result"]["capabilities"][0]["jobTypes"] = [["analysis"]]
        self.assertTrue(self._problems())

    def test_job_types_must_match_registry(self):
        self.fixture["result"]["capabilities"][0]["jobTypes"] = ["analysis"]
        self.assertTrue(self._problems())

    def test_only_jobs_capability_can_advertise_job_types(self):
        self.fixture["result"]["capabilities"][1]["jobTypes"] = ["analysis"]
        self.assertTrue(self._problems())

    def test_duplicate_registry_job_types_fail(self):
        self.registry["capabilities"][0]["jobTypes"] = ["analysis", "analysis"]
        self.assertTrue(self._problems())

    def test_non_jobs_registry_entry_cannot_advertise_job_types(self):
        self.registry["capabilities"][1]["jobTypes"] = ["analysis"]
        self.assertTrue(self._problems())

    def test_advertised_job_types_must_match_runtime_acceptance_list(self):
        candidate = ["analysis", "inference"]
        self.fixture["result"]["capabilities"][0]["jobTypes"] = candidate
        self.registry["capabilities"][0]["jobTypes"] = candidate
        problems = self._problems()
        self.assertTrue(any("SUPPORTED_JOB_TYPES differs" in problem for problem in problems))

    def test_methods_must_equal_operation_union(self):
        self.fixture["result"]["capabilities"][0]["methods"] = ["GET"]
        self.assertTrue(self._problems())

    def test_stale_route_template_fails(self):
        self.fixture["result"]["capabilities"][0]["operations"][0]["route"] = "/genx/v1/missing"
        self.assertTrue(self._problems())

    def test_operation_method_wrong_type_fails_closed(self):
        self.fixture["result"]["capabilities"][0]["operations"][0]["method"] = ["GET"]
        self.assertTrue(self._problems())

    def test_operation_id_mismatch_fails(self):
        self.fixture["result"]["capabilities"][0]["operations"][0]["operationId"] = "genxListJobsTypo"
        self.assertTrue(self._problems())

    def test_missing_operations_mapping_fails(self):
        self.fixture["result"]["capabilities"][0].pop("operations")
        self.assertTrue(self._problems())

    def test_duplicate_scope_fails(self):
        self.fixture["result"]["capabilities"][0]["scopes"] = ["jobs.read", "jobs.read"]
        self.assertTrue(self._problems())

    def test_malformed_scope_list_fails(self):
        self.fixture["result"]["capabilities"][0]["scopes"] = "jobs.read"
        self.assertTrue(self._problems())

    def test_malformed_auth_profile_scopes_fail(self):
        self.fixture["result"]["authProfiles"][0]["scopes"] = "jobs.read"
        self.assertTrue(self._problems())

    def test_duplicate_auth_profile_name_fails(self):
        self.fixture["result"]["authProfiles"].append({"name": "none", "scopes": []})
        self.assertTrue(self._problems())

    def test_duplicate_openapi_operation_id_fails(self):
        self.openapi["paths"]["/jobs"]["post"]["operationId"] = "genxListJobs"
        self.assertTrue(self._problems())

    def test_duplicate_operation_reference_fails(self):
        self.fixture["result"]["capabilities"][0]["operations"].append(
            copy.deepcopy(self.fixture["result"]["capabilities"][0]["operations"][0])
        )
        self.assertTrue(self._problems())


if __name__ == "__main__":
    unittest.main(verbosity=2)
