# Phase A plan-anchor dogfood: offline source parity

Date: 2026-10-10

This record covers request construction only. It is not a Jev verdict and does
not satisfy the live planning gate.

## Inputs

- Anchors: 13 locked records from `anchors.json`; two structural anchors use
  deterministic checks and the other 11 produce Jev requests.
- Markdown source: the eight sprint documents linked by `plan-phase-a.md`.
- Tracker source: descriptions of `br` issues `pa-sza.8`, then `pa-sza.1`
  through `pa-sza.7`, ordered by the sprint ID copied into each document rather
  than by tracker issue ID.
- Command path: `jev_judge.py judge --gate plan --all --dry-run`, once for each
  source and sprint, using the same logical item ID and title for each pair.

## Results

| Sprint | Bytes | Markdown / `br` content SHA-256 | Canonical request-set SHA-256 | Normalized dry runs equal |
| --- | ---: | --- | --- | --- |
| A0 | 5,129 | `d05760b09354809c77b0ff6dba49327a5c33851eec880ee442cb8ebbec520976` | `7352361751bcd8707160775e17288047f95dc2160846ab82b016fd274ed274a7` | yes |
| A1 | 4,114 | `d38f7e1ecabbfbeacce82e2d0851dca789a041510e1b733f4b4f1b79eb58176e` | `67b1b32f36df08d0302c1646d9561c6b5935b12082abed4f2ecdb98410f94a56` | yes |
| A2 | 5,428 | `0dc6264005049ee6fa1e65ac58cc6ca01d380977d53a1ffde446e2028d93fa2a` | `032a73b882c970d43b71e59a41c37cd4af72a5de9052495773424f099c4611ff` | yes |
| A3 | 4,579 | `3147a0a9b49de8b0511ba104f1d74584eedd13d4436e49c1393a2951a484d131` | `d85d3702f3ed2ab640354ca03867a8c6462f519d0c61dbcfaeccffd50a70ef10` | yes |
| A4 | 3,635 | `dfb4032bcdbd8b4d58658485a3e018b3234ecd07abb8d2252fe9a143ca40e7f4` | `d1dff7b0b91240d3ced2539ce771c0b6c02a054c0c58216fe4eea780d8e64d15` | yes |
| A5 | 4,269 | `432c593ebf02ab291a5f15d84bb0573d9b2853564e0506bfc89fe1449346c85d` | `80a20aded775105bcad72bd0575d110fd281b0fa75b26e6a80f2355ed674f89c` | yes |
| A6 | 3,781 | `e3620a8e007a50c8b1ec9dc2ae7644d89c17cbec2220cfb3a9233ad047013b49` | `5ce655e025ec6ac4fdbbc5074a7d374ead329d3bf72f590ccc6573b728293adc` | yes |
| A7 | 5,088 | `4e6f02f05015cc18570faa64ce71f6ae89cfac3e164a21f424e2bb28ded0dfba` | `26460b6f9edf4768d66532e1c9a50a924946f003edf2f23f6b891ed9b8294a01` | yes |

For each pair, the complete item bytes and all 11 serialized Jev requests are
equal. After excluding only the expected source locator (`<path>` versus
`stdin`), item metadata, structural results, placeholder results, summary, and
totals are equal. Every sprint is below the current 24,000-byte per-request
planning cap.

## Bootstrap finding

The registered 0.4.0 `anchor-plan-review` agent cannot execute this dual-source
review as written: it requires `bd` and composes plan text with `bd show`, while
this repository has a `br` workspace and the Markdown source has no plan-issue
dependency. The underlying judge accepts the sprint files and tracker-copy text
directly, which is how this offline parity check was performed. Sprints A2, A3,
and A5 own the permanent source/adapter/agent correction.

## Live follow-up

Before the live gate, the independent Sol tuner must finish ANC-017 v7 and
ANC-018 v6 against their already-frozen oracles. Then a Luna plan-review Agent
must review each sprint from Markdown and from the `br` copy. The TypeSafe
payload is limited to one anchor, its tuned questions, and one normalized sprint
item per request. Payload-specific approval is pending; no live plan verdict is
claimed by this document.
