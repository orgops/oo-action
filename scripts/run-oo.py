#!/usr/bin/env python3
"""Run oo validate with a small, stable GitHub Action interface."""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys


def write_output(name: str, value: str) -> None:
    output_file = os.environ.get("GITHUB_OUTPUT")
    if not output_file:
        return
    with open(output_file, "a", encoding="utf-8") as handle:
        handle.write(f"{name}={value}\n")


def main() -> int:
    target_path = os.environ.get("OO_ACTION_PATH", ".").strip() or "."
    contract_path = os.environ.get("OO_ACTION_CONTRACT", "").strip()
    extra_args = os.environ.get("OO_ACTION_ARGS", "").strip()
    result_dir = os.environ.get("RUNNER_TEMP", "").strip() or os.getcwd()
    result_path = os.path.join(result_dir, "orgops-validate-result.json")
    command = ["oo", "validate", target_path]
    if contract_path:
        command.extend(["--contract", contract_path])
    if extra_args:
        command.extend(shlex.split(extra_args))
    command.extend(["--format", "json", "--output", result_path])

    write_output("result-path", result_path)
    print(f"Running: {shlex.join(command)}")
    completed = subprocess.run(command, check=False)
    if os.path.isfile(result_path):
        with open(result_path, encoding="utf-8") as handle:
            result = json.load(handle)["result"]
        write_output("status", str(result.get("status", "")))
        contract = result.get("contract") or {}
        summary = result.get("summary") or {}
        write_output("contract-digest", str(contract.get("digest", "")))
        write_output("failed-count", str(summary.get("failed", 0)))
        write_output("unknown-count", str(summary.get("unknown", 0)))
    else:
        print("oo validate did not produce its required JSON result.", file=sys.stderr)
        return 3
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
