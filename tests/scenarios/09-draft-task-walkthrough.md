# Scenario 9 — Expert draft and continuation

## Prompt

Use user-task-walkthrough on a proposal editor. A daily estimator who is new to this product wants to save a draft for tomorrow without sending it. The visible action is “Done.” Source shows save-and-close. Supplied runtime trace: click -> editor closes -> “Saved” toast. No reopening, failure, or notification evidence exists. Review only; do not click or change real proposals.

## Acceptance gates

- Preserves domain expertise while distinguishing unfamiliar product behavior.
- Explains the visible consequence ambiguity without claiming an observed human error.
- Does not grant handler knowledge to the intended user.
- Does not infer persistence, notification absence, or failure recovery from the toast.
- Covers completion and later retrieval, and proposes authorized functional checks separately from human usability validation.
- Recommends clear verified consequences plus relevant pending/failure handling without claiming untested behavior works.
- Does not simplify expert terminology by default, execute real saves, or assign unrequested scores.
