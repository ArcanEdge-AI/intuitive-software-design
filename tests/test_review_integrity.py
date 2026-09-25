"""Free regression checks for the current entry point, using synthetic evidence only."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


guard = module("review_integrity", "scripts/review_integrity.py")
fixtures = module("frozen_fixtures", "evals-holdout/analysis/test_analyze.py")


class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.results = Path(fixtures.make_results(self.root))
        self.review_dir = self.root / "review"
        fixtures.quietly(guard.core.automated, self.results)

    def export(self):
        fixtures.quietly(guard.export, self.results, self.review_dir)

    def add_outputs(self):
        sealed = guard.verify(self.results, self.review_dir)
        for case, ids in sealed["key"].items():
            lines = []
            for answer in ids:
                lines.append(fixtures.judgment(answer, "states-limit", required=[fixtures.REQUIRED]))
                lines.append(fixtures.judgment(answer, "no-invented-policy", prohibited=[fixtures.ABSENT_CLAIM]))
            lines.append(json.dumps({"done": True, "judgments": len(lines)}))
            output = "\n".join(lines) + "\n"
            guard.core.write(self.review_dir / "outputs" / f"{case}.jsonl", output)
            records = [{"type": "system", "subtype": "init", "tools": [], "mcp_servers": []},
                       {"type": "result", "subtype": "success", "is_error": False, "result": output}]
            self.write_trace(case, records)

    def write_trace(self, case, records):
        guard.core.write(self.review_dir / "transcripts" / f"{case}.stream.jsonl",
                         "\n".join(json.dumps(r) for r in records) + "\n")

    def assert_stops(self, text):
        with self.assertRaisesRegex(guard.IntegrityError, text):
            fixtures.quietly(guard.review, self.results, self.review_dir)
        self.assertFalse((self.review_dir / "blind-review-analysis.md").exists())

    def test_complete_review_and_audit_preserve_inputs(self):
        self.export()
        self.add_outputs()
        before = guard.result_inputs(self.results)
        fixtures.quietly(guard.audit_sample, self.results, self.review_dir)
        self.assertTrue(fixtures.quietly(guard.review, self.results, self.review_dir))
        self.assertTrue((self.review_dir / "audit/AUDIT-SHEET.csv").is_file())
        self.assertEqual(before, guard.result_inputs(self.results))
        guard.verify(self.results, self.review_dir)

    def test_changed_verdict_with_identical_eligible_ids_is_rejected(self):
        self.export()
        self.add_outputs()
        agg = guard.core.load(self.results)
        agg["cases"][0]["arms"]["with"][0]["graders"][0]["passed"] = False
        # This is the precise defect in the retained historical implementation.
        old_key = guard.core.load_key(self.results, self.review_dir, agg)
        self.assertEqual([], guard.core.validate_review(agg, old_key, self.review_dir)[1])
        guard.core.write(self.results / "aggregate-result.json", json.dumps(agg))
        self.assert_stops("Aggregate changed")

    def test_missing_or_changed_sealed_inputs_stop_review_and_audit(self):
        self.export()
        self.add_outputs()
        paths = [self.results / "aggregate-result.json",
                 self.results / "transcripts/alpha/with-run1.trace.jsonl",
                 self.review_dir / "key/SEALED-KEY.json", self.review_dir / "packets/alpha.md"]
        for path in paths:
            original = path.read_bytes()
            for remove in (False, True):
                with self.subTest(path=path.name, missing=remove):
                    try:
                        path.unlink() if remove else path.write_bytes(original + b"\n")
                        self.assert_stops("changed|missing")
                        with self.assertRaises(guard.IntegrityError):
                            guard.audit_sample(self.results, self.review_dir)
                        self.assertFalse((self.review_dir / "audit/AUDIT-SHEET.csv").exists())
                    finally:
                        path.write_bytes(original)

    def test_missing_or_unsupported_seal_cannot_be_repaired_by_export(self):
        self.export()
        seal = self.review_dir / guard.SEAL
        seal.unlink()
        self.assert_stops("seal is missing")
        with self.assertRaisesRegex(guard.IntegrityError, "empty review"):
            guard.export(self.results, self.review_dir)
        seal.write_text('{"schema": 99}', encoding="utf-8")
        self.assert_stops("Unsupported")

    def test_manifest_cannot_omit_transcripts(self):
        self.export()
        seal = self.review_dir / guard.SEAL
        data = json.loads(seal.read_text(encoding="utf-8"))
        del data["results"]["transcripts/alpha/with-run1.trace.jsonl"]
        seal.write_text(json.dumps(data), encoding="utf-8")
        self.assert_stops("Retained transcripts changed")

    def test_adding_previously_missing_excluded_trace_is_rejected(self):
        missing = self.results / "transcripts/alpha/without-run3.trace.jsonl"
        missing.unlink()
        source = Path(guard.core.load(self.results)["cases"][0]["arms"]["without"][2]["tracePath"])
        source.unlink()
        self.export()
        missing.write_text("", encoding="utf-8")
        self.assert_stops("Retained transcripts changed")

    def test_removed_temp_sources_do_not_destroy_retained_evidence(self):
        for _, _, _, run in guard.core.runs(guard.core.load(self.results)):
            Path(run["tracePath"]).unlink()
        before = guard.result_inputs(self.results)
        self.export()
        self.add_outputs()
        self.assertTrue(fixtures.quietly(guard.review, self.results, self.review_dir))
        self.assertEqual(before, guard.result_inputs(self.results))

    def test_conflicting_source_and_retained_trace_stops_export(self):
        agg = guard.core.load(self.results)
        source = Path(agg["cases"][0]["arms"]["with"][0]["tracePath"])
        source.write_text("different trace", encoding="utf-8")
        with self.assertRaisesRegex(guard.IntegrityError, "transcripts differ"):
            guard.export(self.results, self.review_dir)
        self.assertFalse(self.review_dir.exists())

    def test_export_does_not_adopt_existing_outputs(self):
        guard.core.write(self.review_dir / "outputs/alpha.jsonl", "old evidence")
        with self.assertRaisesRegex(guard.IntegrityError, "empty review"):
            guard.export(self.results, self.review_dir)
        self.assertFalse((self.review_dir / guard.SEAL).exists())

    def test_changes_during_export_leave_no_seal(self):
        original_export = guard.core.export

        def interrupted_export(*args):
            original_export(*args)
            path = self.results / "aggregate-result.json"
            path.write_bytes(path.read_bytes() + b"\n")

        with patch.object(guard.core, "export", interrupted_export):
            with self.assertRaisesRegex(guard.IntegrityError, "changed during export"):
                self.export()
        self.assertFalse((self.review_dir / guard.SEAL).exists())
        self.assert_stops("seal is missing")

    def test_closed_rounds_are_read_only(self):
        self.export()
        self.add_outputs()
        for directory in (self.results, self.review_dir):
            for marker in ("CLOSURE.md", "CLOSURE.sha256"):
                with self.subTest(directory=directory, marker=marker):
                    path = directory / marker
                    path.write_text("closed", encoding="utf-8")
                    try:
                        guard.verify(self.results, self.review_dir)
                        self.assert_stops("round is closed")
                        with self.assertRaisesRegex(guard.IntegrityError, "round is closed"):
                            guard.audit_sample(self.results, self.review_dir)
                        with self.assertRaisesRegex(guard.IntegrityError, "round is closed"):
                            guard.export(self.results, self.review_dir)
                    finally:
                        path.unlink()

    def test_reviewer_transcript_is_required(self):
        self.export()
        self.add_outputs()
        (self.review_dir / "transcripts/alpha.stream.jsonl").unlink()
        self.assert_stops("transcript or output is missing")

    def test_reviewer_tools_mcp_and_success_are_checked(self):
        self.export()
        self.add_outputs()
        path = self.review_dir / "transcripts/alpha.stream.jsonl"
        original = path.read_text(encoding="utf-8")
        mutations = [
            lambda r: r[0].update(tools=["Read"]),
            lambda r: r[0].update(mcp_servers=[{"name": "external"}]),
            lambda r: r[0].pop("tools"),
            lambda r: r.insert(1, {"message": {"content": [{"type": "tool_use", "name": "Read"}]}}),
            lambda r: r.insert(1, {"message": {"content": [{"type": "server_tool_use"}]}}),
            lambda r: r[-1].update(is_error=True),
            lambda r: r[-1].update(subtype="error"),
            lambda r: r.append(r[-1].copy()),
            lambda r: r.pop(),
            lambda r: r[-1].update(result="unrelated review"),
        ]
        for n, mutate in enumerate(mutations):
            with self.subTest(mutation=n):
                records = [json.loads(line) for line in original.splitlines()]
                mutate(records)
                self.write_trace("alpha", records)
                self.assert_stops("reviewer|output differs")

    def test_invalid_judgments_still_fail_core_validation(self):
        self.export()
        self.add_outputs()
        output = self.review_dir / "outputs/alpha.jsonl"
        text = output.read_text(encoding="utf-8").replace(fixtures.QUOTE, "invented quote")
        output.write_text(text, encoding="utf-8")
        path = self.review_dir / "transcripts/alpha.stream.jsonl"
        records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        records[-1]["result"] = text
        self.write_trace("alpha", records)
        self.assertFalse(fixtures.quietly(guard.review, self.results, self.review_dir))
        self.assertFalse((self.review_dir / "blind-review-analysis.md").exists())

    def test_cli_verifies_and_fails_closed(self):
        self.export()
        cmd = [sys.executable, str(ROOT / "scripts/review_integrity.py"), "verify",
               str(self.results), str(self.review_dir)]
        self.assertEqual(0, subprocess.run(cmd, capture_output=True, text=True).returncode)
        (self.review_dir / guard.SEAL).write_text("broken JSON", encoding="utf-8")
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertIn("STOP:", result.stderr)


if __name__ == "__main__":
    unittest.main()
