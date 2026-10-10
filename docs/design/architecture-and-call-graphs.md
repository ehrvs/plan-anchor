# Plan anchoring: architecture and call graphs

Design document for the `plan-anchoring` skill. Companion to the [PRD](../plan-anchor-prd.md) and to [data model, gating and lifecycle](data-model-and-gating.md). Diagrams are Mermaid.

Status: implemented and verified live against Jev `jev-1.13.0` on both gates. Revision 0.3 (2026-10-10) adds, from first use on a real plan: the statement/quote split, the testability rubric, the background question tuner, deduplication, deterministic shape metrics, and size-as-symptom handling of oversized beads. Marketplace packaging is pending.

## 1. Components

Three tiers, following the two-tier skill/agent architecture plus one external judge. Everything that must be exact lives in the script; everything that needs judgment lives in the main session or in Jev.

```mermaid
flowchart LR
    subgraph Session["Main session (planning agent or quality manager)"]
        Skill["plan-anchoring SKILL.md<br/>capture, lock, orchestrate, post reports"]
    end

    subgraph Agents["Isolated subagents (Task tool)"]
        PlanAgent["anchor-plan-review<br/>one planning bead per run"]
        SprintAgent["anchor-sprint-review<br/>one sprint per run"]
        Tuner["anchor-question-tune (background)<br/>one anchor and gate per run"]
    end

    subgraph Script["scripts/jev_judge.py (stdlib Python)"]
        Compose["compose-item"]
        Judge["judge"]
        Gate["decide(): gating in code"]
        Report["report / coverage / diff"]
        Record["add / update / retire / promote / render"]
        Quality["lint / rubric / dedupe / shape<br/>check-fixtures"]
    end

    Jev[("TypeSafe Jev<br/>POST /v1/systemone")]
    Beads[("beads (bd)<br/>anchor bead tree, plan beads, sprint beads")]
    Docs[("doc/plan/phase-current/<br/>intent.md, anchors.json, anchors.md, anchor-runs/")]

    Skill -- "lock / promote / retire" --> Record
    Record --> Docs
    Skill -- "bd create / bd comment" --> Beads
    Skill -- "Task tool, ≤3 in parallel" --> PlanAgent
    Skill -- "Task tool" --> SprintAgent
    Skill -- "Task tool, background, after lock" --> Tuner
    Tuner --> Quality
    Quality -- "rubric, dedupe, fixtures" --> Jev
    Tuner -- "fenced JSON: tested override" --> Skill
    PlanAgent -- "bd show --json (read-only)" --> Beads
    SprintAgent -- "bd children --json, gh pr view, git diff --stat (read-only)" --> Beads
    PlanAgent --> Compose --> Judge
    SprintAgent --> Compose
    Judge -- "one request per anchor" --> Jev
    Jev -- "choice, probabilities, confidence" --> Judge
    Judge --> Gate --> Docs
    PlanAgent -- "fenced JSON" --> Skill
    SprintAgent -- "fenced JSON" --> Skill
    Skill --> Report
```

Responsibilities:

| Tier | Owns | Never does |
| --- | --- | --- |
| Skill (main session) | Detecting candidates, writing each as one testable statement with the verbatim quote kept, running the rubric and dedupe, locking through the script, spinning off the tuner, creating the bead tree, deciding what to judge, posting reports, triaging verdicts and oversized beads | Judging text itself, locking a statement that is just the quote, computing coverage or size by hand, splitting a bead to pass |
| Agents | Composing the exact text Jev sees, resolving question overrides from beads, invoking the script once, returning fenced JSON; the tuner rewrites one question per round and proves it against fixtures and known beads | Editing beads, the record, the plan or code; posting comments; retrying around the script; tuning to make one bead pass |
| Script | IDs, lint, rubric and dedupe requests, the Jev request, retries, response validation, gating, run files, coverage, diffs, shape metrics, report rendering | Calling `bd` or `gh`; deciding what to judge; shortening plan prose |
| Jev | Answering three or four independent typed questions about one anchor and one item | Counting, gating, explaining, seeing more than one item |

## 2. Planning gate call graph

Fan-out happens at two levels. The skill fans out across planning beads (at most three agents at once, one correlation ID each, aggregated in bead order). Inside each agent the script fans out across anchors, one Jev request per anchor, so Jev never sees two anchors or two beads together.

