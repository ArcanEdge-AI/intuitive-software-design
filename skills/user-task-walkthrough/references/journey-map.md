# Interactive journey map

Use the walkthrough to trace a consequential goal from realistic starting points to recognizable outcomes. A map can use a live interface, current source and tests, a prototype, screenshots, or a specification. Tie it to the environment and version its evidence covers.

For a workflow that changes hands, follow [Multi-Role Workflow](../../multi-role-workflow/SKILL.md). Identify whose action is pending, what they can see or change, and which saved item the next person receives.

## Check path coverage

Work outward from the goal and starting states. At each material decision, check the visible choices, the rules that allow each choice, the resulting saved or visible state, and who acts next. Compare current implementation with documented or observed behavior and keep any consequential mismatch visible.

Follow each distinct outcome to completion, closure, a usable return point, or an explicit evidence gap. Include role restrictions, waiting, rejection, retries, and interruption when they change the available action or result. Combine variants when they lead to the same decision, ownership, and outcome. Review the source list at the end to catch supported paths that are missing from the record.

When supplied measurements show how people choose, use [Journey Analytics](../../journey-analytics/SKILL.md) to interpret them. A representative cohort can inform the primary walkthrough. Keep important low-frequency or unmeasured paths reachable.

## Verify what a test covers

When the documentation summarizes a test and its coverage affects the map, inspect the referenced case at the pinned revision. Trace quantities, eligibility, and branches from the test's fixtures and setup through helper calls to the actions and assertions that actually use them. If an excerpt uses a value or helper defined elsewhere, inspect its definition at the same pin before drawing a conclusion.

In the affected step's evidence, state the concrete setup, the action exercised, and the outcome asserted. Cite the original setup and assertion locations in the source entry. If the summary and pinned case disagree, record both the documented claim and the verified detail in that entry. Use the pinned case to describe test coverage. Keep any unresolved behavior as a gap. A run record is needed to establish an execution result.

Before rendering, check the map for each material discrepancy you found. Confirm that the affected step references the entry containing the verified detail and that any gap still describes the behavior left open by that evidence.

## Find implicit evidence gaps

After tracing the supported routes, revisit consequential assignments, waits, and saved transitions. Use these checks even when the source depicts a straightforward success path.

- **Responsibility and receipt.** For every separately assigned role, check whether the evidence establishes the work they own, whether any action is expected, where they would find it, and how they would know it arrived.
- **Work that can stall.** When progress depends on a particular actor or dependency, check what happens if it becomes unavailable. Identify who can take over or resume the work and what the waiting person can see or do.
- **Saved result with uncertain confirmation.** Check what the user can do if a consequential change commits but the confirmation is delayed or lost. Look for evidence that they can recognize the saved outcome, reopen it, or retry safely. Check visible recovery as well as durable state and duplicate protection.
- **Partial completion.** When work spans several targets, check what happens if only some complete. Verify the visible status per target, what can be retried safely, and what stays blocked. A final-success assertion covers the completed outcome. Keep partial completion and recovery as evidence gaps until evidence addresses the intermediate state and next action.

Record questions that could change the user's next action or a design decision. Use a `gaps` entry even when the same uncertainty is described in a role or source note. Map a recovery route when supported by evidence. Use the gap to represent the unresolved behavior when the route is unknown.

## Write the record

Save UTF-8 JSON as `journey.json` in a dedicated output folder. Use plain text, stable lowercase IDs, and an ordered set of short steps. Record user-facing labels with the fidelity of your evidence. Give evidence enough detail to verify the claim later, such as a source file and line range pinned to a revision, an authorized screenshot, or an observed browser state. Avoid credentials, private record contents, and links containing access tokens in both files.

