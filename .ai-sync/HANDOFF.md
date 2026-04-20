# Session Handoff

> **Session context transfer between OpenCode and Antigravity.**
> The last active tool writes here. The next tool reads here.
> This ensures no context is lost when switching between AI tools.

---

## Current Session

<!-- TODO: Fill in at the start of each session -->
- **Tool**: <!-- OpenCode / Antigravity -->
- **Date**: <!-- YYYY-MM-DD -->
- **Branch**: <!-- current git branch -->
- **Task**: <!-- what you're working on -->
- **Progress**: <!-- brief status -->

## Last Session Summary

<!-- TODO: Fill in at the end of each session -->
- **Tool**: <!-- OpenCode / Antigravity -->
- **Date**: <!-- YYYY-MM-DD -->
- **Completed**: <!-- what was done -->
- **Pending**: <!-- what remains -->
- **Notes**: <!-- anything the next tool needs to know -->

## Handoff Protocol

### Starting a Session
1. Read this file for context from previous session
2. Read `TASKS.md` for active tasks
3. Read `MEMORY.md` for relevant lessons
4. Proceed with work, updating files as needed

### Ending a Session
1. Update `Current Session` or `Last Session Summary` above
2. Update `TASKS.md` with task status changes
3. If learned new lessons → add to `MEMORY.md`
4. If rules changed → update `RULES.md` → run `sync.py`
