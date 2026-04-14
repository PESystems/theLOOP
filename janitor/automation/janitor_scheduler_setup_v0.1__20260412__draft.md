# Janitor Scheduler Setup Guide v0.1

**Updated:** 2026-04-13 — migrated primary surface from Windows Task Scheduler to Claude Scheduled Tasks.

---

## Recommended: Claude Scheduled Task (Every 2 Days)

Claude Scheduled Tasks are the primary cadence surface for Janitor. This is consistent with the 8 other LOOP tasks already running on this surface.

### Task parameters

| Field | Value |
|-------|-------|
| **taskId** | `janitor-sweep-2d` |
| **description** | `Floor Janitor sweep — scan responses, check red flags, log findings. Every 2 days.` |
| **cronExpression** | `0 9 */2 * *` (every 2 days at 9:00 AM local) |
| **prompt** | See "Task Prompt" section below |

### Task prompt

The scheduled task runs as a Claude session with a full prompt. The prompt should:

1. Set working directory to `C:\Users\Malik\Documents\Claude\Projects\JANITOR_WrkSps`
2. Run the red-flag checker: `python automation/check_janitor_red_flags.py --output logs/red_flag_latest.json`
3. Run the scheduled sweep: `python automation/run_janitor_scheduled.py --mode sweep`
4. Report findings in the session
5. If new eligible responses are found, note them for Malik's next interactive session
6. Never autonomously apply responses, execute follow-up packets, or write to Notion

### Behavior

| Scenario | What happens |
|----------|-------------|
| Machine is asleep at scheduled time | Task fires on wake (Claude replays skipped runs) |
| Claude Desktop is closed | Task fires on next app open |
| No new responses | Logs "no new responses", exits clean |
| New responses found | Logs eligible files, notes for Malik — does NOT auto-apply |
| Red-flag critical | Reports findings prominently in session output |

### How to create

Use the `/schedule` skill or `mcp__scheduled-tasks__create_scheduled_task` tool with the parameters above.

---

## Fallback: Windows Task Scheduler

Use Windows Task Scheduler **only if** app-independent execution becomes required (i.e., Janitor must run while Claude Desktop is fully closed with no replay).

### Setup (if needed)

1. Open Task Scheduler (`Win+R` > `taskschd.msc`)
2. Create task:
   - Name: `Floor Janitor Sweep`
   - Trigger: Daily, recur every 2 days, start time `09:00`
   - Action: Start a program
     - Program: `python`
     - Arguments: `automation/run_janitor_scheduled.py --mode sweep`
     - Start in: `C:\Users\Malik\Documents\Claude\Projects\JANITOR_WrkSps`

### Optional: Daily red-flag check (Windows)

| Setting | Value |
|---------|-------|
| Name | `Floor Janitor Red-Flag Check` |
| Frequency | Daily |
| Program | `python` |
| Arguments | `automation/check_janitor_red_flags.py --output logs/red_flag_latest.json` |
| Start in | `C:\Users\Malik\Documents\Claude\Projects\JANITOR_WrkSps` |

---

## Fallback: Cron (Linux/macOS)

```cron
# Janitor sweep every 2 days at 9am
0 9 */2 * * cd /path/to/JANITOR_WrkSps && python3 automation/run_janitor_scheduled.py --mode sweep >> logs/cron_sweep.log 2>&1

# Red-flag check daily at 8am
0 8 * * * cd /path/to/JANITOR_WrkSps && python3 automation/check_janitor_red_flags.py --output logs/red_flag_latest.json >> logs/cron_redflag.log 2>&1
```

---

## Log File Expectations

| Log | Path | Updated by |
|-----|------|-----------|
| Automation run log | `logs/janitor_automation_run_log.md` | Every scheduled or red-flag run |
| Dry-run JSON | `logs/janitor_dry_run_YYYYMMDD.json` | Dry-run mode only |
| Red-flag JSON | `logs/red_flag_latest.json` | Red-flag check runs |

---

## Failure Behavior

| Scenario | Behavior |
|----------|----------|
| Python not on PATH | Script exits with error. Claude session reports it. |
| State file missing | Script exits with code 2, logs the failure |
| No responses to process | Script exits with code 0, logs "no new responses" |
| New responses found | Script exits with code 1, logs eligible files |
| Red-flag critical | Checker exits with code 3, JSON notes manual_alert findings |

---

## Verification

Run a dry-run to confirm the entrypoint works:

```
cd C:\Users\Malik\Documents\Claude\Projects\JANITOR_WrkSps
python automation/run_janitor_scheduled.py --mode dry-run
```

Expected: exit code 0, snapshot created, dry-run JSON written to `logs/`.

---

*Janitor Scheduler Setup v0.1 — updated 2026-04-13*
