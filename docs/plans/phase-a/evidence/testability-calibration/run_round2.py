#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures
import datetime
import hashlib
import importlib.util
import json
import os
import pathlib
import statistics
import time

ROOT = pathlib.Path(__file__).resolve().parent
BASE_PATH = ROOT / "run_calibration.py"
spec = importlib.util.spec_from_file_location("base_a0", BASE_PATH)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
ROUND = ROOT / "round2-role-isolated"


def q(instructions, yes, no, unclear):
    return base.choice_question(instructions, yes, no, unclear)


def pool():
    return {
        "atomicity": {
            "atomic-r2-a-one-policy": q(
                "Does anchor.statement state one policy that has one compliance outcome? Conditions and a list of channels, files, or evidence surfaces governed by that same policy remain one constraint. Different subjects or different required actions are separate constraints.",
                "One policy determines the outcome, even if it names several places where the same outcome must hold.",
                "It requires different subjects or actions that can succeed or fail independently.",
                "The clauses cannot be reliably classified as one policy or separate obligations."),
            "atomic-r2-b-same-invariant": q(
                "Is anchor.statement one invariant applied to a subject, trigger, and possibly several output surfaces? Do not count the number of nouns or listed artifacts; count independently enforceable duties.",
                "All details enforce the same invariant and would be evaluated together.",
                "At least two independently enforceable duties are joined in the statement.",
                "The statement leaves independence of its duties ambiguous."),
            "atomic-r2-c-separate-enforcement": q(
                "Would splitting anchor.statement create two anchors that could receive different compliance results? A single security or redaction rule covering stdout, stderr, and artifacts should not be split merely because it lists surfaces.",
                "No meaningful split produces independently different outcomes.",
                "Yes, a split produces independently satisfiable or violable obligations.",
                "It is unclear whether the apparent parts can be enforced independently."),
        },
        "observable": {
            "observable-r2-a-defined-check": q(
                "Does anchor.statement define a checkable behavior or artifact without relying on an undefined label or an approval that has no identified record? Judge only whether the stated outcome can be observed.",
                "It names evidence or behavior that can be inspected with a determinate outcome.",
                "It supplies only a subjective quality, undefined shorthand, or an approval with no observable record.",
                "Some evidence is named, but the observation needed to settle compliance remains ambiguous."),
            "observable-r2-b-repeatable-evidence": q(
                "Can a reviewer identify repeatable evidence that proves or disproves anchor.statement? An undefined code such as R7 and an unrecorded person's approval are not repeatable evidence.",
                "The statement identifies objective evidence or behavior that reviewers can inspect repeatedly.",
                "The decisive evidence is subjective, undefined, private, or unrecorded.",
                "The evidence is partly objective but not sufficient to settle the outcome."),
            "observable-r2-c-outcome-test": q(
                "Does anchor.statement name an outcome test with knowable expected results? Literal token matching is unnecessary, but private shorthand and an approval with no specified record do not define an outcome test.",
                "A test, inspection, or artifact comparison has a knowable passing and failing result.",
                "No knowable result exists because the outcome is vague, private, or unrecorded.",
                "A possible test exists, but its expected result is not settled."),
        },
        "faithful": {
            "faithful-r2-a-plain-directive": q(
                "Does anchor.quote, read as an ordinary user directive even when it says should, needs, or asks informally, support every substantive requirement in anchor.statement? The statement may formalize wording and isolate one directive from a longer quote, but may not invent a policy or mechanism.",
                "Every substantive requirement follows from the quote; formal must-language and atomic extraction add no new meaning.",
                "The statement adds or changes a substantive policy, mechanism, strength, or outcome.",
                "The quote's substantive directive is genuinely ambiguous."),
            "faithful-r2-b-no-new-decision": q(
                "Would adopting anchor.statement require any product or implementation decision beyond anchor.quote's plain directive? Ignore grammatical strength differences between informal user speech and a formal requirement, and ignore unrelated directives in the same quote.",
                "No new decision is required; the statement is a faithful formalization of a supported directive.",
                "Yes; the statement selects an unsupported mechanism, policy, strength, or different outcome.",
                "The quote is too ambiguous to tell whether a new decision was introduced."),
            "faithful-r2-c-substantive-match": q(
                "Compare the substantive action and outcome in anchor.statement with anchor.quote. Do they match, allowing paraphrase, formal must wording, and one atomic anchor per quoted directive?",
                "The same substantive action and outcome are required or forbidden.",
                "A substantive action, outcome, condition, or prohibition differs or lacks quote support.",
                "The quote does not settle the substantive action or outcome."),
        },
        "scoped": {
            "scoped-r2-a-governed-activity": q(
                "Do anchor.statement and anchor.scope identify the governed activity, component, artifact, or explicit global set, independent of whether the requirement itself is vague or otherwise defective?",
                "A reviewer can identify the work area where this anchor applies, including an explicit all-items set.",
                "No work area or applicability set is identifiable.",
                "An area is named but its applicability cannot be determined."),
            "scoped-r2-b-where-not-quality": q(
                "Can a reviewer answer where anchor.statement applies using anchor.statement plus anchor.scope? Judge where, not whether the outcome is observable, faithful, atomic, or self-contained.",
                "The applicable component, activity, output, structure, or global boundary is clear.",
                "There is no identifiable place or activity to which it applies.",
                "The possible scope has unresolved boundaries."),
            "scoped-r2-c-membership": q(
                "Given a proposed plan item, do anchor.statement and anchor.scope provide enough information to decide whether that item belongs to the governed set? An explicit global set is valid; a named activity such as installer behavior is also a boundary.",
                "Membership in the governed set is decidable.",
                "No governed set is supplied.",
                "Membership remains ambiguous for material cases."),
        },
        "self_contained": {
            "self-r2-a-meaning-only": q(
                "Can an independent reviewer understand the required or forbidden behavior from anchor.statement alone? Ignore grammar, atomicity, quote fidelity, and scope because other checks own them. Lists and explicit conditions are allowed. Answer no only for undefined/private terms or an approval with no identified record or rule.",
                "The behavior and any condition have ordinary or explicitly defined meaning without private context.",
                "Understanding compliance requires undefined shorthand, a private definition, or an unrecorded approval/decision.",
                "Most meaning is present, but a material term or condition has multiple plausible interpretations."),
            "self-r2-b-no-private-context": q(
                "Does anchor.statement avoid dependencies on private context? Do not penalize second-person grammar, multiple obligations, unsupported quote detail, negative wording, or multiple output surfaces here; those are separate checks.",
                "Its terms and conditions can be applied without asking the author or consulting an unrecorded decision.",
                "A private label, undefined quality, or unrecorded approval is required to apply it.",
                "A possible external dependency is named but its necessity is unclear."),
            "self-r2-c-condition-complete": q(
                "Are anchor.statement's own terms and conditional decision inputs complete enough for independent application? An unconditional rule, a concrete prohibition, or an explicit input/action/outcome condition passes. Grammar and source fidelity are out of scope.",
                "No unstated meaning or unrecorded decision is needed to apply the behavior described.",
                "A decisive term, shorthand, quality, or approval is undefined or unrecorded.",
                "The statement supplies some but not all meaning needed for independent application."),
        },
    }


