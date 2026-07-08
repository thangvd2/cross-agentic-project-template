# Contributing Guide

<!-- TODO: Replace "MyProject" with your project name throughout this file -->

## Branch Rules

- **NEVER** commit directly to `master` or `dev`. Both are protected.
- **ALWAYS** create a feature branch from `dev`:
  ```bash
  git checkout -b feature/description dev
  git checkout -b fix/description dev
  git checkout -b security/description dev
  git checkout -b refactor/description dev
  git checkout -b docs/description dev
  git checkout -b chore/description dev
  ```
- After work is done, create a PR: `gh pr create --base dev`

### PR Merge Strategy

| PR Type | Target | Merge Method | Why |
|---------|--------|-------------|-----|
| Feature | `dev` | `--squash` | 1 feature = 1 clean commit on dev |
| Release | `master` | `--merge` | Preserve shared history |

## Release Process (dev → master)

### 1. Update version on dev

```bash
git checkout dev && git pull origin dev
# Edit VERSION file with new version
python scripts/bump_version.py <new_version>
# Add entry to RELEASE_NOTES.md
git commit -m "release: vX.Y.Z — update VERSION, release notes"
git push origin dev
```

### 2. Create release branch and PR

```bash
git checkout -b release/vX.Y.Z dev
git push origin release/vX.Y.Z
gh pr create --base master --title "Release vX.Y.Z" --body "See RELEASE_NOTES.md"
```

### 3. Merge with merge commit (CRITICAL)

```bash
gh pr merge <N> --merge    # MUST be --merge, NEVER --squash
```

### 4. Tag and release

```bash
git checkout master && git pull origin master
git tag -a "vX.Y.Z" -m "Release vX.Y.Z"
git push origin "vX.Y.Z"
gh release create "vX.Y.Z" --title "vX.Y.Z" --notes-file RELEASE_NOTES.md
```

### 5. Sync dev from master (REQUIRED)

```bash
git checkout dev && git pull origin dev
git merge origin/master --no-edit
git push origin dev
```

## Development Setup

<!-- TODO: Fill in your project's setup instructions -->

```bash
# 1. Clone repository
git clone <repo-url>
cd <project-name>

# 2. Set up Python environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt

# 3. (Optional) Set up frontend
# cd web-ui && npm install

# 4. Run tests
pytest tests/ -v

# 5. Start development server
# python -m uvicorn main:app --reload
```

## PR Template

When creating a PR, include:

```markdown
## Summary
<!-- 1-3 bullet points describing what this PR does -->

## Changes
<!-- List of key changes -->

## Testing
- [ ] Unit tests pass
- [ ] Manual testing performed

## Checklist
- [ ] No hardcoded secrets
- [ ] No new lint errors
- [ ] Version bumped (if release)
```

## .ai-sync/ Workflow

This project uses `.ai-sync/` for AI tool coordination:

1. **Edit** `.ai-sync/` files (CONTEXT.md, RULES.md, etc.)
2. **Run** `python .ai-sync/sync.py` to generate platform configs
3. **Commit** both source and generated files together

> **NEVER** edit generated files (AGENTS.md, .agents/rules/) directly.
