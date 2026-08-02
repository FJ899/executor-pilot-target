from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from project_registry.cli import main


class ProjectRegistryCliTests(unittest.TestCase):
    def write_payload(self, directory: Path, name: str, projects: list[dict[str, str]]) -> Path:
        path = directory / name
        path.write_text(
            json.dumps({"projects": projects}, ensure_ascii=False),
            encoding="utf-8",
        )
        return path

    def test_different_input_order_produces_identical_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            first = self.write_payload(
                directory,
                "first.json",
                [
                    {"project_id": "B", "name": "Żuraw"},
                    {"project_id": "A", "name": "Łąka"},
                ],
            )
            second = self.write_payload(
                directory,
                "second.json",
                [
                    {"project_id": "A", "name": "Łąka"},
                    {"project_id": "B", "name": "Żuraw"},
                ],
            )

            outputs: list[str] = []
            for path in (first, second):
                stdout = io.StringIO()
                with contextlib.redirect_stdout(stdout):
                    self.assertEqual(main(["canonicalize", str(path)]), 0)
                outputs.append(stdout.getvalue())

            self.assertEqual(outputs[0], outputs[1])
            self.assertIn("Łąka", outputs[0])

    def test_input_file_is_not_modified(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            source = self.write_payload(
                directory,
                "source.json",
                [{"project_id": "A", "name": "Alpha"}],
            )
            before = source.read_bytes()
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(["canonicalize", str(source)]), 0)
            self.assertEqual(source.read_bytes(), before)

    def test_duplicate_input_returns_error_without_output_file(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            source = self.write_payload(
                directory,
                "duplicate.json",
                [
                    {"project_id": "A", "name": "Alpha"},
                    {"project_id": "A", "name": "Again"},
                ],
            )
            output = directory / "result.json"
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                self.assertEqual(
                    main(["canonicalize", str(source), "--output", str(output)]),
                    2,
                )
            self.assertFalse(output.exists())
            self.assertIn("duplicate project_id", stderr.getvalue())

    def test_output_cannot_replace_input(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            source = self.write_payload(
                directory,
                "source.json",
                [{"project_id": "A", "name": "Alpha"}],
            )
            before = source.read_bytes()
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(
                    main(["canonicalize", str(source), "--output", str(source)]),
                    2,
                )
            self.assertEqual(source.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
