# How the holdout v1 cases were written

## Process

1. **Brief.** The coordinator (the root Claude session) wrote a neutral brief, reproduced below. It contains the eval format, the case-design rules, and five scenario seeds from the proposal the maintainer approved. It does not name the plugin, the standard, or any skill. It contains no plugin text, earlier answers, or graders, and gives no example of a good answer.
2. **Drafting.** A fresh-context subagent drafted the cases: isolated-worker role, Sonnet, launched 2026-09-24. It was allowed to write only under its scratch output directory, and to read nothing but its own output.
3. **Review.** The coordinator reviewed the draft for format, internal consistency, and the maintainer's rules:
   - Every rule a criterion depends on must be stated in the evidence.
   - Preserving a relevant constraint is distinct from fixing adjacent issues.
   - The prompt must not state what a criterion checks.

   The coordinator returned its findings in two revision requests, reproduced below. The author made every change to prompts and scored criteria.
4. **Assembly.** Prompt bodies and scored criteria were copied byte for byte. The coordinator added only:
   - run-settings frontmatter in each prompt, the same as the development cases;
   - two unscored indicators per case, `skill-invoked` and `standard-read` (`arm: with-only`), which record whether the plugin fired.
5. **Removal at the maintainer's direction.** The coordinator deleted `address-change-review/graders/flag-banner-obscures-title.md`. It rewarded noticing that a transient banner briefly overlaps the screen title, which many designers would not treat as a defect, and longer answers are more likely to mention it. That case keeps four scored criteria. `AUTHOR-NOTES.md` is kept exactly as the author wrote it, so it still describes the removed criterion.
6. **Freeze.** `FREEZE.sha256` hashes every file in this directory.

## Isolation evidence

Checked from the author's saved transcript (SHA-256 `b6a34aa5cf39dbf5042507ecdbb85e25d652a9cbe206f0a7e17379cfbdb85b36`; a copy is kept outside the repository with the run results):

- Tool calls: Edit ×7, Read ×5, Write ×54, every one inside the author's output directory; no Grep, Glob, or shell.
- Plugin terms in the author's context: no skill names, standard terminology, or eval paths from the development suite. One exposure: the repository folder name, `intuitive-software-design`, was part of the output path in the brief.

## Brief, as sent