```mermaid
flowchart TD
    PA["Planning agent<br/>(main session, plan-anchoring skill)"]
    PA -- "enumerate open children of the phase epic" --> List["bd children &lt;epic&gt; --json"]
    List --> Fan{"fan out, ≤3 concurrent,<br/>correlation_id = bead id"}

    Fan --> A1["anchor-plan-review<br/>bead bd-41"]
    Fan --> A2["anchor-plan-review<br/>bead bd-42"]
    Fan --> A3["anchor-plan-review<br/>bead bd-43"]

    subgraph One["inside one agent (bd-42)"]
        S1["bd show bd-42 --json"] --> S2["compose-item → /tmp/.../bd-42.txt"]
        S3["plan-questions beads → overrides.json"] --> S4
        S2 --> S4["jev_judge.py judge --gate plan --all"]
        S4 --> Q1["Jev: ANC-001 × bd-42<br/>relevant / addressed / contradicted"]
        S4 --> Q2["Jev: ANC-002 × bd-42"]
        S4 --> Q3["Jev: REQ-014 × bd-42"]
        S4 --> Qn["Jev: … one request per locked anchor"]
        Q1 --> G["decide() per anchor"]
        Q2 --> G
        Q3 --> G
        Qn --> G
        G --> Run["anchor-runs/plan-&lt;stamp&gt;-bd-42.json"]
        Run --> Rep["report --format md"]
        Rep --> Env["fenced JSON envelope<br/>pass, failing[], results[], report_markdown"]
    end

    A2 --> One
    A1 --> Agg
    Env --> Agg
    A3 --> Agg

    Agg["skill aggregates in bead order<br/>summary: succeeded[], failed[]"]
    Agg --> Cov["jev_judge.py coverage --gate plan<br/>anchors × beads, uncovered anchors"]
    Agg --> Post["bd comment &lt;bead&gt; --file report.md"]
    Cov --> Act{"any contradicted / not_addressed /<br/>underspecified / error, or uncovered anchor?"}
    Act -- "yes" --> Edit["re-read the bead text that was sent,<br/>edit the plan or escalate"] --> Fan
    Act -- "no" --> Pass["planning gate passes"]
```

Request count is deterministic: locked anchors × planning beads. Twenty anchors across fifteen beads is 300 Jev requests, each about 100 ms and priced on input tokens only, so re-running after every plan edit is the intended cadence. The third identical failing run on one bead is a hard stop that escalates to the user instead of editing again.

## 3. Development gate (sprint review) call graph

The same anchors, judged against an account of delivered work instead of the plan. The quality manager drives it, the agent assembles evidence in a fixed priority order, and the development question set adds an evidence question so a claim of compliance is separated from a demonstration of it.

```mermaid
flowchart TD
    QM["Quality manager<br/>(QA side of the dev/QA matrix)"]
    QM -- "sprint_id, evidence paths or pr_number" --> SA["anchor-sprint-review"]

    subgraph Assemble["assemble the account (≤ 24,000 chars, priority order)"]
        E1["1. sprint report / completion summary"]
        E2["2. PR title and body<br/>(gh pr view --json)"]
        E3["3. git diff --stat base..head<br/>(file names and counts only)"]
        E4["4. test summary lines"]
        E5["5. closed child beads: title + close_reason<br/>(bd children &lt;sprint&gt; --json)"]
        E1 --> E2 --> E3 --> E4 --> E5
    end

    SA --> Assemble --> Work["compose-item → /tmp/.../sprint-2-work.txt"]
    SA --> Ov["dev-questions beads → overrides.json"]
    Work --> J["jev_judge.py judge --gate dev --all"]
    Ov --> J

    J --> D1["Jev: ANC-001 × sprint-2<br/>relevant / implemented / violated / evidenced"]
    J --> D2["Jev: ANC-002 × sprint-2"]
    J --> Dn["Jev: … one request per locked anchor"]
    D1 --> G["decide() per anchor<br/>adds asserted_only when evidence is missing"]
    D2 --> G
    Dn --> G
    G --> Run["anchor-runs/dev-&lt;stamp&gt;-sprint-2.json"]
    Run --> Checks["collect deterministic_checks for<br/>satisfied and asserted_only anchors"]
    Run --> Rep["report --format md"]
    Checks --> Env["fenced JSON envelope<br/>results[], deterministic_checks[], report_markdown"]
    Rep --> Env
    Env --> QM

    QM --> RunChecks["run each deterministic check<br/>(git log --follow, diff -r, rg, tests)"]
    RunChecks --> Decide{"all anchors satisfied,<br/>every check recorded?"}
    Decide -- "no" --> Block["block acceptance; comment on sprint bead and PR"]
    Decide -- "yes" --> Accept["development gate passes"]
```

The two gates are separate because they judge different things. An anchor that was faithfully planned and then abandoned in code passes the planning gate and fails here. Jev only confirms the account *describes* following the directive; the paired deterministic check confirms the code did.

