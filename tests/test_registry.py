from __future__ import annotations

import json
import unittest

from project_registry import (
    DuplicateProjectError,
    InvalidTransitionError,
    Project,
    ProjectRegistry,
    ProjectStatus,
    RegistryError,
)


class ProjectRegistryTests(unittest.TestCase):
    def test_single_project_is_added(self) -> None:
        registry = ProjectRegistry([Project("A", "Alpha")])
        self.assertEqual(len(registry), 1)
        self.assertEqual(registry.get("A").name, "Alpha")

    def test_two_distinct_projects_are_added(self) -> None:
        registry = ProjectRegistry()
        registry.add_many([Project("A", "Alpha"), Project("B", "Beta")])
        self.assertEqual(len(registry), 2)

    def test_duplicate_project_id_is_rejected(self) -> None:
        registry = ProjectRegistry([Project("A", "Alpha")])
        with self.assertRaisesRegex(DuplicateProjectError, "duplicate project_id: A"):
            registry.add_many([Project("A", "Again")])

    def test_duplicate_batch_does_not_partially_mutate_registry(self) -> None:
        registry = ProjectRegistry()
        with self.assertRaises(DuplicateProjectError):
            registry.add_many(
                [Project("A", "Alpha"), Project("B", "Beta"), Project("A", "Again")]
            )
        self.assertEqual(len(registry), 0)

    def test_active_project_can_be_closed(self) -> None:
        registry = ProjectRegistry([Project("A", "Alpha")])
        changed = registry.transition("A", ProjectStatus.CLOSED)
        self.assertEqual(changed.status, ProjectStatus.CLOSED)
        self.assertIsNone(changed.reopen_reason)

    def test_closed_project_requires_reason_before_reopening(self) -> None:
        registry = ProjectRegistry([Project("A", "Alpha", ProjectStatus.CLOSED)])
        with self.assertRaises(InvalidTransitionError):
            registry.transition("A", ProjectStatus.ACTIVE)
        self.assertEqual(registry.get("A").status, ProjectStatus.CLOSED)

    def test_closed_project_can_reopen_with_reason(self) -> None:
        registry = ProjectRegistry([Project("A", "Alpha", ProjectStatus.CLOSED)])
        changed = registry.transition("A", "ACTIVE", reopen_reason="  approved retry  ")
        self.assertEqual(changed.status, ProjectStatus.ACTIVE)
        self.assertEqual(changed.reopen_reason, "approved retry")

    def test_unknown_status_is_rejected(self) -> None:
        with self.assertRaisesRegex(RegistryError, "unknown project status"):
            Project.from_mapping(
                {"project_id": "A", "name": "Alpha", "status": "MISSING"}
            )

    def test_json_output_is_sorted_stable_and_utf8_friendly(self) -> None:
        left = ProjectRegistry([Project("B", "Żuraw"), Project("A", "Łąka")])
        right = ProjectRegistry([Project("A", "Łąka"), Project("B", "Żuraw")])
        self.assertEqual(left.to_json(), right.to_json())
        self.assertIn("Łąka", left.to_json())
        self.assertTrue(left.to_json().endswith("\n"))
        parsed = json.loads(left.to_json())
        self.assertEqual(
            [item["project_id"] for item in parsed["projects"]], ["A", "B"]
        )


if __name__ == "__main__":
    unittest.main()
