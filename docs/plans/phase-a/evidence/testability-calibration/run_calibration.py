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
REPO = pathlib.Path("/Volumes/Extreme Pro/github/sc-runtime-worktrees/plan-anchor-phase-a")
JUDGE = REPO / "plugins/sc-plan-anchor/skills/plan-anchoring/scripts/jev_judge.py"
SOURCE_PATHS = {
    "sprint": REPO / "docs/plans/phase-a/sprint-a0-bootstrap-rubric.md",
    "intent": REPO / "docs/plans/phase-a/intent.md",
    "anchors": REPO / "docs/plans/phase-a/anchors.json",
    "current_testability": REPO / "plugins/sc-plan-anchor/skills/plan-anchoring/assets/questions/testability.json",
    "current_dedupe": REPO / "plugins/sc-plan-anchor/skills/plan-anchoring/assets/questions/dedupe.json",
    "judge": JUDGE,
    "tuner_agent": REPO / "plugins/sc-plan-anchor/.codex/agents/anchor-tuning.md",
    "guidelines": pathlib.Path("/Users/randlee/Documents/github/synaptic-canvas/docs/claude-code-skills-agents-guidelines.md"),
}
PRODUCTION_THRESHOLD = 0.6
DIAGNOSTIC_THRESHOLD = 0.8


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest_obj(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def digest_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value, canonical_form=False):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = canonical(value) if canonical_form else (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()
    path.write_bytes(data)


def choice_question(instructions, yes, no, unclear):
    return {"type": "choice", "instructions": instructions, "criteria": {"yes": yes, "no": no, "unclear": unclear}}


def candidates():
    return {
        "atomicity": {
            "atomic-a-independent-obligation": choice_question(
                "Does anchor.statement impose one independently satisfiable obligation or prohibition? A condition, exception, or several evidence surfaces may belong to one obligation. Judge atomicity only.",
                "It contains one obligation; removing a clause would narrow that obligation rather than remove a separately satisfiable duty.",
                "It contains at least two duties that a plan or implementation could satisfy or violate independently.",
                "The wording is too ambiguous to determine how many independent duties it contains."),
            "atomic-b-separability": choice_question(
                "Can anchor.statement be kept as one atomic anchor, rather than split into two constraints with different pass/fail outcomes? Treat input/action/outcome detail and enumerated output surfaces as detail of one constraint.",
                "There is no useful split into constraints that could receive different outcomes.",
                "It can be split into two or more constraints that could receive different outcomes.",
                "Possible clauses exist, but their independence cannot be determined from the statement."),
            "atomic-c-counterfactual": choice_question(
                "Could the system satisfy one requirement in anchor.statement while violating another requirement in the same statement? Judge only whether the statement bundles requirements.",
                "No; the statement expresses one requirement, possibly with conditions or multiple places where the same outcome must hold.",
                "Yes; the statement expresses multiple requirements with separable satisfaction outcomes.",
                "The statement does not make the requirement boundaries clear enough to decide."),
        },
        "observable": {
            "observable-a-evidence": choice_question(
                "Does anchor.statement identify behavior or an artifact whose presence, absence, value, location, order, or output can be checked? Do not require literal token matching; judge observability only.",
                "A reviewer can identify evidence that would show whether the stated behavior or artifact exists.",
                "It asks only for a subjective quality, preference, or intention with no checkable outcome.",
                "It hints at evidence but does not define enough to know what would demonstrate compliance."),
            "observable-b-falsifiable": choice_question(
                "Is anchor.statement falsifiable from a plan, diff, test, command result, or recorded artifact? Judge the claimed outcome, not grammar or source fidelity.",
                "At least one concrete observation could show the statement met or broken.",
                "No concrete observation could distinguish compliance from noncompliance.",
                "The statement is partly concrete, but what observation settles it remains ambiguous."),
            "observable-c-reviewer": choice_question(
                "Could two reviewers inspect the same relevant evidence and apply anchor.statement to reach a result based on behavior or artifacts rather than taste? Judge only the existence of an observable check.",
                "The statement supplies an objective behavior or artifact to inspect.",
                "The result depends on taste or an undefined quality rather than observable evidence.",
                "Some objective detail exists, but the decisive evidence is not identifiable."),
        },
        "faithful": {
            "faithful-a-supported-obligation": choice_question(
                "Is every obligation in anchor.statement supported by anchor.quote without changing what the quote requires or forbids? An atomic statement may capture one directive from a multi-directive quote without restating unrelated directives.",
                "The quote supports the statement's complete obligation, and the statement adds no unsupported policy or mechanism.",
                "The statement adds, changes, or reverses an obligation beyond what the quote supports.",
                "The quote is too ambiguous to determine whether it supports the statement's obligation."),
            "faithful-b-entailment": choice_question(
                "Read anchor.quote in its ordinary context. Does it entail the constraint written in anchor.statement? It need not entail that unrelated directives from the same quote are also part of this atomic anchor.",
                "The statement follows from the quote without an extra product or implementation decision.",
                "Accepting the statement requires an extra policy, mechanism, strength, or outcome not present in the quote.",
                "The quote admits materially different readings, so entailment cannot be settled."),
            "faithful-c-proof-burden": choice_question(
                "Can the author justify every required or forbidden element of anchor.statement directly from anchor.quote? Judge source support only, not whether the statement is testable.",
                "Each element of the statement has direct support in the quote; unrelated quoted directives may be separate anchors.",
                "At least one element of the statement lacks support or conflicts with the quote.",
                "The quote does not provide enough meaning to verify support."),
        },
        "scoped": {
            "scoped-a-applicability": choice_question(
                "Using anchor.statement together with anchor.scope, can a reviewer decide whether a particular plan item or change falls within this anchor? A deliberately global scope is identifiable and may pass.",
                "The governed component, activity, artifact, command set, or explicit global boundary is identifiable.",
                "No governed area is identified, so applicability to a plan item or change cannot be determined.",
                "A possible area is suggested, but its applicability boundary remains ambiguous."),
            "scoped-b-boundary": choice_question(
                "Do anchor.statement and anchor.scope establish an identifiable boundary for where the constraint applies, including an explicit all-system or all-command boundary? Judge scope only.",
                "The applicability boundary is named or clearly implied, even if it is intentionally global.",
                "The constraint floats without a component, activity, artifact, or global boundary.",
                "The boundary is partially described but cannot be applied consistently."),
            "scoped-c-classification": choice_question(
                "Could a reviewer classify candidate work as inside or outside anchor.statement's governed area from anchor.statement plus anchor.scope?",
                "The statement and scope support a repeatable inside/outside classification; an explicit global scope puts all relevant work inside.",
                "They provide no usable governed area for that classification.",
                "They name an area, but leave material cases impossible to classify."),
        },
        "self_contained": {
            "self-a-recorded-conditions": choice_question(
                "Are the conditions and terms in anchor.statement decidable from the statement and recorded project artifacts, without private shorthand or an unrecorded future approval? Explicit prohibitions and input/action/outcome conditions may pass.",
                "All terms and conditions needed to apply the constraint are stated or point to recorded, identifiable evidence.",
                "Applying it requires private shorthand, an undefined term, or an approval/decision that is neither specified nor recorded.",
                "Most conditions are stated, but at least one dependency may require outside interpretation."),
            "self-b-independent-reader": choice_question(
                "Can an independent reviewer apply anchor.statement without asking its author what shorthand, quality, exception, or approval means? Judge self-containment only.",
                "The statement supplies enough meaning to apply its direct requirement, prohibition, or explicit test condition.",
                "The reviewer must obtain unstated meaning or an unrecorded decision before applying it.",
                "The reviewer can apply part of it, but a material term or condition remains open."),
            "self-c-decision-inputs": choice_question(
                "Does anchor.statement contain or identify every input needed to decide compliance, including any exception or condition? A concrete never/must-not prohibition is self-contained even though it is negative.",
                "Its decision inputs are explicit or recorded and its condition has a checkable trigger and outcome.",
                "A decision input is private, undefined, or dependent on an unrecorded approval.",
                "A decision input is mentioned but not specified well enough to use."),
            "self-d-operational": choice_question(
                "Does anchor.statement stand on its own as an operational constraint: a reviewer knows the trigger, governed subject, and required or forbidden outcome without external conversation?",
                "The trigger, subject, and outcome are explicit enough for independent application; unconditional constraints need no artificial trigger.",
                "One of those elements depends on private shorthand, undefined quality, or unrecorded consent.",
                "The operational meaning is partially present but not settled."),
        },
    }


def dedupe_candidates():
    return {
        "dedupe-a-equivalent-constraint": choice_question(
            "Do a.statement and b.statement express the same testable constraint? Compare statements only; provenance quotes do not make anchors duplicates or distinct.",
            "Any implementation that satisfies one statement necessarily satisfies the other, and violating one violates the other.",
            "There is a plausible implementation that satisfies one statement but not the other.",
            "The statements are too ambiguous to determine whether their compliance sets are the same."),
        "dedupe-b-mutual-entailment": choice_question(
            "Considering only a.statement and b.statement, do the two constraints mutually entail each other? Ignore wording and quote overlap.",
            "Each statement entails the other constraint.",
            "At least one statement can hold while the other does not.",
            "Ambiguity prevents deciding mutual entailment."),
        "dedupe-c-separate-outcomes": choice_question(
            "Could a plan or implementation receive different compliance outcomes for a.statement and b.statement? Judge their testable obligations, not their quotes.",
            "No; their obligations have the same compliance outcome in every relevant case.",
            "Yes; their obligations differ enough to receive different outcomes.",
            "The obligations are too unclear to compare reliably."),
    }


YES = {"atomicity": "yes", "observable": "yes", "faithful": "yes", "scoped": "yes", "self_contained": "yes"}


def case(case_id, title, statement, quote, scope, expected=None, lint="pass", rationale=""):
    return {"case_id": case_id, "title": title, "state": {"anchor": {"statement": statement, "quote": quote, "scope": scope}},
            "expected": dict(YES if expected is None else expected), "requirement_form_lint": lint, "rationale": rationale}


def corpus():
    cases = [
        case("a0-01-valid-directive", "valid directive", "The release command must write a JSON manifest to dist/release.json.", "the release command needs to write a JSON manifest to dist/release.json", "release command output", rationale="One supported, observable, scoped directive."),
        case("a0-02-valid-prohibition", "explicit prohibition", "The request logger must never write raw authentication tokens to stdout or stderr.", "do not print raw auth tokens in request logs or errors", "request logging and error output", rationale="Concrete negative prose is a valid, self-contained prohibition."),
        case("a0-03-structural-scope", "structural scope", "The parser module must remain under src/parser/.", "keep the parser module under src/parser", "repository structure", rationale="A path is observable and structural scope is identifiable."),
        case("a0-04-global-scope", "global scope", "Every CLI subcommand must emit a JSON object on stdout.", "all CLI commands should print JSON on stdout", "all CLI subcommands", rationale="An explicit global command boundary is valid scope."),
        case("a0-05-atomic-from-multi-directive", "one atomic anchor from multi-directive quote", "The build pipeline must use cargo for compilation.", "Use cargo for compilation, and run pytest for integration tests.", "build compilation", rationale="The statement may capture one supported directive without exhausting the quote."),
        case("a0-06-genuinely-bundled", "genuinely bundled statement", "The CLI must emit JSON and the daemon must write an audit log.", "the CLI must emit JSON and the daemon must write an audit log", "CLI output and daemon audit", {**YES, "atomicity": "no"}, rationale="Two independently satisfiable obligations must split."),
        case("a0-07-unsupported-elaboration", "unsupported policy elaboration", "Backup archives must use AES-256-GCM encryption.", "encrypt backup archives", "backup storage", {**YES, "faithful": "no"}, rationale="The algorithm and strength are an unsupported added policy."),
        case("a0-08-vague-outcome", "vague outcome", "The installer must be robust.", "make the installer robust", "installer behavior", {**YES, "observable": "no", "self_contained": "no"}, rationale="Robust has no observable outcome and requires private interpretation."),
        case("a0-09-explicit-testable-condition", "explicit condition", "When --privacy is set, the exporter must replace every email address with [redacted].", "with --privacy, replace email addresses with [redacted]", "exporter privacy mode", rationale="A trigger/action/outcome condition is self-contained."),
        case("a0-10-api-key-redaction", "API-key output redaction", "When TYPESAFE_API_KEY is set to canary-123 and transport fails, stdout, stderr, and saved run artifacts must omit canary-123 and Authorization: Bearer canary-123.", "test a transport failure with a canary TypeSafe key and make sure console output and saved run files contain neither the key nor its bearer header", "transport-error output and persisted run artifacts", rationale="Concrete input/action/outcome proves redaction without literal statement-token dependence."),
        case("a0-11-private-shorthand", "private shorthand", "The deploy path must satisfy R7.", "make the deploy path satisfy R7", "deployment", {**YES, "observable": "no", "self_contained": "no"}, rationale="R7 is undefined private shorthand."),
        case("a0-12-unrecorded-approval", "unrecorded approval dependency", "The package may publish only when the release lead approves.", "only publish after the release lead says yes", "package publishing", {**YES, "observable": "no", "self_contained": "no"}, rationale="No recorded approval artifact or decision rule is identified."),
        case("a0-13-shared-quote-first-atomic", "first atomic anchor sharing quote", "The service must write request logs as JSON.", "The service must log requests as JSON and retry failed requests twice.", "request logging", rationale="First of two distinct atomic anchors from one quote."),
        case("a0-14-shared-quote-second-atomic", "second atomic anchor sharing quote", "The service must retry failed requests twice.", "The service must log requests as JSON and retry failed requests twice.", "failed request handling", rationale="Second of two distinct atomic anchors from one quote."),
        case("a0-15-duplicate-first", "duplicate statement with first quote", "Every CLI command must emit JSON to stdout.", "CLI output must always be JSON", "all CLI commands", rationale="Individually valid; dedupe is statement-based."),
        case("a0-16-duplicate-second", "duplicate statement with different quote", "Every CLI command must emit JSON to stdout.", "all commands should print machine-readable JSON", "all CLI commands", rationale="Same testable statement despite different provenance."),
        case("a0-17-nondeclarative-form", "deterministic requirement-form failure", "You need to record the build digest in build.json.", "you need to record the build digest in build.json", "build output", dict(YES), lint="fail", rationale="Semantic cells are positive, but deterministic grammar lint must reject second-person instruction form."),
    ]
    pairs = [
        {"pair_id": "dup-01-shared-quote-distinct", "a": cases[12]["state"]["anchor"], "b": cases[13]["state"]["anchor"], "expected": "no", "rationale": "Same quote, distinct atomic obligations."},
        {"pair_id": "dup-02-same-statement-different-quotes", "a": cases[14]["state"]["anchor"], "b": cases[15]["state"]["anchor"], "expected": "yes", "rationale": "Identical statement, different provenance."},
        {"pair_id": "dup-03-paraphrased-duplicate", "a": {"statement": "The API client must retry HTTP 503 responses twice.", "quote": "retry service unavailable twice", "scope": "API client"}, "b": {"statement": "On HTTP 503, the API client must make two retry attempts.", "quote": "two retries for 503", "scope": "API client"}, "expected": "yes", "rationale": "Mutually entailing paraphrases."},
        {"pair_id": "dup-04-related-distinct", "a": {"statement": "The API client must retry HTTP 503 responses twice.", "quote": "retry 503 twice", "scope": "API client"}, "b": {"statement": "The API client must log HTTP 503 responses as JSON.", "quote": "log 503 as JSON", "scope": "API client"}, "expected": "no", "rationale": "Related subject, different obligations."},
    ]
    lint_cases = [
        {"id": "lint-01-must", "statement": "The build must emit build.json.", "expected": "pass"},
        {"id": "lint-02-prohibition", "statement": "The logger must never print raw tokens.", "expected": "pass"},
        {"id": "lint-03-is", "statement": "The registry path is .codex/agents/registry.yaml.", "expected": "pass"},
        {"id": "lint-04-first-person", "statement": "I want the build to emit build.json.", "expected": "fail"},
        {"id": "lint-05-second-person", "statement": "You need to record the build digest.", "expected": "fail"},
        {"id": "lint-06-suggestion", "statement": "We should keep the installer reliable.", "expected": "fail"},
        {"id": "lint-07-question", "statement": "Should the build emit build.json?", "expected": "fail"},
        {"id": "lint-08-imperative", "statement": "Record the build digest in build.json.", "expected": "fail"},
    ]
    return {"schema": "plan-anchor/testability-calibration-corpus/1", "authority": "Sprint A0 and approved Phase A intent/anchors",
            "plan_independent": True, "active_phase_a_plan_text_excluded": True, "production_confidence_threshold": PRODUCTION_THRESHOLD,
            "semantic_cases": cases, "dedupe_pairs": pairs, "requirement_form_lint_cases": lint_cases}


def state_machine():
    return {
        "schema": "plan-anchor/testability-confirmation-state-machine/1",
        "production_confidence_threshold": PRODUCTION_THRESHOLD,
        "per_cell": {
            "first_two_same_and_both_confident": "confirmed(answer); yes is positive, no or unclear is a confirmed negative",
            "first_two_same_but_either_low": "inconclusive; do not make a third call",
            "first_two_different": "make exactly one third call",
            "after_third_exactly_one_label_has_two_confident_votes_and_no_other_label_has_a_confident_vote": "confirmed(majority label)",
            "after_third_two_or_more_distinct_labels_have_confident_votes": "unstable",
            "after_third_no_label_has_two_confident_votes": "inconclusive",
        },
        "anchor_verdict": {
            "testable": "deterministic lint passes and every semantic cell is confirmed yes",
            "needs_work": "all cells are resolved and at least one semantic cell is confirmed no or unclear, or deterministic lint fails",
            "inconclusive": "no cell is unstable and at least one required cell is inconclusive",
            "unstable": "at least one required cell is unstable",
            "precedence": ["unstable", "inconclusive", "needs_work", "testable"],
        },
        "no_averaging": True,
        "third_call_only_on_label_disagreement": True,
    }


def freeze():
    source_digests = {name: {"path": str(path), "sha256": digest_file(path)} for name, path in SOURCE_PATHS.items()}
    c = corpus()
    cs = {"schema": "plan-anchor/testability-candidate-pool/1", "semantic_candidates": candidates(), "dedupe_candidates": dedupe_candidates(),
          "candidate_counts": {"semantic": sum(len(v) for v in candidates().values()), "dedupe": len(dedupe_candidates())},
          "production_set_minimum": {"semantic": 5, "dedupe": 1}}
    sm = state_machine()
    write_json(ROOT / "source-digests.frozen.json", source_digests, True)
    write_json(ROOT / "corpus.frozen.json", c, True)
    write_json(ROOT / "candidates.frozen.json", cs, True)
    write_json(ROOT / "state-machine.frozen.json", sm, True)
    manifest = {
        "schema": "plan-anchor/testability-freeze/1",
        "frozen_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "first_live_call_at": None,
        "source_digests_sha256": digest_file(ROOT / "source-digests.frozen.json"),
        "corpus_sha256": digest_file(ROOT / "corpus.frozen.json"),
        "candidate_pool_sha256": digest_file(ROOT / "candidates.frozen.json"),
        "state_machine_sha256": digest_file(ROOT / "state-machine.frozen.json"),
        "source_unchanged": True,
    }
    write_json(ROOT / "freeze-manifest.json", manifest, True)
    print(json.dumps(manifest, indent=2, sort_keys=True))


def load_json(path):
    return json.loads(pathlib.Path(path).read_text())


def jev_module():
    spec = importlib.util.spec_from_file_location("jev_judge_a0", JUDGE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def semantic_questions(pool):
    flat = {}
    mapping = {}
    for role, variants in pool["semantic_candidates"].items():
        for cid, question in variants.items():
            qid = cid
            flat[qid] = question
            mapping[qid] = role
    return flat, mapping


def run_live():
    for required in ("freeze-manifest.json", "corpus.frozen.json", "candidates.frozen.json"):
        if not (ROOT / required).exists():
            raise SystemExit(f"missing frozen artifact: {required}")
    frozen_manifest = load_json(ROOT / "freeze-manifest.json")
    existing_runs = list((ROOT / "runs").rglob("*.json")) if (ROOT / "runs").exists() else []
    if frozen_manifest["first_live_call_at"] is not None and existing_runs:
        raise SystemExit("live tournament already produced evidence; refusing to overwrite it")
    corpus_data = load_json(ROOT / "corpus.frozen.json")
    pool = load_json(ROOT / "candidates.frozen.json")
    api_key = os.environ.get("TYPESAFE_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("TYPESAFE_API_KEY missing")
    if any(name.startswith("PLAN_ANCHOR_") for name in os.environ):
        raise SystemExit("PLAN_ANCHOR_* environment variables are forbidden for this run")
    questions, role_map = semantic_questions(pool)
    dq = pool["dedupe_candidates"]
    jj = jev_module()
    first_at = frozen_manifest["first_live_call_at"] or datetime.datetime.now(datetime.timezone.utc).isoformat()
    if frozen_manifest["first_live_call_at"] is None:
        frozen_manifest["first_live_call_at"] = first_at
        write_json(ROOT / "freeze-manifest.json", frozen_manifest, True)

    jobs = []
    for repeat in (1, 2):
        for item in corpus_data["semantic_cases"]:
            body = {"model": "jev-latest", "questions": questions, "state": item["state"]}
            jobs.append(("semantic", item["case_id"], repeat, body))
        for pair in corpus_data["dedupe_pairs"]:
            body = {"model": "jev-latest", "questions": dq, "state": {"a": {"statement": pair["a"]["statement"]}, "b": {"statement": pair["b"]["statement"]}}}
            jobs.append(("dedupe", pair["pair_id"], repeat, body))

    def one(job):
        kind, case_id, repeat, body = job
        qset = questions if kind == "semantic" else dq
        started = time.monotonic()
        response, meta = jj.judge_with_policy(body, api_key, 30.0, 24000, 2000, qset, shorten=False)
        run_id = f"a0-testability-{kind}-{case_id}-r{repeat}-{hashlib.sha256((first_at + kind + case_id + str(repeat)).encode()).hexdigest()[:12]}"
        record = {"schema": "plan-anchor/direct-jev-evidence/1", "run_id": run_id, "kind": kind, "case_id": case_id, "repeat": repeat,
                  "request_sha256": digest_obj(body), "canonical_request": body, "raw_response": response, "transport_meta": meta,
                  "duration_ms": round((time.monotonic() - started) * 1000), "model_requested": "jev-latest",
                  "policy": {"timeout_seconds": 30.0, "max_request_bytes": 24000, "min_item_chars": 2000, "shorten": False,
                             "allow_remote": True, "environment_allowlist": ["TYPESAFE_API_KEY"]}}
        path = ROOT / "runs" / kind / f"{case_id}-r{repeat}.json"
        write_json(path, record, True)
        return {"kind": kind, "case_id": case_id, "repeat": repeat, "run_id": run_id, "path": str(path),
                "request_sha256": record["request_sha256"], "duration_ms": record["duration_ms"]}

    # Timestamp-separated repeat waves; all cases within a wave execute in parallel.
    results = []
    for repeat in (1, 2):
        wave = [j for j in jobs if j[2] == repeat]
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            results.extend(executor.map(one, wave))
        if repeat == 1:
            time.sleep(1.1)
    write_json(ROOT / "execution-manifest.json", {"schema": "plan-anchor/a0-execution/1", "runs": results}, True)
    analyze(corpus_data, pool, role_map, results)


def answer_tuple(answer):
    return answer.get("choice"), float(answer.get("confidence", 0.0))


def analyze(corpus_data, pool, role_map, results):
    by_run = {(r["kind"], r["case_id"], r["repeat"]): load_json(r["path"]) for r in results}
    identity = []
    for kind, items in (("semantic", corpus_data["semantic_cases"]), ("dedupe", corpus_data["dedupe_pairs"])):
        key = "case_id" if kind == "semantic" else "pair_id"
        for item in items:
            a, b = by_run[(kind, item[key], 1)], by_run[(kind, item[key], 2)]
            identity.append({"kind": kind, key: item[key], "request_sha256": a["request_sha256"],
                             "byte_identical": canonical(a["canonical_request"]) == canonical(b["canonical_request"])})
    write_json(ROOT / "repeat-request-identity.json", {"schema": "plan-anchor/repeat-request-identity/1", "pairs": identity}, True)

    semantic_eval = []
    for role, variants in pool["semantic_candidates"].items():
        for cid, question in variants.items():
            cells = []
            for case_item in corpus_data["semantic_cases"]:
                answers = [by_run[("semantic", case_item["case_id"], r)]["raw_response"]["answers"][cid] for r in (1, 2)]
                tuples = [answer_tuple(a) for a in answers]
                expected = case_item["expected"][role]
                exact = all(choice == expected and confidence >= PRODUCTION_THRESHOLD for choice, confidence in tuples)
                cells.append({"case_id": case_item["case_id"], "expected": expected, "answers": answers, "accepted": exact,
                              "stable": tuples[0][0] == tuples[1][0], "confident": all(x[1] >= PRODUCTION_THRESHOLD for x in tuples)})
            confidences = [answer_tuple(a)[1] for c in cells for a in c["answers"]]
            exact_count = sum(c["accepted"] for c in cells)
            semantic_eval.append({"role": role, "candidate_id": cid, "question": question, "accepted": exact_count == len(cells),
                                  "exact_cells": exact_count, "total_cells": len(cells), "stable_cells": sum(c["stable"] for c in cells),
                                  "confident_cells": sum(c["confident"] for c in cells), "minimum_confidence": min(confidences),
                                  "mean_confidence": statistics.mean(confidences),
                                  "cells_at_or_above_diagnostic": sum(c >= DIAGNOSTIC_THRESHOLD for c in confidences),
                                  "total_answers": len(confidences), "cells": cells})

    dedupe_eval = []
    for cid, question in pool["dedupe_candidates"].items():
        cells = []
        for pair in corpus_data["dedupe_pairs"]:
            answers = [by_run[("dedupe", pair["pair_id"], r)]["raw_response"]["answers"][cid] for r in (1, 2)]
            tuples = [answer_tuple(a) for a in answers]
            exact = all(choice == pair["expected"] and confidence >= PRODUCTION_THRESHOLD for choice, confidence in tuples)
            cells.append({"pair_id": pair["pair_id"], "expected": pair["expected"], "answers": answers, "accepted": exact,
                          "stable": tuples[0][0] == tuples[1][0], "confident": all(x[1] >= PRODUCTION_THRESHOLD for x in tuples)})
        confidences = [answer_tuple(a)[1] for c in cells for a in c["answers"]]
        exact_count = sum(c["accepted"] for c in cells)
        dedupe_eval.append({"candidate_id": cid, "question": question, "accepted": exact_count == len(cells), "exact_cells": exact_count,
                            "total_cells": len(cells), "stable_cells": sum(c["stable"] for c in cells),
                            "confident_cells": sum(c["confident"] for c in cells), "minimum_confidence": min(confidences),
                            "mean_confidence": statistics.mean(confidences),
                            "cells_at_or_above_diagnostic": sum(c >= DIAGNOSTIC_THRESHOLD for c in confidences),
                            "total_answers": len(confidences), "cells": cells})

    def rank_key(e):
        return (-int(e["accepted"]), -e["exact_cells"], -e["stable_cells"], -e["confident_cells"],
                -e["cells_at_or_above_diagnostic"], -e["minimum_confidence"], -e["mean_confidence"], len(canonical(e["question"])), e["candidate_id"])

    rankings = {}
    selected = {}
    for role in pool["semantic_candidates"]:
        ranked = sorted([e for e in semantic_eval if e["role"] == role], key=rank_key)
        rankings[role] = [e["candidate_id"] for e in ranked]
        if ranked[0]["accepted"]:
            selected[role] = ranked[0]
    ranked_dedupe = sorted(dedupe_eval, key=rank_key)
    dedupe_selected = ranked_dedupe[0] if ranked_dedupe and ranked_dedupe[0]["accepted"] else None
    write_json(ROOT / "semantic-evaluations.json", semantic_eval, True)
    write_json(ROOT / "dedupe-evaluations.json", dedupe_eval, True)
    if len(selected) == 5 and dedupe_selected:
        final = {"schema": "plan-anchoring/questions/2", "gate": "testability", "version": 2,
                 "production_confidence_threshold": PRODUCTION_THRESHOLD,
                 "semantic_questions": {role: entry["question"] for role, entry in selected.items()},
                 "dedupe_question": dedupe_selected["question"],
                 "deterministic_lint": {"requirement_form": True},
                 "confirmation_state_machine_sha256": digest_file(ROOT / "state-machine.frozen.json")}
        write_json(ROOT / "selected-rubric.json", final, True)
        selected_digest = digest_file(ROOT / "selected-rubric.json")
    else:
        selected_digest = None
    summary = {"schema": "plan-anchor/a0-calibration-summary/1", "accepted": len(selected) == 5 and dedupe_selected is not None,
               "selected_semantic_candidates": {role: e["candidate_id"] for role, e in selected.items()},
               "selected_dedupe_candidate": dedupe_selected["candidate_id"] if dedupe_selected else None,
               "semantic_rankings": rankings, "dedupe_ranking": [e["candidate_id"] for e in ranked_dedupe],
               "selected_rubric_sha256": selected_digest, "corpus_sha256": digest_file(ROOT / "corpus.frozen.json"),
               "candidate_pool_sha256": digest_file(ROOT / "candidates.frozen.json"), "all_repeat_requests_byte_identical": all(x["byte_identical"] for x in identity),
               "unique_run_ids": len({r["run_id"] for r in results}) == len(results), "live_run_count": len(results),
               "production_confidence_threshold": PRODUCTION_THRESHOLD, "confidence_reference_threshold": DIAGNOSTIC_THRESHOLD,
               "source_digests_before": load_json(ROOT / "source-digests.frozen.json"),
               "source_digests_after": {name: {"path": str(path), "sha256": digest_file(path)} for name, path in SOURCE_PATHS.items()}}
    summary["authoritative_sources_unchanged"] = summary["source_digests_before"] == summary["source_digests_after"]
    write_json(ROOT / "calibration-summary.json", summary, True)
    print(json.dumps(summary, indent=2, sort_keys=True))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("freeze", "live"))
    args = parser.parse_args()
    if args.mode == "freeze":
        freeze()
    else:
        run_live()


if __name__ == "__main__":
    main()
