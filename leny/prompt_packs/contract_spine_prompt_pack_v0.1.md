# Contract Spine Prompt Pack v0.1

Use these prompts in order. Keep LENY in delta mode. No recap unless blocked.

---

## P01 — Issue 01 draft build
Use only:
1. `docs/issues/contract_spine_v0_3/01_lock_contract_spine_ontology.md`
2. `docs/naming/LOOP_contract_spine_nomenclature_v0.1.md`
3. `LOOP Contract Spine Spec + Issue Pack v0.3`

Task:
Build the active Issue 01 delivery under Contract Spine naming.

Deliver:
- `docs/ontology/contract_spine_ontology.md`
- `docs/ontology/contract_spine_ontology_decision_log.md`
- receipt
- status update

Rules:
- lock only the minimum ontology
- keep `intent` out of ontology core
- use directed list as primary relationship map
- include forbidden drift patterns
- mark old YAML-family ontology historical, do not delete it

Return only:
1. files changed
2. exact result
3. blockers
4. recommendation

---

## P02 — Issue 01 patch/sign-off
Use only:
1. `docs/ontology/contract_spine_ontology.md`
2. `docs/ontology/contract_spine_ontology_decision_log.md`
3. naming lock
4. THEO review comments

Task:
Make Issue 01 canon-ready with the smallest valid patch set.

Patch only:
- remove runtime-specific language from ontology body/examples
- replace platform/runtime names with neutral surface terms
- remove implementation-specific surface labels
- align `claim` wording to locked `validation_state` vocabulary

Return only:
1. files changed
2. exact patch summary
3. intentionally not changed
4. removals performed
5. blockers
6. final recommendation: ready / not ready

---

## P03 — Issue 02 draft build
Use only:
1. `docs/issues/contract_spine_v0_3/02_establish_core_contract_spine_schema.md`
2. `docs/naming/LOOP_contract_spine_nomenclature_v0.1.md`
3. active Issue 01 outputs
4. embedded core contract shape in `LOOP Contract Spine Spec + Issue Pack v0.3`

Task:
Build the runtime-neutral core Contract Spine schema.

Deliver:
- active schema artifact
- schema decision log if needed
- receipt
- status update

Rules:
- schema may include `intent`; ontology may not
- keep core contract runtime-neutral
- separate source, artifact, claims, uncertainty, validation, promotion, receipts, adapter-facing fields cleanly
- no model-specific wording in canonical schema

Return only:
1. files changed
2. schema summary
3. blockers
4. recommendation

---

## P04 — Issue 02 patch/sign-off
Use only Issue 02 outputs + Issue 02 spec + THEO review comments.

Task:
Patch Issue 02 to review-ready with the smallest valid change set.

Check only:
- ontology/schema boundary is clean
- required fields are explicit
- states are non-overlapping
- no runtime leakage
- receipt and promotion fields are audit-safe

Return only:
1. files changed
2. exact patch summary
3. intentionally not changed
4. blockers
5. final recommendation: ready / not ready

---

## P05 — Issue 03 validation layer contract
Use only:
1. Issue 03 spec
2. naming lock
3. active Issues 01–02 outputs

Task:
Build the Validation Layer contract.

Deliver:
- validation contract artifact
- receipt
- status update

Rules:
- validation decides claim quality, not promotion destination
- support `pass`, `fail`, `provisional`, `blocked`, `conflict`
- make uncertainty input, validation output
- define minimum checks, block conditions, and conflict handling

Return only:
1. files changed
2. contract summary
3. blockers
4. recommendation

---

## P06 — Issue 04 receipt layer contract
Use only:
1. Issue 04 spec
2. naming lock
3. active Issues 01–03 outputs

Task:
Build the Receipt Layer contract.

Deliver:
- receipt contract artifact
- receipt examples or receipt schema if needed
- status update

Rules:
- one receipt per operation
- structured, not narrative
- receipts reference artifacts; they do not become artifacts
- include dry-run, live-write, blocked, and failure handling

Return only:
1. files changed
2. contract summary
3. blockers
4. recommendation

---

## P07 — Issue 05 adapter layer pattern draft build
Use only:
1. Issue 05 spec
2. naming lock
3. active Issues 01–04 outputs
4. Notion Contract Spine page for active surfaces

Task:
Build the Adapter Layer pattern.

Deliver:
- adapter pattern artifact
- receipt
- status update

Rules:
- adapters translate, they do not redefine ontology or schema
- define adapter responsibilities, limits, and mapping behavior
- keep core contract portable; runtime specifics stay in adapters

Return only:
1. files changed
2. pattern summary
3. blockers
4. recommendation

---

## P08 — Issue 05 adapter layer patch/sign-off
Use only Issue 05 outputs + THEO review comments.

Task:
Patch the Adapter Layer pattern to review-ready.

Check only:
- narrow adapter definition
- no schema invention in adapters
- no ontology drift
- clean separation of core contract vs adapter concerns

