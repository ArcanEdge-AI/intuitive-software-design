---
description: Holdout v1, independently authored and not used to develop or tune the plugin. Scores are not comparable with the development cases in evals/.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---
I manage internal tools at Northgate Corp, and our VP of Finance Ops wants me to replace our expense-report form with a multi-step wizard. Before I commit budget to a rebuild, I want a second opinion. Here's what we know.

**Current form:** a single page — category dropdown, amount field, description field, receipt upload, submit button. That's it.

**Usage data, last quarter (around 2,400 submissions):**
- Completion rate: 96% of people who start the form finish it.
- Field-level error rate: 2% of submissions have any validation error before successful submit.
- Average time to complete: 4 minutes.
- Quarterly employee survey comments (sample): "quick, I can do it between meetings," "way better than our old system," "wish more of our tools were this simple." 88% said they were satisfied or very satisfied with the form.

**The one issue we did find in the data:** of expenses submitted over $75 (which require a receipt under finance policy), 14% are submitted with no receipt attached and get bounced back by finance for correction, adding a day or more to reimbursement. The receipt-upload field sits below the fold on smaller phone screens and isn't visually tied to the $75 threshold anywhere on the form.

**Finance policy constraints (must be enforced by whatever we build):**
- "Any expense over $75 requires an itemized receipt to be attached before submission."
- "Any expense over $500 requires manager approval before it is paid; expenses at or under $500 that meet policy are approved automatically."

**VP note, from her email:** "I really think we should move to a modern multi-step guided wizard, like the big travel booking apps — split it into category, amount, receipt, then review. It'll feel more premium and guide people better."

**One more complaint that came up in the same survey, unrelated to the form itself:** several people wrote that reimbursements take about 3 weeks to actually hit their bank account after approval, which they find frustrating. That's a payments/finance-ops timing issue, not something about the form.

What would you recommend? I want a straight recommendation, not a mockup.
