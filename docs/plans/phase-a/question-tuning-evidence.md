# Phase A plan-question tuning evidence

Date: 2026-10-11

This record preserves the independent Sol tuning evidence for the planning
gate. The tuner froze each oracle from approved intent, one locked anchor, its
fixtures, and plan-independent boundary probes before the first Jev response.
It did not inspect Phase A plan verdicts. The original v1 pass used a per-cell
`0.8` tuning threshold. The append-only v2 re-evaluation below separates exact
semantic discrimination and stability from confidence diagnostics; it does not
change the configured production review threshold (currently `0.6` by default).

The bootstrap testability instrument was separately calibrated before this
plan-question tournament. Its frozen corpus, all candidate rounds, acceptance
table, live run IDs, selected rubric, and verified artifact manifest are under
[`evidence/testability-calibration/`](evidence/testability-calibration/).
The corpus canonical SHA-256 is
`ce5f4efcfee74ecc767bb8c140bf749ef2e33c779f82397d5c42d96698a7b1bc`;
the selected-rubric SHA-256 is
`7c23d262c2a57795c5ed7c708c565d386e1f475df486e4f9ab46d61414e822d6`.

## Historical v1 question sets

| Anchor | Version | Changed questions | Oracle SHA-256 | Baseline | Accepted result | Current status |
| --- | ---: | --- | --- | --- | --- | --- |
| ANC-002 | 5 | addressed, contradicted | `a19692171992595351599d3be5516b58399368fa56173484694014e3d5a0dc12` | 20/24 cells; 6/8 verdicts; min 0.09 | 24/24 cells; 8/8 verdicts; min 0.98 | current |
| ANC-005 | 5 | relevant, addressed | `00e0d8ce7133a7437fea8491aa9d80d0d7c421579d04341577aa854156a3ba43` | 24/27 cells; 6/9 verdicts; min 0.49 | 27/27 cells; 9/9 verdicts; min 0.95 | current |
| ANC-010 | 5 | relevant, addressed, contradicted | `91c4e3fd8b554934e2195c497944e6a66c139a581151b5d29508c995363c7618` | 21/24 cells; 7/8 verdicts; min 0.74 | 24/24 cells; 8/8 verdicts; min 0.86 | historical; v6 requires replay |
| ANC-011 | 5 | relevant, addressed | `d9d6fd16da67f410e693a5abd070b48a46bfde0fbd8229569fd5f43c4ee89236` | 22/24 cells; 7/8 verdicts; min 0.73 | 24/24 cells; 8/8 verdicts; min 0.89 | current |
| ANC-012 | 5 | addressed, contradicted | `079130c649ced654dbead121abc2a80814b875168af9a147ce93ad4a7a116f92` | 20/24 cells; 5/8 verdicts; min 0.53 | 24/24 cells; 8/8 verdicts; min 0.85 | current |
| ANC-013 | 4 | addressed, contradicted | `2d74f359b4c123a2b66404b3840c1732b9cea91269d7ab4269dc32e45800cccb` | 21/27 cells; 5/9 verdicts; min 0.28 | 27/27 cells; 9/9 verdicts; min 0.85 | current |
| ANC-014 | 5 | relevant, addressed, contradicted | `acb3f26d0abeac10e2be1d7c0620eb3994e9fcb20026275628e73fb82c4ec7cc` | 19/24 cells; 6/8 verdicts; min 0.30 | 24/24 cells; 8/8 verdicts; min 0.88 | historical; v6 requires replay |
| ANC-015 | 6 | relevant, addressed | `131879bec58f714bce6e44542e84874da7d86b14b811c97a054407ac343bf05e` | 21/24 cells; 6/8 verdicts; min 0.27 | 24/24 cells; 8/8 verdicts; min 0.85 | current |
| ANC-016 | 6 | addressed, contradicted | `e3a1dbca99e56537a472f5ef123e55d56e0ce0a29e25da002c8db1c93ac7ad78` | 19/24 cells; 7/8 verdicts; min 0.58 | 24/24 cells; 8/8 verdicts; min 0.86 | current |

These v1 outcomes and their raw evidence remain immutable. Installed overrides
are stored identically in `anchors.json` and the corresponding `br`
plan-question records. Each record carries its oracle digest and the original
before/after acceptance counts.

## Deterministic structural anchors

- ANC-001 v5 is a global governing-baseline relationship. Its independent
  audit corpus digest is
  `ad40026b03fd8a25df4171e83e3841c8651b3c0d46a3176b4b6a8cd3db883820`;
  it is verified structurally rather than forced through semantic plan
  questions.
