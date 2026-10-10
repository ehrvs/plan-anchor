---
name: bead-layout
version: 0.1.0
description: The anchor bead tree in beads (bd), the commands to create it, labels, how question overrides live in the child beads, and how agents read them.
---

# Bead layout

Jev questions live in beads so they version alongside the plan work and can be edited per gate without touching the anchor record. One small tree per fact:

```
ANC-012 anchor bead            (type decision, labels: anchor, anchor:ANC-012)
├── plan-questions bead        (type decision, labels: anchor-questions, anchor:ANC-012, gate:plan)
└── dev-questions bead         (type decision, labels: anchor-questions, anchor:ANC-012, gate:dev)
```

Requirements and ADRs that govern the plan get the same tree under their own ID (`REQ-014`, `ADR-0007`).

## Creating the tree

```bash
A=doc/plan/phase-current/anchors.json
S=.claude/skills/plan-anchoring/scripts/jev_judge.py
ID=ANC-012
STATEMENT=$(python3 -c "import json;print(next(a['statement'] for a in json.load(open('$A'))['anchors'] if a['id']=='$ID'))")

ANCHOR=$(bd create "$ID: $(python3 -c "import json;print(next(a['summary'] for a in json.load(open('$A'))['anchors'] if a['id']=='$ID'))")" \
  --type decision --labels "anchor,anchor:$ID" --silent \
  --description "$STATEMENT" \
  --notes "Anchor record: $A. Do not reword the description; it is the user's verbatim statement.")
PLANQ=$(bd create "$ID plan questions" --type decision --parent "$ANCHOR" --labels "anchor-questions,gate:plan" --silent \
  --body-file .claude/skills/plan-anchoring/assets/templates/anchor-questions-bead.md)
DEVQ=$(bd create "$ID dev questions" --type decision --parent "$ANCHOR" --labels "anchor-questions,gate:dev" --silent \
  --body-file .claude/skills/plan-anchoring/assets/templates/anchor-questions-bead.md)
python3 $S set-beads --anchors $A --id $ID --anchor-bead "$ANCHOR" --plan-bead "$PLANQ" --dev-bead "$DEVQ"
python3 $S render --anchors $A
```

Replace the `{{anchor_id}}` and `{{gate}}` placeholders in the two question beads' descriptions with `bd update <id> --description ...` or leave them; the agents only read the fenced JSON block.

Anchor beads are type `decision` and labelled `anchor` so they are not mistaken for work. Keep them out of work queues with `bd ready --exclude-label anchor` (or the equivalent label filter your `bd` version offers).

## Question overrides in the child beads

The default wording of record is `assets/questions/plan.json` and `assets/questions/dev.json`. A child question bead's description holds one fenced JSON block. `{}` means use the defaults. To change wording for this anchor only, include just the questions to override, keyed by the same IDs as the default set:

````markdown
```json
{
  "questions": {
    "addressed": {
      "type": "choice",
      "instructions": "Does `item.text` state that the runtime crates are copied from ATM rather than written new? ...",
      "criteria": {"yes": "...", "no": "...", "unclear": "..."}
    }
  }
}
```
````

Overrides may also be stored in `anchors.json` under `question_overrides.plan` or `.dev`; the bead wins when both exist. Prefer the bead: it is where the planning and development gates evolve their wording independently while pointing at the same root fact, which is the reason the tree exists.

## How the agents read beads

- `bd show <bead> --json` returns the bead with its text fields. The agents compose the item text from title, description, design, acceptance criteria, and notes, in that order, labelled by section.
- Question beads are resolved first from `anchors.json` (`beads.plan_questions` / `beads.dev_questions`), then by `bd children <anchor bead> --json` filtered on the `gate:plan` or `gate:dev` label.
- The fenced JSON is extracted from the question bead's description and passed to the script as `--overrides-file` so the script, not the agent, does the merge.

## Posting results back

The planning gate posts its markdown report as a comment on the judged planning bead; the development gate posts on the sprint bead or the PR:

```bash
python3 $S report --run doc/plan/phase-current/anchor-runs/<run>.json --format md > /tmp/anchor-report.md
bd comment bd-42 --body-file /tmp/anchor-report.md    # or: bd comment bd-42 "$(cat /tmp/anchor-report.md)"
```

Comments are the skill's job, done in the main session after the agent returns; agents never write to beads.
