#!/usr/bin/env python3
"""Regression checks for least-privilege schema generation, not a shell scanner."""
from __future__ import annotations
import copy
from pathlib import Path
import re
import unittest
import yaml

WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/generate-schema.yml"
REMOTE_WRITE = re.compile(r"\bgit\s+(?:push|commit)\b|\bgh\s+pr\s+create\b")


def permission_errors(document: dict) -> list[str]:
    errors = []
    if document.get("permissions") != {"contents": "read"}:
        errors.append("Generator requires top-level contents: read only")
    for name, job in (document.get("jobs") or {}).items():
        if "permissions" in job:
            errors.append(f"Job {name} overrides read-only permissions")
        for step in job.get("steps", []):
            if isinstance(step, dict) and REMOTE_WRITE.search(str(step.get("run", ""))):
                errors.append(f"Job {name} has a remote write command")
    return errors


class GeneratorPermissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))

    def test_existing_workflow_is_read_only(self):
        self.assertEqual([], permission_errors(self.workflow))

    def test_write_scope_is_rejected(self):
        changed = copy.deepcopy(self.workflow)
        changed["permissions"]["contents"] = "write"
        self.assertTrue(permission_errors(changed))

    def test_job_override_is_rejected(self):
        changed = copy.deepcopy(self.workflow)
        changed["jobs"]["generate"]["permissions"] = {"contents": "write"}
        self.assertTrue(any("overrides" in x for x in permission_errors(changed)))

    def test_new_remote_push_is_rejected(self):
        changed = copy.deepcopy(self.workflow)
        changed["jobs"]["generate"]["steps"].append(
            {"name": "publish", "run": "git commit -am change && git push origin"})
        self.assertTrue(any("remote write" in x for x in permission_errors(changed)))


if __name__ == "__main__":
    unittest.main()
