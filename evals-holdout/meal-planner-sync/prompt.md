---
description: Holdout v1, independently authored and not used to develop or tune the plugin. Scores are not comparable with the development cases in evals/.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---
My partner and I share a household meal-planning app called Kitchpal on our two phones, and edits keep vanishing. I want this looked at from a normal user's point of view, not as a technical spec. Here's everything I know, including what our engineering team told me when I pushed on it.

**What we (the users) saw:**
- Mara's phone: added "Thursday: lentil soup" while on the train with no signal. The app showed "All changes saved" right after she typed it.
- Jonas's phone: added "Thursday: tacos" that same evening at home, also saw "All changes saved."
- Both phones reconnected to wifi later that night. The next morning, only "tacos" was on the shared plan. Mara's soup entry was gone — no error, no notification, nothing.

**Support tickets from other households, last month:**
1. Ticket #2210 — "Added three items on the bus, it said saved, they're just gone now."
2. Ticket #2244 — "My roommate and I both edited the shopping list while one of us had no signal. When we reconnected, half my edits disappeared without any warning."

**Analytics:** 9% of households with two or more active devices report at least one instance per month of an edit that was shown as saved but is missing later.

**What engineering told me when I asked:**
- "'All changes saved' is displayed as soon as the edit is written to the phone's local storage. It does not mean the edit has reached the server or the other household member's phone."
- "When two devices reconnect after being offline, and both have edits to the shared meal plan, the system currently keeps whichever edit reaches our server last (by server receipt time) and discards the other edit entirely — there's no merge and no notice to either person."
- "The weekly meal plan and the shared shopping list are synced across every device in the household. Personal notes attached to a recipe, like 'don't buy the discount brand,' are intentionally kept per-person and never synced to the other person's phone — that's by design, not a bug."

**A note from our engineering lead when I raised this:** "My guess is this is mostly a network issue — people are on flaky wifi or subway signal. If we just tell users to make sure they're on solid wifi before editing, most of these reports should go away."

Given all this, how would you redesign the way saving and syncing works here? Please describe it for the screen, not as a technical spec.
