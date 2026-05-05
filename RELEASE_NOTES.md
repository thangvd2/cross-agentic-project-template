# Release Notes

## v0.2.0 (2026-05-06)

### Changed

- **RELEASE RULES**: Enforce `python scripts/bump_version.py X.Y.Z` instead of manual version file edits
- **RELEASE RULES**: Require `python scripts/check_version_consistency.py` before and after bump
- Updated `TEMPLATE_README.md` — added `docs/` directory to file structure and customization table

### Added

- `docs/z-ai-usage-policy-reference.md` — Z.AI GLM Coding Plan usage policy reference
- `RELEASE_NOTES.md` — release history file (referenced by CONTRIBUTING.md and bump process)
- `wiki/` — project concept documentation (architecture, security, smart contracts, etc.)

## v0.1.0 (2026-04-21)

Initial release of the Cross-Agentic Development Template.

### Added

- `.ai-sync/` protocol — single source of truth for dual-AI tool coordination (OpenCode + Antigravity)
- `sync.py` — generates platform-specific configs from shared source files
- `AGENTS.md` — auto-loaded rules for OpenCode (GLM-5.1)
- `.agents/rules/` — auto-loaded rules for Antigravity (Gemini)
- `.ai-sync/workflows/` — shared code review and release procedures
- `scripts/bump_version.py` — version bumper for releases
- `scripts/check_version_consistency.py` — CI version consistency check
- `.github/workflows/ci.yml` — GitHub Actions CI pipeline
- `.pre-commit-config.yaml` — pre-commit hooks (ruff, secrets, ai-sync sync check)
- `docs/z-ai-usage-policy-reference.md` — Z.AI GLM Coding Plan usage policy reference
- `CONTRIBUTING.md` — branch rules, release process, development setup
- `TEMPLATE_README.md` — template usage guide and file structure
