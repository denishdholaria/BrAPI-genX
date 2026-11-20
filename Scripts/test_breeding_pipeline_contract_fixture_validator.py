#!/usr/bin/env python3
"""Regression tests for the non-normative BreedingPipeline fixture validator.

Run from the repository root:
    python -m unittest discover -s Scripts -p 'test_breeding_pipeline_contract_fixture_validator.py' -v

These tests verify the fixture harness, not live BrAPI interoperability.
"""
from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_breeding_pipeline_contract_fixtures as validator


class BreedingPipelineFixtureValidatorTests(unittest.TestCase):
    """Test meaningful mutations instead of trusting a fixed passing corpus."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.corpus = validator.load_fixture_corpus(validator.DEFAULT_FIXTURE_PATH)
        cls.fixtures = {
            fixture["scenarioId"]: fixture for fixture in cls.corpus["fixtures"]
        }

    def scenario(self, scenario_id: str) -> dict:
        return copy.deepcopy(self.fixtures[scenario_id])

    @staticmethod
    def codes(errors: list[str]) -> set[str]:
        return {error.split(":", 1)[0] for error in errors}

    def test_current_corpus_is_consistent(self) -> None:
        self.assertEqual(validator.validate_corpus(copy.deepcopy(self.corpus)), [])

    def test_valid_authority_filters_return_empty_errors(self) -> None:
        fixture = self.scenario("valid-authority-qualified-filters-distinct-authorities")
        result = validator.validate_authority_filter_request(fixture["authorityFilterRequest"])
        self.assertIsInstance(result, list)
        self.assertEqual(result, [])
        self.assertEqual(validator.validate_fixture(fixture), [])

    def test_authority_filter_requires_matching_server(self) -> None:
        fixture = self.scenario("invalid-authority-filter-without-server")
        errors = validator.validate_authority_filter_request(fixture["authorityFilterRequest"])
        self.assertIn("BM-FILTER-01", self.codes(errors))
        self.assertIn("BM-FILTER-01", self.codes(validator.validate_fixture(fixture)))

    def test_population_filter_requires_resource_type(self) -> None:
        fixture = self.scenario("invalid-population-filter-without-resource-type")
        errors = validator.validate_authority_filter_request(fixture["authorityFilterRequest"])
        self.assertIn("BM-FILTER-02", self.codes(errors))

    def test_duplicate_authority_reference_tuple_is_rejected(self) -> None:
        fixture = self.scenario("valid-authority-qualified-filters-distinct-authorities")
        references = fixture["authorityFilterRequest"]["authorityReferences"]
        references.append(copy.deepcopy(references[0]))
        errors = validator.validate_authority_filter_request(fixture["authorityFilterRequest"])
        self.assertIn("BM-FILTER-03", self.codes(errors))

    def test_known_good_scale_evidence(self) -> None:
        fixture = self.scenario("valid-target-scale-evidence-within-bounds")
        self.assertEqual(validator.validate_fixture(fixture), [])

    def test_exact_target_binding_mismatch(self) -> None:
        fixture = self.scenario("valid-target-scale-evidence-within-bounds")
        fixture["scaleEvidence"]["targetBinding"]["traitRequirementIndex"] = 99
        self.assertIn("BM-SCALE-05", self.codes(validator.validate_fixture(fixture)))

    def test_numerical_category_compares_decimal_values(self) -> None:
        fixture = self.scenario("valid-target-scale-evidence-matches-numerical-category")
        fixture["pipelineRevision"]["targetContexts"][0]["traitRequirements"][0]["exactDecimal"] = "5.00"
        self.assertEqual(validator.validate_fixture(fixture), [])

    def test_decimal_category_match_does_not_waive_precision(self) -> None:
        fixture = self.scenario("valid-target-scale-evidence-matches-numerical-category")
        fixture["pipelineRevision"]["targetContexts"][0]["traitRequirements"][0]["exactDecimal"] = "5.000"
        self.assertIn("BM-SCALE-02", self.codes(validator.validate_fixture(fixture)))

    def test_empty_numerical_categories_are_rejected(self) -> None:
        fixture = self.scenario("valid-target-scale-evidence-matches-numerical-category")
        fixture["scaleEvidence"]["scaleProjection"]["validValues"]["categories"] = []
        self.assertIn("BM-SCALE-03", self.codes(validator.validate_fixture(fixture)))

    def test_non_decimal_numerical_category_is_rejected(self) -> None:
        fixture = self.scenario("valid-target-scale-evidence-matches-numerical-category")
        fixture["scaleEvidence"]["scaleProjection"]["validValues"]["categories"][1]["value"] = "medium"
        self.assertIn("BM-SCALE-03", self.codes(validator.validate_fixture(fixture)))

    def test_reversed_scale_bounds_are_rejected(self) -> None:
        fixture = self.scenario("valid-target-scale-evidence-within-bounds")
        fixture["scaleEvidence"]["scaleProjection"]["validValues"].update(
            minimumValue="20", maximumValue="0"
        )
        self.assertIn("BM-SCALE-01", self.codes(validator.validate_fixture(fixture)))

    def test_timestamp_requires_timezone(self) -> None:
        fixture = self.scenario("valid-target-scale-evidence-within-bounds")
        fixture["scaleEvidence"]["sourceRetrievedAt"] = "2026-11-19T06:20:00"
        self.assertIn("BM-SCALE-07", self.codes(validator.validate_fixture(fixture)))

    def test_retrieval_after_validation_is_rejected(self) -> None:
        fixture = self.scenario("valid-target-scale-evidence-within-bounds")
        fixture["scaleEvidence"]["sourceRetrievedAt"] = "2026-11-19T06:20:02Z"
        self.assertIn("BM-SCALE-07", self.codes(validator.validate_fixture(fixture)))

    def test_evidence_mutation_within_one_fixture_is_rejected(self) -> None:
        fixture = self.scenario("invalid-target-scale-evidence-mutates-same-id")
        self.assertIn("BM-SCALE-06", self.codes(validator.validate_fixture(fixture)))
        fixture["evidenceAfter"] = copy.deepcopy(fixture["evidenceBefore"])
        self.assertNotIn("BM-SCALE-06", self.codes(validator.validate_fixture(fixture)))

    def test_cross_fixture_identity_mutation_is_enforced(self) -> None:
        corpus = copy.deepcopy(self.corpus)
        fixture = next(
            item for item in corpus["fixtures"]
            if item["scenarioId"] == "invalid-evidence-identity-reused-with-different-content"
        )
        fixture["scaleEvidence"]["evidenceRecordId"] = "isolated-test-identity"
        failures = validator.validate_corpus(corpus)
        self.assertTrue(
            any(
                "invalid-evidence-identity-reused-with-different-content" in error
                and "expected invariant(s) not detected" in error
                for error in failures
            ),
            failures,
        )

    def test_cross_fixture_evidence_after_is_checked(self) -> None:
        corpus = copy.deepcopy(self.corpus)
        fixture = self.scenario("valid-target-scale-evidence-within-bounds")
        fixture["scenarioId"] = "invalid-after-snapshot-reuses-identity"
        fixture["expectation"] = "invalid"
        fixture["invariantIds"] = ["BM-SCALE-06"]
        fixture["expectedFailure"] = "Reusing an evidence identifier for changed content is invalid."
        fixture["evidenceAfter"] = copy.deepcopy(fixture["scaleEvidence"])
        fixture["evidenceAfter"]["scaleProjection"]["units"] = "kg/ha"
        corpus["fixtures"].append(fixture)
        self.assertEqual(validator.validate_corpus(corpus), [])

    def test_exact_replay_of_immutable_evidence_is_permitted(self) -> None:
        corpus = copy.deepcopy(self.corpus)
        fixture = self.scenario("valid-target-scale-evidence-within-bounds")
        fixture["scenarioId"] = "valid-repeat-identical-evidence-snapshot"
        corpus["fixtures"].append(fixture)
        self.assertEqual(validator.validate_corpus(corpus), [])

    def test_required_scenario_cannot_disappear_silently(self) -> None:
        corpus = copy.deepcopy(self.corpus)
        corpus["fixtures"] = [
            item for item in corpus["fixtures"]
            if item["scenarioId"] != "invalid-evidence-identity-reused-with-different-content"
        ]
        self.assertTrue(
            any("missing required contract scenarios" in err for err in validator.validate_corpus(corpus))
        )

    def test_duplicate_scenario_id_is_rejected(self) -> None:
        corpus = copy.deepcopy(self.corpus)
        corpus["fixtures"].append(self.scenario("valid-target-scale-evidence-within-bounds"))
        self.assertTrue(
            any("duplicate scenarioId" in err for err in validator.validate_corpus(corpus))
        )

    def test_unrelated_failure_cannot_hide_under_expected_invariant(self) -> None:
        corpus = copy.deepcopy(self.corpus)
        fixture = next(
            item for item in corpus["fixtures"]
            if item["scenarioId"] == "invalid-target-precision-exceeds-scale"
        )
        fixture["scaleEvidence"]["pipelineContext"]["breedingPipelineVersionDbId"] = "wrong-version"
        failures = validator.validate_corpus(corpus)
        self.assertTrue(
            any(
                "invalid-target-precision-exceeds-scale" in error
                and ("unrelated failure" in error or "expected invariant(s) not detected" in error)
                for error in failures
            ),
            failures,
        )

    def test_duplicate_json_object_members_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate-keys.json"
            path.write_text('{"a": 1, "a": 2}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate JSON object key"):
                validator.load_fixture_corpus(path)

    def test_non_standard_json_numbers_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid-numbers.json"
            for value in ("NaN", "Infinity", "-Infinity"):
                with self.subTest(value=value):
                    path.write_text('{"number": ' + value + '}', encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, "non-standard JSON numeric constant"):
                        validator.load_fixture_corpus(path)


if __name__ == "__main__":
    unittest.main()
