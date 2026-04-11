# LOOP
**Live Overview of Open Projects**

> LOOP is not a Claude setup. It is a control system for AI-assisted work that forces task classification, execution honesty, and governed knowledge promotion.

![LOOP control-system overview](assets/loop-infographic-notebooklm-v1.webp)

## Why this is worth sharing

Most AI work systems collapse too many things into one surface:
- source material
- working context
- planning
- execution
- memory
- truth

That feels powerful early and sloppy later.

LOOP is an attempt to separate those concerns on purpose.

It makes a stronger argument than a typical second-brain or agent stack:
- **Notion should be a coordination layer, not the brain**
- **execution should happen on explicit execution surfaces, not inside vague chat intent**
- **work should move through bounded packets, not hidden session context**
- **truth should be promoted through gates, not assumed because a model said it**
- **the model should operate as disciplined intelligence, not as warehouse memory**

## The thesis

LOOP makes three core bets:

1. **Intelligence without routing is unreliable**
   Every task should be classified before action.

2. **Planning and execution are not the same event**
   A draft is not a result. A plan is not a change. Suggested work is not completed work.

3. **Truth should be promoted, not assumed**
   Generated material should not become canonical just because it exists.

That is the real point of the system.

## What makes LOOP different

### 1. Notion as coordination truth
LOOP uses Notion as **The Node**: inspectable shared state, handoffs, dashboards, project records, and coordination truth.

That means Notion is **not** asked to be:
- the reasoning layer
- the execution layer
- the file system
- the warehouse of every draft and transcript

That separation is one of the more interesting parts of the system.

### 2. Execution surfaces, not abstract automation
LOOP distinguishes between the **Floor** and the **execution surface**.

- **The Floor** is the full execution environment where side effects and artifacts become real.
- An **execution surface** is the specific runtime or operator on that Floor that takes a bounded packet and produces a real result.

In practice, that can be:
- Claude Code
- Cowork
- a manual human operator
- later, a relay or script runner

That distinction matters because it makes execution explicit, inspectable, and easier to govern.

### 3. Packetized work instead of hidden chat state
LOOP tries to move work through bounded packets with:
- objective
- source material
- anti-goals
- deliverable
- constraints
- proof of completion

That makes execution less dependent on invisible session memory and more dependent on explicit contracts.

### 4. Distillation upward
Only after execution do results move upward:
- concise coordination truth may go to the Node
- repeatable behavioral rules may go to the Container
- deep execution detail stays on the Floor

That is the practical meaning of **distill, don’t duplicate**.

## How work moves through LOOP

At a high level, the system separates:
- **source surfaces** for raw input such as docs, email, PDFs, notes, and files
- **thinking surfaces** such as Theo and Lenny’s Brain for classification, planning, critique, and packaging
- **The Container** for doctrine, skills, and behavior-shaping context
- **The Node** for shared coordination truth
- **execution surfaces** for real work on the Floor
- **the Floor** for artifacts, side effects, receipts, and work-in-progress

The flow is simple:

**source material → planning/classification → packetization → execution surface → Floor artifact + receipt → distillation upward**

That is the system LOOP is trying to make reliable.

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
- a coordination-first use of Notion
- an explicit model of execution surfaces
- a structured intake / validation / write-through direction
- a starting point for human-in-the-loop agent workflows

It is still unfinished.
That is part of why it is worth sharing early.

## Start here

- [Why LOOP is worth sharing](docs/vision/why-loop-is-worth-sharing.md)
- [Notion as coordination layer](docs/architecture/notion-as-coordination-layer.md)
- [Execution surfaces](docs/architecture/execution-surfaces.md)
- [Topology overview](docs/architecture/loop-topology.md)
- [YAML → Notion pipeline spec](docs/specs/yaml-to-notion-pipeline.md)
- [AutoResearch integration plan](docs/roadmap/autoresearch-integration-plan.md)
- [Architecture reference](docs/references/loop-architecture-v2.4.md)
- [Doctrine addendum](docs/references/loop-doctrine-addendum-v2.4.1.md)

## Feedback I actually want

Useful feedback is not cool idea.

Useful feedback is:
- where the boundaries are weak
- where the system is overbuilt
- where it is under-specified
- what should stay opinionated
- what should become more portable
- what failure modes I am not seeing yet

If you have built second-brain systems, agent workflows, structured knowledge pipelines, or human-in-the-loop automation, that is the kind of feedback I care about most.
