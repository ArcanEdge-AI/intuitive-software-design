# Intuitive Software Audit Template

Use this template for a formal screen, workflow, or product audit. Remove sections that do not apply; never invent content to fill them.

# [Screen / Workflow / Product] Intuition Audit

## Evaluation frame

| Field | Value |
| --- | --- |
| Audit type | Screen / Workflow / Product |
| Task | |
| Intended user | |
| Relevant experience | |
| Starting point | |
| Success condition | |
| Risk/consequence | |
| Evidence reviewed | |
| Important exclusions | |
| Confidence | High / Medium / Low, with reason |

## Executive diagnosis

```text
Primary Weakness:
Major Friction:
Earliest Loop Break:
Critical Failures:
Highest-priority change:
```

## Evidence boundary

- **Observed:**
- **Inferred:**
- **Not evaluated:**
- **Evidence needed:**

## Critical Failures

Write `None confirmed in available evidence` when none are confirmed. Do not omit this section.

### CF-[number] — [name]

- **Evidence:**
- **Affected user/task:**
- **Consequence:**
- **Current recovery:**
- **Severity:** Critical / High / Medium / Low
- **Smallest complete correction:**
- **Validation:**

## Intuitive Software Loop

| Stage | Status | Evidence / break |
| --- | --- | --- |
| Orient — Where am I? | Pass / Friction / Broken / NE | |
| Recognize — What is this? | Pass / Friction / Broken / NE | |
| Predict — What will happen? | Pass / Friction / Broken / NE | |
| Act — Can I perform it? | Pass / Friction / Broken / NE | |
| Confirm — Did it work? | Pass / Friction / Broken / NE | |
| Continue — What next? | Pass / Friction / Broken / NE | |

## UI / Flow / Feel summary

| Area | Strengths to preserve | Friction | Evidence confidence |
| --- | --- | --- | --- |
| UI — understand what I see | | | |
| Flow — figure out what to do | | | |
| Feel — behavior matches expectation | | | |
| Cross-cutting | | | |

## Screen scorecard

Use only for an evaluated screen. Enter `NE` when evidence is insufficient.

| Criterion | Score 0–4 or NE | Evidence rationale |
| --- | ---: | --- |
| Orientation | | |
| Visual hierarchy | | |
| Action clarity | | |
| Control recognition | | |
| Information clarity | | |
| Feedback and state visibility | | |
| Cognitive load | | |
| Consistency | | |

```text
Evaluated criteria: __ / 8
Screen percentage: __ / 100 or NE
```

## Workflow scorecard

Use only for an evaluated end-to-end task.

| Criterion | Score 0–4 or NE | Evidence rationale |
| --- | ---: | --- |
| Entry-point clarity | | |
| Next-action clarity | | |
| Sequence matches user task | | |
| Context preservation | | |
| Decision load | | |
| Backtracking required | | |
| Progress visibility | | |
| Completion confidence | | |
| Error recovery | | |
| Prediction consistency | | |

```text
Evaluated criteria: __ / 10
Workflow percentage: __ / 100 or NE
```

## Product assessment

Use only with representative coverage.

For Behavior Confidence, record separate interaction-level outcome predictability, state feedback, cross-context consistency, and failure recovery evidence as defined in the scoring reference. Mark unobserved inputs `NE`; do not reuse UI or Flow scores.

| Dimension | Score / 100 or NE | Coverage | Rationale |
| --- | ---: | --- | --- |
| UI Clarity | | | |
| Flow Intuition | | | |
| Behavior Confidence | | | |
| Overall | | | |

## Prediction Gaps

| Interaction | Reasonable expectation | Actual behavior | Gap | Consequence | Evidence |
| --- | --- | --- | --- | --- | --- |
| | | | Small / Medium / Large | | |

## Decision Density

| Point in flow | Decisions required | Information available | Consequence | Keep / infer / default / defer / remove |
| --- | --- | --- | --- | --- |
| | | | | |

## Friction map

| Friction type | Evidence | Affected step | Severity | Underlying source |
| --- | --- | --- | --- | --- |
| Navigation | | | | |
| Interpretation | | | | |
| Decision | | | | |
| Interaction | | | | |
| Memory | | | | |
| Feedback | | | | |
| Recovery | | | | |
| Process | | | | |

## Findings

### [ID] — [specific finding]

- **Area:** UI / Flow / Feel / Cross-Cutting
- **Principle:**
- **Friction Type:**
- **Loop Break:** Orient / Recognize / Predict / Act / Confirm / Continue
- **Evidence:**
- **User Impact:**
- **Severity:** Critical / High / Medium / Low
- **Score:** criterion and 0–4, or NE
- **Recommendation:** smallest complete corrective change
- **Expected Outcome:** observable improvement
- **Validation:** test or evidence that would demonstrate improvement

## Prioritized improvement plan

| Priority | Change | Problems resolved | What remains unchanged | Validation |
| ---: | --- | --- | --- | --- |
| 1 | | | | |

## Strengths to preserve

-

## Residual risks and evidence gaps

-

## Acceptance checks

- [ ] Intended user and task are explicit.
- [ ] Observations and inferences are distinguishable.
- [ ] UI, Flow, and Feel are separate where evidence permits.
- [ ] `NE` is used instead of unsupported scores.
- [ ] Critical Failures are outside averages.
- [ ] Recommendations fix underlying friction with the smallest complete change.
- [ ] Accessibility evidence and gaps are stated.
- [ ] Every important recommendation has observable validation.
