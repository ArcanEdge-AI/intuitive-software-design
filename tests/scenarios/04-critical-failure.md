# Scenario 4 — Critical Failure

## Prompt

Audit a binding proposal-send step for an estimator. The `Send` button remains unchanged after activation. Sometimes the proposal sends and sometimes it fails, but the user is always returned to the estimate list. There is no sent status, recipient record, error, retry, or draft recovery. Other screen criteria average 3.5/4.

## Acceptance gates

- Flags the important missing confirmation and recovery as an Intuition Critical Failure candidate, independently of the high numerical average.
- States evidence, affected user/task, consequence, severity, and current recovery.
- Identifies Feedback and Recovery friction plus Confirm/Continue Loop failure.
- Does not allow the 3.5 average to hide the issue.
- Recommends a smallest complete pending/success/failure/retry state contract.
