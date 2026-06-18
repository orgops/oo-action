# OrgOps oo Action

Run deterministic OrgOps operating-contract validation in GitHub Actions.

```yaml
- uses: actions/checkout@v4

- id: orgops
  uses: orgops/oo-action@v1
  with:
    path: .

- if: always()
  run: test -f "${{ steps.orgops.outputs.result-path }}"
```

The action exposes only `oo validate`. Repository evidence inspection remains a
local diagnostic workflow.

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `path` | `.` | Repository or regular file to validate. |
| `contract` | empty | Optional explicit local contract path. |
| `args` | empty | Additional `oo validate` arguments. |
| `oo-version` | `0.1.0` | Pinned released `orgops` package version. |
| `package-name` | `orgops` | Package providing `oo`. |
| `python-version` | `3.12` | Python runtime. |
| `skip-install` | `false` | Use an existing `oo` executable. |

## Outputs

| Output | Description |
| --- | --- |
| `status` | `pass`, `fail`, `invalid_input`, or `execution_error`. |
| `result-path` | JSON result path, including for nonzero validation outcomes. |
| `contract-digest` | Normalized contract SHA-256 digest. |
| `failed-count` | Failed decision count. |
| `unknown-count` | Unknown decision count. |
