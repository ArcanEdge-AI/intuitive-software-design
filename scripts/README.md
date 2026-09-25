# Evidence integrity for blind reviews

`review_integrity.py` is the current entry point for exporting, checking, sampling, and analyzing **new, separately authorized** blind reviews. It uses the frozen v1 scoring implementation without changing that historical snapshot. The direct `export`, `audit-sample`, and `review` commands in `evals-holdout/analysis/analyze.py` are historical interfaces and lack these guards; do not use them for new reviews.

The v1 evaluation round is closed. No improvement was demonstrated on its cases. This tooling correction does not reopen that round, authorize model calls, change any scores, or provide new evidence of plugin effectiveness.

## Contract

Before export, prepare an aggregate and preserve its run transcripts under `RESULTS/transcripts/<case>/<arm>-run<N>.trace.jsonl`, using the frozen `automated` helper only on a new, open result directory. Complete the planned provenance checks before export. Retained traces are evidence even after their original temporary sources have been removed. The exporter rejects conflicting copies when the original source still exists; it never deletes retained traces.

Export requires a new, empty review directory. It writes blinded packets and the arm key, then records SHA-256 hashes of:

- the complete aggregate, including prompts, rubrics, answers, scores, and verdicts;
- every expected retained run transcript, including excluded runs and explicit missing-file states;
- the exported packets and arm key.

The seal is `REVIEW/key/INPUTS.sha256.json`. Keep the entire `key/` directory private from blind reviewers. Before sampling or reporting, the tool requires that seal and checks all recorded identities. A missing file, added formerly missing trace, changed input, or unsupported seal stops the command. Old reviews cannot be retroactively sealed. Closure markers in either directory prevent report/export writes.

SHA-256 checks detect input drift; they are not a signature or protection against someone deliberately replacing both evidence and its seal. Do not edit inputs or run another writer concurrently with analysis. Preserve failed exports for investigation and use a new review directory after resolving the cause.

## Local commands

These commands do not call a model:

```bash
python scripts/review_integrity.py export RESULTS NEW_REVIEW
python scripts/review_integrity.py verify RESULTS NEW_REVIEW
python scripts/review_integrity.py audit-sample RESULTS NEW_REVIEW
python scripts/review_integrity.py review RESULTS NEW_REVIEW
```

`export` and `audit-sample` accept `--seed N`; their defaults match the frozen analysis plan. `verify` is read-only and checks exported inputs, not reviewer judgments. Exit codes are 0 for success, 1 for invalid judgments, and 2 for an integrity or stop-rule failure.

Before `review`, save each accepted reviewer output as `outputs/<case>.jsonl` and its selected Claude stream-json transcript as `transcripts/<case>.stream.jsonl` under the review directory. Keep other attempts separately. The transcript must contain exactly one system initialization with empty `tools` and `mcp_servers`, no tool-use blocks, and exactly one successful result whose text matches the output. The existing quote, completeness, duplicate, and eligibility checks then run before reporting. This check enforces the tool-free transcript prerequisite; it does not independently establish which packet the reviewer was given or replace a human audit.

## Free checks

```bash
python tests/test_review_integrity.py
python evals-holdout/analysis/test_analyze.py
python evals-holdout/analysis/analyze.py check evals-holdout --plugin-root .
```

The new tests use temporary synthetic evidence, including a changed automated verdict that the historical guard accepts. They check rejection before reporting, missing/changed input files, missing seals, reviewer tool calls, failed or mismatched reviewer results, and preservation after temporary-source cleanup. They do not touch saved evaluations or invoke models.
