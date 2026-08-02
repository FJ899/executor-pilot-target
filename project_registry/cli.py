"""Command-line interface for canonicalizing a project registry JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .model import Project, RegistryError
from .registry import ProjectRegistry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="project-registry")
    subparsers = parser.add_subparsers(dest="command", required=True)
    canonicalize = subparsers.add_parser(
        "canonicalize", help="validate and emit canonical registry JSON"
    )
    canonicalize.add_argument("input", type=Path)
    canonicalize.add_argument("--output", type=Path)
    return parser


def load_registry(path: Path) -> ProjectRegistry:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise RegistryError(f"cannot read input: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise RegistryError(f"invalid JSON: {exc}") from exc

    projects = payload.get("projects") if isinstance(payload, dict) else None
    if not isinstance(projects, list):
        raise RegistryError("input must contain a projects list")
    return ProjectRegistry(Project.from_mapping(item) for item in projects)


def canonicalize(input_path: Path, output_path: Path | None) -> str:
    if output_path is not None and input_path.resolve() == output_path.resolve():
        raise RegistryError("output path must differ from input path")
    result = load_registry(input_path).to_json()
    if output_path is not None:
        output_path.write_text(result, encoding="utf-8", newline="")
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = canonicalize(args.input, args.output)
    except RegistryError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2

    if args.output is None:
        sys.stdout.write(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
