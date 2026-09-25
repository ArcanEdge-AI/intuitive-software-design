---
description: Holdout v1, independently authored and not used to develop or tune the plugin. Scores are not comparable with the development cases in evals/.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---
I manage product for Cascade Files, a team file-storage tool, and I need help redesigning our plan-downgrade page. Right now the Team-to-Basic downgrade page shows nothing except the price change, and it's biting customers. Here's the situation.

**Current downgrade page copy:**
"Switch to Basic and save $8/month. [Confirm Downgrade]"
That is the entire page. No other text, no other screens.

**Retention policy (from our terms of service):**
- "Team plan: every saved version of every file is kept for 180 days from the date it was saved, after which it is deleted automatically."
- "Basic plan: every saved version of every file is kept for 30 days from the date it was saved, after which it is deleted automatically."
- "When an account moves from Team to Basic, the deletion job re-evaluates every file's version history immediately: any version older than 30 days is deleted within minutes of the downgrade being confirmed. This is the same automatic deletion job that normally runs on Basic accounts — the downgrade just makes it apply to versions that were previously within the Team plan's longer window."
- "Once the deletion job removes a version, there is no way for the customer to restore it themselves through the product — there's no undo and no version trash can. Whether our support team could ever recover something from internal backups, for a fee or otherwise, has never been documented, and nobody on the team is sure it's even possible."

**Support tickets, last 6 weeks:**
1. Ticket #8813 — "I downgraded to save money and didn't realize it would wipe three months of version history on our design files. We needed a version from 11 weeks back for a client dispute and it's just gone."
2. Ticket #8830 — "Downgraded my team account, found out two weeks later that an old version I needed had been deleted the moment I confirmed. Nothing on the downgrade screen mentioned this."
3. Ticket #8899 — "Same issue as others — we didn't even know 'version history' was something that could disappear."

**Analytics:** Of accounts that downgraded from Team to Basic last quarter, 12% opened a support ticket referencing lost or missing file versions within 30 days of the downgrade.

**Stakeholder note (from our support lead, in the ticket-triage doc):** "Honestly most people probably don't care about versions from months ago — they're mostly editing recent files. I don't think this needs much beyond a small tooltip."

**Stakeholder note (from our VP of Retention, same meeting):** "Given what this is costing us in tickets, what if we required people to schedule a callback with support before a downgrade takes effect, or added a 24-hour waiting period? That would cut down on complaints and give us a shot at saving the account."

**One more thing, unrelated:** we also got a couple of comments that the downgrade page doesn't show what happens to shared-folder permissions, but that's a different team's territory and out of scope here.

I want the downgrade experience redesigned — describe the flow and screens, not code.
