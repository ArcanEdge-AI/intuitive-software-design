---
description: Holdout v1, independently authored and not used to develop or tune the plugin. Scores are not comparable with the development cases in evals/.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---
I'm the only product person on a two-person team shipping a delivery app called Parcelly, and I need a pre-release review of our "Change delivery address" screen. I don't have access to the running app right now — just three screenshots from our designer, which I'll describe to you exactly as they look. No other access is available.

**Screenshot 1 — the form, default state:**
White background. Top: a dark grey back arrow (top-left) and the title "Change delivery address" in bold, centered, black text, roughly 18pt. Below that, three stacked input fields, each with a grey label above it and grey placeholder text inside: "Street address," "City," "Postcode." Fields have thin grey 1px borders, rounded corners, white fill. Below the fields, a full-width button, solid blue (roughly #1A73E8), white bold text "Save," positioned near the bottom of the screen with about 24px of space above it. No helper text anywhere explaining which orders the change will affect.

**Screenshot 2 — after typing an invalid postcode:**
Same layout. The "Postcode" field now has a red outline (roughly #E0261E) instead of grey. Directly below the field, small red text — noticeably smaller than the field labels — reads "Postcode not recognized." The blue "Save" button below is still shown in its normal solid-blue, fully-enabled appearance; nothing about it looks disabled or different.

**Screenshot 3 — described by our designer as "right after tapping Save":**
A green rectangular banner has appeared at the very top of the screen, overlapping the title, with white bold text reading "Address updated." Below the banner, the same "Postcode" field is still visible with its red outline and the "Postcode not recognized" text still showing underneath it, unchanged from screenshot 2. The designer's note says the banner "auto-dismisses after about 3 seconds," but we only have this still frame, not a recording.

**Relevant business rule (from our fulfillment policy doc):** "Once an order's status changes to 'Dispatched,' its delivery address is locked. A customer can no longer change the address for that order through the app; they must contact support, and support can only redirect the parcel if the courier hasn't yet attempted the first delivery." The form itself doesn't currently say anything about this on-screen.

**One more note, probably not important:** the designer mentioned the button was originally going to be green to match our brand palette, but they switched it to blue last week for "better contrast" — just background, not something I'm asking you to weigh in on.

Given just these three screenshots and the fulfillment rule above, what would you flag before we release this screen?