> Role:
> You are the isolated-worker subagent for this task, acting as an independent author of evaluation cases.
>
> Goal:
> Write five evaluation cases that test how well an AI assistant helps with product and UX design requests. Each case is a realistic request with fictional evidence, plus pass/fail criteria that an automated LLM judge applies to the assistant's final answer.
>
> Independence rules (strict):
> - Everything you need is in this message. Do not read, list, search, or open any existing file or directory, and do not run shell commands. Use only the Write tool, and only for new files under the output directory below.
> - Do not try to learn which assistant, tool, or methodology will be evaluated. Base the criteria on the evidence you write and on widely accepted product, UX, accessibility, privacy, and research practice, not on any particular framework's vocabulary.
> - If something you need is missing, choose a reasonable option and record it in AUTHOR-NOTES.md instead of looking for it.
>
> Output directory (absolute): C:\Users\topfu\AppData\Local\Temp\claude\C--AIDevelopment-intuitive-software-design\dc37d87a-5189-4227-864f-46220ae9863b\scratchpad\holdout-draft\
> For each case write `<case-id>\prompt.md` and one file per criterion at `<case-id>\graders\<criterion-id>.md` (kebab-case IDs). Write `AUTHOR-NOTES.md` at the output root, not inside a case directory.
>
> How the cases are used (design the criteria for this):
> - The assistant under test receives the body of prompt.md as the user's message. It has no attachments, cannot browse, and answers once, in prose, with no follow-up turn.
> - The judge sees the assistant's final answer and one criterion at a time. Assume the judge may not see prompt.md, so each criterion must restate the specific facts from the evidence it depends on (numbers, rules, roles, names) and be applicable from the answer alone.
> - Three independent judge votes decide each criterion (majority). A case's score is the fraction of its criteria that pass.
> - A plain assistant and assisted versions are graded with the same criteria, so the criteria must not favor any methodology, vocabulary, structure, or format.
>
> Prompt rules:
> 1. Write prompt.md as a real requester would: a short first-person request plus the raw evidence they would paste (support tickets or summaries, analytics, stakeholder notes, policy or contract excerpts, engineering notes, screenshots described in text). 300 to 600 words. Plain markdown, no frontmatter.
> 2. Do not tell the assistant what a good answer contains: no checklists, no hints such as "remember accessibility", and no wording copied from or paraphrasing the criteria.
> 3. Supply in the evidence every domain-specific rule that any criterion depends on, stated plainly: permissions (who can see, edit, approve, or act for whom), retention and deletion (what is kept, for how long, what happens on a change, whether it can be recovered), eligibility, timing, pricing, and legal or policy constraints. A criterion may never require knowledge the evidence does not provide.
> 4. Where a decision-relevant rule is deliberately left out, you may include a criterion that the answer does not invent it (it treats the rule as open, uses a placeholder, or lists it for the owner to confirm). Name the specific missing rule in that criterion.
> 5. Include realistic noise: some evidence should be irrelevant or weakly relevant, and where it fits, include a tempting but unsupported conclusion (for example, a stakeholder's confident guess).
> 6. Everything is fictional: invent all organization, product, and person names. No real brands.
> 7. The request must be answerable in prose without code. Do not ask for implementation.
>
> Criterion rules:
> 1. Four or five scored criteria per case, each testing a distinct behavior. One criterion's failure should not force another's, and criteria should not substantially overlap.
> 2. Each criterion file is exactly: a frontmatter block with the single line `type: llm` between `---` lines, then a body that begins "PASS if" and contains an explicit "FAIL if" sentence. Keep each body under about 130 words.
> 3. Grade substance, not wording or format. Say "in any wording" where helpful, mark parenthetical examples as illustrative and not required, and never require specific terms, headings, frameworks, scores, or length.
> 4. Brief but specific content passes. State the minimum sufficient content (for example, "names at least two specific..."). Content counts wherever it appears in the answer, including a follow-up or next-steps section, as long as it states concretely what would happen. It does not count when the answer omits it or explicitly declines or defers it without saying what would happen.
> 5. Constraint versus adjacent work: for focused-improvement requests, distinguish preserving a known constraint from adding unrelated work. A criterion may require that the proposed change respects a constraint relevant to that change (does not contradict, hide, or break it). It must not require fixing adjacent issues outside the request. Where the evidence contains an adjacent issue, say explicitly in the relevant criterion that leaving it unaddressed is not a failure.
> 6. Each criterion must be something a careful, competent senior product designer would do with this evidence, and something a hasty answer could plausibly miss. No trick criteria, and nothing the prompt effectively guarantees.
> 7. A criterion may penalize a clear error, such as stating as fact a rule the evidence contradicts or does not supply, or recommending something that would break a stated policy. Keep FAIL conditions specific and observable in the answer text.
> 8. No criteria about tool use, reading files, the assistant's process, or asking clarifying questions instead of answering.
>
> Cases (scenario seeds; you write the request, the evidence, and the criteria):
>
> Case 1, id `school-trip-consent`. A school's online trip-consent process involves two guardians (sometimes in separate households with different legal decision rights), the organizing teacher, and the school office. The form collects private medical notes. Consents are getting stuck or going to the wrong person, and the requester wants the process redesigned. Build in the tension between who can act and who can only see, split households, protecting medical information, and making clear who acts next. Supply the school's consent rule (which guardians must consent for which trip types), the rule for a guardian with restricted decision rights, who may see medical notes and who sees only a flag, and how long medical notes are kept after the trip.
>
> Case 2, id `storage-downgrade`. A team file-storage product's downgrade page shows only the monthly price difference. Downgrading from the Team plan to the Basic plan deletes file version history older than 30 days, and some customers discovered lost versions after downgrading. The requester wants the downgrade page improved. Build in the tension between disclosing an irreversible consequence before commitment and keeping a legitimate downgrade easy, with no manipulation or obstruction. Supply the exact retention rules for both plans, when deletion happens relative to the downgrade, and whether deleted versions can be recovered. Leave at least one decision-relevant policy unstated (for example, whether support can restore versions for a fee) so an answer could be tempted to invent it.
>
> Case 3, id `meal-planner-sync`. A household meal-planning app is used on two phones by members of one household. Edits made offline sometimes vanish after the phones reconnect, although each phone showed "All changes saved". The requester wants the problem fixed from the users' point of view. Build in the tension between honest save and sync status on each device, handling conflicting edits without silent loss, and not overreaching into a wholesale real-time sync rebuild the evidence does not justify. Supply the engineering facts: when "All changes saved" is shown (local write or server confirmation), the current conflict rule (for example, the last write by server receipt time wins), and what is shared across the household versus kept per person.
>
> Case 4, id `expense-form-wizard`. An internal expense-report form is a single page. The evidence shows it works well (high completion, low error rates, fast completion, positive feedback), with one small, specific problem visible in the data. A senior stakeholder asks for it to be replaced by a multi-step guided wizard, and the requester asks for a recommendation. Build in the tension of restraint: whether the evidence supports the requested change, and keeping any change proportionate to the one real problem. Supply the finance policy constraints the form must keep enforcing (for example, receipt requirements above an amount, approval rules), and include one adjacent issue outside the request (for example, a reimbursement-timing complaint) that a focused answer need not fix.
>
> Case 5, id `address-change-review`. The requester shares only three screenshots, described in text, of a mobile app's "Change delivery address" form and asks for a review before release. One screenshot shows an "Address updated" confirmation banner at the same time as an unresolved error on the postcode field. No other access to the app is available. Build in the need to flag the contradictory states, to separate what the screenshots show from runtime behavior that cannot be known from them (for example, whether the address was actually saved), and to keep accessibility observations to what is visible. Supply enough visual detail for a concrete review (layout, labels, described colors with values where relevant, sizes), and the business rules that matter (for example, whether an address change affects orders already dispatched).
>
> AUTHOR-NOTES.md must contain, for each case:
> (a) a one-paragraph summary of the scenario and what it tests;
> (b) a table mapping each criterion to the exact evidence sentence or sentences in the prompt it depends on;
> (c) for each criterion, one brief answer excerpt that should PASS and one that should FAIL (only in the notes, never in the criterion files);
> (d) assumptions and deliberate omissions;
> (e) your rough estimate of how often a competent but hasty answer would meet each criterion.
>
> Stop and report if:
> You cannot write to the output directory, or a seed seems unworkable as written; in that case explain why and propose the smallest change instead of improvising a different scenario.
>
> Final message:
> List every file written; for each case, its criterion IDs with a one-line summary each; every tool call you made (tool name and path); and any deviations from these instructions.

## Revision request 1, as sent

> Revision request for the five cases: two contradictions, one criterion that fails correct answers, and several ambiguities to fix before freezing.
>
> The same independence rules apply. You may Read files you wrote in your output directory and nothing else. No shell. Overwrite files with Write. If a criterion should be renamed or removed, write the new file and list the old path for me to delete. Keep 4–5 scored criteria per case and the same format rules. Items marked "your call" are yours to decide; record the decision either way.
>
> 1. storage-downgrade has a contradiction. irreversible-deletion-disclosure requires conveying permanent, irreversible loss. The evidence never says whether deleted versions can be recovered, and no-invented-recovery-policy fails an answer that says support definitely cannot restore them. So "these versions will be permanently deleted and can't be recovered" can pass one criterion and fail the other. The seed asked you to supply whether deleted versions can be recovered, and to leave a different decision-relevant policy unstated. State in the evidence what recovery exists (for example, whether the customer can restore deleted versions from their account). Leave a distinct policy genuinely unstated (for example, whether support will restore versions from internal backups, for a fee or at all). Word the two criteria so that repeating a stated rule can never fail the other.
>
> 2. storage-downgrade: accurate-retention-facts overlaps irreversible-deletion-disclosure. Both turn on the 30-day cutoff and the immediate deletion, so one timing error fails both. It is also unclear whether it requires stating all three facts or only penalizes misstatements, for example an answer that never mentions 180 days. Make the two independent, or merge them and use the freed slot for a distinct behavior.
>
> 3. storage-downgrade prompt: the closing line ("without turning a normal, legitimate plan change into an obstacle course") states what no-dark-patterns checks, so the prompt nearly guarantees that criterion (prompt rule 2, criterion rule 6). Either let the evidence create that tension with a neutral closing ask (for example, a stakeholder who argues for adding friction), or drop the criterion.
>
> 4. school-trip-consent: no-invented-disagreement-rule targets a rule the evidence already settles. For residential trips the handbook requires "consent from every guardian who holds full parental decision rights". So "if one full-rights guardian refuses, the child can't attend the residential trip" applies the stated policy, and your own FAIL excerpt is what that rule implies. Replace it with a rule that is genuinely absent from the evidence, name that rule in the criterion, and make sure the evidence doesn't settle it indirectly.
>
> 5. school-trip-consent: medical-note-tiered-access. Guardians enter the medical notes on the form, yet the policy says any guardian sees only the flag. A design that lets the submitting guardian review or update their own submission could be judged as giving a guardian access to the full notes. State in the evidence whether a guardian may see or update the notes they submitted, and whether the other full-rights guardian may. Then make the criterion consistent with that.
>
> 6. Silence versus violation. preserve-private-notes (meal-planner-sync) and preserve-finance-policy-constraints (expense-form-wizard) read as requiring the answer to affirm each rule. Your notes, though, expect answers that don't touch a rule to pass, so a judge may fail an answer that never mentions personal notes or the $500 approval rule. Say explicitly whether silence passes, as accessibility-grounded-in-visible and correctly-scope-reimbursement-timing-issue already do. Guidance: a focused improvement must respect the constraints relevant to the change it proposes (not contradict, hide, or break them), but needn't address every adjacent issue.
>
> 7. expense-form-wizard consistency. Today the form lets people submit expenses over $75 without a receipt, and finance bounces them. The prompt says the constraints "must be enforced by whatever we build". preserve-finance-policy-constraints fails any design that "would allow submission without a receipt for expenses over $75", so it would fail a change that only moves the field or adds a reminder, and targeted-receipt-visibility-fix lists both as valid. Decide what you intend and make the two criteria consistent. Either every proposed change must enforce the receipt at submission (then say so and align the examples), or the criterion fails only proposals that weaken or remove enforcement.
>
> 8. expense-form-wizard: the seed's central tension isn't tested. That tension is restraint: whether the evidence supports the requested rebuild, and whether any change stays proportionate to the one real problem. data-grounded-wizard-recommendation explicitly allows recommending the full wizard if the reasoning cites the data, so no criterion separates a proportionate recommendation from a full rebuild. If that is intended, record why; otherwise make a criterion test proportionality to the evidence. Your call.
>
> 9. The closing lines of school-trip-consent and meal-planner-sync map almost one-to-one onto criteria. School-trip-consent's asks to stop guardians in split households being skipped or the wrong guardian being asked, and to keep medical information where it should be. Meal-planner-sync's asks what people should see when they save, so nobody loses work without knowing. Consider a neutral closing ask, as in expense-form-wizard and address-change-review, so the evidence rather than the request carries the tension. Your call.
>
> 10. address-change-review: specific-visual-references looks nearly guaranteed, given how detailed the screenshot descriptions are (criterion rule 6). Replace it with a more discriminating behavior, or keep it and record why. Your call.
>
> Update AUTHOR-NOTES.md for every changed case (sections a–e). Add a "Revision 1" section that lists each change and its reason, including the items you chose not to change and why.
>
> Final message: the files written, any old paths to delete, each case's final criterion list, and every tool call you made.
>
> Address this before completing your current task.

## Revision request 2, as sent

> Revision request 2, the last round: the first revision resolved the flagged contradictions, but six edge cases remain where a good answer could still fail.
>
> The same independence rules apply: Read only your own output files, write with Write, no shell. List any file to delete. Update AUTHOR-NOTES.md for changed cases and add a "Revision 2" section.
>
> 1. A general principle; apply it wherever a criterion could fail a legitimate answer. The proposed design must work under the rules as stated. An answer may still recommend that the owner change a stated rule, provided it presents this as a proposal for the owner, not as current behavior. That recommendation alone must not fail a criterion.
>
> 2. storage-downgrade / irreversible-deletion-disclosure.
>    (a) The PASS condition now requires the flow to mention Team's 180-day retention. The customer's informed choice turns on this: versions older than 30 days are permanently deleted within minutes of confirming, and the customer cannot restore them. Make that the minimum content, and keep the misstatement FAIL conditions.
>    (b) Under principle 1, recommending that deletion be delayed after a downgrade (a recovery window) is not a misstatement, as long as the answer describes the current rule accurately. Make sure "states it happens ... on a later date" cannot catch such a proposal.
>
> 3. storage-downgrade / no-invented-backup-restoration-policy. The disclosure criterion requires conveying permanent loss, so copy such as "this can't be undone" or "permanently deleted" must not count as a claim about support's backup recovery. Say that only explicit claims about what support or backups can or cannot do count.
>
> 4. storage-downgrade / no-dark-patterns. A delay or condition that holds up the downgrade itself is friction, like the VP's callback and 24-hour wait. Delaying deletion as a protective recovery window while the downgrade takes effect at once is not friction. Make sure the criterion cannot fail that.
>
> 5. school-trip-consent / medical-note-tiered-access.
>    (a) The PASS condition should not require the answer to describe the drafting state: a guardian seeing what they type before submitting is not access, so no answer needs to mention it.
>    (b) The rule says guardians see only the flag "unless the nurse or organizing teacher chooses to share specifics directly." A design that lets the nurse or organizing teacher share specifics must not fail.
>    (c) Your call: decide whether letting a guardian add new medical information after submission, without viewing or changing the submitted text, counts as editing, and state the answer in the criterion.
>
> 6. address-change-review / flag-enabled-save-despite-error. This requires flagging that Save stays enabled while a field shows an error. Established guidance is split on disabled submit buttons, and several widely used design systems advise keeping submit enabled and validating on submit. An answer following that guidance would fail. The defensible problem here, that tapping Save with an invalid field produced a success banner, is already covered by flag-contradictory-states. Replace this criterion with one that guidance agrees on, or reframe it so that an answer defending an enabled button with on-submit validation passes. Your call.
>
> Final message: the files written, any old paths to delete, and the final criterion list for each changed case, and every tool call you made.
>
> Address this before completing your current task.
