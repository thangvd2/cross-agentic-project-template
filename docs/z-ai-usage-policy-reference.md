# Z.AI GLM Coding Plan — Usage Policy Reference

> Source: https://docs.z.ai/devpack/usage-policy + https://docs.z.ai/legal-agreement/subscription-terms
> Retrieved: 2026-04-21
> Purpose: Reference for using GLM Coding Plan compliantly across projects.

---

## What GLM Coding Plan Covers

Subscription for **AI-powered coding** within **designated coding/IDE tools** (OpenCode, Claude Code, Kilo Code, etc.). Quota is **personal-use only**, tied to a single account.

## Allowed Usage

| Activity | Why OK |
|----------|--------|
| Write/edit/review code in coding tools | Core use case |
| Use subagents (explore, oracle, librarian, etc.) | Explicitly mentioned: *"use methods like Subagent to make concurrent model calls"* |
| Build development projects (git repos, scripts, configs, automation) | Development activity within coding tools |
| Scrape, ingest, lint within a project context | All operations produce artifacts in a codebase (files, configs, docs) |
| Rate/concurrency within plan tier | Lite = 1 project, Pro = 1-2, Max = 2+ concurrent |

## Prohibited Usage

| Activity | Consequence |
|----------|-------------|
| Share account with others | Account ban |
| Use for non-coding requests (general Q&A, essays, translations unrelated to codebase) | Throttle/restriction (auto-lifted when coding usage resumes) |
| Call Z.AI API directly from own apps/scripts | Account ban |
| Resell/redistribute quota to third parties | Account ban |
| **3+ violations** | Permanent account ban |

## Risk Control

Z.AI **automatically detects**:
- Non-coding usage → restrict benefits, auto-lift when coding resumes
- Account sharing → restrict/suspend/ban
- Bulk/automated usage on behalf of others → same

## Practical Rules of Thumb

1. **Every request should be traceable to a file in the repo** — edit, create, review, or analyze codebase artifacts. If it can't be traced to a file, it's risky.

2. **Frame requests as development tasks** — Instead of "explain X", say "implement/update X in the codebase". Instead of "analyze this document", say "update AGENTS.md with these constraints".

3. **Use off-peak for heavy operations** — Higher concurrency during off-peak hours. Batch operations (scraping, bulk ingest) should run outside peak times.

4. **Reasonable concurrency** — 2-5 parallel subagents is fine. Don't spam 10+ concurrent calls.

5. **All work stays in coding tools** — OpenCode, Claude Code, etc. Never call Z.AI APIs from custom scripts or apps.

6. **Single user, single account** — Never share credentials, even with teammates.

## Decision Framework

```
Request → Can it be framed as a development task within a codebase?
  YES → Coding scenario → Safe to proceed
  NO  → Ask: Is it general knowledge/Q&A?
        YES → Non-coding → Avoid or minimize
        NO  → Unclear → Frame it as codebase work before proceeding
```

## Key Quotes from Policy

> *"The GLM Coding Plan is a subscription service designed for developers' code-assistance scenarios."*

> *"The usage quota under this plan may only be used within coding/IDE tools designated or recognized by Z.ai."*

> *"If the system detects that the subscription is being used for requests clearly unrelated to coding scenarios, certain subscription benefits may be restricted to maintain fairness and platform stability. Once normal coding-related usage resumes, these restrictions may be automatically lifted."*

> *"Violating the Usage Rules three or more times will result in an account ban."*
