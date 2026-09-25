---
description: Holdout v1, independently authored and not used to develop or tune the plugin. Scores are not comparable with the development cases in evals/.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---
I run the trips office at Bramholt Primary School and our online trip-consent process is falling apart. Parents are missing deadlines, forms are going to the wrong parent, and I'm worried we're going to send a coachful of kids on a residential trip without proper consent. Can you help me redesign how consent, visibility, and medical information flow through this process? Here's what I'm working with.

**Our consent policy (from the parent handbook):**
- "For day trips (single-day, no overnight stay), consent from one guardian who holds full parental decision rights is sufficient to enrol a child."
- "For residential trips (any trip involving an overnight stay), consent from every guardian who holds full parental decision rights is required before a child may attend."
- "Where a student's record notes that a guardian has restricted decision rights (for example, following a court order), that guardian is not counted toward the required consent and their agreement or refusal has no effect on whether the child may attend. However, restricted-rights guardians must still receive all trip information and be able to view the medical-considerations flag, since they may have caregiving responsibility on scheduled days."

**Medical information rule:**
- "Only the school nurse and the trip's organizing teacher may view a student's full medical notes. All other staff, and any guardian, see only a yes/no 'medical considerations' flag, without detail, unless the nurse or organizing teacher chooses to share specifics directly."
- "A guardian filling in the medical-notes field on the consent form can see and edit exactly what they type while completing the form. Once the form is submitted, that guardian loses the ability to view or edit the full note text — from that point on, only the nurse and the organizing teacher can see the full text. Every guardian, including whichever one originally wrote the notes, sees only the yes/no flag after submission."
- "Full medical notes are permanently deleted 90 days after the trip's return date. The medical-considerations flag itself remains on the student's general record for the school year."

**Support tickets from the last two months:**
1. Ticket #4021 — Residential Year 6 trip. Dad consented online, but Mum (separate household, full rights) never got an email because the system only has one "primary contact" field and it had Dad's address in it. The trip nearly went ahead without her consent.
2. Ticket #4058 — Day trip. The system sent the consent request to the birth father, who has restricted rights under a custody order, and he "consented" — but Mum, who holds full rights, was never asked. We only caught it because she called the office confused about why she hadn't received anything.
3. Ticket #4102 — Residential trip. One guardian consented three days after the other, and the office couldn't tell whether the trip was "go" until someone manually checked both records — the parent-facing status page still said "Pending" even after the second consent came in overnight.

**Stakeholder note (from our IT lead, quoted at the planning meeting):**
"Honestly, I think this is mostly because parents don't check their email. If we just add SMS text reminders on top of the current form, most of this will sort itself out."

**Other info, probably not relevant:** Trip insurance costs the school roughly £3.40 per student for day trips, which comes out of the general trips budget — just flagging it since it's on the same form, not something I need help with.

Given all of this, can you help me redesign the process — the flow and how information is shown, not code?