def freeze():
    ROUND.mkdir(parents=True, exist_ok=True)
    data = {"schema": "plan-anchor/testability-candidate-pool/1", "round": 2, "evaluation_mode": "role-isolated",
            "corpus_sha256": base.digest_file(base.ROOT / "corpus.frozen.json"), "semantic_candidates": pool(),
            "candidate_count": sum(len(v) for v in pool().values()), "prior_round_preserved": str(base.ROOT / "semantic-evaluations.json")}
    base.write_json(ROUND / "candidates-round2.frozen.json", data, True)
    manifest = {"schema": "plan-anchor/testability-round-freeze/1", "round": 2,
                "frozen_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "first_live_call_at": None,
                "corpus_sha256": data["corpus_sha256"], "candidate_pool_sha256": base.digest_file(ROUND / "candidates-round2.frozen.json")}
    base.write_json(ROUND / "freeze-manifest.json", manifest, True)
    print(json.dumps(manifest, indent=2, sort_keys=True))


def live():
    fm = base.load_json(ROUND / "freeze-manifest.json")
    if fm["first_live_call_at"] is not None:
        raise SystemExit("round already started")
    corpus = base.load_json(base.ROOT / "corpus.frozen.json")
    candidates = base.load_json(ROUND / "candidates-round2.frozen.json")["semantic_candidates"]
    key = os.environ.get("TYPESAFE_API_KEY", "").strip()
    if not key:
        raise SystemExit("TYPESAFE_API_KEY missing")
    if any(k.startswith("PLAN_ANCHOR_") for k in os.environ):
        raise SystemExit("PLAN_ANCHOR_* environment variables forbidden")
    jj = base.jev_module()
    first = datetime.datetime.now(datetime.timezone.utc).isoformat()
    fm["first_live_call_at"] = first
    base.write_json(ROUND / "freeze-manifest.json", fm, True)

    jobs = []
    for repeat in (1, 2):
        for role, questions in candidates.items():
            for item in corpus["semantic_cases"]:
                body = {"model": "jev-latest", "questions": questions, "state": item["state"]}
                jobs.append((role, item["case_id"], repeat, body))

    def one(job):
        role, case_id, repeat, body = job
        started = time.monotonic()
        response, meta = jj.judge_with_policy(body, key, 30.0, 24000, 2000, body["questions"], shorten=False)
        run_id = f"a0-r2-{role}-{case_id}-r{repeat}-{hashlib.sha256((first+role+case_id+str(repeat)).encode()).hexdigest()[:12]}"
        record = {"schema": "plan-anchor/direct-jev-evidence/1", "run_id": run_id, "role": role, "case_id": case_id, "repeat": repeat,
                  "request_sha256": base.digest_obj(body), "canonical_request": body, "raw_response": response, "transport_meta": meta,
                  "duration_ms": round((time.monotonic()-started)*1000), "model_requested": "jev-latest",
                  "policy": {"timeout_seconds": 30.0, "max_request_bytes": 24000, "shorten": False, "allow_remote": True,
                             "environment_allowlist": ["TYPESAFE_API_KEY"]}}
        path = ROUND / "runs" / role / f"{case_id}-r{repeat}.json"
        base.write_json(path, record, True)
        return {"role": role, "case_id": case_id, "repeat": repeat, "run_id": run_id, "path": str(path), "request_sha256": record["request_sha256"]}

    results = []
    for repeat in (1, 2):
        wave = [j for j in jobs if j[2] == repeat]
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
            results.extend(ex.map(one, wave))
        if repeat == 1:
            time.sleep(1.1)
    base.write_json(ROUND / "execution-manifest.json", {"schema": "plan-anchor/a0-execution/1", "runs": results}, True)
    analyze(corpus, candidates, results)


