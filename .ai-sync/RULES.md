# Shared Coding Rules

> **AUTO-GENERATED into AGENTS.md and .agents/rules/project-rules.md. DO NOT edit those files directly.**
> Edit this file, then run `python .ai-sync/sync.py`.

---

## MEMORY SYSTEM

On starting a new session or task, check `docs/learnings/` for relevant reference docs before asking questions.

- After completing complex work, write a reference doc to `docs/learnings/`
- Format: `YYYY-MM-DD-short-description.md` with context, problem, root cause, solution
- Read only docs relevant to current task — do not read all docs every session

## BRANCH RULES (MANDATORY)

- NEVER commit directly to `master` or `dev`. Both are protected.
- ALWAYS create a feature branch from `dev`: `git checkout -b {type}/{description} dev`
- Branch naming: `feature/`, `fix/`, `security/`, `refactor/`, `docs/`, `chore/`
- After work is done: `gh pr create --base dev`
- Feature PR → dev: use `--squash` (keep dev history clean: 1 feature = 1 commit)
- Release PR → master: use `--merge` (keep shared history, prevent future conflicts)
- NEVER merge any PR without explicit user confirmation. Always ask first.

## RELEASE RULES (MANDATORY)

- Release PR is ALWAYS `dev` → `master`, merged with `gh pr merge <N> --merge` (NOT --squash)
- **ALWAYS use `python scripts/bump_version.py X.Y.Z` to sync ALL version locations** — NEVER edit version files manually. Script updates: `VERSION`, source headers, `README.md`, `package.json` (if frontend exists)
- **ALWAYS run `python scripts/check_version_consistency.py` BEFORE and AFTER bump** to verify all files in sync
- Update `RELEASE_NOTES.md` manually (the bump script does NOT touch release notes)
- NEVER squash or rebase dev → master — this destroys shared history and causes permanent conflicts
- Full process: see `CONTRIBUTING.md` → "Release Process (dev → master)"

## BEFORE EVERY COMMIT

1. `pytest tests/ -v` — must pass <!-- TODO: Replace with your test command -->
2. `npm run build` — must pass (if frontend changed) <!-- TODO: Remove if no frontend -->
3. `npm run lint` — must pass (if frontend changed) <!-- TODO: Remove if no frontend -->
4. Linter/diagnostics on changed files — no new errors
5. No hardcode secrets/credentials
6. No silent `except: pass` — must log the error
7. If ANY file in `.ai-sync/` was edited — run `python .ai-sync/sync.py` to regenerate platform configs, then commit the generated files in the SAME commit

## CODE RULES

- Match existing patterns in the codebase
- Files > 300 lines need justification in commit/PR
- No `as any`, `@ts-ignore`, `@ts-expect-error` — they hide type errors that surface in production
- No deleting tests to make them pass
- No silent `except: pass` — unlogged errors become impossible to debug; always log with context
- Bug fixes: fix minimally, never refactor while fixing — mixed commits make rollback impossible
- New Python dependencies: add to `requirements-dev.txt` (dev) or `requirements.txt` (prod) AND explain why — hidden deps break reproducibility
- New npm dependencies: add via `npm install` AND explain why

## AGENT VERIFICATION RULES

Model-agnostic rules that improve output reliability across any LLM.

### Ground Progress Claims
- Before declaring a task "done", READ each file you created or modified to verify it exists and has the expected content
- Do NOT trust your memory of what you wrote — verify against the actual file system state
- If a file was supposed to be created but you're unsure, READ it to confirm before reporting completion

### Fresh-Context Verification
- Use SEPARATE agents or sessions for building and reviewing — fresh-context verification outperforms self-critique
- The reviewer MUST independently verify claims by reading the actual diff/test output, never trust self-reported status

## EXTERNAL REVIEWER INTEGRATION (AGY / GEMINI)

External reviewer (e.g. `agy` with Gemini) provides fresh-context verification. It is ADVISORY, not authoritative.

### When to invoke

| Task type | Invoke? |
|-----------|---------|
| Q&A, read files, single-line fix, typo | No |
| Multi-file change, new feature | Yes |
| PR creation, pre-merge, pre-push, release | Yes |
| Security-sensitive ops | Yes |

### Authority

- Reviewer flags issues → builder VERIFIES each before acting (apply anti-false-positive rules)
- Builder STILL DELIVERS response with findings noted — reviewer does NOT block delivery
- User retains final authority

### Invocation

- `--dangerously-skip-permissions` REQUIRED for headless/background — without it, agy prompts per tool call and stalls. Interactive TTY (user approves) can omit it.
- `--print-timeout` in seconds (e.g. `3600s`), not `60m`.
- Run in FOREGROUND (blocking) when review gates a decision (PR merge, release). Background mode is unreliable for blocking reviews.

```bash
agy -p "Review PR <URL>. READ-ONLY: do NOT modify files or commit. Read diff + CI, provide 2-pass review per AGENTS.md rules." --model "Gemini 3.5 Flash (High)" --dangerously-skip-permissions --add-dir "$(pwd)" --print-timeout 3600s
```

Models: `agy models`.

## MANDATORY PRE-PUSH REVIEW (EVERY FEATURE)