- Set `version` to `1`. Write `title`, `goal`, `role`, `entry`, `success`, and `coverage` as text. Coverage states what was inspected and what remains uncertain.
- Set `start` to the first step's ID. In `steps`, give each step an `id`, `title`, and `surface` the person could recognize.
- If the journey crosses roles, list `people` as objects with an `id`, `label`, and `responsibility`. Use roles in place of personal names. Set each step's `actor` to the ID of the person performing the action. Add `authority` when eligibility or permissions need to be explicit.
- Give each step a `cue` for what is visible and what the person knows, `expectation` for what they would predict, `action` for what they do, `result` for what the system actually does or is expected to do, and `continuation` for how they recognize completion or resume. Pair the action with the result it produces. Put the prior cue before the action and the next action in the continuation or the next step. When an action fails, describe the failed attempt at its own step and give the retry its own action and result. Predictions remain hypotheses without user evidence.
- Set each step's `basis` to `observed` for inspected runtime behavior, `code` for source or test contracts, `specified` for documented behavior, `proposed` for a design hypothesis, or `unknown` for an unresolved result. Qualify mixed claims in the relevant field. In `sources`, use IDs from the map's top-level source list. A proposed or unknown step can use an empty list.
- Set each step's `next` to the next main continuation's step ID, or to `null` when it has none. Follow `next` from `start` to form the finite main path. Use `nextLabel` when the visible action label matters. Add alternate choices in `branches`, with a visible `label` and destination step ID in `to`. A recovery branch can return to a prior step.
- When a transition depends on a condition, record it as `nextCondition` for the main continuation or `condition` on the branch. For a confirmed handoff, add `nextHandoff` to the step or `handoff` to the branch. Each handoff has `work` for what is passed, `entry` for where it arrives, and `acknowledgment` for how the people involved can tell. Both endpoint steps need an `actor`.
- Each top-level source has an `id`, a readable `label`, a `location`, and a `note` stating what it supports. Reference the same ID where the evidence applies to multiple steps.

## Record coverage and evidence gaps

Use `coverage` for the product version, environment, and overall evidence boundary. For a full map, add a top-level `scenarios` list for entry conditions, roles, and outcomes that could change a decision. Each scenario takes a `label` and a `steps` list of distinct checkpoint IDs in journey order. Select enough checkpoints to locate the route. The panel shows each checkpoint's evidence basis.

Nest each `gaps` list inside its `scenarios` entry. Give each gap a `question`, an `impact` on the decision, and a concrete `check` that could resolve it. Set `step` to the earliest checkpoint in the scenario where the answer would change the user's action or understanding. Use the assignment or handoff for an unknown receiving action, the point where work becomes pending for an unavailable owner, and the committing action or mapped recovery step for uncertain confirmation. Include that checkpoint in the scenario's `steps`.

Omit `step` for a journey-wide question or a gap without an evidenced location so it appears in Coverage alone. A scenario whose route is unknown can use an empty `steps` list with at least one gap.

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

Add a top-level `comparisons` list when the team is deciding what to change. Give each decision a `question`, the shared user `goal`, and two or more materially different `options`. Compare the options under the same permissions, recovery, and task constraints.

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

## Render and check

From the skill directory, run the bundled [renderer](../scripts/render_journey.py), passing the path to the saved record. It uses the Python 3.8+ standard library.

```sh
python scripts/render_journey.py "<output-folder>/journey.json"
```

The command validates the record and writes `index.html` beside it. It can replace a page it generated previously. The HTML opens on the connected journey map. Select a card to open its details and evidence, select a labeled branch to follow it, or choose **Start walkthrough** for guided steps. Open **Coverage** to jump to a scenario checkpoint and **What to change** to compare options when the record supplies them. Check the main route, one recovery branch, a coverage checkpoint with a gap, and any available comparison links in a browser when available. Use **Fit map** for an overview at any zoom.

The map opens directly as a local file. If the environment lacks Python or a preview, give the user the files that were produced and state what remains.

To refresh, start from the saved record. Recheck the cited locations and changed behavior, preserve IDs for the same steps, and mark stale results unknown until checked. Edit the record and rerun the renderer.
