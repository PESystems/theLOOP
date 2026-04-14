# Janitor Claude Scheduled Task Spec v0.1

---

## Task Definition

| Field | Value |
|-------|-------|
| **taskId** | `janitor-sweep-2d` |
| **description** | `Floor Janitor sweep — scan responses, check red flags, log findings. Every 2 days.` |
| **cronExpression** | `0 9 */2 * *` |
| **Cadence** | Every 2 days at 9:00 AM local time |

---

## Task Prompt

```
Floor Janitor Scheduled Sweep

Working directory: C:\Users\Malik\Documents\Claude\Projects\JANITOR_WrkSps

You are running a scheduled Floor Janitor sweep. This is an automated heartbeat — not an interactive session.

## Steps

1. Run the red-flag checker:
   python automation/check_janitor_red_flags.py --output logs/red_flag_latest.json

2. Run the scheduled sweep entrypoint:
   python automation/run_janitor_scheduled.py --mode sweep

3. Read the outputs:
   - logs/red_flag_latest.json
   - logs/janitor_automation_run_log.md (last entry)
   - The sweep console output

4. Summarize findings:
   - How many response files scanned
   - How many new eligible responses found (if any)
   - Red-flag findings (if any)
   - Whether any action is needed from Malik

5. If new eligible responses are found:
   - List them by filename and blocker_id
   - Note: "Malik should run the ingestion pipeline in his next interactive session"
   - Do NOT autonomously apply responses

6. If red-flag severity is critical (exit code 3):
   - Prominently flag the integrity issue
   - Note: "Manual investigation required"

## Hard constraints

- Do NOT apply responses autonomously
- Do NOT execute follow-up packets
- Do NOT write to Notion
- Do NOT modify state files beyond what the Python scripts do (snapshot + log entry)
- Do NOT widen scope into D1, D2, or unrelated work
- This is a detection and reporting run only
```

---

## Run Mode

| Property | Value |
|----------|-------|
| Mode | Recurring (cron) |
| Mutation allowed | Snapshot creation + run log append only (via Python scripts) |
| Decision authority | None — detection and reporting only |
| Ingestion allowed | NO — deferred to Malik's next interactive session |
| Notion writes | NO |
| Follow-up execution | NO |

---

## Expected Outputs Per Run

| Output | Path | Created by |
|--------|------|-----------|
| Red-flag JSON | `logs/red_flag_latest.json` | `check_janitor_red_flags.py` |
| Run log entry | `logs/janitor_automation_run_log.md` | `run_janitor_scheduled.py` |
| Snapshot folder | `state/snapshots/JAUTO-{timestamp}/` | `run_janitor_scheduled.py` |
| Dry-run JSON (if dry-run) | `logs/janitor_dry_run_YYYYMMDD.json` | `run_janitor_scheduled.py` |

---

## What Remains Out of Scope

| Action | Why |
|--------|-----|
| Response ingestion (Phase 2C pipeline) | Requires interactive Claude Code session |
| Blocker decision-making | Malik-only authority |
| Follow-up packet execution | Requires explicit per-packet authorization |
| Notion writes | Out of Janitor automation scope |
| Hook activation | Deferred until 3+ successful scheduled runs |
| Dispatch sending | Janitor queues, does not send |

---

## Operator Review Expectations

After each scheduled run:
- Claude session output will contain a summary of findings
- If `notifyOnCompletion` is true, Malik receives a notification
- Malik reviews at his cadence — no urgent response required unless critical red flags appear

---

## Creation Command

To create this task, use:

```
mcp__scheduled-tasks__create_scheduled_task
  taskId: "janitor-sweep-2d"
  description: "Floor Janitor sweep — scan responses, check red flags, log findings. Every 2 days."
  cronExpression: "0 9 */2 * *"
  prompt: <the full prompt above>
```

---

*Janitor Claude Scheduled Task Spec v0.1 — 2026-04-13*
