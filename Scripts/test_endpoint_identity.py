#!/usr/bin/env python3
"""Mutation tests for the GenX endpoint identity and overlap guardrail.

Run: python Scripts/test_endpoint_identity.py
These tests operate on temporary synthetic API documents. They prove that the
static guardrail rejects the covered identity, route, register, and catalogue
mutations; they do not test production server readiness.
"""

import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("checkGenXConformance.py")
SPEC = importlib.util.spec_from_file_location("genx_conformance_checker", SCRIPT)
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class EndpointIdentityGuardrailTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.genx_dir = self.root / "Specification" / "BrAPI-GenX"
        self.v21_dir = self.root / "Specification" / "BrAPI-Core"
        (self.genx_dir / "Conformance").mkdir(parents=True)
        (self.genx_dir / "VariableTerms").mkdir(parents=True)
        self.v21_dir.mkdir(parents=True)

        self.genx_doc = {
            "paths": {
                "/serverinfo": {
                    "get": {
                        "operationId": "genxGetServerInfoV3",
                        "summary": "Get the GenX capability document",
                        "description": "Return the server's advertised GenX capabilities.",
                    }
                },
                "/variable-terms/{variableDbId}": {
                    "get": {
                        "operationId": "genxGetVariableTermVersion",
                        "summary": "Get a versioned variable term",
                        "description": "Return one namespaced VariableTerm version.",
                    }
                },
            }
        }
        self.v21_doc = {
            "paths": {
                "/serverinfo": {
                    "get": {
                        "operationId": "getServerInfo",
                        "summary": "Get server info",
                        "description": "Return the V2.1 server information document.",
                    }
                },
                "/variables/{observationVariableDbId}": {
                    "get": {
                        "operationId": "getObservationVariableById",
                        "summary": "Get an observation variable",
                        "description": "Return one V2.1 ObservationVariable.",
                    }
                },
            }
        }
        self.register = {
            "schema_version": 1,
            "api_base_paths": {
                "brapi_v21": "/brapi/v2",
                "genx": "/brapi/v3",
            },
            "allowed_relative_path_overlaps": [
                {
                    "method": "GET",
                    "path": "/serverinfo",
                    "genx_operation_id": "genxGetServerInfoV3",
                    "relationship": "versioned-contract-for-same-discovery-purpose",
                    "risk": "medium",
                    "rationale": "Both discover capabilities but return distinct versioned contracts.",
                }
            ],
            "semantic_neighbors": [
                {
                    "id": "SEM-TEST-01",
                    "v21_surface": "GET /brapi/v2/variables/{observationVariableDbId}",
                    "genx_surface": "GET /brapi/v3/variable-terms/{variableDbId}",
                    "relationship": "domain-neighbor-distinct-route-and-contract",
                    "risk": "high",
                    "rationale": "The resource, route, and payload contracts are not interchangeable.",
                }
            ],
        }
        self.catalogue_rows = [
            "| Full route | Method | Stable operation ID | Primary meaning | Boundary / do not infer |",
            "|---|---|---|---|---|",
            "| `/brapi/v3/serverinfo` | GET | `genxGetServerInfoV3` | Discover GenX capabilities | Not interchangeable with V2.1 serverinfo. |",
            "| `/brapi/v3/variable-terms/{variableDbId}` | GET | `genxGetVariableTermVersion` | Retrieve a versioned variable term | Not V2.1 ObservationVariable. |",
        ]
        self._write_fixtures()

    def tearDown(self):
        self.temp.cleanup()

    def _write_yaml(self, path, document):
        import yaml
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")

    def _write_fixtures(self):
        self._write_yaml(self.genx_dir / "VariableTerms" / "VariableTerms.yaml", self.genx_doc)
        self._write_yaml(self.v21_dir / "ServerInfo.yaml", self.v21_doc)
        self._write_yaml(
            self.genx_dir / "Conformance" / "endpoint-overlaps.yaml", self.register
        )
        (self.genx_dir / "ENDPOINT-IDENTITY.md").write_text(
            "# Endpoint identity test fixture\n\n## 5. Current operation catalogue\n\n" + "\n".join(self.catalogue_rows) + "\n",
            encoding="utf-8",
        )

    def _run_check(self):
        results = CHECKER.Results()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            CHECKER.check_endpoint_identity(
                str(self.root),
                {"id": "S-21", "title": "endpoint identity mutation test"},
                {},
                results,
            )
        results.output = output.getvalue()
        return results

    def test_valid_route_identity_register_and_catalogue_pass(self):
        result = self._run_check()
        self.assertEqual(result.failures, 0, result.output)

    def test_missing_operation_id_fails(self):
        self.genx_doc["paths"]["/variable-terms/{variableDbId}"]["get"].pop("operationId")
        self._write_fixtures()
        self.assertGreater(self._run_check().failures, 0)

    def test_duplicate_operation_id_fails(self):
        self.genx_doc["paths"]["/jobs"] = {
            "get": {
                "operationId": "genxGetVariableTermVersion",
                "summary": "List jobs",
                "description": "Return the caller's jobs.",
            }
        }
        self._write_fixtures()
        self.assertGreater(self._run_check().failures, 0)

    def test_unregistered_relative_path_overlap_fails(self):
        self.register["allowed_relative_path_overlaps"] = []
        self._write_fixtures()
        self.assertGreater(self._run_check().failures, 0)

    def test_stale_overlap_register_entry_fails(self):
        self.register["allowed_relative_path_overlaps"][0]["path"] = "/not-a-real-route"
        self._write_fixtures()
        self.assertGreater(self._run_check().failures, 0)

    def test_incomplete_semantic_neighbor_fails(self):
        self.register["semantic_neighbors"][0].pop("rationale")
        self._write_fixtures()
        self.assertGreater(self._run_check().failures, 0)

    def test_duplicate_normalized_genx_route_template_fails(self):
        self.genx_doc["paths"]["/variable-terms/{anotherVariableId}"] = {
            "get": {
                "operationId": "genxGetAnotherVariableTerm",
                "summary": "Get another variable term",
                "description": "This route template duplicates the existing route.",
            }
        }
        self.catalogue_rows.append(
            "| `/brapi/v3/variable-terms/{anotherVariableId}` | GET | `genxGetAnotherVariableTerm` | Duplicate route | Same normalized route template; must fail. |"
        )
        self._write_fixtures()
        self.assertGreater(self._run_check().failures, 0)

    def test_v21_operation_id_collision_fails(self):
        self.v21_doc["paths"]["/variables/{observationVariableDbId}"]["get"][
            "operationId"
        ] = "genxGetVariableTermVersion"
        self._write_fixtures()
        self.assertGreater(self._run_check().failures, 0)

    def test_catalogue_operation_id_mismatch_fails(self):
        self.catalogue_rows[3] = (
            "| `/brapi/v3/variable-terms/{variableDbId}` | GET | "
            "`genxGetWrongVariableTermVersion` | Retrieve a term | Wrong ID is being tested. |"
        )
        self._write_fixtures()
        self.assertGreater(self._run_check().failures, 0)

    def test_missing_catalogue_operation_fails(self):
        self.catalogue_rows.pop(3)
        self._write_fixtures()
        self.assertGreater(self._run_check().failures, 0)

    def test_catalogue_row_without_boundary_fails(self):
        self.catalogue_rows[3] = (
            "| `/brapi/v3/variable-terms/{variableDbId}` | GET | "
            "`genxGetVariableTermVersion` | Retrieve a versioned variable term |"
        )
        self._write_fixtures()
        self.assertGreater(self._run_check().failures, 0)

    def test_catalogue_row_without_primary_meaning_fails(self):
        self.catalogue_rows[3] = (
            "| `/brapi/v3/variable-terms/{variableDbId}` | GET | "
            "`genxGetVariableTermVersion` | | Not a V2.1 ObservationVariable. |"
        )
        self._write_fixtures()
        self.assertGreater(self._run_check().failures, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