def analyze(corpus, candidates, results):
    runs = {(r["role"], r["case_id"], r["repeat"]): base.load_json(r["path"]) for r in results}
    evals = []
    identity = []
    for role, questions in candidates.items():
        for item in corpus["semantic_cases"]:
            a, b = runs[(role, item["case_id"], 1)], runs[(role, item["case_id"], 2)]
            identity.append({"role": role, "case_id": item["case_id"], "request_sha256": a["request_sha256"],
                             "byte_identical": base.canonical(a["canonical_request"]) == base.canonical(b["canonical_request"])})
        for cid, question in questions.items():
            cells = []
            for item in corpus["semantic_cases"]:
                answers = [runs[(role, item["case_id"], r)]["raw_response"]["answers"][cid] for r in (1, 2)]
                tuples = [base.answer_tuple(a) for a in answers]
                expected = item["expected"][role]
                accepted = all(choice == expected and confidence >= base.PRODUCTION_THRESHOLD for choice, confidence in tuples)
                cells.append({"case_id": item["case_id"], "expected": expected, "answers": answers, "accepted": accepted,
                              "stable": tuples[0][0] == tuples[1][0], "confident": all(t[1] >= base.PRODUCTION_THRESHOLD for t in tuples)})
            confs = [base.answer_tuple(a)[1] for cell in cells for a in cell["answers"]]
            evals.append({"role": role, "candidate_id": cid, "question": question, "accepted": all(c["accepted"] for c in cells),
                          "exact_cells": sum(c["accepted"] for c in cells), "total_cells": len(cells),
                          "stable_cells": sum(c["stable"] for c in cells), "confident_cells": sum(c["confident"] for c in cells),
                          "minimum_confidence": min(confs), "mean_confidence": statistics.mean(confs),
                          "cells_at_or_above_diagnostic": sum(c >= base.DIAGNOSTIC_THRESHOLD for c in confs), "total_answers": len(confs), "cells": cells})
    base.write_json(ROUND / "repeat-request-identity.json", {"schema": "plan-anchor/repeat-request-identity/1", "pairs": identity}, True)
    base.write_json(ROUND / "semantic-evaluations.json", evals, True)

    def rank_key(e):
        return (-int(e["accepted"]), -e["exact_cells"], -e["stable_cells"], -e["confident_cells"],
                -e["cells_at_or_above_diagnostic"], -e["minimum_confidence"], -e["mean_confidence"], len(base.canonical(e["question"])), e["candidate_id"])
    rankings, selected = {}, {}
    for role in candidates:
        ranked = sorted([e for e in evals if e["role"] == role], key=rank_key)
        rankings[role] = [e["candidate_id"] for e in ranked]
        if ranked[0]["accepted"]:
            selected[role] = ranked[0]
    summary = {"schema": "plan-anchor/a0-round-summary/1", "round": 2, "accepted": len(selected) == 5,
               "selected_candidates": {k: v["candidate_id"] for k,v in selected.items()}, "rankings": rankings,
               "corpus_sha256": base.digest_file(base.ROOT / "corpus.frozen.json"),
               "candidate_pool_sha256": base.digest_file(ROUND / "candidates-round2.frozen.json"),
               "all_repeat_requests_byte_identical": all(x["byte_identical"] for x in identity),
               "unique_run_ids": len({r["run_id"] for r in results}) == len(results), "live_run_count": len(results),
               "production_confidence_threshold": base.PRODUCTION_THRESHOLD, "confidence_reference_threshold": base.DIAGNOSTIC_THRESHOLD}
    if len(selected) == 5:
        rubric = {"schema":"plan-anchoring/questions/2","gate":"testability","version":2,
                  "questions":{role:e["question"] for role,e in selected.items()},
                  "dedupe_question":base.load_json(base.ROOT/"candidates.frozen.json")["dedupe_candidates"]["dedupe-b-mutual-entailment"],
                  "deterministic_lint":{"requirement_form":True},
                  "confirmation_state_machine_sha256":base.digest_file(base.ROOT/"state-machine.frozen.json")}
        base.write_json(ROUND/"selected-rubric.json",rubric,True)
        summary["selected_rubric_sha256"] = base.digest_file(ROUND/"selected-rubric.json")
    else:
        summary["selected_rubric_sha256"] = None
    base.write_json(ROUND/"round-summary.json",summary,True)
    print(json.dumps(summary,indent=2,sort_keys=True))


def main():
    p=argparse.ArgumentParser(); p.add_argument("mode",choices=("freeze","live")); a=p.parse_args()
    freeze() if a.mode=="freeze" else live()

if __name__=="__main__": main()
