#!/usr/bin/env python3
"""Run oo with a small, stable GitHub Action interface."""

from __future__ import annotations

import os
import shlex
import subprocess
import sys
from pathlib import Path


REPORT_FILES = {
    "topology": "ORGOPS_TOPOLOGY_REPORT.md",
    "team": "ORGOPS_TEAM_REPORT.md",
    "maturity": "ORGOPS_MATURITY_REPORT.md",
}

SUPPORTED_COMMANDS = frozenset({"topology", "team", "maturity", "validate"})


def write_output(name: str, value: str) -> None:
    output_file = os.environ.get("GITHUB_OUTPUT")
    if not output_file:
        return
    with open(output_file, "a", encoding="utf-8") as handle:
        handle.write(f"{name}={value}\n")


def expected_report_path(command: str, target_path: str) -> str:
    report_name = REPORT_FILES.get(command)
    if not report_name:
        return ""

    path = Path(target_path)
    report_dir = path if path.is_dir() else path.parent
    return str(report_dir / report_name)


def main() -> int:
    command_name = os.environ.get("OO_ACTION_COMMAND", "").strip()
    target_path = os.environ.get("OO_ACTION_PATH", ".").strip() or "."
    extra_args = os.environ.get("OO_ACTION_ARGS", "").strip()

    if command_name not in SUPPORTED_COMMANDS:
        supported = ", ".join(sorted(SUPPORTED_COMMANDS))
        print(
            f"Unsupported oo command '{command_name}'. Supported commands: {supported}.",
            file=sys.stderr,
        )
        return 2

    command = ["oo", command_name, target_path]
    if extra_args:
        command.extend(shlex.split(extra_args))

    report_path = expected_report_path(command_name, target_path)
    if report_path:
        write_output("report-path", report_path)

    print(f"Running: {shlex.join(command)}")
    return subprocess.call(command)


if __name__ == "__main__":
    raise SystemExit(main())
