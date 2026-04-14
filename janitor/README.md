# Floor Janitor

**A bounded, detection-first sweeper for LOOP trackers, blockers, and packet queues.**

Janitor is the automated heartbeat that keeps Floor work visible without letting any AI agent make decisions on Malik's behalf. It discovers, validates, and logs — it never approves.

---

## What Janitor does

| Capability | Behavior |
|-----------|----------|
| **Response ingestion** | Scans `forms/*_response.yaml`, validates against contract rules, applies approved decisions to state |
| **Blocker tracking** | Maintains a registry of blockers across trackers with escalation stages, days-unresolved, and status lifecycle |
| **Packet queue** | Tracks Type 1 follow-up packets through `generated → ready_for_review → executed_verified` |
| **Red-flag detection** | 12 read-only rules across 4 families (aging, response, queue, integrity) |
| **Scheduled sweep** | Runs every 2 days via Claude Scheduled Task, produces receipts |
| **Pre-mutation snapshots** | SHA-256-verified backups of all 4 core state files before any mutation |

## What Janitor does NOT do

- Does not make blocker decisions (Malik-only authority)
- Does not auto-execute follow-up packets (explicit per-packet authorization required)
- Does not write to Notion
- Does not send dispatches
- Does not widen scope beyond what's been authorized

---

## Package Contents

```
janitor/
├── README.md                          ← you are here
├── STATUS.md                          ← phase tracker
├── automation/
│   ├── run_janitor_scheduled.py       ← scheduled sweep entrypoint
│   ├── check_janitor_red_flags.py     ← read-only red-flag checker
│   ├── janitor_scheduler_setup_v0.1   ← setup guide (Claude Scheduled Tasks primary)
│   └── janitor_claude_scheduled_task_spec_v0.1
├── architecture/
│   ├── floor_janitor_agent_design_v0.3           ← original agent spec
│   ├── floor_janitor_implementation_phases_v0.3  ← phase plan
│   ├── floor_janitor_state_schema_v0.3.yaml      ← state file schema
│   ├── floor_janitor_output_templates_v0.3
│   ├── janitor_sweep_prompt_v0.3
│   ├── janitor_response_ingestion_contract_v0.1  ← validation + idempotency rules
│   ├── janitor_type1_packet_contract_v0.1        ← packet model
│   ├── janitor_routing_rules_v0.1
│   ├── janitor_automation_architecture_v0.1      ← 3-layer automation model
│   └── janitor_red_flag_rules_v0.1               ← 12 detection rules
├── hooks/
│   └── janitor_hooks_draft.md         ← hook scaffolding (deferred)
├── receipts/                          ← phase completion receipts
└── reports/                           ← phase execution reports
```

---

## Runtime Data (NOT in git)

Janitor's operational state lives **outside** this repo, in `JANITOR_WrkSps/`:
- `state/janitor_state.yaml` — blocker registry
- `state/packet_queue.yaml` — queue state
- `state/response_application_log.yaml` — ingestion audit trail
- `state/blocker_decision_register.yaml` — decision record
- `state/snapshots/` — pre-mutation backups
- `forms/*.yaml` — Malik's filled response decisions
- `dispatch_packets/` — generated follow-ups
- `logs/*.md` — run logs (mutated every automated run)

These are excluded by design — they change constantly and may contain decision context. The packaged app is code + contracts + history.

---

## How to Use

### 1. Run a red-flag check (read-only, anytime)
```
python automation/check_janitor_red_flags.py
```
Exit codes: 0 = clear, 1 = low/medium, 2 = high, 3 = critical integrity.

### 2. Run a dry-run sweep (proves the pipeline without mutating state)
```
python automation/run_janitor_scheduled.py --mode dry-run
```

### 3. Run a real sweep (produces snapshot + run log entry)
```
python automation/run_janitor_scheduled.py --mode sweep
```

### 4. Scheduled automation
The Claude Scheduled Task `janitor-sweep-2d` runs every 2 days at 9:00 AM local.
See `automation/janitor_scheduler_setup_v0.1__20260412__draft.md` for details.

---

## Design Documents

Start with these, in order:
1. `architecture/floor_janitor_agent_design_v0.3` — what Janitor is and why
2. `architecture/floor_janitor_implementation_phases_v0.3` — build plan
3. `architecture/janitor_response_ingestion_contract_v0.1` — how responses get validated
4. `architecture/janitor_automation_architecture_v0.1` — 3-layer automation model
5. `architecture/janitor_red_flag_rules_v0.1` — detection rules

---

*Floor Janitor — packaged 2026-04-13*
