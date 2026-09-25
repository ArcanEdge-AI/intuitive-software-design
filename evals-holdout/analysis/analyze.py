"""Pre-registered analysis for the holdout eval suite; see ../ANALYSIS-PLAN.md.

Every command is local and free: nothing here calls a model.

  python analyze.py check <suite dir> [--plugin-root <dir>]
      Structural checks of the suite, a FREEZE.sha256 check, and reports of
      rubric-like hints, framework vocabulary, and text shared with the plugin.
  python analyze.py automated <results dir>
      Preserves transcripts, records which runs are eligible, enforces the
      exclusion stop rule, and reports automated scores and criterion counts.
  python analyze.py export <results dir> <review dir> [--seed N]
      Blinded, shuffled reviewer packets for the eligible runs, and a sealed key.
  python analyze.py audit-sample <results dir> <review dir> [--seed N]
      The predefined manual-audit sample: 15 judgments the judge passed and 15 it
      failed, as a blank sheet that shows neither verdict.
  python analyze.py review <results dir> <review dir>
      Validates every reviewer output first. Any invalid, duplicate, missing, or
      reviewer-flagged judgment produces a validation report and no conclusions.
      Otherwise reports blind-review scores, agreement with the judge, and the
      manual audit once it is filled in.

Eligibility is decided once, from the results and the preserved transcripts, and
every command reuses that decision. Automated results are never modified.
Exit codes: 0 success, 1 failed check or invalid output, 2 stop rule.
"""
import argparse
import csv
import hashlib
import json
import os
import random
import re
import shutil
import sys
from collections import Counter, defaultdict

ARMS = ("with", "without")
BOOTSTRAP_SEED = 7
ITERATIONS = 10_000
EXPORT_SEED = 20260924
AUDIT_SEED = 20260925
AUDIT_PER_VERDICT = 15
MAX_EXCLUDED_PER_ARM = 1

# Identity markers only; content words stay, so grading is unaffected.
REDACTIONS = [
    r"intuitive[- ]software[- ]design(?:[- ]standard)?",
    r"purpose-first(?:-redesign)?|user-task-walkthrough|product-mental-model|decision-support-design"
    r"|multi-role-workflow|connected-experience-design|behavioral-evaluation",
    r"\bSKILL\.md\b|scoring-reference(?:\.md)?|audit-template(?:\.md)?|review-template(?:\.md)?|examples\.md",
    r"§\s?\d+(?:\.\d+)*",
    r"[A-Za-z]:\\[^\s)`'\"]+",
    r"\bplugins?\b",
]
HINT_PHRASES = [r"make sure", r"remember to", r"be sure to", r"don't forget", r"please (?:also )?(?:cover|include|consider)",
                r"your answer should", r"we expect", r"checklist"]
FRAMEWORK_TERMS = [r"friction", r"UI Clarity", r"Flow Intuition", r"Behavior Confidence", r"mental model", r"decision density",
                   r"prediction gap", r"recovery and validation", r"intended[- ]user", r"smallest complete", r"\bNE\b",
                   r"\bstandard\b", r"UI, Flow", r"\bFeel\b"]
GRADER_KEYS = {"type", "weight", "arm", "tool", "input_match", "target", "match", "flags", "pattern"}
# Tool-input fields that hold a path: naming the suite directory itself there is an access.
PATH_FIELDS = {"file_path", "path", "notebook_path", "glob"}
TYPOGRAPHY = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"',
                            "–": "-", "—": "-", " ": " "})


class StopRule(Exception):
    """Too many runs in some case and arm are ineligible, so no conclusions are drawn."""