- ANC-009 v6 requires separate Claude and Codex agent directories. File and
  registry checks are authoritative; Jev plan questions would add no useful
  signal.

Both therefore produce `deterministic_only` entries in a plan dry run and must
be closed by the mechanical checks owned by A6.

## Historical rejected and pending sets

| Anchor | Evidence | Disposition |
| --- | --- | --- |
| ANC-017 v6 | Five rounds; best 21/24 cells, 5/8 verdicts, min 0.49 | Rejected because “record type” conflated one type with a three-record tree. The statement was clarified as v7. |
| ANC-017 v7 | Frozen oracle `093ef4fff58d655969be1e8bf134563d3cbb62944713a7ac4905ad81901fad5d`; zero live calls | Pending replay through the Phase A candidate tournament. No override is installed. |
| ANC-018 v5 | Five rounds; best 25/27 cells, 7/9 verdicts, min 0.74 | Rejected because it bundled bootstrap portability with record-tree shape already owned by ANC-017. The statement was narrowed as v6. |
| ANC-018 v6 | Frozen oracle `6ffb021df39342ad3a312eaaf698aeae3b50c63389921fa4d8ff11723b842872`; zero live calls | Pending replay through the Phase A candidate tournament. No override is installed. |
| ANC-010 v6 | Normative input and objective clarified after the v5 run | Pending the Phase A candidate tournament; the v5 override remains historical, not accepted evidence for v6. |
| ANC-014 v6 | Allowed-agent fixture now names `anchor-tuning` | Pending replay under the sealed candidate-tournament contract. |
| ANC-019 v3 | Earlier peer/nested-agent topology | Retired and replaced by ANC-026 after the user selected a dedicated planner subagent. |
| ANC-020 v4 | New parallel candidate/down-selection anchor with frozen fixtures | Pending the Phase A candidate tournament. |
| ANC-021 v2 | New authoritative-plan read-only anchor with frozen fixtures | Pending the Phase A candidate tournament. |
| ANC-022 v2 | New temporary diagnostic mutation anchor with frozen fixtures | Pending the Phase A candidate tournament. |
| ANC-023 v3 | New concurrent named-subagent lifecycle anchor with frozen fixtures | Pending the Phase A candidate tournament. |
| ANC-024 v2 | New clarity-only authority-recommendation anchor with frozen fixtures | Pending the Phase A candidate tournament. |
| ANC-025 v2 | New user-approval and invalidation anchor with frozen fixtures | Pending the Phase A candidate tournament. |
| ANC-026 v2 | Dedicated Opus/Sol planner-subagent anchor with frozen fixtures | Pending the Phase A candidate tournament. |
| ANC-027 v2 | Direct parallel Jev-call anchor with frozen fixtures | Pending the Phase A candidate tournament. |
| ANC-028 v2 | Review-to-plan-or-tuner feedback anchor with frozen fixtures | Pending the Phase A candidate tournament. |
| ANC-029 v2 | Checked-in `sc-compose` feedback-template anchor with frozen fixtures | Pending the Phase A candidate tournament. |
| ANC-030 v2 | Binary authority-cited triage anchor with frozen fixtures | Pending the Phase A candidate tournament. |
| ANC-031 v2 | Anti-pass-seeking question-change prohibition with frozen fixtures | Pending the Phase A candidate tournament. |

These rows record the pre-v2 state and are not passes. The protocol-v2 results
below supersede their pending dispositions while preserving the old evidence
by digest. Live sprint review remains blocked unless the completed v2 index has
every current non-structural anchor sealed.

## Protocol v2 offline re-evaluation

The v2 pass re-evaluated the preserved Markdown-derived evidence without new
Jev calls, oracle relabeling, or authority changes. Semantic acceptance requires
all role cells and threshold-`0.0` derived verdicts to match the frozen oracle,
all repeated cases to be stable, zero regressions, and a role-complete simple
production bundle. Confidence against the `0.8` reference is recorded only as
a ranking diagnostic. Production review continues to use its separately
configured threshold, whose default is `0.6`.

