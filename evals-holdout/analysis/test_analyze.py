"""Regression checks for analyze.py, on synthetic results only. Free: nothing calls a model.

Run from the repository root:  python evals-holdout/analysis/test_analyze.py
"""
import contextlib
import csv
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("analyze", os.path.join(HERE, "analyze.py"))
analyze = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(analyze)

ARMS = ("with", "without")
CASES = ("alpha", "beta")
CRITERIA = ("states-limit", "no-invented-policy")
QUOTE = "the limit is stated plainly"
REQUIRED = {"element": "states the limit", "applies": True, "quote": QUOTE}
ABSENT_CLAIM = {"claim": "invents a policy", "quote": None}


def quietly(function, *args):
    with contextlib.redirect_stdout(io.StringIO()):
        return function(*args)


def read_text(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def trace_text(blocks):
    return "".join(json.dumps({"message": {"role": "assistant" if block["type"] == "tool_use" else "user",
                                           "content": [block]}}) + "\n" for block in blocks)


def tool(name, **fields):
    return [{"type": "tool_use", "id": "t1", "name": name, "input": fields}]


def listing(text):
    return tool("Glob", pattern="**/*.md") + [{"type": "tool_result", "tool_use_id": "t1", "content": text}]


def make_results(root, errors=(), traces=None):
    """Two cases with three runs per arm; `errors` lists the (case, arm, run) that errored."""
    agg = {"claudeVersion": "test", "costUsd": 0.0, "partial": False,
           "suite": {"modelOverride": "model", "judgeModel": "judge"}, "cases": []}
    for case_name in CASES:
        case = {"name": case_name, "dir": f"evals-holdout\\{case_name}", "promptMarkdown": "A request.", "arms": {},
                "graders": [{"name": c, "type": "llm", "graderMarkdown": f"PASS if {c}. FAIL if not."} for c in CRITERIA]}
        for arm in ARMS:
            case["arms"][arm] = []
            for n in (1, 2, 3):
                trace = os.path.join(root, "traces", f"{case_name}-{arm}-{n}.jsonl")
                os.makedirs(os.path.dirname(trace), exist_ok=True)
                with open(trace, "w", encoding="utf-8") as handle:
                    handle.write(trace_text((traces or {}).get((case_name, arm, n), [])))
                passed = {"states-limit": arm == "with" or n == 1, "no-invented-policy": True}
                case["arms"][arm].append({
                    "score": sum(passed.values()) / len(passed), "skippedPaidGraders": False, "tracePath": trace,
                    "error": "crashed" if (case_name, arm, n) in errors else None,
                    "graders": [{"name": c, "passed": passed[c], "scored": True, "judgeVotes": [passed[c]] * 3,
                                 "evidence": f"Answer {arm} {n}: {QUOTE}."} for c in CRITERIA]})
        agg["cases"].append(case)
    results = os.path.join(root, "results")
    os.makedirs(results)
    with open(os.path.join(results, "aggregate-result.json"), "w", encoding="utf-8") as handle:
        json.dump(agg, handle)
    return results


def mark_errors(results, runs):
    path = os.path.join(results, "aggregate-result.json")
    agg = json.loads(read_text(path))
    for case in agg["cases"]:
        for arm in ARMS:
            for n, run in enumerate(case["arms"][arm], 1):
                if (case["name"], arm, n) in runs:
                    run["error"] = "crashed later"
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(agg, handle)


def judgment(answer, criterion, verdict="PASS", required=(), prohibited=()):
    return json.dumps({"answer": answer, "criterion": criterion, "required": list(required),
                       "prohibited": list(prohibited), "verdict": verdict})


class Fixture(unittest.TestCase):
    def setUp(self):
        self._temp = tempfile.TemporaryDirectory()
        self.root = self._temp.name
        self.review_dir = os.path.join(self.root, "review")

    def tearDown(self):
        self._temp.cleanup()

    def exported(self, errors=()):
        results = make_results(self.root, errors)
        quietly(analyze.automated, results)
        quietly(analyze.export, results, self.review_dir, analyze.EXPORT_SEED)
        return results

    def sealed(self):
        return json.loads(read_text(os.path.join(self.review_dir, "key", "SEALED-KEY.json")))

    def valid_outputs(self):
        """A complete, valid review: the required element is quoted, and the prohibited claim is absent."""
        outputs = {}
        for case_name, ids in self.sealed()["key"].items():
            outputs[case_name] = []
            for answer_id in sorted(ids):
                outputs[case_name].append(judgment(answer_id, "states-limit", required=[REQUIRED]))
                outputs[case_name].append(judgment(answer_id, "no-invented-policy", prohibited=[ABSENT_CLAIM]))
        return outputs

    def run_review(self, results, outputs, done=True):
        os.makedirs(os.path.join(self.review_dir, "outputs"), exist_ok=True)
        for case_name, lines in outputs.items():
            closing = [json.dumps({"done": True, "judgments": len(lines)})] if done else []
            with open(os.path.join(self.review_dir, "outputs", f"{case_name}.jsonl"), "w", encoding="utf-8") as handle:
                handle.write("\n".join(list(lines) + closing) + "\n")
        ok = quietly(analyze.review, results, self.review_dir)
        validation = os.path.join(self.review_dir, "blind-review-validation.md")
        analysis = os.path.join(self.review_dir, "blind-review-analysis.md")
        return (ok, read_text(validation) if os.path.exists(validation) else "",
                read_text(analysis) if os.path.exists(analysis) else None)

    def assert_rejected(self, results, outputs, expected, done=True):
        ok, validation, analysis = self.run_review(results, outputs, done)
        self.assertIs(ok, False)
        self.assertIn(expected, validation)
        self.assertIsNone(analysis, "conclusions were written despite invalid reviewer output")


class LeakageDetection(unittest.TestCase):
    def exposed(self, blocks):
        with tempfile.TemporaryDirectory() as root:
            path = os.path.join(root, "trace.jsonl")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(trace_text(blocks))
            return bool(analyze.trace_facts(path, "evals-holdout")[2])

    def test_relative_path_is_detected(self):
        self.assertTrue(self.exposed(tool("Read", file_path="evals-holdout/demo/graders/rule.md")))

    def test_other_path_forms_are_detected(self):
        for blocks in (tool("Read", file_path="./evals-holdout/demo/graders/rule.md"),
                       tool("Read", file_path=r"C:\repo\evals-holdout\demo\graders\rule.md"),
                       tool("Glob", pattern="*.md", path="evals-holdout"),
                       tool("Glob", pattern="**/evals-holdout"),
                       listing("skills/demo/SKILL.md\nevals-holdout/demo/graders/rule.md")):
            with self.subTest(blocks=blocks):
                self.assertTrue(self.exposed(blocks))

    def test_similar_names_and_prose_are_not_detected(self):
        for blocks in (tool("Read", file_path="my-evals-holdout/demo/rule.md"),
                       tool("Read", file_path="evals-holdout-v2/demo/rule.md"),
                       tool("Read", file_path="skills/demo/SKILL.md"),
                       tool("Grep", pattern="evals-holdout", path="skills"),
                       listing("The evals-holdout suite is described elsewhere.")):
            with self.subTest(blocks=blocks):
                self.assertFalse(self.exposed(blocks))

    def test_exposed_run_is_excluded(self):
        with tempfile.TemporaryDirectory() as root:
            leak = tool("Read", file_path="evals-holdout/alpha/graders/states-limit.md")
            results = make_results(root, traces={("alpha", "with", 1): leak})
            quietly(analyze.automated, results)
            self.assertIn("Excluded alpha / with / run 1", read_text(os.path.join(results, "automated-analysis.md")))


class SharedEligibility(Fixture):
    def test_errored_run_is_excluded_from_every_step(self):
        results = self.exported(errors={("alpha", "with", 2)})
        report = read_text(os.path.join(results, "automated-analysis.md"))
        self.assertIn("Excluded alpha / with / run 2", report)
        row = next(line for line in report.splitlines() if line.startswith("| alpha |"))
        self.assertTrue(row.endswith("| 2/3, 3/3 |"), row)
        exported = {(meta["arm"], meta["run"]) for meta in self.sealed()["key"]["alpha"].values()}
        self.assertEqual(len(exported), 5)
        self.assertNotIn(("with", 2), exported)
        ok, validation, analysis = self.run_review(results, self.valid_outputs())
        self.assertIs(ok, True, validation)
        self.assertNotIn("not reviewed", analysis)

    def test_stop_rule_blocks_scores_and_export(self):
        results = make_results(self.root, errors={("alpha", "with", 1), ("alpha", "with", 2)})
        with self.assertRaises(analyze.StopRule):
            quietly(analyze.automated, results)
        report = read_text(os.path.join(results, "automated-analysis.md"))
        self.assertIn("## Stopped", report)
        self.assertNotIn("Pooled", report)
        with self.assertRaises(analyze.StopRule):
            quietly(analyze.export, results, self.review_dir, analyze.EXPORT_SEED)
        self.assertFalse(os.path.exists(os.path.join(self.review_dir, "key", "SEALED-KEY.json")))

    def test_stop_rule_blocks_review(self):
        results = self.exported()
        outputs = self.valid_outputs()
        mark_errors(results, {("beta", "without", 1), ("beta", "without", 3)})
        with self.assertRaises(analyze.StopRule):
            self.run_review(results, outputs)

    def test_review_refuses_when_eligibility_changed_after_export(self):
        results = self.exported()
        outputs = self.valid_outputs()
        mark_errors(results, {("alpha", "with", 1)})
        with self.assertRaises(SystemExit):
            self.run_review(results, outputs)


class InvalidReviewerOutput(Fixture):
    def setUp(self):
        super().setUp()
        self.results = self.exported()
        self.outputs = self.valid_outputs()

    def test_valid_output_produces_conclusions(self):
        ok, validation, analysis = self.run_review(self.results, self.outputs)
        self.assertIs(ok, True, validation)
        self.assertIn("Pooled", analysis)

    def test_invalid_verdict_is_rejected(self):
        self.outputs["alpha"][0] = self.outputs["alpha"][0].replace('"verdict": "PASS"', '"verdict": "MAYBE"')
        self.assert_rejected(self.results, self.outputs, "invalid verdict 'MAYBE'")

    def test_duplicate_judgment_is_rejected(self):
        self.outputs["alpha"].append(self.outputs["alpha"][0])
        self.assert_rejected(self.results, self.outputs, "duplicate judgment")

    def test_missing_judgment_is_rejected(self):
        self.outputs["beta"].pop()
        self.assert_rejected(self.results, self.outputs, "judgments missing")

    def test_truncated_output_is_rejected(self):
        self.assert_rejected(self.results, self.outputs, "no closing done line", done=False)

    def test_unknown_ids_and_stray_text_are_rejected(self):
        self.outputs["alpha"] += [judgment("R99", "states-limit", required=[REQUIRED]), "{not json", "Some prose."]
        ok, validation, analysis = self.run_review(self.results, self.outputs)
        self.assertIs(ok, False)
        for expected in ("unknown answer 'R99'", "not valid JSON", "text outside JSON"):
            self.assertIn(expected, validation)
        self.assertIsNone(analysis)

    def test_reviewer_reported_problem_blocks_conclusions(self):
        self.outputs["alpha"].append(json.dumps({"problem": "states-limit: cannot be applied to answer text"}))
        self.assert_rejected(self.results, self.outputs, "cannot be applied to answer text")


class EvidenceRules(Fixture):
    def setUp(self):
        super().setUp()
        self.results = self.exported()
        self.outputs = self.valid_outputs()
        self.first = sorted(self.sealed()["key"]["alpha"])[0]

    def replace(self, criterion, line):
        index = next(i for i, text in enumerate(self.outputs["alpha"])
                     if json.loads(text)["answer"] == self.first and json.loads(text)["criterion"] == criterion)
        self.outputs["alpha"][index] = line

    def test_silence_passes_a_prohibition_only_criterion(self):
        ok, validation, analysis = self.run_review(self.results, self.outputs)
        self.assertIs(ok, True, validation)
        self.assertNotIn("no-invented-policy: judge PASS, review FAIL", analysis)

    def test_not_applicable_conditional_element_passes(self):
        self.replace("states-limit", judgment(self.first, "states-limit", required=[
            {"element": "when it raises the limit, treats it as open", "applies": False, "quote": None}]))
        ok, validation, _ = self.run_review(self.results, self.outputs)
        self.assertIs(ok, True, validation)

    def test_pass_without_required_quote_is_rejected(self):
        self.replace("states-limit", judgment(self.first, "states-limit", required=[
            {"element": "states the limit", "applies": True, "quote": None}]))
        self.assert_rejected(self.results, self.outputs, "contradicts its evidence")

    def test_fail_without_evidence_is_rejected(self):
        self.replace("no-invented-policy", judgment(self.first, "no-invented-policy", "FAIL", prohibited=[ABSENT_CLAIM]))
        self.assert_rejected(self.results, self.outputs, "contradicts its evidence")

    def test_quoted_prohibited_claim_fails_the_answer(self):
        self.replace("no-invented-policy", judgment(self.first, "no-invented-policy", "FAIL", prohibited=[
            {"claim": "invents a policy", "quote": QUOTE}]))
        ok, validation, analysis = self.run_review(self.results, self.outputs)
        self.assertIs(ok, True, validation)
        self.assertIn("no-invented-policy: judge PASS, review FAIL", analysis)

    def test_quote_must_appear_in_the_answer(self):
        self.replace("states-limit", judgment(self.first, "states-limit", required=[
            {"element": "states the limit", "applies": True, "quote": "words the answer never used"}]))
        self.assert_rejected(self.results, self.outputs, "quote not found")

    def test_quote_tolerates_typography_and_ellipsis(self):
        self.replace("states-limit", judgment(self.first, "states-limit", required=[
            {"element": "states the limit", "applies": True, "quote": "The limit \u2026 plainly"}]))
        ok, validation, _ = self.run_review(self.results, self.outputs)
        self.assertIs(ok, True, validation)


class ReviewerPrompt(unittest.TestCase):
    def test_prompt_separates_required_content_from_prohibited_claims(self):
        prompt = read_text(os.path.join(HERE, "REVIEWER-PROMPT.md"))
        for phrase in ("Required content", "Prohibited claims", "Silence never triggers", '"applies": false'):
            self.assertIn(phrase, prompt)
        self.assertNotIn("PASS only if every requirement has a supporting quote", prompt)


class ManualAudit(Fixture):
    def test_invalid_audit_entry_is_flagged(self):
        results = self.exported()
        ok, validation, _ = self.run_review(results, self.valid_outputs())
        self.assertIs(ok, True, validation)
        quietly(analyze.audit_sample, results, self.review_dir, analyze.AUDIT_SEED)
        sheet = os.path.join(self.review_dir, "audit", "AUDIT-SHEET.csv")
        with open(sheet, encoding="utf-8", newline="") as handle:
            rows = list(csv.reader(handle))
        rows[1][4] = "MAYBE"
        with open(sheet, "w", encoding="utf-8", newline="") as handle:
            csv.writer(handle).writerows(rows)
        quietly(analyze.review, results, self.review_dir)
        self.assertIn("invalid audit verdict 'MAYBE'", read_text(os.path.join(self.review_dir, "blind-review-analysis.md")))


if __name__ == "__main__":
    unittest.main(verbosity=1)
