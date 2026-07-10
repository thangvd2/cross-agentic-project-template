# 2026-07-10 — Unified AGENTS.md Architecture (Redesign .ai-sync/)

**Context**: Discovered `project-rules.md` is 98% duplicate of `AGENTS.md`. Both are auto-loaded by Antigravity, wasting ~2,000 tokens/prompt. The 12,000 char limit (Antigravity hard limit) only applies to `.agents/rules/` files — `AGENTS.md` has no limit. All char-budget fights this session were for a redundant file.

---

## Problem (verified)

Current `.ai-sync/` generates 3 output files:

```
AGENTS.md                       = CONTEXT + RULES + ext/opencode       → OpenCode + Antigravity
.agents/rules/project-rules.md  = CONTEXT + RULES                     → Antigravity (98% DUPLICATE!)
.agents/rules/platform-antigravity.md = ext/antigravity + permissions  → Antigravity
```

**Verified problems:**
1. `project-rules.md` is 98% duplicate of `AGENTS.md` — Antigravity loads BOTH (confirmed via `<user_rules>` tag inspection: only `AGENTS.md` appears, `.agents/rules/` does NOT load into context)
2. 12,000 char limit only applies to `project-rules.md` (the duplicate)
3. `project-rules.md` leaked OpenCode content (3 OpenCode refs in Antigravity-targeted file)
4. OpenCode does NOT read `.agents/rules/` — only reads `AGENTS.md` from project root ([opencode.ai/docs/rules](https://opencode.ai/docs/rules/), [GitHub issue #11454](https://github.com/anomalyco/opencode/issues/11454))

**Critical empirical finding (from Gemini session inspection):**
> Antigravity's `<user_rules>` context contains ONLY `<RULE[AGENTS.md]>`. Files in `.agents/rules/` are NOT loaded into agent context — they're only parsed for YAML frontmatter (permissions). This means antigravity ext text rules were NEVER reaching the agent.

---

## Root Cause

Two misconceptions in original `.ai-sync/` design:
1. Assumed Antigravity loads `.agents/rules/*.md` as context → generated duplicate `project-rules.md`
2. Assumed OpenCode reads `.agents/rules/` → considered splitting extensions into separate files

Reality (verified July 2026):
- **Antigravity**: auto-loads `AGENTS.md` as context ([official docs](https://antigravity.google), [gcli-migration](https://antigravity.google/docs/gcli-migration)). `.agents/rules/` files are parsed for YAML frontmatter (permissions) only, markdown body ignored.
- **OpenCode**: auto-loads `AGENTS.md` only. Does NOT read `.agents/rules/` ([docs](https://opencode.ai/docs/rules/)).

---

## Solution — Unified AGENTS.md

### New architecture

```
AGENTS.md (single source, both platforms auto-load):
├── CONTEXT.md body                                    → shared (both)
├── RULES.md body                                      → shared (both)
├── ext/opencode body — labeled "(OpenCode Only)"      → OpenCode applies, Antigravity ignores
└── ext/antigravity body — labeled "(Antigravity Only)" → Antigravity applies, OpenCode ignores

.agents/rules/platform-antigravity.md (Antigravity-specific):
└── YAML frontmatter (permissions) + short header      → <1,000 chars, never overflows

.agents/rules/project-rules.md → DELETED (migration cleanup)
```

### Why this works

- **OpenCode**: reads `AGENTS.md` → gets shared rules + OpenCode extensions (labeled) + sees Antigravity extensions (ignores via "(OpenCode Only)" / "(Antigravity Only)" natural language labels)
- **Antigravity**: reads `AGENTS.md` → gets shared rules + sees OpenCode extensions (ignores) + gets Antigravity extensions (labeled). Also reads `platform-antigravity.md` frontmatter for permissions enforcement.
- **No duplication.** No char-limit pressure (AGENTS.md has no limit). Labels use natural language (already proven pattern — `(OpenCode Only)` exists today and works).

### Label mechanism

LLMs filter platform-specific sections via natural language labels in section headers:
- `## AGENT SYSTEM (OpenCode Only)` → OpenCode applies, Antigravity ignores
- `## RULE ACTIVATION (Antigravity Only)` → Antigravity applies, OpenCode ignores

This is already proven (both labels exist in current extensions). No technical mechanism needed — LLMs understand parenthetical platform qualifiers.

---

## Implementation — sync.py changes

### Change 1: Rename + merge generate function

`generate_opencode_agents()` → `generate_agents_md()`. Now includes BOTH extensions (opencode + antigravity) in AGENTS.md.

### Change 2: Delete generate_antigravity_shared()

Stop generating `project-rules.md` (was redundant).

### Change 3: Simplify generate_antigravity_platform()

`platform-antigravity.md` now emits ONLY YAML frontmatter (permissions) + short header pointing to AGENTS.md. Body text removed entirely.
- Rationale: Antigravity only parses YAML frontmatter for permissions, ignores markdown body
- File drops from ~3,596 chars to <1,000 chars — eliminates 12k overflow risk permanently

### Change 4: Standardize labels

In source extensions: `(OpenCode-Specific)` → `(OpenCode Only)`, `(Antigravity-Specific)` → `(Antigravity Only)`, `(OpenCode Pattern)` → `(OpenCode Only)`. Fix stale comments.

### Change 5: Migration cleanup

In `main()`: if legacy `project-rules.md` exists, delete via `Path.unlink(missing_ok=True)` + print warning. Git-safe (shows as unstaged deletion).

### Additional: Fix stale references

- `.ai-sync/README.md`: update sync formula
- `.gitignore`: remove stale commented-out `project-rules.md` line
- `.ai-sync/CONTEXT.md`, `RULES.md`, `extensions/antigravity.md`: fix comments referencing project-rules.md

---

## Verification plan

1. `python3 .ai-sync/sync.py` → exit 0
2. AGENTS.md contains both `(OpenCode Only)` + `(Antigravity Only)` labeled sections
3. `platform-antigravity.md` = YAML frontmatter + header only (<1,000 chars)
4. `project-rules.md` deleted
5. `python3 .ai-sync/sync.py --check` → passes
6. `ruff check .ai-sync/sync.py` → passes
7. No stale `project-rules.md` references remain

---

## Propagation

After template PR merges, apply same sync.py changes to 5 projects:
- `multi-agent-orchestrator`, `ai-debate-arena`, `posting_sheet_management`, `tm-llm-wiki`, `ai_agents`

Each project's `AGENTS.md` grows (includes antigravity ext) but `project-rules.md` deleted (removes ~11k chars). Net: less total tracked content, no char-limit pressure.

---

## Gemini verification history

- **Round 1**: CONFIRMED architecture direction. Raised 2 challenges (platform-antigravity.md redundancy + 12k risk).
- **Round 2**: CHALLENGE — claimed Antigravity doesn't load AGENTS.md. **INTERNAL CONTRADICTION with round 1.**
- **Round 3 (contradiction resolution)**: DEFINITIVE — Antigravity DOES auto-load AGENTS.md (3 evidence layers: empirical `<user_rules>` inspection, official docs, gcli-migration docs). Plan validated as safe.

**Lesson**: When reviewer contradicts itself across rounds, resolve via empirical evidence (inspect actual session context), not docs interpretation alone.
