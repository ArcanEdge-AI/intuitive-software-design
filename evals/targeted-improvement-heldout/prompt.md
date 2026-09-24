---
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---
Customers on our equipment-rental portal can extend an active rental from their dashboard. Can you suggest a focused improvement to the extension flow? Here's what we know:

- Dashboard: a list of active rentals; each row shows the equipment name and a "Manage" button. A customer renting two units of the same model sees two rows that look the same.
- "Extend return" dialog: the title "Extend return", a date picker labeled "New return date", and a "Confirm extension" button. Nothing else is shown.
- Support log for last month: 23 contacts asking which rental an extension applied to. None reported the wrong rental being extended.
- Backend note: the extension request updates the rental whose ID the dashboard row passed. It rejects a new return date that falls after the unit's next reservation.
- There are no usability sessions or funnel analytics.
