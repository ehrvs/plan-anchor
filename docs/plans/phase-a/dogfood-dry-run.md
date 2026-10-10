# Phase A plan-anchor dogfood: offline source parity

Date: 2026-10-10

This record covers request construction only. It is not a Jev verdict and does
not satisfy the live planning gate.

## Inputs

- Anchors: 18 locked records from `anchors.json`.
- Markdown source: the seven sprint documents linked by `plan-phase-a.md`.
- Tracker source: descriptions of `br` issues `pa-sza.1` through `pa-sza.7`.
- Command path: `jev_judge.py judge --gate plan --all --dry-run`, once for each
  source and sprint, using the same logical item ID and title for each pair.

## Results

| Sprint | Characters | Markdown / `br` content SHA-256 | Normalized requests/results equal |
| --- | ---: | --- | --- |
| A1 | 4,033 | `34f18dd16c7b7975889199befb2b4a8e78b1b6471ee8b4b73f8d7e73d265cc20` | yes |
| A2 | 5,220 | `39abf66e6ef9f80baaf4cfe58e3355671848f086b699c4399e79214a6ba4612b` | yes |
| A3 | 4,588 | `b06cf6b6d911c332d1e43c19f9885b4502a16601134f3a37d7e9355dcd4d716e` | yes |
| A4 | 3,626 | `7133c74451ee111aecdfa67d61089649b4f13522f02692d25be427590c65499a` | yes |
| A5 | 4,021 | `33665f9b39cc43802cb6b656659ce2d05409e122cba6d9594d930c558405609d` | yes |
| A6 | 3,383 | `f5c5f86168f6d96bab298a6eeca20dbffa6a0397375d0470bad6a2b7681bd29d` | yes |
| A7 | 4,574 | `f42e2267622aa2d2a429c3a84d9e8a0e66f468eb84c9212f35c9cb66b1926e67` | yes |

For each pair, the dry-run item metadata after excluding the source locator,
all 18 serialized Jev requests, all placeholder results, and the summary were
equal. Every sprint is below the current 24,000-byte planning request cap.

## Bootstrap finding

The registered 0.4.0 `anchor-plan-review` agent cannot execute this dual-source
review as written: it requires `bd` and composes plan text with `bd show`, while
this repository has a `br` workspace and the Markdown source has no plan-issue
dependency. The underlying judge accepts the sprint files and tracker-copy text
directly, which is how this offline parity check was performed. Sprints A2, A3,
and A5 own the permanent source/adapter/agent correction.

## Live follow-up

Before the live gate, the independent Sol tuner must run the rubric and frozen
oracle workflow for the locked anchors. Then a Luna plan-review Agent must review
each sprint from Markdown and from the `br` copy. The TypeSafe payload is limited
to one anchor, its tuned questions, and one normalized sprint item per request.
