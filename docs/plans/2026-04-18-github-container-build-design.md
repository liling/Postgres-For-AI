# GitHub Container Build Design

**Date:** 2026-04-18

## Goal

Add GitHub-native Docker image automation for this repository so that pushes to `main` publish testable images to GitHub Container Registry, and version tags publish release images plus `latest`. The published image must support both `linux/amd64` and `linux/arm64` so it runs on Apple Silicon Macs without manual platform selection.

## Current State

- The repository contains a single `Dockerfile` that builds a PostgreSQL-based image with `pgvector`, Apache AGE, and `pg_cron`.
- Local usage is documented through `docker-compose.yml`.
- The repository has no GitHub Actions workflow today.
- The current docs and compose example point at Docker Hub instead of GitHub Container Registry.

## Requirements

- Registry: `ghcr.io/<repo-owner>/postgres-for-ai`
- Trigger strategy:
  - Push to `main` publishes branch-oriented test tags
  - Git tag releases publish version tags and `latest`
- Multi-arch support:
  - `linux/amd64`
  - `linux/arm64`
- Authentication should use GitHub-native permissions and `GITHUB_TOKEN`
- The setup should work cleanly for maintainers and forks with minimal manual configuration

## Options Considered

### Option 1: Single workflow with Buildx multi-arch publish

Use one workflow that handles both branch and tag publishing with `docker/setup-qemu-action`, `docker/setup-buildx-action`, `docker/metadata-action`, and `docker/build-push-action`.

**Pros**
- Smallest configuration surface
- Easiest to maintain
- Good fit for the current repository size
- Native support for `amd64` + `arm64` manifest publishing

**Cons**
- ARM builds run through emulation on standard GitHub-hosted runners, so build time may be higher

### Option 2: Separate CI and release workflows

Split validation and publishing into two workflows.

**Pros**
- Clearer separation of responsibilities
- Easier to extend later if the project gains test jobs

**Cons**
- More operational overhead for a very small repository
- Adds structure before the project needs it

### Option 3: Per-architecture matrix builds plus manifest assembly

Build each architecture separately and merge them into a manifest list.

**Pros**
- Highest control over per-arch debugging and future optimization
- Easier to adopt native ARM runners later

**Cons**
- Most complex option
- Not justified for the repository’s current needs

## Recommended Approach

Choose **Option 1**: a single workflow that builds and publishes multi-architecture images to `ghcr.io`.

This meets every stated requirement with the least maintenance cost. The repository does not yet have a broader CI surface, so splitting the logic into multiple workflows or manifest stages would add complexity without meaningful payoff.

## Release Behavior

### `main` branch

On every push to `main`, publish:

- `ghcr.io/<owner>/postgres-for-ai:main`
- `ghcr.io/<owner>/postgres-for-ai:sha-<short_sha>`

These tags serve as continuously updated testable builds.

### Version tags

On push of tags matching `v*`, publish:

- `ghcr.io/<owner>/postgres-for-ai:<major>.<minor>.<patch>`
- `ghcr.io/<owner>/postgres-for-ai:<major>.<minor>`
- `ghcr.io/<owner>/postgres-for-ai:<major>`
- `ghcr.io/<owner>/postgres-for-ai:latest`

For example, tag `v1.2.3` would publish `1.2.3`, `1.2`, `1`, and `latest`.

## Workflow Design

Create `.github/workflows/docker-publish.yml` with:

- `on.push.branches: [main]`
- `on.push.tags: [v*]`
- minimal permissions:
  - `contents: read`
  - `packages: write`

Core steps:

1. `actions/checkout`
2. `docker/setup-qemu-action`
3. `docker/setup-buildx-action`
4. `docker/login-action` for `ghcr.io` using `${{ github.actor }}` and `${{ secrets.GITHUB_TOKEN }}`
5. `docker/metadata-action` to generate image tags and OCI labels
6. `docker/build-push-action` to build and push `linux/amd64,linux/arm64`

Recommended build settings:

- `platforms: linux/amd64,linux/arm64`
- `push: true`
- GitHub Actions cache enabled through Buildx cache parameters

## Image Naming

The image repository should be derived automatically from GitHub context so the workflow adapts to forks:

- Base image name: `ghcr.io/${{ github.repository_owner }}/postgres-for-ai`

The owner should be normalized to lowercase before publishing because container registry names are case-insensitive but often enforced as lowercase by tooling.

## Documentation Changes

Update `README.md` to:

- Replace Docker Hub pull instructions with `ghcr.io/<owner>/postgres-for-ai`
- Explain the GitHub Actions publishing behavior for `main` and version tags
- State explicit support for `linux/amd64` and `linux/arm64`
- Mention Apple Silicon Mac compatibility

Update `docker-compose.yml` to:

- Point the sample image to `ghcr.io/<owner>/postgres-for-ai`

This keeps local documentation aligned with the actual registry output.

## Risks And Mitigations

### Multi-arch compile risk

The base image likely supports both architectures, but extension compilation is the real compatibility boundary, especially:

- Apache AGE
- `pg_cron`

**Mitigation**
- Let the GitHub Actions workflow perform the real multi-arch build
- Keep the initial design simple so failures are isolated to dependency compatibility rather than workflow complexity
- If `arm64` fails, adjust extension versions or build dependencies with targeted fixes

### Publishing drift

If docs keep pointing to Docker Hub while CI publishes to GHCR, users will pull the wrong image.

**Mitigation**
- Update README and compose examples in the same change set as the workflow

## Validation Strategy

The workflow itself is the primary validation mechanism:

- Build both target platforms on GitHub Actions
- Push a manifest list to GHCR
- Verify that `main` pushes create branch tags
- Verify that release tags create semver tags and `latest`

After publishing, a maintainer should be able to run the image on an Apple Silicon Mac with a normal `docker pull` and `docker run` flow, without forcing `--platform`.

## Out Of Scope

- Splitting CI into validation and release pipelines
- Native ARM runners
- Signing images or generating SBOM/provenance attestations
- Docker Hub publishing

These can be added later if the project grows, but they are unnecessary for the initial goal.
