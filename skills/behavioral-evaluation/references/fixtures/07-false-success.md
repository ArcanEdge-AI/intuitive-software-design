# Failed save — raw fixture

## Task

Review the supplied draft-save trace. Identify what the evidence establishes and what must be corrected. No live actions or implementation.

## Artifacts

- Authorized test trace: user changes title Old to New; activates Save; interface shows “Saved” and clears its dirty marker; network request returns HTTP 500; editor is closed and reopened; title reads Old.
- Source note: success toast and dirty-marker reset occur before the request resolves. Error handler logs the failure but displays no error.
- Other fields, concurrent edits, duplicate requests, and production incidence were not tested.
- The expected task is retaining the new title for later use. No observed human interpretation is supplied.
