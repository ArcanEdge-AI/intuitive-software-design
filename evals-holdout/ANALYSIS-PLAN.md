# Holdout suite v1: analysis plan

Written and frozen before any run. Nothing in this plan may change after the run starts; a later change creates a new version.

## Question

Does the plugin improve answers to design requests it was not developed against? The five cases in this directory test situations, skills, and failure modes that were not used to develop or tune the plugin. The plugin under test is commit `43f042d`, unchanged.

## Frozen inputs

- Case prompts and scored criteria, written by an independent author who saw no plugin instructions, earlier answers, or graders; see `AUTHORING.md`. At the maintainer's direction, one criterion (`address-change-review/flag-banner-obscures-title`) was removed before freezing, leaving 24 scored criteria.
- Run settings in each prompt's frontmatter (`max_turns: 15`, `allowed_tools: [Read, Glob, Grep, Skill]`), the same as the development cases.
- Unscored indicators (`skill-invoked`, `standard-read`) that record whether the plugin fired. The coordinator added both the run settings and the indicators, and neither affects a score.
- This plan, `analysis/analyze.py`, its regression checks in `analysis/test_analyze.py`, and `analysis/REVIEWER-PROMPT.md`.
- `FREEZE.sha256`, which lists the SHA-256 of every file above.

The run proceeds only if all three of these pass, run from the repository root:

- `python evals-holdout/analysis/analyze.py check evals-holdout --plugin-root .`, with every hash matching;
- `python evals-holdout/analysis/test_analyze.py`;
- `git diff --quiet 43f042d HEAD -- . ":(exclude)evals-holdout"`, which confirms that the plugin files are unchanged.

## Run (only after approval)

```text
claude plugin eval . --eval-dir evals-holdout --ablation with-without --no-publish --keep-temp --trust-plugin
  --model claude-sonnet-5 --judge-model sonnet --runs 3 --max-cost-usd 9
  --output-dir evals/results/<timestamp>-holdout-v1-43f042d
```

This makes 5 cases × 3 runs × 2 arms, or 30 agent runs. Each LLM criterion gets three judge votes, and the majority decides. The results directory is already gitignored.

## Eligibility, decided once before any score is read

`analyze.py automated` preserves the transcripts, with SHA-256 hashes, and decides which runs are eligible. It records the decision in `eligibility.json`. Every later step recomputes the same decision from the same inputs and uses only those runs: automated scoring, the reviewer export, blind-review scoring, and the audit sample. The export records the eligible runs in its key, and review refuses to run if they have changed.

A run is excluded, and listed with its reasons, when any of these holds:

1. It ended with an error, or its paid graders were skipped.
2. Its transcript is missing, so leakage cannot be checked.
3. A tool call or tool result in its transcript refers to a file or folder in `evals-holdout/`. The reference counts whether it is a relative path, a `./` path, an absolute path, or the folder name given as a path or glob.

**Stop rule.** If more than one run is excluded in any case and arm, or none remains, the tooling stops. `automated` reports the exclusions and no scores, and `export`, `audit-sample`, and `review` refuse to run. A rerun needs approval.

## Automated results (primary, never edited)

- For each case, the score of a run is the fraction of its scored criteria that pass. Report the mean with and without the plugin, and the difference.
- Pooled result: the mean over cases of the per-case differences, so each case counts equally. The 90% interval comes from a stratified bootstrap that resamples runs within each case and arm (10,000 iterations, seed 7).
- Report the criterion-level pass counts for each arm, so a pooled result driven by one or two criteria is visible. From the transcripts, also report which skills fired and whether the standard was read.
- Interpretation:
  - The result is **improvement detected** only if the pooled interval is above 0 under both the automated scores and the blind-review scores.
  - If it is above 0 under only one of them, the result is **inconclusive (depends on grading)**.
  - If the interval includes 0, the result is **no clear difference detected**.
  - If the interval is below 0, the result is **worse**.
- Per-case results are descriptive only, because three runs per arm cannot support per-case claims. A case where both arms average at least 0.9, or both at most 0.1, is labeled non-discriminating. It stays in the pooled analysis.
- Power: with three runs per arm, only pooled differences of roughly 0.2 or more are likely to be detected. A smaller real effect may go undetected.

## Independent blind review (separate from the automated results)

- **Scope.** Every scored LLM judgment for the eligible runs, whether the judge passed or failed it. With all 30 runs eligible, that is 144 judgments: 24 criteria × 6 answers.
- **Blinding.**
  - `analyze.py export` extracts each eligible final answer and applies the same identity redactions to every answer in both arms: plugin and skill names, reference file names, section symbols, and file paths.
  - It shuffles the answers within each case (seed 20260924), gives them opaque IDs, and writes the key to a separate file.
  - Reviewers never see the arm, the judge's votes, the other reviewers' verdicts, or the key.
  - Style and length can still hint at the arm. Reviewers are not told that arms exist.
- **Reviewers.**
  - There is one fresh-context reviewer per case, five in total, on the senior-reviewer route (Sonnet, high effort).
  - Each reviewer gets only `analysis/REVIEWER-PROMPT.md` and its case packet, which holds the request, the criteria, and the shuffled answers. It uses no tools.
  - The reviewer splits each criterion into required content and prohibited claims:
    - Each applicable required element needs a verbatim quote.
    - A conditional element whose situation does not arise, or one the criterion says silence satisfies, is marked not applicable.
    - A prohibited claim fails an answer only when the reviewer quotes it; silence never triggers one.
    - The verdict must follow from that evidence.
  - Its final message is saved verbatim. Its transcript is checked to confirm it made no tool calls.
  - At most one retry per case, and only for output that fails validation.
- **Validation before conclusions.** `analyze.py review` checks every output before reporting anything. It flags:
  - verdicts other than PASS or FAIL;
  - duplicate, missing, or unknown judgments;
  - unparseable lines, or text outside the JSON lines;
  - a closing line that is missing or has the wrong count;
  - quotes that do not appear in the answer;
  - verdicts that contradict their own evidence;
  - problems the reviewer reports.

  If anything is flagged, it writes `blind-review-validation.md` and no conclusions.
- **Scoring.**
  - `analyze.py review` recomputes the case and pooled results from the blind verdicts, using the same bootstrap.
  - It reports agreement with the judge for each arm: both passed, both failed, judge passed but review failed, and judge failed but review passed.
  - It lists every disagreement with the reviewer's evidence.
- **Manual audit.**
  - A person grades a predefined sample of 30 judgments without knowing the arm or either earlier verdict.
  - The sample draws 15 judgments the judge passed and 15 it failed, across cases and arms, with seed 20260925 (all of one kind if fewer exist).
  - Entries other than PASS, FAIL, or blank are flagged, and the audit comparison is withheld until they are corrected.
  - The audit estimates how often the judge and the blind reviewer are wrong. It overrides neither.
- **Separation.**
  - Automated results stay in `aggregate-result.json`, `eligibility.json`, and `automated-analysis.md`.
  - The blind review and the audit live in a separate `<run>-blind-review/` directory.
  - Reports show the three side by side and never merge them.

## What will not happen

- No criterion is edited or dropped after the run. A criterion that proves ambiguous is reported and fixed in a v2 for future runs; v1 results stand.
- No plugin edits based on these outputs until the write-up is delivered. After any later plugin change, these cases no longer count as held out for that change.
- No additional runs without approval.
