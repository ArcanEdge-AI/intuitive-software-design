---
description: Version 2 of targeted-improvement-heldout. Adds evidence that a rental can change while the extension dialog is open. Scores are not comparable with version 1 runs.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---
Customers on our equipment-rental portal can extend an active rental from their dashboard. Can you suggest a focused improvement to the extension flow? Here's what we know:

- Dashboard: a list of active rentals; each row shows the equipment name and a "Manage" button. A customer renting two units of the same model sees two rows that look the same.
- "Extend return" dialog: the title "Extend return", a date picker labeled "New return date", and a "Confirm extension" button. Nothing else is shown.
- Support log for last month: 23 contacts asking which rental an extension applied to. None reported the wrong rental being extended.
- Backend note: the extension request updates the rental whose ID the dashboard row passed. It rejects a new return date that falls after the unit's next reservation.
- Account note: business accounts can have several authorized users, and an open "Extend return" dialog does not refresh. Last month two customers confirmed an extension for a rental that a colleague had already returned; both saw only "Something went wrong."
- There are no usability sessions or funnel analytics.
