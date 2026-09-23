# Scenario 2 — Workflow Audit

## Prompt

Audit this workflow for an occasional estimator: Dashboard -> New Estimate -> choose project type, subtype, billing method, labor model, markup, tax profile, location profile, crew type -> Save -> dashboard. The next Scope step requires re-opening the estimate and re-entering customer type. Save provides only a two-second toast. Evaluate context loss, unnecessary steps, Prediction Gap, Decision Density, friction types, and Intuitive Software Loop failures.

## Acceptance gates

- Classifies the request as AUDIT and establishes user/task/success/evidence.
- Identifies context loss and avoidable re-entry.
- Analyzes Decision Density rather than calling the screen merely busy.
- Names applicable Memory, Decision, Process, Feedback, or Navigation friction.
- Locates Intuitive Software Loop breaks, including weak Confirm/Continue.
- Scores only supported workflow criteria and keeps evidence gaps explicit.
