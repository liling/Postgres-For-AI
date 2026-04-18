# GitHub Container Publishing Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add GitHub Actions automation that builds and publishes multi-architecture Docker images to GitHub Container Registry for `main` and version tags, with `arm64` support for Apple Silicon Macs.

**Architecture:** Use a single GitHub Actions workflow to build the existing `Dockerfile` with Docker Buildx, publish a multi-arch manifest to `ghcr.io`, and derive tags from branch and release context with `docker/metadata-action`. Update repository documentation and compose examples in the same change set so local usage matches the published registry source.

**Tech Stack:** GitHub Actions, Docker Buildx, GitHub Container Registry, Docker metadata-action, existing Dockerfile/Compose setup

---

### Task 1: Add the GitHub Actions publish workflow

**Files:**
- Create: `.github/workflows/docker-publish.yml`
- Reference: `Dockerfile`
- Reference: `docs/plans/2026-04-18-github-container-build-design.md`

**Step 1: Write the failing configuration mentally against requirements**

Required behaviors to encode:

```text
- Push to main publishes main + sha tags
- Push to v* tags publishes semver tags + latest
- Platforms are linux/amd64 and linux/arm64
- Registry is ghcr.io/<repo-owner>/postgres-for-ai
- Workflow uses contents:read and packages:write
```

**Step 2: Add the workflow with minimal permissions and publish triggers**

Implement `.github/workflows/docker-publish.yml` with:

```yaml
name: Publish Docker image

on:
  push:
    branches:
      - main
    tags:
      - "v*"

permissions:
  contents: read
  packages: write
```

**Step 3: Add checkout, QEMU, Buildx, GHCR login, and metadata setup**

Implement steps using:

```yaml
- uses: actions/checkout@v4
- uses: docker/setup-qemu-action@v3
- uses: docker/setup-buildx-action@v3
- uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

Add a metadata step that targets:

```text
ghcr.io/<lowercase-owner>/postgres-for-ai
```

and emits:

```text
main
sha-<short_sha>
<major>.<minor>.<patch>
<major>.<minor>
<major>
latest
```

depending on branch or tag context.

**Step 4: Add build and push with multi-arch platforms and cache**

Implement a build step equivalent to:

```yaml
- uses: docker/build-push-action@v6
  with:
    context: .
    file: ./Dockerfile
    platforms: linux/amd64,linux/arm64
    push: true
    tags: ${{ steps.meta.outputs.tags }}
    labels: ${{ steps.meta.outputs.labels }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

**Step 5: Review the final workflow for branch/tag correctness**

Check that:

```text
- latest is not emitted on main pushes
- tag pushes publish semver tags and latest
- image name does not require hardcoded owner changes
```

**Step 6: Commit**

```bash
git add .github/workflows/docker-publish.yml
git commit -m "ci: publish multi-arch images to ghcr"
```

### Task 2: Align local usage docs with GHCR publishing

**Files:**
- Modify: `README.md`
- Modify: `docker-compose.yml`

**Step 1: Write the expected user-facing behavior**

The docs must clearly tell a new user:

```text
- where to pull the image from
- which tags appear on main and releases
- that Apple Silicon is supported through arm64
```

**Step 2: Update README image references**

Change Docker pull examples from Docker Hub to:

```bash
docker pull ghcr.io/<owner>/postgres-for-ai:latest
```

Explain:

```text
- main branch publishes testable tags
- v* tags publish release tags plus latest
- amd64 and arm64 are both available
```

**Step 3: Update compose example to use GHCR**

Change the `postgres` service image to:

```yaml
image: ghcr.io/<owner>/postgres-for-ai:latest
```

If owner interpolation is not practical in compose, use a concrete placeholder form in docs and keep the file internally consistent with README guidance.

**Step 4: Review the wording for accuracy against the workflow**

Check that README statements match the actual workflow behavior exactly. Avoid claiming Docker Hub publishing or unsupported tags.

**Step 5: Commit**

```bash
git add README.md docker-compose.yml
git commit -m "docs: document ghcr image publishing"
```

### Task 3: Verify repository consistency before claiming completion

**Files:**
- Reference: `.github/workflows/docker-publish.yml`
- Reference: `README.md`
- Reference: `docker-compose.yml`

**Step 1: Run focused file inspection**

Run:

```bash
sed -n '1,240p' .github/workflows/docker-publish.yml
```

Expected:

```text
Shows triggers for main and v* tags, docker login, metadata, and multi-arch build-push configuration
```

**Step 2: Re-read the published image references**

Run:

```bash
rg -n "ghcr.io|Docker Hub|vishva123/postgres-for-ai" README.md docker-compose.yml
```

Expected:

```text
GHCR references remain where intended, and stale Docker Hub references are removed or intentionally rewritten
```

**Step 3: Check git diff**

Run:

```bash
git diff -- .github/workflows/docker-publish.yml README.md docker-compose.yml
```

Expected:

```text
Shows only the workflow and documentation changes required for GHCR publishing
```

**Step 4: Note the unverified boundary explicitly**

Record that actual `arm64` compatibility depends on GitHub Actions successfully compiling the extensions in the Dockerfile. This cannot be claimed as proven until the workflow runs on GitHub.

**Step 5: Commit**

```bash
git add .github/workflows/docker-publish.yml README.md docker-compose.yml
git commit -m "chore: finalize ghcr publishing setup"
```
