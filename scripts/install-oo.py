#!/usr/bin/env python3
"""Install the Python package that provides the oo console script."""

from __future__ import annotations

import os
import shlex
import subprocess
import sys


def main() -> int:
    package_name = os.environ.get("OO_ACTION_PACKAGE_NAME", "orgops").strip()
    version = os.environ.get("OO_ACTION_OO_VERSION", "latest").strip()
    index_url = os.environ.get("OO_ACTION_PACKAGE_INDEX_URL", "").strip()
    extra_index_url = os.environ.get("OO_ACTION_EXTRA_INDEX_URL", "").strip()
    extra_args = os.environ.get("OO_ACTION_INSTALL_EXTRA_ARGS", "").strip()

    if not package_name:
        print("package-name input must not be empty", file=sys.stderr)
        return 2

    package_spec = package_name if version in {"", "latest"} else f"{package_name}=={version}"
    command = [sys.executable, "-m", "pip", "install", "--upgrade"]

    if index_url:
        command.extend(["--index-url", index_url])
    if extra_index_url:
        command.extend(["--extra-index-url", extra_index_url])
    if extra_args:
        command.extend(shlex.split(extra_args))

    command.append(package_spec)

    print(f"Installing {package_spec}")
    return subprocess.call(command)


if __name__ == "__main__":
    raise SystemExit(main())
