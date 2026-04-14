# Issue 01 Sign-off Patch Prompt v0.1

LENY — token discipline mode.

You already have the context. Do not restate background, naming history, or prior reasoning unless a real conflict appears.

Use only:
1. `docs/issues/contract_spine_v0_3/01_lock_contract_spine_ontology.md`
2. `docs/naming/LOOP_contract_spine_nomenclature_v0.1.md`
3. `docs/ontology/contract_spine_ontology.md`
4. `docs/ontology/contract_spine_ontology_decision_log.md`
5. THEO’s last review comments

Do not reread broad doctrine unless needed to resolve a conflict.

## Task
Patch Issue 01 to final-review quality with the smallest valid change set.

## Patch only
- remove runtime-specific language from ontology body/examples
- replace platform/runtime names with neutral surface terms
- remove implementation-specific surface labels
- align `claim` wording to the locked `validation_state` vocabulary

Do not:
- rewrite the ontology
- expand examples
- reopen naming design

## Removal / deprecation rule
If anything is removed, archived, deprecated, replaced, or reduced to pointer-only, report for each item:
- exact item
- action type
- reason
- replacement/forward pointer
- nearby items intentionally not touched
- rollback

No vague cleanup wording. No silent removals. Prefer deprecation/pointers over destructive cleanup. If none, state: `No removals performed`.

## Return only
1. files changed
2. exact patch summary
3. intentionally not changed
4. removals performed
5. blockers, if any
6. final recommendation: `ready` or `not ready` for THEO sign-off

## Silence rules
- no recap
- no rationale dump
- no repeated issue summary
- no future planning unless blocked

Success condition:
THEO can review the revised draft immediately without another loop.
