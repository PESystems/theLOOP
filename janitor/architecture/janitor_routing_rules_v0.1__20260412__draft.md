---
tags:
- janitor
- routing
- v0_1_1
---
# Janitor Routing Rules v0.1.1

**Patch:** Phase 2A.1 — packet model normalization

## When a blocker becomes a Dispatch packet

Route to Dispatch when **all three** are true:
1. The blocker maps to a specific skill in the orchestrated set (`skill-improvement`, `artifact-version-promotion`, `workspace-path-migration`)
2. The triggering evidence is concrete (file path, miss count, version mismatch — not "needs investigation")
3. The target skill can verify completion autonomously (grep returns zero, version bumps, file exists)

Dispatch packets are YAML. Target surface = `dispatch`. Malik does not need to approve the routing itself, but the downstream skill may still gate on Malik (e.g., promotion requires Malik sign-off).

## When a blocker becomes a Claude Code packet

Route to Claude Code when **all three** are true:
1. The work is bounded T2 Floor execution (design doc, code, schema change, file sweep)
2. The work fits in a single Claude Code session
3. No external API calls, no Notion writes, no Container mutations required

Claude Code packets are Markdown execution prompts. Target surface = `claude_code`. These require Malik to invoke the prompt manually.

## When a blocker becomes a Cowork packet

Route to Cowork when:
1. The work requires interactive Malik collaboration (e.g., reviewing options, iterating on design)
2. OR the work spans Container + Floor (Cowork sessions can bridge both)
3. OR the blocker is partially unblocked and needs Malik to finish the last step in-session

Cowork packets are Markdown. Target surface = `cowork`. Malik opens a Cowork session and pastes or loads the prompt.

## When a blocker remains Malik-only

A blocker stays as a Malik decision form (no dispatch packet) when:
1. The blocker is typed `malik_decision` and requires a choice between options that only Malik can evaluate
2. OR the blocker requires manual action via a UI Lenny cannot access (claude.ai Container management, Notion UI, browser-only operations)
3. OR the blocker is a strategic/business decision (naming conventions, priority ordering, scope decisions)

Malik-only items get HTML decision forms + YAML response templates. No dispatch packet is generated. After Malik responds, the next Janitor sweep reads the YAML response and may then route a follow-up dispatch.

## When Janitor must halt instead of routing

Janitor does NOT route and logs a hard-stop when:
1. The blocker type is `external_dependency` and no Malik action can resolve it (e.g., third-party service down, file system access issue)
2. The blocker description contains insufficient evidence to construct a bounded packet (no file paths, no skill name, no version — too vague)
3. Routing would require writing to Notion, mutating LENY_WrkSps, or triggering automation hooks (none of these are available in Phase 2A)
4. The blocker is already in the `pending_*_dispatches` register and the previous dispatch has not been confirmed or expired

In halt cases, the blocker is logged in the generation report as `not_generated` with a reason. It remains in the active blocker register and will be re-evaluated on the next sweep.

## Routing precedence

When a blocker could route to multiple surfaces:
1. If it requires Malik's decision first → Malik-only form (always wins)
2. If it maps to an orchestrated skill → Dispatch
3. If it's bounded T2 Floor work → Claude Code
4. If it needs interactive collaboration → Cowork
5. If none of the above → Halt, log as unroutable

## Surface-to-format mapping

| `target_surface` | `artifact_format` | `routing_mode` | Invocation |
|-----------------|-------------------|----------------|-----------|
| `dispatch` | `yaml` | `dispatch_ready` | Loaded by Dispatch protocol for skill routing |
| `claude_code` | `markdown` | `direct_execution` | Malik pastes into Claude Code CLI |
| `cowork` | `markdown` | `direct_execution` | Malik loads in Cowork session |
| `lenny` | `markdown` | `direct_execution` | Malik loads in standard Lenny session |
| `manual` | `html` | `manual_decision` | Malik opens HTML, fills form, saves YAML |

## Routing mode definitions

| `routing_mode` | Meaning |
|----------------|---------|
| `direct_execution` | Packet is a self-contained execution prompt. Malik invokes it manually in the target surface. |
| `manual_decision` | Packet surfaces a choice for Malik. No execution until Malik responds via form/YAML. |
| `dispatch_ready` | Packet is structured for automated dispatch to an orchestrated skill. |
| `watch_only` | No artifact generated. Blocker is monitored across sweeps for self-resolution. |

---

*Janitor Routing Rules v0.1.1 -- 2026-04-12*
