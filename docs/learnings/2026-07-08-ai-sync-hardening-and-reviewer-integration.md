# 2026-07-08 — .ai-sync Hardening + External Reviewer Integration

**Context**: Session started with syncing Z.ai usage policy to 4 projects, evolved into hardening `.ai-sync/` infrastructure + integrating `agy` (Antigravity CLI) as external reviewer. 6 PRs merged across 5 repos, 5 iterative Gemini review rounds on the hardening PR.

---

## Lesson 1: Antigravity YAML Frontmatter Must Be at Line 1

**Problem**: `platform-antigravity.md` had HTML auto-gen comments before the YAML frontmatter `---` separator. Antigravity silently ignored the permissions block.

**Root Cause**: `generate_antigravity_platform()` in `sync.py` concatenated `AUTOGEN_HEADER + frontmatter + body`. HTML comments pushed `---` to line 3.

**Solution**: Order matters — `frontmatter + AUTOGEN_HEADER + body`. YAML frontmatter MUST be the very first thing in the file.

**Prevention**: Always verify generated output with `head -5 <file>` after editing sync generators. Antigravity docs confirm: frontmatter is only parsed when at line 1.

---

## Lesson 2: Antigravity Permissions Require action(target) Declarations, Not Prose

**Problem**: Original `antigravity.md` had "TERMINAL POLICIES" + "AGENT PERMISSIONS" sections with markdown prose like "Default Allow: `npm run test`". Zero enforcement.

**Root Cause**: Antigravity only reads `action(target)` declarations in YAML frontmatter of rules files. Markdown body text is documentation only.

**Solution**: Extract declarations to `antigravity-permissions.yml`, inject via sync.py into frontmatter. Body text points to the yml file.