def sha256(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def read_text(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def read_json(path):
    return json.loads(read_text(path))


def write(path, text):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def load(results_dir):
    return read_json(os.path.join(results_dir, "aggregate-result.json"))


def split_frontmatter(text):
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?(.*)$", text, re.S)
    if not match:
        return {}, text
    fields = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields, match.group(2)


def mean(values):
    return sum(values) / len(values)


def pooled_difference(samples):
    """Mean over cases of (with mean - without mean); each case weighs the same."""
    return mean([mean(w) - mean(wo) for w, wo in samples.values()])


def bootstrap(samples):
    """90% stratified bootstrap: resample runs within each case and arm."""
    rng = random.Random(BOOTSTRAP_SEED)
    diffs = sorted(pooled_difference({c: ([rng.choice(w) for _ in w], [rng.choice(wo) for _ in wo])
                                      for c, (w, wo) in samples.items()}) for _ in range(ITERATIONS))
    return diffs[int(0.05 * ITERATIONS)], diffs[int(0.95 * ITERATIONS)]


def verdict(low, high):
    if low > 0:
        return "interval above 0"
    if high < 0:
        return "interval below 0"
    return "interval includes 0"


# ---------------------------------------------------------------- check
def check(suite, plugin_root):
    problems, notes = [], []
    cases = sorted(d for d in os.listdir(suite) if os.path.isfile(os.path.join(suite, d, "prompt.md")))
    nested = [os.path.relpath(os.path.join(root, "prompt.md"), suite) for root, _, files in os.walk(suite)
              if "prompt.md" in files and os.path.dirname(os.path.relpath(root, suite)) not in ("", ".")]
    if nested:
        problems.append(f"prompt.md below case level would become extra cases: {nested}")
    plugin_text = {}
    if plugin_root:
        for root, dirs, files in os.walk(plugin_root):
            dirs[:] = [d for d in dirs if d not in (".git", "results", os.path.basename(os.path.abspath(suite)))]
            for name in files:
                if name.endswith(".md"):
                    path = os.path.join(root, name)
                    plugin_text[os.path.relpath(path, plugin_root)] = read_text(path)
    for case in cases:
        fields, body = split_frontmatter(read_text(os.path.join(suite, case, "prompt.md")))
        for key in ("description", "max_turns", "allowed_tools"):
            if key not in fields:
                problems.append(f"{case}: prompt frontmatter lacks {key}")
        words = len(body.split())
        scored, indicators = [], []
        grader_dir = os.path.join(suite, case, "graders")
        for name in sorted(os.listdir(grader_dir)):
            gfields, gbody = split_frontmatter(read_text(os.path.join(grader_dir, name)))
            unknown = set(gfields) - GRADER_KEYS
            if unknown or "type" not in gfields:
                problems.append(f"{case}/{name}: frontmatter keys {sorted(gfields)}")
            if gfields.get("arm") == "with-only" or gfields.get("type") == "tool_used":
                indicators.append(name)
                continue
            scored.append(name)
            if gfields.get("type") == "llm":
                if not gbody.lstrip().startswith("PASS if") or not re.search(r"FAIL (?:only )?if", gbody):
                    problems.append(f"{case}/{name}: body must start with 'PASS if' and contain a 'FAIL if' condition")
                if len(gbody.split()) > 160:
                    notes.append(f"{case}/{name}: {len(gbody.split())} words")
                for term in FRAMEWORK_TERMS:
                    for hit in re.findall(term, gbody, re.I):
                        notes.append(f"{case}/{name}: framework-like term '{hit}'")
        if len(scored) < 4:
            problems.append(f"{case}: {len(scored)} scored criteria (need at least 4)")
        if not any("skill" in n for n in indicators) or "standard-read.md" not in indicators:
            problems.append(f"{case}: missing unscored indicators (have {indicators})")
        for phrase in HINT_PHRASES:
            for hit in re.finditer(phrase, body, re.I):
                notes.append(f"{case}: prompt phrase '{body[max(0, hit.start() - 40):hit.end() + 40].strip()}'")
        for term in FRAMEWORK_TERMS:
            for hit in re.findall(term, body, re.I):
                notes.append(f"{case}: prompt framework-like term '{hit}'")
        shared = []
        if plugin_text:
            tokens = re.findall(r"[a-z0-9']+", body.lower())
            grams = {" ".join(tokens[i:i + 8]) for i in range(len(tokens) - 7)}
            for path, text in plugin_text.items():
                other = re.findall(r"[a-z0-9']+", text.lower())
                common = grams & {" ".join(other[i:i + 8]) for i in range(len(other) - 7)}
                if common:
                    shared.append(f"{path}: {len(common)} ({sorted(common)[:2]})")
        print(f"{case}: prompt {words} words; scored {len(scored)} {scored}; indicators {indicators}")
        for item in shared:
            print(f"   shares 8-word sequences with {item}")
    manifest = os.path.join(suite, "FREEZE.sha256")
    if os.path.exists(manifest):
        listed = {}
        for line in read_text(manifest).splitlines():
            digest, _, rel = line.strip().partition("  ")
            listed[rel] = digest
        for rel, digest in listed.items():
            path = os.path.join(suite, rel)
            if not os.path.exists(path) or sha256(path) != digest:
                problems.append(f"FREEZE mismatch: {rel}")
        on_disk = {os.path.relpath(os.path.join(r, f), suite).replace(os.sep, "/")
                   for r, ds, fs in os.walk(suite) for f in fs if "results" not in r.split(os.sep)
                   and "__pycache__" not in r.split(os.sep)} - {"FREEZE.sha256"}
        if on_disk - set(listed):
            problems.append(f"files not in FREEZE.sha256: {sorted(on_disk - set(listed))}")
        print(f"FREEZE.sha256: {len(listed)} files checked")
    else:
        notes.append("no FREEZE.sha256 yet")
    for note in notes:
        print("note:", note)
    for problem in problems:
        print("PROBLEM:", problem)
    print("check:", "FAILED" if problems else "passed", f"({len(cases)} cases)")
    return not problems


# ---------------------------------------------------------------- transcripts
def strings(value):
    """Every string inside a tool input or result, so paths are matched unescaped."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def references_suite(text, suite_name, whole_value=False):
    """True when text names the suite directory as a path: relative, ./-prefixed, or absolute.

    Any text counts when the name is followed by a path separator. A path field or a
    shell word also counts when it ends at the suite directory itself."""
    name = re.escape(suite_name)
    if re.search(rf"(?<![\w.-]){name}[\\/]", text, re.I):
        return True
    return whole_value and any(re.fullmatch(rf"(?:.*[\\/])?{name}[\\/]?", word.strip("'\"`,;()[]{}"), re.I)
                               for word in text.split())


def trace_facts(path, suite_name):
    """Skills invoked, verified standard reads, and any exposure to the eval suite's files."""
    uses, results, skills, exposure = {}, {}, [], []
    for line in read_text(path).splitlines():
        try:
            record = json.loads(line)
        except ValueError:
            continue
        message = record.get("message") if isinstance(record.get("message"), dict) else {}
        content = message.get("content")
        for block in content if isinstance(content, list) else []:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use":
                name, tool_input = block.get("name"), block.get("input")
                tool_input = tool_input if isinstance(tool_input, dict) else {"": tool_input}
                uses[block.get("id")] = (name, tool_input)
                if name == "Skill":
                    skills.append(str(tool_input.get("skill", "")))
                for field, value in tool_input.items():
                    whole = field in PATH_FIELDS or (name, field) in (("Glob", "pattern"), ("Bash", "command"))
                    if any(references_suite(text, suite_name, whole) for text in strings(value)):
                        exposure.append(f"{name} {field}: {json.dumps(value)[:160]}")
            elif block.get("type") == "tool_result":
                results[block.get("tool_use_id")] = block
                if any(references_suite(text, suite_name) for text in strings(block.get("content"))):
                    exposure.append(f"result of {block.get('tool_use_id')}: {json.dumps(block.get('content'))[:160]}")
    reads = 0
    for use_id, (name, tool_input) in uses.items():
        if name != "Read" or not str(tool_input.get("file_path", "")).endswith("intuitive-software-design-standard.md"):
            continue
        result = results.get(use_id, {})
        content = result.get("content")
        text = content if isinstance(content, str) else " ".join(
            item.get("text", "") for item in (content or []) if isinstance(item, dict))
        # An offset read returns numbered lines without the title, so success is a non-error, non-empty result.
        if not result.get("is_error") and re.search(r"^\s*\d+[\t→]", text, re.M):
            reads += 1
    return skills, reads, exposure


# ---------------------------------------------------------------- eligibility
def runs(agg):
    for case in agg["cases"]:
        for arm in ARMS:
            for n, run in enumerate(case["arms"][arm], 1):
                yield case, arm, n, run


def transcript_path(results_dir, case_name, arm, n):
    return os.path.join(results_dir, "transcripts", case_name, f"{arm}-run{n}.trace.jsonl")


def suite_name_of(agg):
    return re.split(r"[\\/]", agg["cases"][0]["dir"])[0]


def preserve_transcripts(results_dir, agg):
    index = ["case\tarm\trun\tsource\tsha256"]
    for case, arm, n, run in runs(agg):
        source, target = run.get("tracePath"), transcript_path(results_dir, case["name"], arm, n)
        if source and os.path.exists(source) and os.path.abspath(source) != os.path.abspath(target):
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.copyfile(source, target)
        index.append(f"{case['name']}\t{arm}\t{n}\t{source}\t{sha256(target) if os.path.exists(target) else 'MISSING'}")
    write(os.path.join(results_dir, "transcripts", "INDEX.tsv"), "\n".join(index) + "\n")


def eligibility(results_dir, agg):
    """Decide which runs count. Read-only, and reused by every command."""
    suite_name, exclusions, totals = suite_name_of(agg), {}, Counter()
    for case, arm, n, run in runs(agg):
        totals[(case["name"], arm)] += 1
        reasons = []
        if run.get("error"):
            reasons.append(f"error: {run['error']}")
        if run.get("skippedPaidGraders"):
            reasons.append("paid graders skipped")
        trace = transcript_path(results_dir, case["name"], arm, n)
        if not os.path.exists(trace):
            reasons.append("transcript missing, so leakage cannot be checked")
        else:
            exposure = trace_facts(trace, suite_name)[2]
            if exposure:
                reasons.append(f"exposure to {suite_name}/ files: {exposure[0]}")
        if reasons:
            exclusions[(case["name"], arm, n)] = reasons
    excluded = Counter((case_name, arm) for case_name, arm, _ in exclusions)
    stop = [f"{case_name} / {arm} ({excluded[(case_name, arm)]} of {total} runs excluded)"
            for (case_name, arm), total in sorted(totals.items())
            if excluded[(case_name, arm)] > MAX_EXCLUDED_PER_ARM or excluded[(case_name, arm)] == total]
    eligible = [(case["name"], arm, n) for case, arm, n, _ in runs(agg) if (case["name"], arm, n) not in exclusions]
    return eligible, exclusions, stop


def require_eligible(results_dir, agg):
    eligible, exclusions, stop = eligibility(results_dir, agg)
    if stop:
        raise StopRule("too many runs excluded in " + "; ".join(stop))
    return eligible, exclusions


# ---------------------------------------------------------------- automated
def automated(results_dir):
    """Raises StopRule, after reporting the exclusions, when the stop rule applies."""
    agg = load(results_dir)
    preserve_transcripts(results_dir, agg)
    eligible, exclusions, stop = eligibility(results_dir, agg)
    write(os.path.join(results_dir, "eligibility.json"), json.dumps({
        "eligible": [list(key) for key in eligible],
        "excluded": [{"run": list(key), "reasons": reasons} for key, reasons in sorted(exclusions.items())],
        "stop": stop}, indent=2) + "\n")
    out = ["# Automated analysis (unchanged judge verdicts)", "",
           f"Results: `{os.path.basename(os.path.abspath(results_dir))}`; aggregate-result.json sha256 "
           f"`{sha256(os.path.join(results_dir, 'aggregate-result.json'))}`",
           f"Claude Code {agg.get('claudeVersion')}; model {agg['suite'].get('modelOverride')}; judge "
           f"{agg['suite'].get('judgeModel')}; cost ${agg.get('costUsd', 0):.2f}; partial {agg.get('partial')}", "",
           "## Validity checks", ""]
    out += [f"- Excluded {case_name} / {arm} / run {n}: {'; '.join(reasons)}"
            for (case_name, arm, n), reasons in sorted(exclusions.items())] or [
        "- Every run is eligible: no errors, skipped graders, missing transcripts, or eval-file exposure."]
    if stop:
        out += ["", "## Stopped", "", f"Too many runs are excluded in {'; '.join(stop)}. Under the analysis plan "
                "no scores are reported, and a rerun needs approval."]
        finish(os.path.join(results_dir, "automated-analysis.md"), out)
        raise StopRule("too many runs excluded in " + "; ".join(stop))
    eligible_set, suite_name = set(eligible), suite_name_of(agg)
    samples, criteria = {}, defaultdict(lambda: defaultdict(Counter))
    skills_by_case, reads_by_case = defaultdict(list), defaultdict(int)
    out += ["", "## Scores", "", "| Case | With | Without | Difference (90% bootstrap) | Runs used (with, without) |",
            "| --- | --- | --- | --- | --- |"]
    for case in agg["cases"]:
        chosen = {arm: [(n, run) for n, run in enumerate(case["arms"][arm], 1) if (case["name"], arm, n) in eligible_set]
                  for arm in ARMS}
        w, wo = [run["score"] for _, run in chosen["with"]], [run["score"] for _, run in chosen["without"]]
        samples[case["name"]] = (w, wo)
        low, high = bootstrap({case["name"]: (w, wo)})
        out.append(f"| {case['name']} | {mean(w):.2f} | {mean(wo):.2f} | {mean(w) - mean(wo):+.2f} ({low:+.2f} to {high:+.2f}) "
                   f"| {len(w)}/{len(case['arms']['with'])}, {len(wo)}/{len(case['arms']['without'])} |")
        for arm, arm_runs in chosen.items():
            for n, run in arm_runs:
                for grader in run["graders"]:
                    if grader.get("scored"):
                        criteria[case["name"]][grader["name"]][arm] += 1 if grader.get("passed") else 0
                        criteria[case["name"]][grader["name"]][arm + "_n"] += 1
                if arm == "with":
                    skills, reads, _ = trace_facts(transcript_path(results_dir, case["name"], arm, n), suite_name)
                    skills_by_case[case["name"]].append(skills)
                    reads_by_case[case["name"]] += reads > 0
    low, high = bootstrap(samples)
    out += ["", f"**Pooled (mean of case differences): {pooled_difference(samples):+.2f} "
                f"(90% stratified bootstrap {low:+.2f} to {high:+.2f}; {verdict(low, high)}).**"]
    out += ["", "## Criteria (passes / eligible runs)", "", "| Case | Criterion | With | Without |", "| --- | --- | --- | --- |"]
    for case_name, graders in criteria.items():
        for grader_name, c in graders.items():
            out.append(f"| {case_name} | {grader_name} | {c['with']}/{c['with_n']} | {c['without']}/{c['without_n']} |")
    out += ["", "## Unscored indicators (eligible plugin-arm runs, from transcripts)", ""]
    for case_name, case_skills in skills_by_case.items():
        fired = sum(bool(s) for s in case_skills)
        names = Counter(name for s in case_skills for name in s)
        out.append(f"- {case_name}: a skill fired in {fired}/{len(case_skills)} runs {dict(names)}; "
                   f"verified standard read in {reads_by_case[case_name]}/{len(case_skills)} runs")
    finish(os.path.join(results_dir, "automated-analysis.md"), out)


def finish(path, lines):
    report = "\n".join(lines) + "\n"
    write(path, report)
    print(report)


# ---------------------------------------------------------------- blind review
def final_answer(run):
    for grader in run["graders"]:
        if grader.get("judgeVotes") is not None and grader.get("evidence") is not None:
            return grader["evidence"]
    return None


def redacted_answer(run):
    """The answer exactly as reviewers see it, and how many identity markers were redacted."""
    text = final_answer(run)
    if text is None:
        return None, 0
    count = 0
    for pattern in REDACTIONS:
        text, hits = re.subn(pattern, "[redacted]", text, flags=re.I)
        count += hits
    return text, count


def scored_llm_graders(case):
    names = {g["name"] for _, _, _, run in runs({"cases": [case]}) for g in run["graders"]
             if g.get("scored") and g.get("judgeVotes") is not None}
    return [g for g in case["graders"] if g["name"] in names]


def export(results_dir, review_dir, seed):
    agg = load(results_dir)
    eligible, _ = require_eligible(results_dir, agg)
    key_path = os.path.join(review_dir, "key", "SEALED-KEY.json")
    if os.path.exists(key_path):
        raise SystemExit(f"{key_path} exists; refusing to reshuffle an exported review")
    eligible_set, rng, key = set(eligible), random.Random(seed), {}
    for case in sorted(agg["cases"], key=lambda c: c["name"]):
        answers = []
        for arm in ARMS:
            for n, run in enumerate(case["arms"][arm], 1):
                if (case["name"], arm, n) not in eligible_set:
                    continue
                text, count = redacted_answer(run)
                if text is None:
                    raise SystemExit(f"{case['name']} {arm} run {n} is eligible but has no final answer")
                answers.append({"arm": arm, "run": n, "text": text, "redactions": count})
        rng.shuffle(answers)
        lines = [f"# Case: {case['name']}", "", "## Request the assistant received", "", case["promptMarkdown"].strip(), "",
                 "## Criteria", ""]
        for grader in scored_llm_graders(case):
            lines += [f"### {grader['name']}", "", grader["graderMarkdown"].strip(), ""]
        lines += ["## Answers", ""]
        key[case["name"]] = {}
        for i, answer in enumerate(answers, 1):
            answer_id = f"R{i:02d}"
            key[case["name"]][answer_id] = {k: answer[k] for k in ("arm", "run", "redactions")}
            lines += [f"### Answer {answer_id}", "", answer["text"].strip(), ""]
        write(os.path.join(review_dir, "packets", f"{case['name']}.md"), "\n".join(lines))
        print(f"{case['name']}: {len(answers)} answers, redactions "
              f"{[key[case['name']][a]['redactions'] for a in sorted(key[case['name']])]}")
    write(key_path, json.dumps({"seed": seed, "results": os.path.abspath(results_dir),
                                "eligible": [list(k) for k in eligible], "key": key}, indent=2) + "\n")


def load_key(results_dir, review_dir, agg):
    """The sealed key, after confirming the eligible runs have not changed since export."""
    eligible, _ = require_eligible(results_dir, agg)
    sealed = read_json(os.path.join(review_dir, "key", "SEALED-KEY.json"))
    if sealed.get("eligible") != [list(k) for k in eligible]:
        raise SystemExit("The eligible runs differ from those exported for review; stop and investigate before reviewing.")
    return sealed


def audit_sample(results_dir, review_dir, seed):
    agg = load(results_dir)
    key = load_key(results_dir, review_dir, agg)["key"]
    sheet = os.path.join(review_dir, "audit", "AUDIT-SHEET.csv")
    if os.path.exists(sheet):
        raise SystemExit(f"{sheet} exists; refusing to overwrite the audit sheet")
    strata = {"PASS": [], "FAIL": []}
    for case in sorted(agg["cases"], key=lambda c: c["name"]):
        for answer_id, meta in sorted(key[case["name"]].items()):
            run = case["arms"][meta["arm"]][meta["run"] - 1]
            for grader in run["graders"]:
                if grader.get("scored") and grader.get("judgeVotes") is not None:
                    strata["PASS" if grader.get("passed") else "FAIL"].append((case["name"], answer_id, grader["name"]))
    rng = random.Random(seed)
    chosen = []
    for label in ("PASS", "FAIL"):
        chosen += [(item, label) for item in rng.sample(strata[label], min(AUDIT_PER_VERDICT, len(strata[label])))]
    rng.shuffle(chosen)
    rows = ["item,case,answer,criterion,verdict,note"] + [f"{i},{c},{a},{g},," for i, ((c, a, g), _) in enumerate(chosen, 1)]
    write(sheet, "\n".join(rows) + "\n")
    write(os.path.join(review_dir, "key", "AUDIT-KEY.json"), json.dumps(
        {"seed": seed, "items": [{"item": i, "case": c, "answer": a, "criterion": g, "judge": label}
                                 for i, ((c, a, g), label) in enumerate(chosen, 1)]}, indent=2) + "\n")
    print(f"audit sample: {len(chosen)} judgments ({sum(l == 'PASS' for _, l in chosen)} judge PASS, "
          f"{sum(l == 'FAIL' for _, l in chosen)} judge FAIL); answers are in packets/<case>.md")


def normalized(text):
    text = re.sub(r"[*_`#>]+", "", text.translate(TYPOGRAPHY))
    return re.sub(r"\s+", " ", text).strip().lower()


def quote_found(quote, answer):
    """True when the quote appears in the answer; '...' may join passages in order."""
    parts = [normalized(part) for part in re.split(r"\.\.\.|…", quote)]
    target, position = normalized(answer), 0
    for part in [p for p in parts if p]:
        found = target.find(part, position)
        if found < 0:
            return False
        position = found + len(part)
    return any(parts)


def judgment_errors(item, criteria, answers):
    """Problems with one judgment line, including a verdict its own evidence does not support."""
    issues, answer_id = [], item.get("answer")
    if answer_id not in answers:
        issues.append(f"unknown answer {answer_id!r}")
    if item.get("criterion") not in criteria:
        issues.append(f"unknown criterion {item.get('criterion')!r}")
    if item.get("verdict") not in ("PASS", "FAIL"):
        issues.append(f"invalid verdict {item.get('verdict')!r}")
    required, prohibited = item.get("required"), item.get("prohibited")
    if not isinstance(required, list) or not isinstance(prohibited, list):
        return issues + ["'required' and 'prohibited' must be lists"]
    text, supported, triggered = answers.get(answer_id), True, False
    for element in required:
        if not isinstance(element, dict) or not isinstance(element.get("applies"), bool):
            issues.append("each required element needs 'applies': true or false")
            continue
        quote = element.get("quote")
        if quote is not None and not isinstance(quote, str):
            issues.append("each quote must be a string or null")
        elif element["applies"] and not quote:
            supported = False
        elif element["applies"] and text is not None and not quote_found(quote, text):
            issues.append(f"quote not found in the answer: {quote[:60]!r}")
    for claim in prohibited:
        quote = claim.get("quote") if isinstance(claim, dict) else None
        if not isinstance(claim, dict) or (quote is not None and not isinstance(quote, str)):
            issues.append("each prohibited claim must be an object whose quote is a string or null")
        elif quote:
            triggered = True
            if text is not None and not quote_found(quote, text):
                issues.append(f"quote not found in the answer: {quote[:60]!r}")
    derived = "PASS" if supported and not triggered else "FAIL"
    if item.get("verdict") in ("PASS", "FAIL") and item["verdict"] != derived:
        issues.append(f"verdict {item['verdict']} contradicts its evidence, which gives {derived}")
    return issues


def validate_review(agg, sealed, review_dir):
    """Every judgment, keyed by case and (answer, criterion), plus errors and reviewer-reported problems."""
    verdicts, errors, problems = {}, [], []
    for case in agg["cases"]:
        name, ids = case["name"], sealed["key"][case["name"]]
        criteria = [g["name"] for g in scored_llm_graders(case)]
        answers = {answer_id: redacted_answer(case["arms"][meta["arm"]][meta["run"] - 1])[0] for answer_id, meta in ids.items()}
        path = os.path.join(review_dir, "outputs", f"{name}.jsonl")
        if not os.path.exists(path):
            errors.append(f"{name}: no reviewer output")
            continue
        seen, done, count = {}, None, 0
        for number, raw in enumerate(read_text(path).splitlines(), 1):
            line = raw.strip()
            if not line or line.startswith("```"):
                continue
            if not line.startswith("{"):
                errors.append(f"{name} line {number}: text outside JSON: {line[:60]!r}")
                continue
            try:
                item = json.loads(line.rstrip(","))
            except ValueError:
                errors.append(f"{name} line {number}: not valid JSON")
                continue
            if not isinstance(item, dict):
                errors.append(f"{name} line {number}: not a JSON object")
            elif "problem" in item:
                problems.append(f"{name}: {item['problem']}")
            elif "done" in item:
                if done is not None:
                    errors.append(f"{name} line {number}: a second closing done line")
                done = item
            else:
                count += 1
                pair = (item.get("answer"), item.get("criterion"))
                errors += [f"{name} line {number}: {issue}" for issue in judgment_errors(item, criteria, answers)]
                if pair in seen:
                    errors.append(f"{name} line {number}: duplicate judgment for {pair[0]} / {pair[1]}")
                else:
                    seen[pair] = item
        missing = [f"{a} / {c}" for a in sorted(ids) for c in criteria if (a, c) not in seen]
        if missing:
            errors.append(f"{name}: {len(missing)} judgments missing, for example {missing[:3]}")
        if done is None:
            errors.append(f"{name}: no closing done line, so the output may be truncated")
        elif done.get("done") is not True or done.get("judgments") != count:
            errors.append(f"{name}: the closing line reports {done.get('judgments')!r} judgments, but {count} were given")
        verdicts[name] = seen
    return verdicts, errors, problems


def audit_section(review_dir, verdicts):
    sheet, key_path = os.path.join(review_dir, "audit", "AUDIT-SHEET.csv"), os.path.join(review_dir, "key", "AUDIT-KEY.json")
    if not (os.path.exists(sheet) and os.path.exists(key_path)):
        return []
    sampled = {item["item"]: item for item in read_json(key_path)["items"]}
    pending, invalid, graded = 0, [], []
    with open(sheet, encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            number = (row.get("item") or "").strip()
            value, item = (row.get("verdict") or "").strip(), sampled.get(int(number)) if number.isdigit() else None
            if item is None:
                invalid.append(f"unknown audit item {row.get('item')!r}")
            elif not value:
                pending += 1
            elif value in ("PASS", "FAIL"):
                graded.append((item, value))
            else:
                invalid.append(f"item {row['item']}: invalid audit verdict {value!r}")
    out = ["", "## Manual audit (predefined sample)", ""]
    if invalid:
        return out + [f"- {entry}" for entry in invalid] + ["- The audit comparison is withheld until these entries are corrected."]
    if not graded:
        return out + [f"- Not yet graded ({pending} of {len(sampled)} pending)."]
    judge = sum(item["judge"] == human for item, human in graded)
    blind = sum(verdicts[item["case"]][(item["answer"], item["criterion"])]["verdict"] == human for item, human in graded)
    return out + [f"- Graded {len(graded)} of {len(sampled)} sampled judgments; {pending} pending.",
                  f"- The judge agrees with the audit on {judge}/{len(graded)}; the blind reviewer on {blind}/{len(graded)}."]


def review(results_dir, review_dir):
    """Returns False, and writes no conclusions, when any reviewer output fails validation."""
    agg = load(results_dir)
    sealed = load_key(results_dir, review_dir, agg)
    verdicts, errors, problems = validate_review(agg, sealed, review_dir)
    if errors or problems:
        lines = ["# Blind-review validation failed", "",
                 "No blind-review conclusions are reported until every item below is resolved. "
                 "Under the analysis plan a case may be re-reviewed once.", ""]
        lines += [f"- Reviewer-reported problem: {problem}" for problem in problems] + [f"- {error}" for error in errors]
        finish(os.path.join(review_dir, "blind-review-validation.md"), lines)
        return False
    samples, agreement, disagreements = {}, defaultdict(Counter), []
    for case in agg["cases"]:
        ids = {(meta["arm"], meta["run"]): answer_id for answer_id, meta in sealed["key"][case["name"]].items()}
        scores = {arm: [] for arm in ARMS}
        for arm in ARMS:
            for n, run in enumerate(case["arms"][arm], 1):
                answer_id = ids.get((arm, n))
                if answer_id is None:
                    continue  # ineligible, so never exported
                scored = [g for g in run["graders"] if g.get("scored")]
                passed = 0
                for grader in scored:
                    if grader.get("judgeVotes") is None:  # deterministic graders keep their automated verdict
                        passed += bool(grader.get("passed"))
                        continue
                    item = verdicts[case["name"]][(answer_id, grader["name"])]
                    judge = "PASS" if grader.get("passed") else "FAIL"
                    passed += item["verdict"] == "PASS"
                    agreement[arm][(judge, item["verdict"])] += 1
                    if judge != item["verdict"]:
                        disagreements.append((case["name"], answer_id, grader["name"], judge, item))
                scores[arm].append(passed / len(scored))
        samples[case["name"]] = (scores["with"], scores["without"])
    out = ["# Blind-review analysis (separate from the automated verdicts)", "", "## Scores from blind review", "",
           "| Case | With | Without | Difference (90% bootstrap) |", "| --- | --- | --- | --- |"]
    for name, (w, wo) in samples.items():
        low, high = bootstrap({name: (w, wo)})
        out.append(f"| {name} | {mean(w):.2f} | {mean(wo):.2f} | {mean(w) - mean(wo):+.2f} ({low:+.2f} to {high:+.2f}) |")
    low, high = bootstrap(samples)
    out += ["", f"**Pooled: {pooled_difference(samples):+.2f} (90% stratified bootstrap {low:+.2f} to {high:+.2f}; "
                f"{verdict(low, high)}).**"]
    out += ["", "## Agreement with the automated judge", "",
            "| Arm | Both PASS | Both FAIL | Judge PASS, review FAIL | Judge FAIL, review PASS |", "| --- | --- | --- | --- | --- |"]
    for arm in ARMS:
        c = agreement[arm]
        out.append(f"| {arm} | {c[('PASS', 'PASS')]} | {c[('FAIL', 'FAIL')]} | {c[('PASS', 'FAIL')]} | {c[('FAIL', 'PASS')]} |")
    out += ["", "## Disagreements for adjudication", ""]
    for case_name, answer_id, grader_name, judge, item in disagreements:
        evidence = json.dumps({k: item.get(k) for k in ("required", "prohibited")})[:600]
        out.append(f"- {case_name} / {answer_id} / {grader_name}: judge {judge}, review {item['verdict']}. Review evidence: {evidence}")
    out += audit_section(review_dir, verdicts)
    finish(os.path.join(review_dir, "blind-review-analysis.md"), out)
    return True


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("check"); p.add_argument("suite"); p.add_argument("--plugin-root")
    p = sub.add_parser("automated"); p.add_argument("results")
    p = sub.add_parser("export"); p.add_argument("results"); p.add_argument("review"); p.add_argument("--seed", type=int, default=EXPORT_SEED)
    p = sub.add_parser("audit-sample"); p.add_argument("results"); p.add_argument("review"); p.add_argument("--seed", type=int, default=AUDIT_SEED)
    p = sub.add_parser("review"); p.add_argument("results"); p.add_argument("review")
    args = parser.parse_args()
    try:
        if args.command == "check":
            return 0 if check(args.suite, args.plugin_root) else 1
        if args.command == "automated":
            automated(args.results)
        elif args.command == "export":
            export(args.results, args.review, args.seed)
        elif args.command == "audit-sample":
            audit_sample(args.results, args.review, args.seed)
        elif not review(args.results, args.review):
            return 1
    except StopRule as stop:
        print(f"STOP: {stop}. Under the analysis plan nothing further is reported; a rerun needs approval.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
