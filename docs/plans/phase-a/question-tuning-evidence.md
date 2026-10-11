# Phase A plan-question tuning evidence

Date: 2026-10-11

This record covers the independent Sol tuning pass for the planning gate. The
tuner froze each oracle from the approved intent, one locked anchor, its
fixtures, and plan-independent boundary probes before the first Jev response.
It did not inspect Phase A plan verdicts. A question set is accepted only when
every expected semantic cell and derived verdict agrees with the frozen oracle
at confidence 0.8 or higher.

## Accepted question sets

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

The accepted overrides are stored identically in `anchors.json` and the
corresponding `br` plan-question records. Each question record also carries a
comment with its oracle digest and before/after acceptance counts.

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

## Rejected and pending sets

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

These pending rows are failures to complete the calibration gate, not passes.
PR #10 plans the dedicated tuning subagent and tournament that will replace this
single-candidate evidence format. Phase A must not enter live sprint review
until every current non-structural anchor reaches the new acceptance standard.

## Offline validation finding

The current `dedupe` command reports ANC-017 and ANC-018 as likely duplicates
solely because their immutable quotes are identical. ANC-019 was separately
retired when the user simplified the topology; ANC-020 remains the independent
candidate-question tournament requirement. A0 owns the correction to compare
testable statements while retaining shared provenance; A6 owns the regression
cases. These findings remain visible rather than being waived or combined.
