# Execution Surfaces

## The short version

An **execution surface** is not the whole system.
It is the specific runtime or operator on the Floor that takes a bounded instruction and turns it into a real side effect.

That distinction matters.

In LOOP terms:
- **The Container** teaches the system how to think and behave
- **The Node** tracks shared state and coordination
- **The Floor** is where real work artifacts and side effects live
- an **execution surface** is the particular runnable layer on that Floor that actually does the job

## Why this matters

A lot of AI workflow talk is vague about where execution really happens.
That makes it easy for planning, generation, and real action to blur together.

LOOP tries to make execution explicit.

## What makes up an execution surface

A true execution surface has five parts:

1. **A runtime**
   Something that can actually act.

2. **A reachable workspace**
   It can see the files, inputs, or systems it needs.

3. **A bounded instruction**
   Usually a packet, prompt, or task contract.

4. **Permission boundaries**
   What it may read, write, or change.

5. **Proof of completion**
   Output, receipt, and failure handling.

Without those five things, you do not really have an execution surface. You just have chat intent.

## Main execution surfaces inside LOOP

### Claude Code
Best for:
- repos
- scripts
- file operations
- code generation
- structured local automation

### Cowork
Best for:
- local knowledge work
- staged file work
- multi-step workspace tasks
- execution that still benefits from a broader desktop context

### Manual human execution
Best for:
- approval gates
- risky operations
- ambiguous migrations
- anything not yet safe to automate

### Future relay or script runner
Best for:
- repeatable automation
- timed jobs
- webhook reactions
- batch processing

## The world flow

In plain language, work moves like this:

1. **Source surfaces** provide raw material
   - docs
   - email
   - PDFs
   - local notes
   - uploaded files

2. **Thinking surfaces** classify and plan
   - Theo
   - Lenny’s Brain

3. **The Container** shapes behavior
   - doctrine
   - skills
   - naming
   - prompt specs

4. **Packetization** turns work into a bounded contract
   - objective
   - source material
   - anti-goals
   - deliverable
   - constraints
   - proof of completion

5. **An execution surface** acts on the Floor

6. **Floor artifacts** become real
   - outputs
   - receipts
   - scripts
   - reports

7. **Distillation upward** happens only after execution
   - concise coordination truth may go to the Node
   - repeatable behavior may go to the Container
   - deep execution detail stays on the Floor

That is the practical meaning of distill, don’t duplicate.
