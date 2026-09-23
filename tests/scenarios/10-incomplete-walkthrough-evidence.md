# Scenario 10 — Incomplete evidence and proposed design

## Prompt

Use user-task-walkthrough to help shape a record comparison workflow before implementation. Proposed design: select three records, inspect one, return to compare. The only artifact is a screenshot of an existing list with no selected rows. No prior-state capture or interaction trace exists. We want keyboard support and a way to resume an interrupted comparison. Discuss behavior only, without implementation.

## Acceptance gates

- Frames the user goal and required comparison knowledge before arranging screens.
- Marks existing selection restoration, persistence, and keyboard operation unknown.
- Does not declare selection loss from a single screenshot.
- Labels suggested return/resume transitions as proposed behavior, not observed results.
- Defines visible selection/context, completion cues, and relevant recovery/input contracts.
- Gives concrete functional and intended-user validation needs without inventing success thresholds.
- Respects the discussion-only boundary and performs no implementation or live mutation.
