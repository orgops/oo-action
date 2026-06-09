# OrgOps oo Action

Run deterministic OrgOps validation and repository analysis in GitHub Actions.
The action installs `orgops`, runs a supported `oo` command, and writes its
versioned JSON result to `result-path`.

## Validate A Repository

```yaml
name: OrgOps

on:
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - id: orgops
        uses: orgops/oo-action@v1
        with:
          command: validate
          path: .

      - run: test -f "${{ steps.orgops.outputs.result-path }}"
```

`validate` is the primary CI and agent workflow. The action also supports
`topology`, `ownership`, and `assess`.

The pre-release names `team` and `maturity` are unsupported. `drift` and `why`
are not part of v1.

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `command` | required | `validate`, `topology`, `ownership`, or `assess`. |
| `path` | `.` | Repository path or file path passed to `oo`. |
| `args` | empty | Additional command arguments, such as `--branch main`. |
| `oo-version` | `latest` | Released `orgops` package version to install. |
| `package-name` | `orgops` | Package that provides the `oo` script. |
| `python-version` | `3.12` | Python version used by the action. |
| `package-index-url` | empty | Optional package index URL. |
| `extra-index-url` | empty | Optional extra package index URL. |
| `install-extra-args` | empty | Additional `pip install` flags. |
| `skip-install` | `false` | Use an `oo` executable already available on `PATH`. |

## Output

| Output | Description |
| --- | --- |
| `result-path` | Path to the versioned JSON result produced by `oo`. |

```json
{
  "schema_version": "v1",
  "command": "validate",
  "result": {}
}
```

The action does not create or depend on Markdown reports.

## Examples

```yaml
- uses: orgops/oo-action@v1
  with:
    command: assess
    path: .
    oo-version: "1.0.0"
```

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.12"

- run: python -m pip install .

- uses: orgops/oo-action@v1
  with:
    command: validate
    path: README.md
    skip-install: "true"
```

```yaml
- uses: orgops/oo-action@v1
  with:
    command: topology
    path: .
    args: "--branch main"
```
