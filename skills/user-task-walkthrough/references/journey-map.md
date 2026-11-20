# Interactive journey map

Use the walkthrough to trace a consequential goal from realistic starting points to recognizable outcomes. A map can use a live interface, current source and tests, a prototype, screenshots, or a specification. Tie it to the environment and version its evidence covers.

For a workflow that changes hands, follow [Multi-Role Workflow](../../multi-role-workflow/SKILL.md). Identify whose action is pending, what they can see or change, and which saved item the next person receives.

## Map a proposed journey

Start from the idea's stated job, intended users, and constraints. Propose a plausible entry, meaningful decisions and handoffs, a recognizable outcome, and an alternate route for a consequential problem such as interruption, rejection, or unavailable work. Use a labeled branch and an ordered Coverage scenario for supported design alternatives or recovery. Use `basis: "proposed"` for candidate steps and label proposed cues, locations, system effects, and actor responsibilities as design hypotheses. Cite the brief for requirements it actually establishes.

Anchor assumptions that could change the design in Coverage. Each should say what would happen if the assumption is wrong and how to check it with an intended user, a prototype, or a policy owner. Leave unknown business rules undecided. Use two materially different proposed options for consequential decisions without a current workflow. Review the outline against the brief and the proposed rules, and cite each according to its status when reviewed rendering applies.

## Outline the routes before writing steps

Work outward from the goal and starting states. At each material decision, trace the available choice, the condition checked after the attempt, the resulting state, and the next supported checkpoint. Compare implementation, tests, and documentation and preserve consequential differences. Include role restrictions, waiting, unsuccessful outcomes, and recovery where they change what the person can do.