Return only:
1. files changed
2. exact patch summary
3. intentionally not changed
4. blockers
5. final recommendation: ready / not ready

---

## P09 — Issue 06 Claude.ai ingress lane
Use only:
1. Issue 06 spec
2. naming lock
3. active Issues 01–05 outputs
4. Contract Spine Notion page

Task:
Define the Claude.ai Ingress Lane under active Contract Spine naming.

Deliver:
- ingress lane contract/artifact
- receipt
- status update

Rules:
- cover source intake, normalization boundary, packetization handoff, and receipt behavior
- keep Claude.ai-specific behavior in lane/adapters, not in core ontology/schema
- no fake Floor access assumptions

Return only:
1. files changed
2. lane summary
3. blockers
4. recommendation

---

## P10 — Issue 07 Floor execution lane draft build
Use only:
1. Issue 07 spec
2. naming lock
3. active Issues 01–06 outputs
4. closure artifacts from naming sync / Floor sync if relevant

Task:
Define the Floor Execution Lane.

Deliver:
- floor execution lane artifact
- receipt
- status update

Rules:
- Floor = execution truth
- lane must define what belongs on Floor, what gets written back, and what remains local
- active Floor scope only; do not sweep historical debris

Return only:
1. files changed
2. lane summary
3. active Floor surfaces implicated
4. blockers
5. recommendation

---

## P11 — Issue 07 Floor sync / patch / sign-off
Use only Issue 07 outputs + active Floor sync artifacts + THEO review comments.

Task:
Run the narrow active-surface sync or patch pass required to make the Floor Execution Lane review-ready.

Rules:
- patch active Floor control docs only
- preserve historical artifacts
- every removal/deprecation must include exact item, reason, replacement, scope boundary, rollback
- if no removals, state `No removals performed`

Return only:
1. files changed
2. exact patch summary
3. active Floor docs touched
4. removals performed
5. blockers
6. final recommendation: ready / not ready

---

## P12 — Issue 08 Node compile boundary draft build
Use only:
1. Issue 08 spec
2. naming lock
3. active Issues 01–07 outputs
4. Contract Spine Notion page

Task:
Build the Node Compile Boundary contract.

Deliver:
- compile boundary artifact
- receipt
- status update

Rules:
- define what crosses into Node / canonical state and under what conditions
- distinguish validation from promotion
- require auditable review/promotion logic
- no broad Node mutation assumptions

Return only:
1. files changed
2. boundary summary
3. blockers
4. recommendation

---

## P13 — Issue 08 boundary check / patch / sign-off
Use only Issue 08 outputs + THEO review comments + any active Node-side closure notes.

Task:
Patch the Node Compile Boundary to review-ready.

Check only:
- compile boundary is explicit
- promotion gate is explicit
- Node writes are scoped and auditable
- no conflict between compile logic and Receipt Layer / Validation Layer

Return only:
1. files changed
2. exact patch summary
3. intentionally not changed
4. blockers
5. final recommendation: ready / not ready

---

## P14 — Issue 09 migration packet build
Use only:
1. Issue 09 spec
2. naming lock
3. active Issues 01–08 outputs
4. prior naming closure audit/packet/receipt artifacts

Task:
Build the migration packet for existing Contract Spine lanes.

Deliver:
- migration packet
- migration checklist
- receipt or draft execution note

Rules:
- active namespace is singular
- preserve historical artifacts as historical
- migration must be non-destructive by default
- distinguish active control surfaces from archives

Return only:
1. files changed
2. migration packet summary
3. blockers
4. recommendation

---

## P15 — Issue 09 migration execution / verification
Use only Issue 09 packet + active audits + THEO review comments.

Task:
Execute or stage the narrow migration/verification pass needed to align GitHub + active Floor surfaces.

Rules:
- active GitHub namespace + active Floor control docs only
- explicit removal/deprecation proof if anything is removed, archived, deprecated, replaced, or pointer-only
- preserve historical paths with forward pointers where needed
- stop if scope expands beyond active surfaces

Return only:
1. execution verdict: complete / partial / blocked
2. files changed
3. exact migration summary
4. legacy preserved
5. blockers
6. final recommendation

---

## P16 — Issue 10 acceptance pack + final rollout review
Use only:
1. Issue 10 spec
2. naming lock
3. active outputs from Issues 01–09
4. status board

Task:
Build the Contract Spine acceptance pack and final rollout review artifact.

Deliver:
- acceptance pack
- rollout review / completion receipt
- final status update

Rules:
- verify contract stack coherence, naming coherence, active-surface coherence, and outstanding blockers
- distinguish complete vs ready-for-testing vs deferred
- do not canonically promote items that still fail review gates

Return only:
1. files changed
2. acceptance summary
3. unresolved blockers
4. final recommendation: ready for canonical review / one more pass needed / hold
