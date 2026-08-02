"""Domain model for the deterministic pilot registry."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Mapping


class RegistryError(ValueError):
    """Base error for invalid registry input."""


class ProjectStatus(StrEnum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    CLOSED = "CLOSED"


@dataclass(frozen=True, slots=True)
class Project:
    project_id: str
    name: str
    status: ProjectStatus = ProjectStatus.ACTIVE
    reopen_reason: str | None = None

    def __post_init__(self) -> None:
        project_id = self.project_id.strip()
        name = self.name.strip()
        reason = self.reopen_reason.strip() if self.reopen_reason else None
        if not project_id:
            raise RegistryError("project_id must not be empty")
        if not name:
            raise RegistryError("name must not be empty")
        object.__setattr__(self, "project_id", project_id)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "reopen_reason", reason)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "Project":
        try:
            raw_status = value.get("status", ProjectStatus.ACTIVE.value)
            status = ProjectStatus(str(raw_status))
            return cls(
                project_id=str(value["project_id"]),
                name=str(value["name"]),
                status=status,
                reopen_reason=(
                    str(value["reopen_reason"])
                    if value.get("reopen_reason") is not None
                    else None
                ),
            )
        except KeyError as exc:
            raise RegistryError(f"missing required field: {exc.args[0]}") from exc
        except ValueError as exc:
            raise RegistryError(f"unknown project status: {value.get('status')}") from exc

    def to_mapping(self) -> dict[str, str]:
        result = {
            "project_id": self.project_id,
            "name": self.name,
            "status": self.status.value,
        }
        if self.reopen_reason:
            result["reopen_reason"] = self.reopen_reason
        return result
