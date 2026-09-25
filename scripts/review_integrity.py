"""Guard new blind reviews without changing the frozen v1 scoring implementation.

See scripts/README.md. All operations are local; this tool never calls a model.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "frozen_analysis", ROOT / "evals-holdout/analysis/analyze.py")
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)
SEAL = Path("key/INPUTS.sha256.json")


class IntegrityError(ValueError):
    """Evidence no longer satisfies the export/review contract."""


def fingerprint(path):
    return core.sha256(path) if path.is_file() else None


def result_inputs(results):
    """Include excluded runs too: adding a missing trace can change eligibility."""
    files = {"aggregate-result.json": fingerprint(results / "aggregate-result.json")}
    agg = core.load(results)
    names = [case["name"] for case in agg["cases"]]
    if len(names) != len(set(names)) or any(
            not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", name) for name in names):
        raise IntegrityError("Case names must be unique, simple directory names.")
    for case, arm, n, _ in core.runs(agg):
        path = Path(core.transcript_path(results, case["name"], arm, n))
        files[path.relative_to(results).as_posix()] = fingerprint(path)
    return files


def review_inputs(review, agg):
    files = {"key/SEALED-KEY.json": fingerprint(review / "key/SEALED-KEY.json")}
    for case in agg["cases"]:
        name = f"packets/{case['name']}.md"
        files[name] = fingerprint(review / name)
    if any(value is None for value in files.values()):
        raise IntegrityError("An exported key or packet is missing.")
    return files


def require_open_round(results, review):
    for folder in (results, review):
        if any((folder / marker).exists() for marker in ("CLOSURE.md", "CLOSURE.sha256")):
            raise IntegrityError("This round is closed; preserve its reports and evidence.")


def export(results, review, seed=core.EXPORT_SEED):
    results, review = Path(results), Path(review)
    require_open_round(results, review)
    if review.exists() and any(review.iterdir()):
        raise IntegrityError("Export requires a new, empty review directory; do not reseal old reviews.")
    before = result_inputs(results)
    agg = core.load(results)
    # A retained trace is valid after Temp cleanup, but conflicting copies need investigation.
    for case, arm, n, run in core.runs(agg):
        source = Path(run["tracePath"]) if run.get("tracePath") else None
        target = Path(core.transcript_path(results, case["name"], arm, n))
        if source and source.is_file() and fingerprint(source) != fingerprint(target):
            raise IntegrityError("Original and retained transcripts differ; preserve and investigate both copies.")
    core.export(results, review, seed)
    if result_inputs(results) != before:
        raise IntegrityError("Results changed during export; no input seal was written.")
    sealed = {"schema": 1, "results": before, "review": review_inputs(review, agg)}
    core.write(review / SEAL, json.dumps(sealed, indent=2, sort_keys=True) + "\n")


def verify(results, review):
    results, review = Path(results), Path(review)
    if not (review / SEAL).is_file():
        raise IntegrityError("Input seal is missing; historical reviews cannot be retroactively sealed.")
    sealed = core.read_json(review / SEAL)
    if sealed.get("schema") != 1:
        raise IntegrityError("Unsupported input seal schema.")
    # Check the raw aggregate before using any paths or eligibility from its contents.
    expected = sealed.get("results", {})
    if not expected.get("aggregate-result.json") or (
            fingerprint(results / "aggregate-result.json") != expected["aggregate-result.json"]):
        raise IntegrityError("Aggregate changed or is missing since export.")
    if result_inputs(results) != expected:
        raise IntegrityError("Retained transcripts changed or are missing since export.")
    agg = core.load(results)
    if review_inputs(review, agg) != sealed.get("review"):
        raise IntegrityError("Exported packets or key changed since export.")
    return core.load_key(results, review, agg)


def contains_tool_use(value):
    if isinstance(value, dict):
        return value.get("type") in ("tool_use", "server_tool_use") or any(
            contains_tool_use(child) for child in value.values())
    if isinstance(value, list):
        return any(contains_tool_use(child) for child in value)
    return False


def verify_reviewers(review, sealed):
    """Require the selected, successful, tool-free stream for each accepted output."""
    for case in sealed["key"]:
        trace = review / "transcripts" / f"{case}.stream.jsonl"
        output = review / "outputs" / f"{case}.jsonl"
        if not trace.is_file() or not output.is_file():
            raise IntegrityError(f"{case}: reviewer transcript or output is missing.")
        records = [json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines() if line.strip()]
        init = [r for r in records if r.get("type") == "system" and r.get("subtype") == "init"]
        finals = [r for r in records if r.get("type") == "result"]
        if len(init) != 1 or init[0].get("tools") != [] or init[0].get("mcp_servers") != []:
            raise IntegrityError(f"{case}: reviewer must start with tools and MCP servers disabled.")
        if contains_tool_use(records):
            raise IntegrityError(f"{case}: reviewer transcript contains tool use.")
        if (len(finals) != 1 or finals[0].get("subtype") != "success"
                or finals[0].get("is_error") is not False):
            raise IntegrityError(f"{case}: reviewer did not complete successfully exactly once.")
        if finals[0].get("result", "").strip() != output.read_text(encoding="utf-8").strip():
            raise IntegrityError(f"{case}: output differs from the reviewer transcript.")


def review(results, review_dir):
    results, review_dir = Path(results), Path(review_dir)
    require_open_round(results, review_dir)
    sealed = verify(results, review_dir)
    verify_reviewers(review_dir, sealed)
    return core.review(results, review_dir)


def audit_sample(results, review_dir, seed=core.AUDIT_SEED):
    results, review_dir = Path(results), Path(review_dir)
    require_open_round(results, review_dir)
    verify(results, review_dir)
    core.audit_sample(results, review_dir, seed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("export", "verify", "audit-sample", "review"):
        p = sub.add_parser(command)
        p.add_argument("results", type=Path)
        p.add_argument("review", type=Path)
        if command in ("export", "audit-sample"):
            p.add_argument("--seed", type=int, default=(
                core.EXPORT_SEED if command == "export" else core.AUDIT_SEED))
    args = parser.parse_args()
    try:
        if args.command == "export":
            export(args.results, args.review, args.seed)
        elif args.command == "verify":
            verify(args.results, args.review)
            print("Exported inputs match their seal.")
        elif args.command == "audit-sample":
            audit_sample(args.results, args.review, args.seed)
        elif not review(args.results, args.review):
            return 1
    except (IntegrityError, core.StopRule, OSError, ValueError, KeyError, TypeError) as error:
        print(f"STOP: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