Record consequential alternatives in the [source outline](#check-a-separately-derived-source-outline) before creating `journey.json`. In the map, give each distinct success, rejection, and recovery path its own Coverage scenario with `path: true` and consecutive step IDs. Include each branch's trigger and first shared or terminal checkpoint. Keep a topic with separate, unconnected checkpoints as an ordinary scenario.

For example, a renewal copies eligible items into a draft and resumes at editing before returning to review. Outline one route from attempt to copied edit to review. If the copy rejects empty or ineligible items, outline a separate route from attempt to rejection. The attempt must reach that outcome even when the next action after rejection is unknown.

Keep every documented continuation reachable under its prerequisite, even if the preceding actor, location, or receipt is unknown. When the action creates a new record, mark the successful edge with `nextCreates` or `creates`, and give the new record its own receiving checkpoint. Use the same new-record label as the receiving checkpoint's `record`. Join a shared route when its actor, authority, and prerequisites apply. Mark a checkpoint with `continuationUnknown: true` and anchor the gap when the sources end at a supported outcome but leave the next action open. Documented closure needs no such marker.

Distinguish one item's outcome from the state of the work as a whole. When routing depends on other items or earlier decisions, state the aggregate prerequisite on the edge that depends on it. If the other items' states are unknown, show the known item result without assuming the aggregate state. For example, rejection of one item does not establish that no other item was accepted.

After each recovery transition, check the resulting state, who can act, and which choices are available again. Give each consequential restored choice a navigable transition from that state, even when it appears elsewhere in the map. Reuse the existing checkpoint when its choices and conditions still apply. When recovery changes a deadline, rule, or owner, use conditions or a distinct checkpoint so the restored choices carry the correct rules.

Verify where a person sees a status, which actions are available from that state, and where they can take each action. These are separate claims. A source can establish a status display or a permission without locating a control. For example, when an activity list shows that an export is ready, set its `statusLocation` to the activity list. If the sources do not locate the download action, set its `actionLocation` to `null`. Add a step-level gap when finding it matters.

Extract locations from the evidence before writing or reviewing the map. For each status, action, or alternate control, identify the actor, the named surface on which it appears, and the source span that connects them. A record name or a control label such as “Resubmit” can establish the object or action while leaving its surface unknown. Copy a status location into an action location only when the action is shown or explicitly placed there. When a separate evidence review is available, give the reviewer the original sources and scope before showing them the draft. Use their findings in the source outline, including explicit `null` values for unsupported locations.

Read each checkpoint's status location, action location, and outgoing choices together. Use a branch's own `actionLocation` for an alternate action. Keep distinct actions on separate checkpoints when their locations or outcomes would otherwise be unclear.

When supplied measurements show how people choose, use [Journey Analytics](../../journey-analytics/SKILL.md) to interpret them. A representative cohort can inform the primary walkthrough. Keep important low-frequency or unmeasured paths reachable.

## Trace conditional transitions

When a full journey has conditional outcomes or assignment modes, start the source review by listing the in-scope controls that assign, return, or transfer work, including alternatives that create or copy a record. Take each through both passes before writing steps or constructing Coverage. Use one short working note per operation and mode with the decisive spans for the saved result and the receiver's next action.

1. **Outcomes.** Follow each operation from control and eligibility to saved result and next action. For a filtered operation, identify which source records survive each filter or join for every supported record variant. Check zero selected rows even when source records exist, then check the prerequisites for each selected row. Record rejections, recovery actions, and the difference between saving and advancing. Check whether the whole task can advance as well as what happens to each item.
2. **People and locations.** Follow the assignment saved on the resulting record to a permission check or witnessed action. When permission allows several assignment types, check which of those assignments this operation actually saves. Check status, acknowledgment, and action location from the receiving side. Record independently assigned roles even when their first action is unknown.

Work through one representative stored row for each input mode before writing its route condition. Carry the stored keys, including null keys, through the selection and join. Name any mode that produces zero eligible rows and tell it apart from a matched row that fails a later check.

For a created or copied record, trace who can create it, who can open it from the result, and who can do the next work on it. Follow a confirmation link to the destination's access checks. Establish the next actor from a permission check, witnessed action, or explicit assignment rule for that record and mode before citing it in `actorSources`. Give different actors separate steps. When saving the record makes the next work available, branch from the saved outcome so the receiver's route can start there. Leave an unknown actor or control unspecified and attach the evidence gap to the handoff.

When a supplied excerpt stops at the control, a help string, or a role summary, locate the deciding implementation or test before resolving the next step. In an authorized pinned Git repository, start with `git grep -n -F -e '<operation identifier>' <revision> -- <in-scope paths>` and open the relevant match at that revision. Use the operation or handler identifier passed by the control where possible. Follow calls into the write and assignment rules, then follow the result link or receiver's action into its permission and UI checks. Cite the evidence that connects the resulting record to the next actor. If that relationship is unresolved, keep the recipient or action location unknown and place the gap where the evidence ends.

Match the results by operation, record type, and input variant before writing step details. Reopen the deciding spans together if the accounts conflict. Put eligibility on the success edge and connect a sourced rejection to its own checkpoint. Check the actual post-failure handler before drawing a reload, retry, or correction. If the next action remains unknown, attach the gap at that outcome. Cite the transition in `nextSources` or the branch's `sources` and the receiving actor's authority in `actorSources`.

## Verify what a test covers

When the documentation summarizes a test and its coverage affects the map, inspect the referenced case at the pinned revision. Trace quantities, eligibility, and branches from the fixture setup through each helper's caller and arguments to the actions and assertions that use them. A per-item assertion or a label seen during the first iteration does not establish the fixture total. If the setup or argument cannot be verified at the same pin, leave the exact quantity unknown.

In the affected step's evidence, state the concrete setup, the action exercised, and the outcome asserted. Cite the original setup and assertion locations in the source entry. If the summary and pinned case disagree, record both the documented claim and the verified detail in that entry. Use the pinned case to describe test coverage. Keep any unresolved behavior as a gap. A run record is needed to establish an execution result.

Before rendering, check the map for each material discrepancy you found. Confirm that the affected step references the entry containing the verified detail and that any gap still describes the behavior left open by that evidence. Review each retry, reopening, and hand-back at its origin and destination. Check the generated success and rejection edges against the exact state or record-selection predicates in their sources. Cite evidence that connects each edge or end the mapped route at the evidence gap.

## Find implicit evidence gaps

After tracing the supported routes, revisit consequential assignments, waits, and saved transitions. Use these checks even when the source depicts a straightforward success path.

- **Responsibility and receipt.** For every separately assigned role, check whether the evidence establishes the work they own, whether any action is expected, where they would find it, and how they would know it arrived.
- **Work that can stall.** When progress depends on a particular actor or dependency, check what happens if it becomes unavailable. Identify who can take over or resume the work and what the waiting person can see or do.
- **Saved result with uncertain confirmation.** Check what the user can do if a consequential change commits but the confirmation is delayed or lost. Look for evidence that they can recognize the saved outcome, reopen it, or retry safely. Check visible recovery as well as durable state and duplicate protection.
- **Partial completion.** When work spans several targets, check what happens if only some complete. Verify the visible status per target, what can be retried safely, and what stays blocked. A final-success assertion covers the completed outcome. Keep partial completion and recovery as evidence gaps until evidence addresses the intermediate state and next action.

Record questions that could change the user's next action or a design decision. Use a `gaps` entry even when the same uncertainty is described in a role or source note. Map a recovery route when supported by evidence. Use the gap to represent the unresolved behavior when the route is unknown.

## Write the record

Save UTF-8 JSON as `journey.json` in a dedicated output folder. Use plain text, stable lowercase IDs, and an ordered set of short steps. Record user-facing labels with the fidelity of your evidence. Give evidence enough detail to verify the claim later, such as a source file and line range pinned to a revision, an authorized screenshot, or an observed browser state. Avoid credentials, private record contents, and links containing access tokens in both files.

- Set `version` to `2`. Write `title`, `goal`, `role`, `entry`, `success`, and `coverage` as text. Coverage states what was inspected and what remains uncertain.
- Set `start` to the first step's ID. Give each step an `id`, `title`, `statusLocation` for where the actor sees the status in `cue`, and `actionLocation` for where the actor does the work in `action`. Both location fields are required. Use source-supported text or `null` when no location can be specified. Copy a location into both fields only when the evidence supports both uses. For a handoff, distinguish a documented notice or status from how the recipient opens or acts on the work.
- If the journey crosses roles, list `people` as objects with an `id`, `label`, and `responsibility`. Use roles in place of personal names. Set each step's `actor` to the ID of the person performing its `action`. Keep `statusLocation` and `actionLocation` scoped to that actor. When a continuation or branch hands work to another actor, link to a separate step for that actor's action and location. Keep alternate actors' routes distinct until their work reaches a shared result. Add `authority` when eligibility or permissions need to be explicit.
- When a step creates or changes independently owned assignments, record each evidenced responsibility in `assignments`. Each entry has a `role` referencing `people` and `work` stating what that role owns and its scope. Include roles whose assignment is known even if their next action or location is unknown. Put that uncertainty in Coverage without inventing a follow-on step.
- Give each step a `cue` for what is visible and what the person knows, `expectation` for what they would predict, `action` for what they do, `result` for what the system actually does or is expected to do, and `continuation` for how they recognize completion or resume. Pair the action with the result it produces. Put the prior cue before the action and the next action in the continuation or the next step. When an action fails, describe the failed attempt at its own step and give the retry its own action and result. Predictions remain hypotheses without user evidence.
- Set each step's `basis` to `observed` for inspected runtime behavior, `code` for source or test contracts, `specified` for documented behavior, `proposed` for a design hypothesis, or `unknown` for an unresolved result. Qualify mixed claims in the relevant field. In `sources`, use IDs from the map's top-level source list. A proposed or unknown step can use an empty list.
- Set each step's `next` to the next main continuation's step ID, or to `null` when it has none. Follow `next` from `start` to form the finite main path. Use `nextLabel` when the visible action label matters. Add alternate choices in `branches`, with a visible `label` and destination step ID in `to`. If the branch names an alternate action, set its own `actionLocation` to the supported location or `null` when unknown. Omit it for branches that only describe an outcome or condition. A recovery branch can return to a prior step.
- When a transition depends on a condition, record it as `nextCondition` for the main continuation or `condition` on the branch. For a confirmed handoff, add `nextHandoff` to the step or `handoff` to the branch. Each handoff has `work` for what is passed, `entry` for where it arrives, and `acknowledgment` for how the people involved can tell. Both endpoint steps need an `actor`.
- Use `nextSources` for evidence specific to the main transition and `sources` on a branch for evidence specific to that branch. Use `actorSources` for evidence that the step's actor can take the stated action on this record. Each field, when supplied, is a nonempty list of top-level source IDs. Put receipts and location claims in step evidence when they need different support.
- For a new record, set `nextCreates` on the successful main continuation or `creates` on the successful branch to a short label such as “Renewal draft.” Use `nextExistingRecord` or branch `existingRecord` when a different record already exists, including when reloading confirms that an earlier attempt saved it. These effects are mutually exclusive. Give the distinct receiving step the same `record` label. Cite the transition and include `actorSources` for a known receiving actor. Use `continuationUnknown: true` for a supported outcome whose next action is unknown, with a gap at that step and no outgoing transitions.
- Each top-level source has an `id`, a readable `label`, a `location`, and a `note` stating what it supports. Reference the same ID where the evidence applies to multiple steps.
- For file citations, write `path/to/file.ext:12–18, 24 @ <full Git revision>` in `location`. Use one file per citation. Use paths relative to the source root and inclusive line ranges starting at 1. For an unversioned local file, use the same format without ` @ <full Git revision>`. Use a descriptive location for evidence such as screenshots or browser observations.

## Record coverage and evidence gaps

Use `coverage` for the product version, environment, and overall evidence boundary. For a full map, add a top-level `scenarios` list for entry conditions, roles, and outcomes that could change a decision. Each scenario takes a `label` and a `steps` list of checkpoint IDs. Set `path: true` for an ordered route. Each consecutive pair must have a `next` or branch transition, including a return to an earlier checkpoint during a retry. The panel lists checkpoints in that order. Other scenarios group distinct checkpoints or gaps across paths.

Nest each `gaps` list inside its `scenarios` entry. Give each gap a `question`, an `impact` on the decision, and a concrete `check` that could resolve it. Set `step` to the earliest checkpoint in the scenario where the answer would change the user's action or understanding. Use the assignment or handoff for an unknown receiving action, the point where work becomes pending for an unavailable owner, and the committing action or mapped recovery step for uncertain confirmation. Include that checkpoint in the scenario's `steps`.

When the same gap affects separate routes, use one gap with `steps` listing each affected checkpoint in the scenario. Use this for alternate paths that stop for the same unknown next action so readers see the question on each path. Use either `step` or `steps` on a gap. Omit both for a journey-wide question or a gap without an evidenced location so it appears in Coverage alone. A scenario whose route is unknown can use an empty `steps` list with at least one gap.

```json
{
  "scenarios": [{
    "label": "Resume a returned request",
    "steps": ["receive-return", "resubmit"],
    "gaps": [{
      "step": "receive-return",
      "question": "Can the requester find the correction instructions after reopening the request?",
      "impact": "Determines whether the return view needs a clearer entry point or a content change.",
      "check": "Open a returned request as the requester in a test account and locate the saved instructions."
    }]
  }]
}
```

## Record measured decisions

Add `measurements` to the measured step. Each record uses one cohort and one set of eligible decision opportunities. Specify `basis` as `observed` for measured product behavior or `fixture` for supplied synthetic events or measured aggregates. Keep scripted choices and test assertions in the step's route evidence. Use a `source` ID from the top-level sources for the aggregate and its provenance.

Give each group a `cohort`, capture `period`, follow-up `window`, and a plural `unit` such as `review opportunities`. Set `eligible` to the positive number of opportunities. Set `counts` to the first mapped choice counts, keyed by `next` for the main continuation or by a branch's lowercase hyphenated `id`. Use unique branch IDs when measuring alternate choices. The sum must fit within the eligible denominator. An omitted choice has unknown coverage. An explicit zero represents an observed zero.

```json
{
  "basis": "fixture",
  "source": "demo-export",
  "cohort": "First-time setup visitors offered either option",
  "period": "Synthetic sample",
  "window": "First mapped choice within one day",
  "unit": "setup opportunities",
  "eligible": 10,
  "counts": {"next": 4, "import-list": 5}
}
```

The viewer ranks measured choices per cohort and identifies unmapped opportunities and choices with no count supplied. A branch with one measurement group can display its share on the arrow. Each cohort stays attached to its own unit, time frame, and source.

## Record journey outcomes

Follow [Journey Analytics](../../journey-analytics/SKILL.md#measure-journey-outcomes) to derive completion, waiting time, rework, and recovery from supported events or aggregates. Add a top-level `outcomes` list for those results. Use separate groups when the cohort, source, counting unit, capture period, or follow-up window differs. Each group has `cohort`, `period`, `window`, a plural `unit`, `basis` (`observed` or `fixture`), a `source` ID, and a nonempty `metrics` list.

- For each metric, set `kind` to `completion`, `waiting`, `rework`, or `recovery`. Write a `definition` that names the outcome and eligibility, including the start and end of a timed wait. Use optional `steps` to link the relevant checkpoints.
- For completion, rework, and recovery, set `eligible` to the metric's total eligible population, `measured` to the eligible items with a known result, and `count` to those measured items that meet the definition. The viewer calculates the share among measured items and shows follow-up coverage separately.
- For waiting, set `measured` to the number of timed items, `statistic` to `median` or `mean`, and `seconds` to the nonnegative elapsed result in seconds. Include `eligible` when the total that could enter the wait is known.
- Keep metrics with no measured sample absent. Surface material omissions in `scenarios[].gaps`. Zero is a measured result. Omit `outcomes` when the inputs support no outcome measurements.

```json
{
  "outcomes": [{
    "cohort": "First-time importers",
    "basis": "fixture",
    "source": "import-follow-up",
    "period": "Synthetic sample",
    "window": "Within two days of starting an import",
    "unit": "imports",
    "metrics": [{
      "kind": "completion",
      "definition": "Eligible first imports that reached a saved, readable result.",
      "eligible": 15,
      "measured": 12,
      "count": 9,
      "steps": ["open-saved-result"]
    }, {
      "kind": "waiting",
      "definition": "From an eligible import submission to its first saved or failed result.",
      "eligible": 15,
      "measured": 10,
      "statistic": "median",
      "seconds": 42,
      "steps": ["wait-for-import"]
    }]
  }]
}
```

## Compare changes

Inspect full maps for material friction after tracing the proposed or existing paths. Look for avoidable effort, unclear decisions, repeated work, waiting without a next action, lost progress, or handoffs that leave either party unsure. Prioritize cases that could prevent completion, cause consequential errors, or create meaningful work for the user or platform. State the actual consequence and leave its prevalence unmeasured when data is missing. Use Coverage for unknowns that need investigation. Keep low-impact observations out of **What to change**.

Add a top-level `comparisons` list for worthwhile changes or requested design decisions. Give each decision a `question`, the shared user `goal`, and two or more materially different `options`. Compare the current or proposed choices under the same permissions, recovery, and task constraints and include the option of keeping the current flow when supported.

For a friction finding, add `"finding": {"step": "checkpoint-id", "basis": "code", "summary": "What happens and the consequence", "sources": ["source-id"]}` to its comparison. Pick the step where the person encounters the friction. Use `observed`, `code`, or `specified` with supporting sources for an established behavior and qualify untested user consequences. Use `proposed` for a design risk. The finding appears on the affected step with a link to its comparison.

A `baseline` describes current behavior or the current specification within the scope of its cited sources. Match each material claim in the option to that evidence. Sources can establish available actions and rules independently of presentation, sequence, or discoverability. Narrow the baseline to the known facts when evidence is incomplete. An assumed design belongs in a `proposed` option. A comparison can use proposed options when a sourced baseline is unavailable.

Write the baseline's `label` from its cited `support`. Name the documented behavior, rule, or state the option preserves. Read the label by itself against the source and check every qualifier. A label that names a screen, layout, sequence, or number of steps needs evidence of that detail. For example, if the source confirms availability of a retry after a failed upload, “Keep upload retry available” names the supported behavior.

Draft the baseline from the mapped routes. From the decision being compared, follow its immediate branches and downstream handoffs. Include each documented route that returns work to that decision, including returns initiated later by another role. Also include returns that change what users must do to reach the stated outcome. In the option's `change` or `effect`, state what triggers each return or retry, who acts, and where work resumes. Link the relevant checkpoints for the return, the corrective action, and the resumed work in `steps`.

Describe each alternate route with its condition up front. For example, “If validation fails, the operator can correct the saved input and rerun validation.” Apply this same scope to the effect of a baseline. Check any claim containing “only,” “always,” or “once” for an explicit limit in the sources. When a source describes one route, state what people can do on that route. Record uncertainty about other routes as a gap when it matters to the decision.

- Each option has a `label` and a `kind` of `baseline` or `proposed`. Describe the workflow in `change`, who benefits or takes on work in `effect`, and the material cost, risk, or prerequisite in `tradeoff`.
- State what the evidence actually supports in `support`. A baseline requires cited `sources`. Cite sources for proposed options where available and state hypothesized outcomes as such. When citing measurements, use each cohort's own counts and denominator. State a missing measurement as “the [action] count is unavailable.” Use product evidence to describe which actions are available. Link `steps` to one or more affected checkpoints.
- Give the comparison a `check` that exercises the meaningful difference between options for the intended users. Use `decisionRule` to state which observable results favor each direction and when more evidence is needed.

Before rendering, verify each baseline's `label` on its own, then read its `change`, `effect`, and `tradeoff` against the cited sources. Check the text and links cover all applicable return paths, and any implied restrictions or stated counts match the evidence. Review the option tradeoffs, support, open questions, and decision rule for missing current-state facts that could change the choice. For each, add or reuse a `scenarios[].gaps` entry on the affected checkpoint with the question, its impact, and a check. Include the checkpoint in both the scenario and the affected option's `steps`. This still applies when the baseline has been narrowed to confirmed facts. An uncertainty described in `tradeoff` or `openQuestion` also needs this entry to appear on the journey step.

```json
{
  "scenarios": [{
    "label": "Resume a saved submission",
    "steps": ["reopen-request"],
    "gaps": [{
      "step": "reopen-request",
      "question": "Can requesters find the correct saved item in the current list after an interruption?",
      "impact": "Determines whether the existing entry point is sufficient or a more direct route should be tested.",
      "check": "Ask requesters to find and reopen the saved item after an interruption using the current interface."
    }]
  }],
  "comparisons": [{
    "question": "How should someone resume an interrupted submission?",
    "goal": "Let the requester finish the original task safely after interruption.",
    "options": [{
      "label": "Keep access to saved work",
      "kind": "baseline",
      "change": "The requester reopens the item from their existing list.",
      "effect": "The requester can resume from the saved item.",
      "tradeoff": "The specification leaves the item's findability in the list unverified.",
      "support": "The specification says requesters can reopen saved work from the list.",
      "steps": ["reopen-request"],
      "sources": ["workflow-spec"]
    }, {
      "label": "Link to the saved item from confirmation",
      "kind": "proposed",
      "change": "Show a durable link back to the saved item when confirmation is available.",
      "effect": "The requester may need less searching after an interruption.",
      "tradeoff": "The link needs a stable item identifier and the same access checks as the list.",
      "support": "The specification establishes that the saved item can be reopened.",
      "openQuestion": "Can requesters find the right item after confirmation is lost?",
      "steps": ["reopen-request"],
      "sources": ["workflow-spec"]
    }],
    "check": "Have intended requesters resume interrupted work in each design and verify that only one item was saved.",
    "decisionRule": "Keep the list when people can find and identify the saved item. Choose the link if it improves recovery for the tested interruptions and preserves access and saved state."
  }]
}
```

## Preview a proposed flow

Add a `preview` object to a proposed option whose change meaningfully affects what users see or do. Use sample values and realistic labels from the brief or product evidence. Start just before the affected action and include a recognizable outcome, plus the failure, recovery, or handoff that matters for the comparison. When a different person takes over, give them their own screen and show the context they receive.

`preview.start` names the first screen. Each entry in `preview.screens` has a unique `id`, a `title`, the visible `actor`, and a short `body` with the screen's state or message. Use optional `fields` with `label` and `value` for information the person needs. Use `actions` with a `label` and destination screen ID in `to`. Omit actions on an ending screen. Put the usual action first. Give alternate choices concrete labels such as “Try a failed upload.” Keep every screen reachable and give each recovery loop a way to finish. Back and restart are provided by the renderer.

Use text and local simulated transitions. Mark proposed outcomes as hypotheses in the comparison and keep assumed policy and evidence gaps visible. Omit credentials, personal data, real record identifiers, and working links or commands from preview screens.

## Audit the draft from the sources

Before checking the saved graph, take a second pass starting with the product evidence. For a review of someone else's map, do this before opening the map. Build a short list of what must be true at the decisions that change a person, record, action, or outcome. Use the pinned source rather than the draft's summaries or route labels to derive the list. Keep these facts in the working notes until the map is checked.

- Pair an assignment write with the read or permission check for the next action. Check each supported assignment mode and each independently selected role.
- Pair an attempted operation with its eligibility, each distinct result, and the next available action. Check the handler of a failure control. A reload, a new attempt, and a correction to the input have different effects.
- Check the saved state, the action that advances it, and the next actor's entry independently. For mutually exclusive states, such as a new record form and an existing record link, preserve the state-specific actions. Check the pinned assertion or handler when a prose summary combines steps.
- Separate the outcome for one item from the prerequisite for the whole task. Check whether the documented next action is available after waiting, a decline, cancellation, or another interrupted outcome.

Compare the list to the draft. Reopen the decisive source spans while checking each disputed outcome and handoff. Follow each required outcome as an edge and confirm that the destination has the right record, actor, and action location. Record uncovered outcomes and unsupported claims with exact source spans. Correct the map when authoring or updating it. For a read-only review, return the discrepancies and preserve the candidate. Run the structural check below after resolving or reporting those findings. A structural pass can verify reachability and references. Source review establishes whether the route belongs in the map.

### Check a separately derived source outline

Complete the outline from the original evidence before creating the journey record. Save it as a working `source-outline.json`. Use stable checkpoint IDs, record each route condition and actor, and write `statusLocation` and `actionLocation` separately, including `null` when a source leaves either unknown. A source that names a status surface and lists available decisions establishes the location of those decisions only if it places the controls there.

Use the saved outline to draft the map. When another person does the evidence pass, give them the scope and original sources before they see a draft. Revise an outline assertion only after reopening the relevant evidence. Cite the span that changes it. Follow the requested deliverable format when deciding whether to return the working outline. Use this format:

```json
{
  "steps": [
    {"id": "submit-renewal", "source": "Renewal policy, section 4", "routesComplete": true},
    {"id": "open-new-draft", "record": "Renewal draft", "actor": null,
     "actionLocation": null, "source": "Renewal policy, sections 4 and 5", "routesComplete": true}
  ],
  "routes": [
    {"from": "submit-renewal", "to": "open-new-draft", "creates": "Renewal draft",
     "condition": "At least one item is eligible.", "source": "Renewal policy, section 4"}
  ]
}
```

Each step needs `id` and `source`. Include `actor`, `record`, `statusLocation`, `actionLocation`, or `continuationUnknown` only when the draft must match it. If the reviewed evidence specifies a set of assignees, use `assignees` with their distinct role IDs. The draft must record them in `assignments`, including roles whose next action is unknown. Use `null` for an explicitly unknown text field. Each route needs declared step IDs for `from` and `to`, plus `source`. Include `creates`, `existingRecord`, and `condition` when those facts must match. Use `"handoff": true` when the sources establish a transfer of work that the map must describe on that route. Specify each endpoint's actor and action location where the evidence establishes them. Keep the same labels and conditions when transferring the outline to the draft.

For reviewed rendering, assert every named `statusLocation` and `actionLocation` in the outline. Cite the original evidence that places each claim. For a branch's `actionLocation`, put the assertion on its route, with the condition that selects that branch when it has one. Add explicit null assertions for unresolved locations when an inaccurate location would change the next action or a design decision.

Set `"routesComplete": true` when the outline lists every supported outgoing transition in scope at that checkpoint. Include failures and alternate actors. Record each exact `condition`, or omit it for an unconditional route. If the sources establish an outcome but leave the next action unknown, end that route with a local evidence gap as described above. Leave the flag off for a spot check that covers only some outgoing routes.

From the installed skill directory, check the draft without writing HTML:

```sh
python -X utf8 scripts/render_journey.py "<output-folder>/journey.json" --check-outline "<source-outline.json>"
```

The command reports missing checkpoints, mismatches, and extra transitions from a step whose reviewed routes are complete. Resolve those findings before rendering. Verify the outline's citations and completeness against the product evidence.

## Check the saved routes

After writing `journey.json`, run the [bundled renderer](../scripts/render_journey.py) in review mode from the installed `skills/user-task-walkthrough/` directory:

```sh
python -X utf8 scripts/render_journey.py "<output-folder>/journey.json" --review-routes
```

Read the printed routes for each change of owner, successor record, retry, and reopening. For consequential or ambiguous routes, append the origin step ID after `--review-routes` to inspect just those transitions and their full source locations. Reopen the named evidence for the receiving actor and action. Check both what grants that actor authority and where the specific record or assignment type becomes actionable. Correct the saved condition, actor, action, or location if the source cannot support it. For a documented copy rejection, confirm that the attempted choice can reach the rejection in the map. Put eligibility on the edge that advances after the check.

Check the action that actually advances each shared stage. If a source shows a save followed by separate approval, record the approval as the transition and keep saving as preparation. For a gap that affects more than one checkpoint, verify it appears at each affected action in the saved record.

## Render and check

From the installed `skills/user-task-walkthrough/` directory, use reviewed rendering for a map with changes of record or actor:

```sh
python -X utf8 scripts/render_journey.py "<output-folder>/journey.json" --render-reviewed "<source-outline.json>"
```

Append `--source-root "<source-directory>"` when your record contains file citations. Supply the Git checkout for pinned citations and the source directory for unversioned files. Repeat the option for sources in different roots. Each path and revision must resolve to exactly one file. Both render modes verify the cited line ranges before writing HTML. When a citation fails, open that version of the file and correct the range or record what evidence is missing.

The reviewed command checks and renders the same record. It requires complete outgoing routes at both ends of an explicit change of record and at every checkpoint that sends work to a different named actor. It also checks that the outline covers every named status, action, and branch location on version 2 maps. Resolve findings against the original product evidence before rerunning. Keep unsupported routes and locations as evidence gaps.

For a walkthrough without those boundaries, run the bundled [renderer](../scripts/render_journey.py) with the saved record alone. It uses the Python 3.8+ standard library.

```sh
python -X utf8 scripts/render_journey.py "<output-folder>/journey.json"
```

The command validates the record and writes `index.html` beside it. It can replace a page it generated previously. The HTML opens on the main route. Select a card to see its actions, select **Alternate paths** to show the wider graph, or choose **Start walkthrough** for guided steps. **Step details and evidence** holds the source notes and supporting context. Open **Coverage** to jump to a scenario checkpoint and **What to change** to compare options when the record supplies them. Use **Preview proposed flow** on an option to try its sample screens. Check a main route, a recovery branch, a Coverage link, and the preview's outcome, Back, restart and close controls in a browser when available. Use **Fit map** to fit the visible graph.

The map opens directly as a local file. If the environment lacks Python or a preview, give the user the files that were produced and state what remains.

To refresh, start from the saved record. Recheck the cited locations and changed behavior, preserve IDs for the same steps, and mark stale results unknown until checked. When refreshing a version 1 record, replace its `surface` with independently verified `statusLocation` and `actionLocation` values and set `version` to `2`. The renderer still accepts saved version 1 records and shows their original label as a generic location.
