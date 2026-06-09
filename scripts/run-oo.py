#!/usr/bin/env python3
"""Run oo with a small, stable GitHub Action interface."""

from __future__ import annotations

import os
import shlex
import subprocess
import sys


SUPPORTED_COMMANDS = frozenset({"assess", "ownership", "topology", "validate"})


def write_output(name: str, value: str) -> None:
    output_file = os.environ.get("GITHUB_OUTPUT")
    if not output_file:
        return
    with open(output_file, "a", encoding="utf-8") as handle:
        handle.write(f"{name}={value}\n")


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

    result_dir = os.environ.get("RUNNER_TEMP", "").strip() or os.getcwd()
    result_path = os.path.join(result_dir, f"orgops-{command_name}-result.json")
    command = ["oo", command_name, target_path]
    if extra_args:
        command.extend(shlex.split(extra_args))
    command.extend(["--format", "json", "--output", result_path])

    write_output("result-path", result_path)
    print(f"Running: {shlex.join(command)}")
    return subprocess.call(command)


if __name__ == "__main__":
    raise SystemExit(main())
