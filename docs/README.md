# Docs

Additional documentation for the OrgOps `oo` GitHub Action.

## Release Checklist

- Confirm `action.yml` has the desired Marketplace `name`, `description`, and branding.
- Confirm CI passes on the release candidate commit.
- Confirm `orgops==0.1.0` is published and verified from real PyPI.
- Create an immutable version tag, for example `v1.0.0`.
- Run consumer smoke tests against the immutable tag with passing and failing repositories.
- Move the `v1` major tag only after the immutable tag passes smoke testing.
- Draft a GitHub release from that tag.
- Select **Publish this Action to the GitHub Marketplace** in the release flow.
- Select the Marketplace category that best matches repository analysis or CI.
- Publish the release.
