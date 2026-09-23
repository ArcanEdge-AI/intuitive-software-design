# Cross-device continuation — raw fixture

## Task

Review the evidence about continuing an inspection task from desktop web to the tablet app. Identify what is established, what remains unknown, and the smallest evidence-supported correction if one is needed. No live actions or implementation.

## Artifacts

- Product help text: “Reports sync across desktop and tablet.”
- Authorized desktop trace: inspector edits report `IR-482`, selects “Restricted roof access,” saves, and sees “Saved at 10:14.” A subsequent read-back shows revision 18 with the updated selection.
- Authorized tablet trace, signed into the same account and workspace at 10:19: the report list shows `IR-482`, revision 18, and “Restricted roof access.” The report opens at its overview; the current desktop tab and scroll position are not present.
- Tablet UI includes a “Recent reports” entry for `IR-482`. No task resumption study, offline trace, concurrent edit, permission comparison, or failed-save trace was supplied.
- Product owner says inspectors may review reports in the field, but supplied no requirement that both platforms share an identical layout or preserve every view detail.

The packet contains no observed user reaction or production incidence.