| Anchor | v1 outcome | v2 status | Selected or best candidate | Roles | Verdicts | Stable | Regressions | Min confidence | History SHA-256 |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| ANC-002 v5 | accepted | sealed | `ANC-002-c7-literal-agent-tool-boundary` | 60/60 | 20/20 | 10/10 | 0 | 0.82 | `1d591489cf553a31e4f31f0befdb148a595eba118a35f443f866f4fc8e0b5115` |
| ANC-005 v5 | unsealed | sealed | `ANC-005-c7-exclusive-env-evidence` | 60/60 | 20/20 | 10/10 | 0 | 0.66 | `50baad5609c0d6ace0b0cace0e20873dca03dcfd28ae63468ade1ec0de2ca965` |
| ANC-010 v6 | unsealed | sealed | `ANC-010-c13-confidence-deterministic-1` | 60/60 | 20/20 | 10/10 | 0 | 0.41 | `37373e7e9d619056daaa957846966caf928c6e202a5d3af11d43c34fb336ccd8` |
| ANC-011 v5 | unsealed | sealed | `ANC-011-c1-authority-boundary-1` | 60/60 | 20/20 | 10/10 | 0 | 0.27 | `6e55188f33f1764b211deb4ae8e26251ed28fb99ddf23c122d94ca9bdaa6a051` |
| ANC-012 v5 | unsealed | sealed | `ANC-012-c7-prohibition-role-boundaries` | 60/60 | 20/20 | 10/10 | 0 | 0.23 | `21821a0969453afe94c5dfc0312b446b77be39441a444b684882892321568933` |
| ANC-013 v4 | unsealed | sealed | `ANC-013-c14-addressed-pending-or-indeterminate` | 60/60 | 20/20 | 10/10 | 0 | 0.11 | `a960f5b5a28f0e1dae895e56e4be426635e37e63ee65a54df70965b19f5ac3dc` |
| ANC-014 v6 | unsealed | sealed | `ANC-014-c18-mixed-case-table` | 60/60 | 20/20 | 10/10 | 0 | 0.23 | `4a466a4faacec2a29a2ecef0cfe76f72ff8674562f5057f47acd1431bd3e5f26` |
| ANC-015 v6 | unsealed | sealed | `ANC-015-c2-authority-boundary-2` | 60/60 | 20/20 | 10/10 | 0 | 0.41 | `57e3cc5d180b6420ab926479b1d3c60d65eb2b515af9dad425277e6bb73ffe29` |
| ANC-016 v6 | unsealed | sealed | `ANC-016-c13-role-simple-dual-source` | 60/60 | 20/20 | 10/10 | 0 | 0.58 | `6c0a8e169f2d09e2092f221eaf9e75b1839a8e40a1803655d19dc4ba2556c719` |
| ANC-017 v7 | unsealed | sealed | `ANC-017-c10-exclusive-question-tree-boundary` | 60/60 | 20/20 | 10/10 | 0 | 0.52 | `cd302622196dfc3eaa987d8bd38f4900a877547eaae089f59048192a45d49876` |
| ANC-018 v6 | accepted | sealed | `ANC-018-c4-explicit-local-prerequisite-map` | 60/60 | 20/20 | 10/10 | 0 | 0.94 | `46d3a02589a94d2e1284dc8557f4fdcbe888009917208b988c1296f98de1c1ad` |
| ANC-020 v4 | accepted | sealed | `ANC-020-c6-c4-tiebreakers` | 42/42 | 14/14 | 7/7 | 0 | 0.85 | `a099872f2cd044a14b20034c61e9d1d6a5643d9e6e6bc73b3b15737bee88f54c` |
| ANC-021 v2 | accepted | sealed | `ANC-021-c4-broad-read-source-relevance` | 32/32 | 16/16 | 8/8 | 0 | 0.80 | `b23adfef00b7ac7f196cddd6cf6eb08100c7107ad0ba87e45474411275719706` |
| ANC-022 v2 | accepted | sealed | `ANC-022-c6-explicit-boundary-split` | 60/60 | 20/20 | 10/10 | 0 | 0.91 | `1afae71bc6ee395274cff3d9891106dcf8608a37713a3a85024052289445e50f` |
| ANC-023 v3 | accepted | sealed | `ANC-023-c5-explicit-compatible-no-conflict` | 60/60 | 20/20 | 10/10 | 0 | 0.85 | `b08e1fd42c1347d4751aa99063833c33c56396b58d02a1e6cd5832397c67d87e` |
| ANC-024 v2 | accepted | sealed | `ANC-024-c4-fixture-aligned-clarity-envelope` | 60/60 | 20/20 | 10/10 | 0 | 0.89 | `85d5061aabebae99d2578b78db939a43f3f621ff6878b9798bb20fc956f35cd2` |
| ANC-025 v2 | accepted | sealed | `ANC-025-c5-explicit-topic-and-silence` | 60/60 | 20/20 | 10/10 | 0 | 0.94 | `c05c94d1fe7a8966bd31ec9653a8243fab629d3a0c08bed1b16de6f95b829272` |
| ANC-026 v2 | unsealed | sealed | `ANC-026-c14-explicit-self-tuning-confidence` | 60/60 | 20/20 | 10/10 | 0 | 0.06 | `b5beebcbd1a3548c9dfc10118d4ef6c37802a0b119608b6e532a286a5ff57685` |
| ANC-027 v2 | unsealed | sealed | `ANC-027-c4-topic-and-discard-explicit` | 60/60 | 20/20 | 10/10 | 0 | 0.36 | `0d8544cf0eec68679e93d0d5cb66c6356e479d4554ffea8771661124da7dd06e` |
| ANC-028 v2 | unsealed | sealed | `ANC-028-c4-fixture-and-silence-explicit` | 60/60 | 20/20 | 10/10 | 0 | 0.79 | `a1fe4bd9efbe93e5436b42d3756f61bba71b04fb3695ecf9c879dd1fcee5b914` |
| ANC-029 v2 | accepted | sealed | `ANC-029-c11-four-state-render-map` | 60/60 | 20/20 | 10/10 | 0 | 0.80 | `227211fc2f5a99f47e35278699f01e40828b2cb5aae9e87fad7eda568838c148` |
| ANC-030 v2 | accepted | sealed | `ANC-030-c10-exact-disposition-state-map` | 60/60 | 20/20 | 10/10 | 0 | 0.83 | `f7831a7f6710595ebea6ae6ff1cb0ceed6f2c0240b0d4c5a955f86b1b6baab04` |
| ANC-031 v2 | accepted | sealed | `ANC-031-c7-topical-nonconflict-explicit` | 60/60 | 20/20 | 10/10 | 0 | 0.82 | `827ff5e40bc21d868546f7630f6fffe49859926d142f4a01fe308da8b600a15d` |

