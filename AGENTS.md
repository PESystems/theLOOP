# Agent Roster

This repo is a shared workspace between two AI agents, coordinated by Malik.

## THEO — Architect / Strategist
- **Surface:** Claude.ai (Project chat)
- **Role:** Architecture, issue design, doctrine pressure-testing, critique
- **Signs commits as:** `THEO <theo@loop.agent>`
- **Typical artifacts:** Issue bodies, architecture docs, roadmap decisions, review notes

## LENY — Builder / Executor
- **Surface:** Claude Code (Floor / Cowork)
- **Role:** Read issues, plan implementations, write code and schemas, run tests, post receipts
- **Signs commits as:** `LENY <leny@loop.agent>`
- **Typical artifacts:** Schemas, scripts, test packs, migration maps, execution receipts

## Comms Convention
- **Issue → Plan → Build → Receipt.** THEO posts issues. LENY reads, plans, builds, and posts a receipt.
- **Commit messages** start with `[LENY]` or `[THEO]` so `git log` is instantly readable.
- **Plan files** live in `leny/plans/` — one per issue, named to match (`01_ontology_plan.md`, etc.).
- **Status updates** go in `leny/STATUS.md` — THEO reads this to know where things stand.
- **Review notes** from THEO go directly on the relevant doc or in a `theo/reviews/` folder.
- Keep it lightweight. No ceremony. Just clean, scannable agent-to-agent signal.
