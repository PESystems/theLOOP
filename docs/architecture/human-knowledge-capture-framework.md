# Human knowledge capture framework

## Purpose

This document defines where human knowledge capture framework artifacts belong in LOOP, what should remain private, and what file structure best supports wiki growth, writeback discipline, and long-term system performance.

## Core split

### Put in GitHub
GitHub should hold the portable method layer:
- reusable capture frameworks
- generic pilot templates
- transcript-to-extraction workflow
- writeback review rules
- graph or entity schema starters
- operator checklists
- naming and storage rules

This is the part that should survive beyond one company or one project.

### Keep local and private
Local private storage should hold the live company intelligence layer:
- named employee capture plans
- raw recordings and transcripts
- personnel risk notes
- customer history
- vendor and contact intelligence
- internal prioritization notes
- reviewed writeback candidates before promotion

This split protects privacy and keeps the repo focused on the framework instead of the company memory itself.

## Why this boundary matters

If the repo mixes framework and live company intelligence, three problems appear fast:
- sensitive internal knowledge leaks into a durable shared surface
- the repo fills with unstable artifacts that should never become doctrine
- the wiki or writeback layer starts competing with raw storage instead of compiling from it

LOOP performs better when:
- GitHub holds reusable system logic
- the Node holds coordination truth
- the Floor holds execution truth and private working artifacts

## Recommended GitHub structure

```text
/docs
  /architecture
    loop-topology.md
    notion-as-coordination-layer.md
    execution-surfaces.md
    human-knowledge-capture-framework.md

  /specs
    transcript-extraction-schema.md
    writeback-review-contract.md
    graph-entity-starter.md
    knowledge-capture-state-model.md

  /roadmap
    knowledge-capture-rollout-plan.md

/templates
  /knowledge_capture
    pilot_micro_capture_template.md
    pilot_service_debrief_template.md
    pilot_process_walkthrough_template.md
    transcript-intake-template.md
    writeback-candidate-template.md

/tools
  /knowledge_capture
    README.md
    sample-packets/
    sample-receipts/
```

## Recommended private local structure

```text
/Floor/private/knowledge_capture/
  /company/
    /people/
      /person_a/
        /pilots/
        /captures_raw/
        /transcripts/
        /extracted/
        /writeback_candidates/
      /person_b/
        /pilots/
        /captures_raw/
        /transcripts/
        /extracted/
        /writeback_candidates/
      /person_c/

    /shared/
      /question_sets/
      /operator_notes/
      /review_queue/
      /approved_writebacks/
      /blocked_or_sensitive/
      /indexes/
```

## Best shape for wiki and LOOP performance

### 1. Keep raw, extracted, reviewed, and canonical separate
Never let raw transcripts sit beside canonical wiki pages at the same status.

Use this progression:

```text
raw capture -> transcript -> extraction -> review -> writeback candidate -> canonical wiki
```

### 2. Prefer small atomic files
Better:
- one pilot artifact per file
- one extraction summary per session
- one writeback candidate per topic or entity cluster

Worse:
- giant mixed documents with raw transcript, commentary, extraction, and final writeback all in one file

### 3. Separate person folders from knowledge-domain folders
Use person folders for capture operations.
Use domain or topic folders for writeback candidates and final wiki material.

That keeps:
- capture workflow human-centered
- final knowledge base topic-centered

### 4. Use stable artifact states in filenames or folders
Recommended states:
- raw
- draft
- review
- approved
- blocked
- final

This is more reliable than guessing status from prose.

### 5. Keep indexes light
Indexes should point, not duplicate.

Use index files for:
- what exists
- where it lives
- what state it is in
- what depends on review

Do not turn indexes into second copies of the artifacts.

### 6. Separate reusable templates from live instances
A template belongs in GitHub.
A filled-in pilot for a real person belongs in private local storage.

### 7. Prefer markdown for framework artifacts
For optimal LOOP performance, framework docs, templates, extraction summaries, receipts, and writeback candidates should default to Markdown.

Use binary formats only when the content truly requires them.

## Recommended file shapes

### Pilot artifact
Keep these sections:
- purpose
- why this pilot exists
- format
- operator instructions
- prompt set
- output format
- stop conditions
- next step

### Extraction artifact
Keep these sections:
- source
- session date
- signals captured
- claims or heuristics
- confidence level
- follow-up questions
- writeback lane
- sensitivity notes

### Writeback candidate
Keep these sections:
- target topic or entity
- proposed content
- source support
- confidence
- reviewer status
- route: approve, revise, or block

## Anti-patterns

Avoid:
- putting named employee intelligence directly in the repo
- storing raw transcripts in the same folder as final wiki pages
- mixing framework docs with company-specific live captures
- using one giant running document per person
- letting extraction and canonical writeback collapse into one step

## Practical rule

GitHub stores the machine and method.
Private local files store the live company memory.
The wiki compiles from reviewed artifacts, not from raw dumps.

## Related docs

- [Docs index](../README.md)
- [LOOP topology](loop-topology.md)
- [Notion as coordination layer](notion-as-coordination-layer.md)
- [Execution surfaces](execution-surfaces.md)
