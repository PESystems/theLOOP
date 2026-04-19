# ETH Bot v1.0 — Handoff Packet for THEO Review

**From:** LENY (Floor / Claude Code)
**To:** THEO (Architect / Strategist)
**Date:** 2026-04-19
**Project:** `Projects/ETH_BOT_v1/` — NOT part of Contract Spine issue stack. Separate initiative using the Contract Spine pattern as an architectural scaffold.
**Status:** Stable. Ready for architectural critique before a first training run is attempted.
**Commit:** `c0622b7` — `[LENY] Initial commit — ETH bot v1.0 through Batch 5`

---

## TL;DR

ETH/USD paper-trading bot with an auto-research loop that uses Claude to propose strategy parameter deltas based on a governed wiki pipeline. Built over 5 architectural batches. Core runtime path (Kraken WS → candles → regime classification → research cron) is live. Training loop **execution side** (signal → paper trade → journal) is intentionally unwired — deferred to the next experiment file. A modular experiment plugin system means every future addition is a single file, deletable in one motion.

**What I'm asking for:** architectural critique on three specific decisions (listed at the bottom) before a real training run is attempted.

---

## The project in one paragraph

The ETH bot is a Contract-Spine-patterned trading bot where Claude serves as the research analyst inside a gated pipeline. Kraken WS emits ticks, a CandleBuilder aggregates 4h OHLCV candles, a RegimeDetector classifies bull/bear/crab with conflict detection, and every 6 hours a ResearchRunner reads the verified market context and trade journal and proposes parameter deltas. An IngressRunner experiment fetches live market data every 4h through the ingress → distillation → validation → compile-boundary pipeline. A KnowledgeLoader experiment augments the research analyst's system prompt with entries from a compounding knowledge base. Params never reach production without passing through `scripts/approve-params.ts` (the sole promotion path) with Loop A bounds validation.

---

## Architecture batches — what each did

| Batch | Scope | Key change |
|---|---|---|
| 1 | Hard blockers | Fix stale model ID; remove duplicate approval gate |
| 2 | Regime foundation | Create CandleBuilder module; time-based lookback; 8 regime output fields |
| 2.5 | Controller wiring | Connect Kraken → Candle → Regime path |
| 3A | Classify trigger | Candle-close invokes `regimeDetector.classify()` |
| 3 | Research runner compliance | Load skill doc as system prompt; read verified context; 19-field YAML receipts; Loop A bounds validation; `conflict_notes` field |
| 4 | Config + index cleanup | `config.research.sources`; Contract Spine dirs in wikiIndex; table-format output |
| 5 | Auto-research loop + knowledge base | Modular experiment system; 3 experiments (ingress-runner, context-refresh, knowledge-loader); 6-file knowledge base with frontmatter-addressed selection |

Full receipts in `Projects/ETH_BOT_v1/wiki/research-runs/*-receipt.md`.

---

## Current state — what works, what doesn't

### ✅ Works

- Kraken WS connects; tick stream → CandleBuilder (4h windows)
- CandleBuilder → RegimeDetector (needs 10 candles = 40h warmup)
- RegimeDetector writes `wiki/regimes/current.md` with all 8 required fields
- IngressRunner cron (4h) fetches from alternative.me / coingecko / binance-futures / defillama; writes full Contract Spine artifacts (ingress → distilled → conflicts → verified → receipt)
- ContextRefresh cron (2h) updates marker-delimited provisional block
- KnowledgeLoader injects 4 of 6 knowledge files (`always` + `on_research_run` triggers) into research-analyst.md at boot; auto-reverts on stop
- ResearchRunner cron (6h) reads augmented skill + verified context; writes 19-field YAML receipt; bounds-validates before proposing
- approve-params.ts is the sole write path to `active-params.json`; archives prior version before overwrite

### ❌ Not wired (intentional — next experiment to build)

- SignalEngine exists (EMA/RSI/MACD) but is not wired to the tick stream
- PaperExecutor exists (simulated testnet trades) but is never called
- TrainingLogger exists (writes `wiki/trade-journal/*.md`) but never invoked
- On-chain parallel path (Sepolia OnChainExecutor) reachable only from unreachable `startLiveMode()` path

**Consequence:** if the bot starts now, it will run cleanly for 6h, write its first research receipt, have zero trade journal evidence, produce confidence ~0.12, and never propose a promotion. Pipeline smoke test only.

### ⚠️ Known open items (non-blocking, flagged)

- No typecheck run — deps not installed at ETH_BOT_v1/node_modules/
- `pass` promotion in ingress-runner returns false — multi-run consistency window designed but not implemented
- KnowledgeLoader mutates `research-analyst.md` at runtime then reverts on stop. Visible/auditable but non-standard. Alternative would be to read knowledge files directly inside researchRunner. Flagged for review.
- Live mode is stubbed — throws on entry

---

## Modular experiment system — the compounding surface

`src/experiments/` with a typed Experiment contract (scope + proof declaration required):

```
src/experiments/
├── types.ts           ← Experiment interface (stable contract)
├── index.ts           ← explicit registry — 1 import + 1 array entry per experiment
├── ingress-runner.ts  ← deletable
├── context-refresh.ts ← deletable
└── knowledge-loader.ts ← deletable
```

Controller dispatches `onTrainingStart`, `onTick`, `onCandle`, `onStop` lifecycle hooks. Adding an experiment is one file. Removing is deletion + two registry edits. No coupling to core modules.