Before pushing ANY new feature or significant change:
1. **Self-review**: Audit code for edge cases, race conditions, thread safety, and error handling
2. **Test coverage**: New backend logic MUST have corresponding tests. No exceptions.
3. **No tests = not done**: If you can't write tests for it, explain why in the PR and flag it as untested
4. **Thread safety audit**: Any code using threading, locks, timers, or shared state MUST be reviewed for:
   - Lock ordering (deadlock risk)
   - Race conditions (concurrent access without locks)
   - Resource leaks (timers, threads, connections not cleaned up)
   - Stale references (captured variables in callbacks that may be outdated)

## CODE REVIEW ANTI-FALSE-POSITIVE RULES (MANDATORY)

When flagging a potential issue during code review, you MUST:
1. **Read ALL files in the dependency chain** — not just the immediate file.
2. **Trace the FULL call path** — callers, callees, related modules.
3. **Check mitigations FIRST** — before flagging, ask: "Is this already handled elsewhere?"
4. **Provide FOR and AGAINST evidence** — every flagged issue MUST include:
   - EVIDENCE FOR: why this seems like a real issue (with file:line)
   - EVIDENCE AGAINST: why this might NOT be a real issue — check guards, related code, production config
   - DEPENDENCY CHAIN: list ALL related files/modules that affect this issue
5. **Classify before reporting** — every issue gets one of:
   - `REAL`: Confirmed with full dependency trace. Has user impact.
   - `SPECULATIVE`: Plausible but unverified. Needs deeper investigation.
   - `FALSE POSITIVE`: Initially seemed real, but mitigated elsewhere.

**Issue without full dependency trace = SPECULATIVE, not actionable.**
**Issue without AGAINST evidence = incomplete review.**

## REVIEW PROMPT TEMPLATE (USE WHEN DELEGATING REVIEW TASKS)
When firing explore/librarian agents for code review, include this structure in the prompt:

```
For EACH potential issue found, you MUST provide:

1. ISSUE: [one-line description]
2. FILES READ: [list ALL files you actually read to verify this — not just where the issue appears]
3. EVIDENCE FOR: [why this seems like a real issue, with file:line references]
4. EVIDENCE AGAINST: [why this might NOT be a real issue — check mitigations, guards,
   fallbacks, related modules, production config. If you cannot find any against-evidence,
   state "No against-evidence found after checking [files checked]"]
5. DEPENDENCY CHAIN: [list all related files/modules that could affect whether this is real]
6. VERDICT: REAL / SPECULATIVE / FALSE POSITIVE

DO NOT flag issues without reading the full dependency chain.
DO NOT skip AGAINST evidence — it is MANDATORY.
```

## 2-PASS REVIEW PROCESS (FOR RELEASE REVIEWS & SECURITY AUDITS)
For release PRs, security audits, and critical code changes:
- **Pass 1 (scan)**: Flag potential issues across areas (backend, frontend, tests) using the evidence template above. Collect ALL — do not filter.
- **Pass 2 (verify)**: For EACH flag — read the FULL dependency chain, trace locks/fallbacks/related modules, give verdict: REAL, SPECULATIVE, or FALSE POSITIVE. Only REAL reported to user; SPECULATIVE with caveat; FALSE POSITIVE documented.
- **Why 2 passes?** Single pass creates confirmation bias. Separating detection from verification reduces false positives.

## MANDATORY SELF-VERIFICATION CHECKLIST (BEFORE SAYING "DONE")
You MUST NOT report a task as complete until EVERY item below passes.
No exceptions. If you skip any item, the user WILL find the bug on double-check.

### For EVERY code change (Python, JS, JSX, YAML):
- [ ] NOT on `master` or `dev` — must be on a feature branch (`feature/`, `fix/`, `security/`, `refactor/`, `docs/`, `chore/`)
- [ ] `ruff check .` passes on changed files (or `npm run lint` for frontend)
- [ ] `lsp_diagnostics` shows no NEW errors on changed files
- [ ] No duplicate lines, duplicate comments, or copy-paste artifacts
- [ ] No unused imports, unused variables, or dead code left behind
- [ ] Every new shared state variable has cleanup path on shutdown/exit
- [ ] Git diff reviewed line-by-line — no accidental inclusions (log files, screenshots)

### For backend Python changes:
- [ ] `pytest tests/ -q` passes (or specific test file if targeted)
- [ ] New functions with threading/locks/timers: verify lock ordering, cancel paths, cleanup on error

### For frontend changes:
- [ ] `npm run build` passes
- [ ] `npm run lint` passes
- [ ] useEffect deps arrays correct (no stale closures)
- [ ] catch blocks have error handling (alert/toast/setError + console.warn, not bare `catch {}`)

### For CI/YAML changes:
- [ ] YAML syntax valid (no duplicate keys, correct indentation)
- [ ] New jobs added to branch protection required checks
- [ ] Path filters cover all relevant file patterns
- [ ] If adding `if:` conditions — verified that skipped jobs still satisfy branch protection

### For docs/config changes (AGENTS.md, CONTRIBUTING.md, VERSION):
- [ ] VERSION file matches source headers
- [ ] Cross-references between docs are accurate (section names, file paths)
- [ ] No contradictory rules between AGENTS.md and CONTRIBUTING.md

### For release PRs:
- [ ] `gh pr merge <N> --merge` (NOT --squash)
- [ ] VERSION, source headers, RELEASE_NOTES.md all updated on dev BEFORE creating PR