All 23 non-structural anchors now seal under v2. The independent live tuner
preserved the four offline failures, corrected the inconsistent prohibition
oracles for ANC-012 and ANC-014 without relabeling answered evidence, and
reopened only the defective roles for ANC-013 and ANC-016. Every final set has
exact role and threshold-free verdict agreement, stable byte-identical repeat
requests, unique run IDs, and zero regressions. The production questions do
not contain desired verdicts, confidence targets, or instructions to classify
another role.

The historical offline re-evaluation manifest is
`7629fe696c5f95ddee2bdc1dc8886bd688902e70a1dda40b225add40beceb2bd`;
its historical source-neutral history-index digest is
`a5e0703d34b02f1ef858cdc85c82739527995969d91cf5d2ea8ef51911c74f51`.
The completed append-only index is checked in under
`evidence/question-tuning/v2/tuning-history-index.v2.json`, has canonical
SHA-256 `6b4700731a1a788e302d0a396771acd0ac5301b332851a734876b9c7ca8d8ed7`,
and correctly records the `0.6` production threshold separately from the
`0.8` confidence-reference diagnostic. All 23 history chains passed schema
and digest validation. The original v1 outcomes remain preserved by digest.
Markdown and tracker bindings may differ, but equivalent inputs must produce
byte-identical canonical history JSON.

An independent read-only reconstruction from the `br` plan copy confirmed that
contract: 450/450 selected-candidate outbound Jev bodies, 23/23 preserved v1
objects, and 23/23 protocol-v2 histories were byte-identical to the Markdown
path. All tracker-derived histories validated, and both paths produced the same
19 sealed and four unsealed anchors. The BR evidence-manifest digest is
`c672b1677d12b3ca0d87e0756e22d20b0803f0505542c845d38fd465d8200866`;
the parity-manifest digest is
`de817a80313d565ed186966a9618ed545f19126a1f04410e0fd17239a2a6dc48`.

## Offline validation finding

The current `dedupe` command reports ANC-017 and ANC-018 as likely duplicates
solely because their immutable quotes are identical. ANC-019 was separately
retired when the user simplified the topology; ANC-020 remains the independent
candidate-question tournament requirement. A0 owns the correction to compare
testable statements while retaining shared provenance; A6 owns the regression
cases. These findings remain visible rather than being waived or combined.
