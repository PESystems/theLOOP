# LOOP
**Live Overview of Open Projects**

> LOOP is not a “Claude setup.” It is a control system for AI-assisted work that forces task classification, execution honesty, and governed knowledge promotion.

![LOOP control-system overview](assets/loop-infographic-notebooklm-v1.webp)

## What this is

LOOP is an attempt to build a working system for AI-assisted execution that does not collapse planning, execution, memory, and truth into the same surface.

The claim is simple:

Most AI workflows feel impressive at first, then get sloppy.
They blur:
- raw input
- working context
- plans
- executed actions
- canonical truth

LOOP tries to separate them on purpose.

## The thesis

LOOP makes three core bets:

1. **Intelligence without routing is unreliable**
   Every task should be classified before action.

2. **Planning and execution are not the same event**
   A draft is not a result. A plan is not a change. Suggested work is not completed work.

3. **Truth should be promoted, not assumed**
   Generated material should not become canonical just because it exists.

That is the real point of the system.

## Why this matters

Most AI tooling is optimized for generation.
LOOP is trying to optimize for:
- governed execution
- inspectable state
- bounded agency
- reusable operational context
- cleaner handoffs between humans, chats, files, and execution surfaces

In other words:

> not smarter chat for its own sake
>
> better control over AI-assisted work

## A real example

One practical test for LOOP was taking a rough handwritten project dump and turning it into structured project context.

A notebook page with:
- client names
- partial scope notes
- equipment references
- contact cues
- follow-up hints

was pushed through a structured intake contract and used to generate project records that could connect to:
- clients
- project types
- system types
- priorities
- next actions
- import notes
- AI scope summaries

The value was not just cleanup.
It was the beginning of **compounding context**.

## Core architecture

LOOP uses a layered model:

- **The Node** → coordination truth
- **The Container** → behavioral truth
- **The Floor** → execution truth

Supporting roles sit around that core:

- **Theo** → strategy, critique, architecture pressure-testing
- **Lenny’s Brain** → planning, routing, synthesis, controlled low-risk action
- **Cowork / Claude Code** → structured execution on the Floor
- **The Relay / Connectors** → integrations and automation surfaces

Two governing rules matter a lot:

> planning is not execution

> distill, don’t duplicate

## Current state

This repo is not a polished framework release.
It is an early public version of a working system.

Right now it is strongest as:
- a theory of governed AI work
- a system architecture and operating model
- a structured intake / validation / write-through direction
- a starting point for human-in-the-loop agent workflows

It is still unfinished.
That is part of why it is worth sharing early.

## Start here

- [Topology overview](docs/architecture/loop-topology.md)
- [YAML → Notion pipeline spec](docs/specs/yaml-to-notion-pipeline.md)
- [AutoResearch integration plan](docs/roadmap/autoresearch-integration-plan.md)
- [Architecture reference](docs/references/loop-architecture-v2.4.md)
- [Doctrine addendum](docs/references/loop-doctrine-addendum-v2.4.1.md)

## Feedback I actually want

Useful feedback is not “cool idea.”

Useful feedback is:
- where the boundaries are weak
- where the system is overbuilt
- where it is under-specified
- what should stay opinionated
- what should become more portable
- what failure modes I am not seeing yet

If you have built second-brain systems, agent workflows, structured knowledge pipelines, or human-in-the-loop automation, that is the kind of feedback I care about most.
