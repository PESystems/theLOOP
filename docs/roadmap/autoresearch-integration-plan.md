# LOOP AutoResearch Integration Plan
**Version:** v0.1  
**Date:** 2026-04-09  
**Status:** Draft

---

## 1. Purpose

Define how AutoResearch-style improvement loops should be integrated into LOOP without corrupting:
- canonical truth
- schema discipline
- operator trust
- execution boundaries

This is not a plan to let agents freely self-improve.

It is a plan to introduce controlled ratchets where the evaluation signal is strong enough to justify automation.

---

## 2. Core idea

AutoResearch works best when three conditions exist:

1. **Constrained surface**
2. **Executable evaluation**
3. **Clear keep / reject signal**

That is why it compounds in bounded technical systems.

LOOP can use the same pattern, but only in the parts of the system where the evaluation signal is stable enough.

---

## 3. The main caution

LOOP is not a single-file benchmarked codebase.

It includes:
- fuzzy human input
- evolving schemas
- subjective output quality
- multiple surfaces
- coordination truth vs execution truth
- human judgment

So the mistake to avoid is pretending the entire system can be optimized with one metric.

It cannot.

---

## 4. Strong recommendation: use dual-loop improvement

LOOP should use **two different evaluation loops**.

### Loop A — Objective loop
For things that can be mechanically evaluated.

### Loop B — Preference loop
For things that need human judgment.

This is the right architecture for LOOP.

---

## 5. Loop A — Objective AutoResearch domain

Use objective loops for:
- extraction accuracy
- schema compliance
- field completeness
- source-linking completeness
- claim validation
- contradiction handling
- formatting contracts
- packet validity
- write-through rule compliance

These are the best candidates for monotonic improvement.

### Generic objective loop
```text
Propose change
→ Run validation set
→ Compare score
→ Keep or reject
→ Repeat
```

### Important constraint
Objective loops may optimize:
- extraction logic
- validation logic
- formatting logic
- packet assembly logic

They may not directly rewrite canonical doctrine.

---

## 6. Loop B — Human preference domain

Use human preference loops for:
- README clarity
- wiki readability
- dashboard usefulness
- page layout
- note structure
- prompt UX
- diagram quality
- operator confidence / usability

These are not stable enough for pure metric optimization.

They should be optimized with structured human judgment.

### Good preference criteria
- clearer
- more scannable
- less cluttered
- more useful in practice
- easier to act on
- more honest about uncertainty

---

## 7. Human-in-the-loop rule

Malik / Theo can act as evaluator, but not as a pure vibe metric.

To avoid drift, human evaluation should be structured.

Minimum pattern:
- better / worse / same
- why
- what improved
- what regressed
- approval yes / no

---

## 8. Best immediate next step

Do not start with self-improving LOOP.

Start with this:
1. build an extraction + validation eval set
2. lock the write-through validation contract
3. define structured human preference review for readable outputs
4. only then start running improvement loops

That is the path that compounds without wrecking trust.
