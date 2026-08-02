"""Registry behavior exercised by the three Executor pilot cases."""

from __future__ import annotations

import json
from dataclasses import replace
from typing import Iterable

from .model import Project, ProjectStatus, RegistryError


class DuplicateProjectError(RegistryError):
    """Raised when a project identifier is already present."""


class InvalidTransitionError(RegistryError):
    """Raised when a status transition violates the registry rules."""


class ProjectRegistry:
    """In-memory registry with atomic batch insertion and canonical output."""

    def __init__(self, projects: Iterable[Project] = ()) -> None:
        self._projects: dict[str, Project] = {}
        self.add_many(projects)

    def __len__(self) -> int:
        return len(self._projects)

    def get(self, project_id: str) -> Project:
        try:
            return self._projects[project_id]
        except KeyError as exc:
            raise RegistryError(f"unknown project_id: {project_id}") from exc

    def add_many(self, projects: Iterable[Project]) -> None:
        """Add a batch atomically; any duplicate leaves the registry unchanged."""

        batch = list(projects)
        seen = set(self._projects)
        for project in batch:
            if project.project_id in seen:
                raise DuplicateProjectError(
                    f"duplicate project_id: {project.project_id}"
                )
            seen.add(project.project_id)

        updated = dict(self._projects)
        updated.update((project.project_id, project) for project in batch)
        self._projects = updated

    def transition(
        self,
        project_id: str,
        new_status: ProjectStatus | str,
        *,
        reopen_reason: str | None = None,
    ) -> Project:
        project = self.get(project_id)
        try:
            target = (
                new_status
                if isinstance(new_status, ProjectStatus)
                else ProjectStatus(new_status)
            )
        except ValueError as exc:
            raise RegistryError(f"unknown project status: {new_status}") from exc

        reason = reopen_reason.strip() if reopen_reason else None
        if (
            project.status is ProjectStatus.CLOSED
            and target is ProjectStatus.ACTIVE
            and not reason
        ):
            raise InvalidTransitionError(
                "CLOSED -> ACTIVE requires a non-empty reopen_reason"
            )

        changed = replace(
            project,
            status=target,
            reopen_reason=(reason if target is ProjectStatus.ACTIVE else None),
        )
        self._projects[project_id] = changed
        return changed

    def to_payload(self) -> dict[str, list[dict[str, str]]]:
        ordered = [project.to_mapping() for project in self._projects.values()]
        return {"projects": ordered}

    def to_json(self) -> str:
        """Return stable UTF-8-friendly JSON with one trailing newline."""

        return (
            json.dumps(
                self.to_payload(),
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n"
        )
