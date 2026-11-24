#!/usr/bin/env python3
"""Regression checks for D-026 advisory navigation in generated catalogues."""
from __future__ import annotations

from copy import deepcopy
import unittest

from generateEndpointArtifacts import render_entry, render_catalog, render_genx_catalog


def sample_entry():
    return {
        "method": "GET",
        "basePath": "/genx/v1",
        "path": "/sample",
        "catalogId": "brapi-genx.genx.v1.sample.list",
        "recommendedOperationId": "genxListSample",
        "operationIdInSource": "genxListSample",
        "apiGeneration": "genx-v1",
        "genxModule": "Jobs",
        "classification": {},
        "semanticNeighborIds": ["genxGetSample"],
        "semanticNeighborCatalogIds": ["brapi-genx.genx.v1.sample.get"],
        "source": {"path": "Specification/BrAPI-GenX/Core/Jobs/Jobs_GET_POST.yaml"},
    }


class AdvisoryNavigationRenderingTests(unittest.TestCase):
    def test_operation_neighbors_labeled_advisory(self):
        result = "\n".join(render_entry(sample_entry()))
        self.assertIn("Advisory operation neighbors (not verified scientific relationships):", result)
        self.assertIn("genxGetSample", result)
        self.assertNotIn("Semantic relationship IDs / labels:", result)

    def test_catalogue_neighbors_labeled_advisory(self):
        result = "\n".join(render_entry(sample_entry()))
        self.assertIn("Related catalogue IDs (advisory navigation):", result)
        self.assertIn("brapi-genx.genx.v1.sample.get", result)

    def test_no_neighbor_rows_when_none_exist(self):
        row = sample_entry()
        row.pop("semanticNeighborIds")
        row.pop("semanticNeighborCatalogIds")
        result = "\n".join(render_entry(row))
        self.assertNotIn("Advisory operation neighbors", result)
        self.assertNotIn("Related catalogue IDs (advisory", result)

    def test_does_not_mutate_source_record(self):
        original = sample_entry()
        copy = deepcopy(original)
        render_entry(original)
        self.assertEqual(original, copy)

    def test_master_explains_navigation_is_not_equivalence(self):
        doc = render_catalog({"entries": [], "semanticRelationships": []})
        self.assertIn("Navigation alone does not establish scientific equivalence", doc)
        self.assertIn("Operation-neighbor IDs are advisory navigation", doc)

    def test_genx_focus_explains_navigation_boundary(self):
        doc = render_genx_catalog({"entries": [sample_entry()]})
        self.assertIn("Operation-neighbor labels below are advisory navigation", doc)
        self.assertIn("Advisory operation neighbors (not verified scientific relationships)", doc)


if __name__ == "__main__":
    unittest.main()
