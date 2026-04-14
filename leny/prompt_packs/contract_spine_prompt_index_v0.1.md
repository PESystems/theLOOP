# Contract Spine Prompt Index v0.1

Branch purpose: companion execution prompt pack for the active Contract Spine issue stack.

## Operating rule
- Use Contract Spine naming only.
- Treat GitHub issue files + naming lock + active Notion spec as the authority slice.
- Prefer one build prompt and one review/patch prompt only where needed.
- Keep active Floor scope narrow: active control docs only, not historical sweep.

## 16-prompt map
| Prompt | Issue | Purpose |
|---|---|---|
| P01 | 01 | ontology draft build |
| P02 | 01 | ontology patch/sign-off |
| P03 | 02 | core schema draft build |
| P04 | 02 | core schema patch/sign-off |
| P05 | 03 | validation layer contract |
| P06 | 04 | receipt layer contract |
| P07 | 05 | adapter layer pattern draft build |
| P08 | 05 | adapter layer patch/sign-off |
| P09 | 06 | Claude.ai ingress lane |
| P10 | 07 | Floor execution lane draft build |
| P11 | 07 | Floor sync / patch / sign-off |
| P12 | 08 | Node compile boundary draft build |
| P13 | 08 | boundary check / patch / sign-off |
| P14 | 09 | migration packet build |
| P15 | 09 | migration execution / verification |
| P16 | 10 | acceptance pack + final rollout review |

## Primary companion file
- `leny/prompt_packs/contract_spine_prompt_pack_v0.1.md`

## Special-case companion file
- `leny/prompt_packs/issue01_signoff_patch_prompt_v0.1.md`
