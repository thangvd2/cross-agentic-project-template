# Cross-Agentic Development Template

> A reusable project skeleton with built-in dual-AI (OpenCode + Antigravity) workflow support.
> Extracted from real-world production patterns proven in the V-Pack Monitor project.

---

## What Is This?

This template provides a complete project skeleton that supports **simultaneous use of two AI coding tools** — [OpenCode](https://opencode.ai) (GLM-5.1) and [Antigravity](https://antigravity.google) (Gemini) — on the same codebase without conflicts.

The core innovation is the **`.ai-sync/` protocol**: a set of shared source files that `sync.py` compiles into platform-specific configuration files for each AI tool. This means:

- **One source of truth** for rules, context, and workflows
- **Zero conflicts** when switching between AI tools mid-project
- **Session continuity** via HANDOFF.md — pick up exactly where you left off
- **Structured memory** — lessons learned persist across sessions and tools

## Quick Start

### 1. Copy this template

```bash
# Copy the entire template to your new project directory
cp -r cross_agentic_project_template/ /path/to/my-new-project/
cd /path/to/my-new-project/
```

### 2. Customize project identity

Edit `.ai-sync/CONTEXT.md`:
- Replace `<!-- TODO: Replace -->` markers with your project name, description, and tech stack
- Choose your tech stack option (Python / Node / Fullstack)
- Adjust language preferences

### 3. Customize rules (optional)

Edit `.ai-sync/RULES.md`:
- The default rules are battle-tested and generic — you may not need to change anything
- Adjust TODO markers for test/lint commands
- Add project-specific rules as needed

### 4. Generate platform configs

```bash
python .ai-sync/sync.py
```

This generates:
- `AGENTS.md` — auto-loaded by OpenCode
- `.agents/rules/project-rules.md` — loaded by Antigravity
- `.agents/rules/platform-antigravity.md` — Antigravity-specific rules
- `.agents/workflows/` — shared workflow files

### 5. Initialize git

```bash
git init
git add .
git commit -m "init: project scaffold from cross-agentic template"
git branch -M master
git branch dev master
git push -u origin master
git push -u origin dev
```

### 6. Start coding

Open the project in both OpenCode and Antigravity. Both will automatically load their respective rules.

---

## File Structure

```
cross_agentic_project_template/
├── .ai-sync/                          ← YOU EDIT HERE (single source of truth)
│   ├── CONTEXT.md                     ← Project overview, tech stack, constraints
│   ├── RULES.md                       ← Shared coding rules (both platforms)
│   ├── MEMORY.md                      ← Learned lessons (episodic/procedural)
│   ├── TASKS.md                       ← Cross-tool task tracking
│   ├── HANDOFF.md                     ← Session handoff between tools
│   ├── sync.py                        ← Generates platform configs
│   ├── README.md                      ← Full .ai-sync/ documentation
│   ├── extensions/
│   │   ├── opencode.md                ← OpenCode-specific rules (→ AGENTS.md)
│   │   └── antigravity.md             ← Antigravity-specific rules (→ .agents/rules/)
│   └── workflows/
│       ├── code-review.md             ← Shared code review procedure
│       └── release.md                 ← Shared release procedure
├── .github/
│   └── workflows/
│       └── ci.yml                     ← GitHub Actions CI pipeline
├── docs/
│   └── z-ai-usage-policy-reference.md ← Z.AI usage policy reference
├── scripts/
│   ├── bump_version.py                ← Version bumper for releases
│   └── check_version_consistency.py   ← CI check: all versions match
├── .pre-commit-config.yaml            ← Pre-commit hooks (ruff, secrets, ai-sync)
├── .gitignore                         ← Comprehensive gitignore template
├── ruff.toml                          ← Python linter configuration
├── VERSION                            ← Current version (v0.1.0)
├── CONTRIBUTING.md                    ← Branch rules, release process, setup guide
└── TEMPLATE_README.md                 ← This file (usage guide)
```

---

## What to Customize

| File | What to Change | What NOT to Change |
|------|---------------|-------------------|
| `.ai-sync/CONTEXT.md` | Project name, description, tech stack | Structure, format |
| `.ai-sync/RULES.md` | Test/lint commands, project-specific rules | Branch rules, review process |
| `.ai-sync/MEMORY.md` | Add entries as you learn | Structure, format |
| `.ai-sync/TASKS.md` | Add tasks as you work | Task protocol section |
| `.ai-sync/HANDOFF.md` | Session info at start/end of sessions | Handoff protocol section |
| `.ai-sync/sync.py` | Nothing — this is already generic | Everything |
| `.ai-sync/README.md` | Nothing — this is documentation | Everything |
| `.ai-sync/extensions/` | Nothing — these are already generic | Everything |
| `.ai-sync/workflows/` | Nothing — these are already generic | Everything |
| `scripts/bump_version.py` | `PROJECT_NAME`, `FRONTEND_DIR` | Structure, logic |
| `scripts/check_version_consistency.py` | `PROJECT_NAME`, `FRONTEND_DIR` | Structure, logic |
| `.github/workflows/ci.yml` | Uncomment frontend section, adjust env vars | Structure, jobs |
| `.pre-commit-config.yaml` | Uncomment frontend hooks | Core hooks |
| `CONTRIBUTING.md` | Setup instructions, project name | Branch/release rules |
| `docs/` | Add project-specific documentation | z-ai-usage-policy-reference.md |
| `ruff.toml` | Lint rules if needed | Baseline rules |
| `.gitignore` | Add project-specific patterns | Existing patterns |
| `VERSION` | Update on releases | Format (vX.Y.Z) |

---

## Dual-AI Workflow

### OpenCode = Reviewer & Architect

OpenCode excels at:
- **Code review** with 2-pass process (flag → verify)
- **Architecture decisions** with full dependency tracing
- **Subagent delegation** — fire explore/librarian agents in parallel
- **LSP integration** — diagnostics, references, AST search
- **Plan-before-execute** pattern

### Antigravity = Executor & Implementer

Antigravity excels at:
- **Feature implementation** with agent personas (Dev, DevOps, Review)
- **Terminal commands** with configurable allow/deny policies
- **Workflow automation** via `/workflow-name` slash commands
- **Planning vs Fast modes** for task complexity matching

### How They Coordinate

```
┌──────────────┐     HANDOFF.md     ┌──────────────┐
│   OpenCode    │ ◄──────────────► │  Antigravity  │
│  (Reviewer)   │                   │  (Executor)   │
├──────────────┤                   ├──────────────┤
│ Reads:        │                   │ Reads:        │
│  AGENTS.md    │                   │  .agents/     │
│               │                   │   rules/      │
│ Writes:       │                   │               │
│  HANDOFF.md   │                   │ Writes:       │
│  MEMORY.md    │                   │  HANDOFF.md   │
│  TASKS.md     │                   │  MEMORY.md    │
└──────────────┘                   └──────────────┘
         │                                │
         └────── .ai-sync/ (shared) ──────┘
                CONTEXT.md  ← both read
                RULES.md    ← both read
                workflows/  ← both read
```

**Key principle**: Both tools read the same shared files. Neither tool's generated config conflicts with the other.

---

## The 2-Pass Review Process

This template includes a proven **2-pass code review** system that dramatically reduces false positives:

**Pass 1 — Flag issues (broad scan):**
- Review different areas (backend, frontend, tests)
- Flag potential issues using the evidence template
- Collect ALL flagged issues — do not filter yet

**Pass 2 — Verify issues (deep investigation):**
- For EACH flagged issue, read the FULL dependency chain
- Provide FOR and AGAINST evidence
- Give final verdict: REAL, SPECULATIVE, or FALSE POSITIVE
- Only REAL issues are reported to the user

This prevents the common AI review anti-pattern where agents find "evidence" to support initial concerns without checking if mitigations already exist.

---

## Version Management

The template includes a complete version management system:

1. **`VERSION` file** — single source of truth for current version
2. **`scripts/bump_version.py`** — updates VERSION + all source file headers + README + package.json
3. **`scripts/check_version_consistency.py`** — CI check ensuring all versions match
4. **Release workflow** (`.ai-sync/workflows/release.md`) — 8-step release process

---

## Credits

This template was extracted from the [V-Pack Monitor](https://github.com/thangvd2/V-Pack-Monitor) project, a production-grade system that has been developed using the dual-AI workflow since early 2025.

The `.ai-sync/` protocol is designed to be platform-agnostic and can be extended to support additional AI coding tools (Cursor, Claude Code, etc.) by adding new extension files and updating `sync.py`.
