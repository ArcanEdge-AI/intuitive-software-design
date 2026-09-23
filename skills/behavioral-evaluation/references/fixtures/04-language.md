# Keep a draft — raw fixture

## Task

Review the proposal editor for an experienced estimator who is new to this product and wants to keep edits for tomorrow without sending them. Do not modify a proposal.

## Artifacts

- Editor screenshot transcription: Proposal fields, recipient details, action “Done.” No separate save/send explanation appears in the capture.
- Source note: Done calls saveDraft and closes the editor on success. Downstream notification behavior was not inspected.
- Runtime trace from a test account: click Done, “Saved” toast, editor closes. No reopen or failure trace is supplied.
- No observed human choice or confusion is supplied.
