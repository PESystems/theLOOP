# Janitor Hook Scaffolding — Draft
**Status:** DEFERRED — not yet activated
**Date:** 2026-04-12

---

## Why Hooks Are Deferred

Claude Code hooks require a stable automation layer before activation. The scheduled sweep has not yet had its first real automated run. Activating hooks now would add complexity before the foundation is proven.

**Activation criteria:** Hooks should be enabled after the scheduled entrypoint has completed at least 3 successful real runs (not dry-run).

---

## Planned Hooks (Draft)

### Hook 1 — State File Mutation Logger

**Event:** `PostToolUse` (after Edit/Write on `state/*.yaml`)
**Purpose:** Log when any automation or session modifies Janitor state files
**Action:** Append to `logs/janitor_state_mutation_log.md`
**Risk level:** Low — purely observational

Draft config:
```json
{
  "hooks": [
    {
      "event": "PostToolUse",
      "tools": ["Edit", "Write"],
      "match_paths": ["state/*.yaml"],
      "command": "echo \"STATE_MUTATED: $CLAUDE_TOOL_FILE_PATH at $(date -u +%Y-%m-%dT%H:%M:%SZ)\" >> logs/janitor_state_mutation_log.md"
    }
  ]
}
```

### Hook 2 — Protected Config Guard

**Event:** `PreToolUse` (before Edit/Write on automation config)
**Purpose:** Warn before modifying automation scripts or hook configs
**Action:** Print warning, do not block (advisory only initially)
**Risk level:** Low

Draft config:
```json
{
  "hooks": [
    {
      "event": "PreToolUse",
      "tools": ["Edit", "Write"],
      "match_paths": ["automation/*", ".claude/hooks/*"],
      "command": "echo \"WARNING: About to modify Janitor automation config: $CLAUDE_TOOL_FILE_PATH\""
    }
  ]
}
```

### Hook 3 — Red-Flag Check on Session Open

**Event:** `SessionStart` (if supported)
**Purpose:** Run red-flag checker at start of every Claude Code session in this project
**Action:** Run `check_janitor_red_flags.py`, surface findings
**Risk level:** Low — read-only check

Draft config:
```json
{
  "hooks": [
    {
      "event": "SessionStart",
      "command": "python automation/check_janitor_red_flags.py 2>/dev/null || true"
    }
  ]
}
```

**Note:** SessionStart hooks may not be a supported event type in Claude Code. If not, this hook can be replaced by including the red-flag check in the session-open skill.

---

## What Hooks Will NOT Do

- Will not serve as the recurring timer/scheduler
- Will not auto-execute follow-up packets
- Will not write to Notion
- Will not make decisions
- Will not mutate Janitor state (except logging observations)

---

*Hook scaffolding draft — activation deferred until scheduled automation is proven stable.*