**Prevention**: When documenting platform-specific behavior, verify against official docs (https://antigravity.google/docs/permissions), not assumptions. A doc that "looks right" can be completely non-functional.

---

## Lesson 3: sync.py Char Limit Overflow = Silent Stale Files

**Problem**: When `CONTEXT.md + RULES.md` exceeded 12,000 chars (Antigravity hard limit), sync.py printed ERROR but **exit 0**. CI couldn't detect the failure → generated files went silently stale.

**Root Cause**: `write_output()` returned `False` for both "no change" and "overflow". `main()` didn't track errors or exit non-zero.

**Solution**: 
- Track errors across `write_output()` + `sync_workflows()`, exit 1 on any failure
- Add early warning at 90% of limit (before ERROR at 100%)
- `check_up_to_date()` must also validate char limits (not just hash compare)

**Prevention**: Any tool that "skips on error" must propagate exit code. Silent failures are worse than loud ones.

---

## Lesson 4: --dangerously-skip-permissions REQUIRED for Headless agy

**Problem**: `agy -p "..."` run in background/headless mode stalled indefinitely — agent kept exploring but never converged. Interactive terminal runs completed in 1-2 min.

**Root Cause**: Without `--dangerously-skip-permissions`, agy prompts for approval on every tool call (read file, run command). In non-TTY mode, no one approves → agent stuck waiting.

**Solution**: Pattern from `multi-agent-orchestrator/orchestrator/gemini_client.py`:
```python
cmd = ["agy", "-p", prompt, "--dangerously-skip-permissions",
       "--add-dir", str(project_dir), "--print-timeout", f"{timeout}s"]
subprocess.Popen(cmd, cwd=project_dir, start_new_session=True, ...)
```

**Prevention**: When integrating any CLI tool into automation, check if it has interactive prompts. Headless mode usually needs an explicit "auto-approve" or "non-interactive" flag.

---

## Lesson 5: Auto-Timer + Exponential Backoff Does NOT Work for Self-Monitoring

**Problem**: Designed rule: "background task + auto-timer (sleep 180) to force interim check via system notification". Failed 3/3 times — timer fired, notification arrived, but I didn't respond because I was in "user-wait state".

**Root Cause**: System notifications don't reliably trigger agent response when agent is waiting for user input. The "enforcement mechanism" was an illusion.

**Solution**: Use **foreground (blocking) execution** for review tasks that gate decisions (PR merge, release). Background only for non-blocking research/exploration.

**Prevention**: Don't design self-monitoring rules that depend on the agent responding to its own timers. If a task MUST complete before proceeding, block on it directly.

---

## Lesson 6: Branch Verification Before amend

**Problem**: Ran `git commit --amend` intending to update `refactor/harden-ai-sync` branch, but was actually on `dev` (protected!). Commit landed on dev locally.

**Root Cause**: No `git branch --show-current` sanity check before amend. Assumed branch context carried over from previous operation.

**Solution**: Always run `git branch --show-current` and verify it matches expectation before any amend/reset/commit operation. Added to personal checklist.

**Prevention**: Git operations that rewrite history (amend, reset --hard, rebase) are dangerous. Always confirm branch first. The cost of one extra command is nothing vs. cost of polluting a protected branch.

---

## Lesson 7: Push Before Review, Not After

**Problem**: Ran Gemini review on PR #13 round 2, but the latest fixes weren't pushed yet. Gemini reviewed stale commit, reported 5 issues that were already fixed locally.

**Root Cause**: Sequence was: amend locally → run review → force-push. Should be: amend → force-push → run review.

**Solution**: Always force-push amend BEFORE invoking reviewer. Reviewer reads GitHub state, not local state.

**Prevention**: Reviewer sees what's on the remote. Any local-only commit is invisible to review. Push first, review second.

---

## Lesson 8: Gemini Reviewer Can Read Stale Sources (Cross-Verify Findings)

**Problem**: Gemini round 1 flagged "missing quota multipliers (3× peak / 2× off-peak)" as REAL. Verification showed this came from a STALE `.md` version of Z.ai docs — the current HTML version had removed this info, and the June promo had expired.

**Root Cause**: Gemini fetched raw markdown (`.md` URL) which was cached/older, instead of current HTML render.

**Solution**: Cross-verify every reviewer finding against actual source before acting. Apply CODE REVIEW ANTI-FALSE-POSITIVE RULES — provide FOR and AGAINST evidence, classify REAL vs SPECULATIVE vs FALSE POSITIVE.

**Prevention**: Reviewer is advisory, not authoritative. Builder must verify each finding. "The reviewer said so" is never sufficient justification to change code.

---

## Lesson 9: Iterative Review Rounds Catch Progressively Subtler Issues

**Pattern observed across 5 rounds on PR #13**:

| Round | Findings | Nature |
|-------|----------|--------|
| 1 | 5 issues (1 HIGH: fictional permissions) | Major design flaws |
| 2 | 1 REAL (requirements-dev.txt) + stale | Missing infrastructure |
| 3 | 4 REAL (all minor/cosmetic) | Code quality |
| 4 | 1 HIGH (frontmatter position!) + 3 LOW | Subtle integration bugs |
| 5 | 0 — APPROVED | Clean |

**Insight**: Each round found issues the previous round missed — including a HIGH severity one in round 4. Single-pass review would have missed the frontmatter position bug (which completely disabled permissions enforcement).

**Prevention**: For complex changes (multi-file, infrastructure), run multiple review rounds until clean. Don't assume one pass is sufficient.

---

## Lesson 10: Condense Before Adding (12,000 Char Constraint)

**Problem**: Adding new rule (EXTERNAL REVIEWER INTEGRATION) pushed combined `CONTEXT.md + RULES.md` over Antigravity's 12,000 char hard limit. Had to emergency-prune existing content mid-session.

**Root Cause**: No visibility into char budget before editing. Rule additions were additive without considering removals.

**Solution**: Before adding any new section to RULES.md:
1. Check current char count: `python3 -c "from pathlib import Path; ..."`
2. Identify condensation candidates (redundant sections, verbose explanations)
3. Condense FIRST, then add

**Prevention**: Treat rule files like a budget — every addition requires a removal or condensation. The 12,000 limit is a hard platform constraint, not a guideline.

---

## Summary: Meta-Lesson

**The most expensive errors this session were assumption-based**:
- Assumed prose permissions would enforce (they don't)
- Assumed auto-timer would trigger self-response (it didn't)
- Assumed amend was on correct branch (it wasn't)
- Assumed local commit was visible to reviewer (it wasn't)
- Assumed one review round was enough (round 4 found HIGH issue)

**Rule**: Verify against actual state (filesystem, git, docs, platform behavior) before acting. Assumptions compound — each unchecked assumption becomes a bug that's harder to trace.
