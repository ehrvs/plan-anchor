# ANC-012 / ANC-014 prohibition-oracle v2 tuning report

Status: both anchors sealed. No authority recommendation is required.

## Authority and oracle supersession

The approved INTENT and locked anchor meanings are unambiguous. Both anchors
are `prohibition` records, so the existing plan-gate mapping uses `relevant`
and `contradicted` and deliberately ignores `addressed`/compliance. The v1
oracle files and answered v1/v2 evidence remain unchanged under
`/private/tmp/phase-a-anchor-tuning-markdown-v2-reevaluation-20261011`.

The superseding oracles keep every fixture text, authority rationale, and
expected role answer unchanged. Only mechanically derived verdict labels
change:

- ANC-012: `silent-relevant` and `topical-only` change from `not_addressed` to
  `satisfied`; `boundary` changes from `underspecified` to `satisfied` because
  its relevance/conflict tuple is `yes`/`no` and compliance is non-gating.
- ANC-014: `silent-relevant` and `topical-only` change from `not_addressed` to
  `satisfied`.

Canonical oracle-content digests (canonical JSON without a trailing newline):

- ANC-012: `6cae36388aafea8e729605e24ab8849ddbdaa7f0e0672ddfbedd4d5031b6b109`
- ANC-014: `8d0ab25ed507ffcb0fb50ea04c5700901a8e3f2153825e1fa28a10fc36fddb42`

Production confidence remains configured/default `0.6`. Tournament semantic
evaluation uses `0.0`. The separate `0.8` value is diagnostic and affects
ranking only.

## Final tournament

Each anchor used three materially distinct, role-complete question candidates,
ten frozen cases, and two repeats per candidate/case: 60 live Jev runs per
anchor. Every repeat pair has byte-identical canonical requests, and all 60 run
IDs per anchor are unique. The command supplied `--allow-remote`; it supplied
no `PLAN_ANCHOR_*` environment variable.

| Anchor | Selected candidate | Question digest | Role cells | Semantic verdicts | Stable cases | Regressions |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| ANC-012 | `ANC-012-c7-prohibition-role-boundaries` | `145d407d7e6222fd055e54d52015426699e59a337d83c2c8cb38c6e7dd8e240f` | 60/60 | 20/20 | 10/10 | 0 |
| ANC-014 | `ANC-014-c18-mixed-case-table` | `bd76be8c805a44cbf1dffeabbcfe3c8ed963072d78971ea480e312b2acc99542` | 60/60 | 20/20 | 10/10 | 0 |

Jev answered as `jev-1.13.0`. Confidence diagnostics are retained but were not
semantic acceptance conjuncts. ANC-012 had 55/60 cells at or above 0.8,
minimum 0.23, mean 0.9372. ANC-014 had 50/60 cells at or above 0.8, minimum
0.23, mean 0.8880.

## Evidence integrity

The history for each anchor is source-neutral, schema-valid, and append-only:

1. the original v2 re-evaluation rejection is byte-preserved;
2. a diagnostic round is rejected because repeat item IDs made request bodies
   non-identical;
3. a byte-identical diagnostic round is rejected because concurrent calls
   produced duplicate second-resolution run IDs; and
4. the timestamp-separated, byte-identical round seals the question set.

All 401 SHA-256 sidecars under this evidence root validate. A scan for the
actual `TYPESAFE_API_KEY` value found zero matches. The runner does not expose
the private HTTP response body separately; `raw-cli-responses/` contains the
exact, unmodified structured stdout emitted by `jev_judge.py`, while
`live-runs/` contains the persisted normalized response and answers.

Key artifact file SHA-256 digests:

| Artifact | File SHA-256 |
| --- | --- |
| `manifest.json` | `8aa3939ffd4ec913128c8c71796a651f9f535d0fea1f358246e9ef27abcbf344` |
| `ANC-012/evaluation.json` | `fa216bb3ebefd865ee5d0865794f9e2bb0e2ad801f234fefc60b2407eeb4106c` |
| `ANC-012/tuning-history.v2.appended.json` | `001a3e49fe0d35d023f9b8dac6743cc948ba988805ea96dc5fe3cb618d89c9d4` |
| `ANC-012/sealed-question-set.json` | `5124ba922a3393977cb4050094a86efe507b32a7c9695c737423ec79ddc0688e` |
| `ANC-014/evaluation.json` | `1693fbb91465f5c838d7fdf9276b0dc50bf1ce664ac7add62d0e9e4be92773a8` |
| `ANC-014/tuning-history.v2.appended.json` | `db870e7b5b94b8964c254d5729c2db802305ccd62055d1ee483cde7ad75bfee0` |
| `ANC-014/sealed-question-set.json` | `c6e4f2ac3846146e5b66749b0b3e83547ee5455cc2e712ecc7ed18ee29693501` |

No repository file or BR state was modified by this tuning task.