**Design intent:** experiments are the fast-iteration surface; the core bot (Kraken → candle → regime → signal → executor → journal) stays stable.

---

## Knowledge base — wiki/knowledge/

6 distilled concept pages + README. Each has frontmatter tags, trigger_contexts, and compound_weight. KnowledgeLoader selects entries by matching trigger_contexts to runtime events.

| File | Weight | Trigger |
|---|---|---|
| autoresearch-core-pattern.md | high | always |
| execution-surface-model.md | high | always |
| slop-is-control-failure.md | high | on_low_confidence |
| narrow-bounded-gated.md | medium | on_research_run |
| research-spine-decomposition.md | medium | on_research_run |
| provenance-and-validation.md | medium | on_param_proposal |

Sourced from: LOOP autoresearch bootstrap + reference-lock notes, research spine prompt pack, agentic coding anti-slop report, cold-run proto-autoresearch stack, human knowledge graphing methods. Excluded: industrial automation / client tracking / LOOP-specific workflow docs (scope: bot-relevant autoresearch only).

**The compounding mechanism:** adding a knowledge file = bot uses it immediately on next research run. No code change. After 30 days with 15 new files, the research analyst has 21 doctrine patterns vs today's 6. This is the leverage point.

---

## THREE QUESTIONS FOR THEO'S REVIEW

I'd like architectural pressure-testing on these three specifically. Everything else I'm confident in; these are the places I'm not.

### Q1 — Is the KnowledgeLoader's runtime-mutation pattern defensible?

`src/experiments/knowledge-loader.ts` augments `wiki/skills/research-analyst.md` in place at training start, reads snapshot, appends marker-delimited knowledge block, writes file back. On stop, original is restored from the in-memory snapshot.

**Pros:** simple, visible (open the file and see exactly what the research runner is sending); no changes needed to researchRunner.ts; delete the experiment file and behavior reverts cleanly.

**Cons:** runtime mutation of a file that's also a governance artifact feels wrong; if the process crashes mid-run, the augmented file persists (startup would re-augment on top of augmentation — idempotent due to marker-replace, but still); it couples skill-file state to process lifecycle.

**Alternatives I considered:**
- (B) Read knowledge files directly in researchRunner.loadSkillDoc() — cleaner separation but couples researchRunner to knowledge-loader's concerns and breaks the "experiments are deletable" promise
- (C) Use the `system` parameter as an array of blocks (Anthropic SDK supports this) — researchRunner passes `system: [base, ...knowledgeBlocks]` — cleanest semantically but requires researchRunner to know about knowledge base

Which would you choose and why?

### Q2 — Should the 6 knowledge files be inside the ETH bot wiki, or lifted up to theLOOP?

Right now the knowledge base lives at `Projects/ETH_BOT_v1/wiki/knowledge/`. Most of the content (reference-lock pattern, execution surface model, anti-slop doctrine, provenance chains) is NOT bot-specific — it's general autoresearch doctrine. I could move 4 of the 6 files to a shared location (maybe `Claude/wiki/knowledge/` or a new LOOP doctrine dir) and have multiple projects reference them.

**Tradeoff:** duplication now (bot reads from its own copy) vs coupling later (if doctrine moves, bot references break). Also, lifted files would need to be loaded by the KnowledgeLoader from a path outside the ETH_BOT_v1 tree — doable but crosses a boundary.

Keep local for now and lift later, or lift now and set the precedent?

### Q3 — Is it architecturally wrong to ship the first training run with zero execution wiring?

The bot today runs a research loop on a tick stream with no signal evaluation, no executor, no trade journal. The research runner will produce low-confidence receipts forever because there's nothing to evaluate. I flagged this as "Option: wire trade-signal-dispatch before first training run" — one more single-file experiment, probably 100 lines.

**The question:** is this a real architectural concern or am I over-worrying? The loop IS functional — it just loops on emptiness. Letting it run for 24h before wiring execution would at least verify Kraken stability, ingress-runner stability, research API stability. That's data. But it's also dishonest to call it a "training run" when nothing trains.

Your call: ship the execution wiring before starting, or run headless first to shake out pipeline bugs?

---

## Specific files for review

If you want to dig into the code, these are the highest-signal files:

- `Projects/ETH_BOT_v1/src/experiments/types.ts` — Experiment contract (30 lines)
- `Projects/ETH_BOT_v1/src/experiments/knowledge-loader.ts` — the runtime-mutation pattern (Q1)
- `Projects/ETH_BOT_v1/src/experiments/ingress-runner.ts` — Contract Spine pipeline in code
- `Projects/ETH_BOT_v1/src/wiki/researchRunner.ts` — main research loop
- `Projects/ETH_BOT_v1/src/core/controller.ts` — experiments dispatcher
- `Projects/ETH_BOT_v1/wiki/knowledge/*.md` — the 6 knowledge pages (Q2)
- `Projects/ETH_BOT_v1/wiki/research-runs/2026-04-16-batch5-receipt.md` — full Batch 5 receipt with open issues

---

## Review artifacts expected back

Per theLOOP AGENTS.md pattern — review notes from THEO can go:
- Inline comments in the source files (for Q1/Q2 implementation-level feedback)
- A `theo/reviews/eth_bot_v1_batch_5_review.md` in the theLOOP repo (for Q3 and higher-level critique)
- Issues in the LENY/THEO stack if any findings warrant dedicated follow-up work

No rush — the bot is stable as-is and I'll not ship a first training run until the three questions above get pressure-tested.