## 4. One judge invocation, with retries

Every call to Jev goes through the script, which owns the attempt policy. Agents call the script once and never add a retry loop of their own, so the behaviour is identical under Claude Code (agent) and Codex (skill running the agent's steps inline).

```mermaid
sequenceDiagram
    autonumber
    participant Ag as anchor-*-review agent
    participant S as jev_judge.py judge
    participant J as Jev API

    Ag->>S: --gate, --item-file, --overrides-file, --all
    S->>S: validate anchors.json, load question set, merge overrides
    S->>S: fail closed unless TYPESAFE_API_KEY and PLAN_ANCHOR_ALLOW_REMOTE_JUDGE=1

    loop for each locked or promoted anchor
        S->>S: build state {anchor, item}, pre-flight: shorten item until request ≤ 24,000 bytes
        loop up to 3 attempts
            S->>J: POST /v1/systemone {model, state, questions}
            alt 200 and response validates
                J-->>S: answers {choice, probabilities, confidence}
                S->>S: decide() → verdict, min_confidence
            else 422 token limit exceeded
                J-->>S: max_tokens_exceeded
                S->>S: halve item text (keep head, mark truncation), retry<br/>stop at 2,000 chars → verdict error JEV.CONTEXT_EXCEEDED
            else 429 / 529 / 5xx / network / invalid response
                J-->>S: transient failure
                S->>S: wait Retry-After or 1 s, then 2 s, next attempt<br/>after 3 attempts → verdict error (JEV.*)
            else 401
                J-->>S: unauthorized
                S-->>Ag: abort run, AUTH.CREDENTIALS (never retried)
            end
        end
        S->>S: record answers, attempts, item_chars_sent, questions_sha256
    end

    S->>S: sort by severity, summary {counts, failing, pass}
    S->>S: write anchor-runs/<gate>-<stamp>-<item>.json
    S-->>Ag: JSON {success, data: {run_path, results, summary}}, exit 0 pass, 1 fail, 2 fatal
    Ag->>S: report --run <run_path> --format md
    S-->>Ag: markdown with each failing anchor's statement and verbatim quote
    Ag-->>Ag: return fenced JSON envelope to the skill
```

Policy summary:

| Situation | Behaviour | Where |
| --- | --- | --- |
| Request too large before sending | Shorten the item to fit 24,000 bytes, keep the head, mark truncation | script pre-flight |
| Jev reports the context window exceeded (422) | Halve the item and retry; stop below 2,000 characters with `JEV.CONTEXT_EXCEEDED` | script, per anchor |
| 429, 529, 5xx, timeout, network error, malformed response | At least two more attempts (three total) with `Retry-After` or 1 s then 2 s backoff; then `verdict: error` for that anchor only | script, per anchor |
| 401 or missing opt-in | Abort the whole run immediately; never retried; never bypassed by an agent | script pre-flight |
| Agent sees `success: false` | Return the script's error object in the fenced envelope; no second judge call | agent |
| Skill sees a failed bead among several | Report it in the aggregation summary; do not drop it or silently re-run | skill |

## 5. Two execution modes

Claude Code has subagents; Codex and Cursor do not. The agent files are written so the same steps run either way.

```mermaid
flowchart LR
    subgraph CC["Claude Code"]
        S1["skill"] -- "Task tool, isolated context" --> A1["anchor-plan-review agent"] --> J1["jev_judge.py"]
    end
    subgraph CX["Codex / Cursor"]
        S2["skill"] -- "follows ../../agents/anchor-plan-review.md itself" --> J2["jev_judge.py"]
    end
    J1 --> Jev[("Jev")]
    J2 --> Jev
```

The script path is resolved relative to the skill directory (`scripts/jev_judge.py` next to `SKILL.md`), with `$CLAUDE_PLUGIN_ROOT/skills/plan-anchoring/scripts/jev_judge.py` as the fallback when installed as a plugin, so neither mode depends on a project-level `.claude/` path.

## 6. What leaves the machine

Only a `judge` or `check-fixtures` call contacts TypeSafe, and only after both `TYPESAFE_API_KEY` and `PLAN_ANCHOR_ALLOW_REMOTE_JUDGE=1` are set. Each request carries exactly: the anchor's testable statement and scope (the verbatim quote stays local, except in `rubric`), the item's ID, title and composed text (bead fields or the evidence account, never full diffs or source), and the question set. The key travels only as a bearer header and is never printed, logged or written to a run file. `--dry-run` writes the exact request bodies and totals to the run directory without sending anything; `--answers-file` exercises the whole pipeline with fixture answers for tests and CI.
