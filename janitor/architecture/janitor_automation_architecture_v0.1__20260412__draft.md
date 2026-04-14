# Janitor Automation Architecture v0.1

---

## Model

Janitor automation is a **three-layer hybrid**:

| Layer | Purpose | Mechanism | Frequency |
|-------|---------|-----------|-----------|
| **A — Scheduled sweep** | Periodic full Janitor run | Claude Scheduled Task (primary) / OS scheduler (fallback) | Every 2 days |
| **B — Red-flag activation** | Detect conditions that warrant an extra run or alert | Python checker script, callable on-demand or by scheduler | Between sweeps or on file-change events |
| **C — Guardrails** | Prevent silent drift, enforce logging, protect state | Pre-run snapshots, run logs, hook scaffolding | Every run |

---

## Why Claude Scheduled Tasks

Claude Scheduled Tasks are the primary cadence mechanism for Janitor:

- **Native to Malik's environment** — 8 other LOOP tasks already run on this surface (daily + weekly)
- **Runs as a Claude session** — the sweep prompt executes directly, no Python PATH issues
- **Skipped runs replay** — if the machine is asleep or Claude Desktop is closed, the task fires on wake/reopen
- **Consistent operator surface** — Malik monitors all scheduled work in one place

Claude Code hooks are event-driven, not time-driven — they serve as guardrails, not the cadence mechanism.

### Fallback: OS-level scheduling

If app-independent execution becomes required later (e.g., Janitor must run while Claude Desktop is fully closed with no replay), Windows Task Scheduler or cron can invoke the Python entrypoint scripts. This is a fallback path, not the default.

---

## Why Hooks Are Used Only for Events

Claude Code hooks fire on specific events (pre-tool-use, post-tool-use, etc.). They are useful for:

- Logging when automation modifies state files
- Blocking unauthorized edits to protected config
- Surfacing integrity failures detected during a session

Hooks are **not** used for:

- Recurring timers (no cron-like capability)
- Autonomous follow-up execution
- External writes (Notion, email, etc.)

Hook scaffolding is created as a draft. Activation is deferred until the scheduled sweep has proven stable in at least 3 real runs.

---

## What Is Automated vs. Manual

### Automated

| Action | Trigger |
|--------|---------|
| Full Janitor sweep (response discovery, validation, state scan) | Scheduled (every 2 days) or red-flag request |
| Pre-run snapshot of 4 core state files | Every automated run |
| Red-flag detection scan | Scheduled (can piggyback on sweep) or on-demand |
| Run logging | Every automated run |
| Escalation stage tracking | Sweep increments `sweeps_persisted` and checks thresholds |

### Manual (by design)

| Action | Why |
|--------|-----|
| Filling blocker response YAMLs | Malik's decision authority |
| Approving/rejecting/deferring blockers | Malik's decision authority |
| Executing follow-up packets (D1, D2, future work) | Requires explicit authorization per ingestion contract |
| Notion writes | Out of scope for Janitor automation |
| Dispatch sending | Out of scope — Janitor detects and queues, does not send |
| Widening blocker scope | Requires new prompt or response |

---

## Safe Run Modes

### 1. Scheduled Sweep Mode

```
python automation/run_janitor_scheduled.py --mode sweep
```

- Full Janitor sweep: snapshot, scan responses, validate, apply if eligible, generate follow-ups, write reports
- Creates run log entry
- No autonomous external writes
- Exit code 0 on success

### 2. Red-Flag Check Mode

```
python automation/check_janitor_red_flags.py
```

- Lightweight state scan only
- **No mutation** — reads state files, emits findings
- Returns exit code indicating severity
- Can be run frequently (even every session open)

### 3. Dry-Run Mode

```
python automation/run_janitor_scheduled.py --mode dry-run
```

- Proves the automation path without mutating production state
- Creates snapshot but does not apply changes
- Writes dry-run report
- Used for testing scheduler setup

---

## State Files Protected by Automation

| File | Role |
|------|------|
| `state/janitor_state.yaml` | Blocker registry |
| `state/packet_queue.yaml` | Queue state |
| `state/response_application_log.yaml` | Ingestion audit trail |
| `state/blocker_decision_register.yaml` | Decision record |

All 4 are snapshotted before every automated run. Snapshots go to `state/snapshots/<run_id>/`.

---

## Automation Boundary Enforcement

1. **No autonomous approval** — automation discovers and validates responses but never fabricates decisions
2. **No autonomous execution** — follow-up packets are generated but never auto-executed
3. **No external writes** — no Notion, no email, no API calls
4. **Logging is mandatory** — every run writes to `logs/janitor_automation_run_log.md`
5. **Snapshot before mutate** — pre-run snapshot is a hard requirement, not optional
6. **Red-flag check is read-only** — the checker script never writes to state files

---

*Janitor Automation Architecture v0.1 — 2026-04-12*
