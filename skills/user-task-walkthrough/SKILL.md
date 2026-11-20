---
name: user-task-walkthrough
description: Trace how people discover, decide, act, and verify completion in software. Use for task usability reviews, end-to-end user journey maps, and workflow design. For a full map, trace meaningful choices, recovery, and changes of ownership. Generate interactive HTML when requested. Distinguish user-visible knowledge from implementation evidence.
---
<!-- Copyright 2026 ArcanEdge AI. Licensed under Apache-2.0; preserve this notice when redistributing. Source: https://github.com/ArcanEdge-AI/intuitive-software-design -->

# User-Task Walkthrough

Trace a person's goal through the interface, including the information they need to choose each action and recognize its outcome. A successful agent execution proves only that tested path worked; it does not establish human discoverability or usability.

Read the foundation, UI/Flow/Feel model, Intuitive Software Loop, and guardrails in [the authoritative standard](../intuitive-software-design/references/intuitive-software-design-standard.md). This skill operationalizes those principles; it adds no scoring system. Use [worked examples](references/worked-examples.md) when knowledge boundaries, website journeys, or incomplete evidence need clarification.

## Establish the task and knowledge boundary

Use the user's brief, product evidence, and relevant research to establish:

- **Person and goal:** role, relevant domain/product experience, trigger, and desired outcome. Describe task-relevant differences rather than inventing demographic personas.
- **Starting point:** where they arrive, prior choices, current object/account, and what they reasonably know at that moment.
- **Success:** the result they need and how they could recognize completion. Include continuation or later retrieval when part of the job.
- **Context:** frequency, stakes, permissions, device/input, and environmental constraints that materially affect this task.
- **Evidence:** what can be inspected, its scope and recency, assumptions, and missing information that could change the conclusion.

Infer cautiously from reliable context and ask only about material gaps. Preserve useful expertise: first use of this product does not imply ignorance of the domain.

Maintain a boundary between **user-accessible knowledge** and **agent-only knowledge**. Source code, API names, hidden routes, database fields, and test selectors can explain behavior but cannot establish that a person knows where to go. Update the user's knowledge only when the journey exposes information, or prior knowledge is justified. Do not jump to a hidden route to prove an entry point is discoverable.

## Trace the journey before recommending structure

Choose the consequential task or tasks within scope; do not inventory every control. Begin at the realistic entry point and follow the goal across pages, dialogs, and handoffs to recognizable completion. Do not equate reaching the final screen with achieving the result.

At each meaningful transition, examine:

1. **Intent and information:** What question is the person answering? What do they know, need to remember, or still need to learn?
2. **Visible clue and choice:** Which label, grouping, state, or convention suggests an action? Are competing choices distinguishable, and is the information needed to decide available?
3. **Prediction:** What consequence would that action reasonably suggest before activation? Treat this as an inference unless supported by actual user evidence.
4. **Action and result:** What behavior is demonstrated, specified, or proposed? Does it match the predicted consequence? Can pending, success, failure, and partial completion be distinguished?
5. **Continuation and recovery:** What signals completion or the next step? How can the person backtrack, correct a mistake, or resume with context intact?

If several actions appear plausible, record the ambiguity and trace a consequential alternative when useful. Do not choose the correct action solely because implementation inspection revealed it.

For a website, the job may be to understand the offer, establish trust, compare options, or decide whether to enquire. Evaluate whether the person's information needs are met; do not assume conversion is their only goal. When a claim promises less re-entry, saved progress, or use across devices or services, follow that promise into the first relevant product task and compare it with demonstrated behavior. For an application, trace the domain work and its effects on saved state and downstream work. For an unbuilt design, trace proposed cues and transitions and label them as design hypotheses.

## Choose relevant variants and evidence

Select variants by task consequence and available evidence: first encounter versus repeat use; invalid input or a changed decision; interruption and return; slow/failed/partial work; permission boundaries; supported mobile, keyboard, or assistive-technology use. If continuation crosses devices, platforms, or service boundaries, use [Connected Experience Design](../connected-experience-design/SKILL.md) to select the relevant identity, task-state, persistence, and recovery checks. Explain the coverage selected. Do not manufacture errors or force an exhaustive matrix onto a small request.

When runtime access is available, use the available browser or product tools to inspect visible states and authorized interactions. Record the tested role, route/state, action, outcome, and supporting screenshot, log, or artifact where useful. Review authority before saving, sending, purchasing, deleting, or changing permissions; a walkthrough is not permission to mutate real data. If an action cannot be exercised, preserve the prediction and mark its result unknown.

Without runtime access, use screenshots, source, specifications, or prototypes within their limits. Cite source paths for implemented behavior; do not call it observed runtime behavior. Screenshot-only evidence cannot prove transitions, persistence, recovery, or keyboard operation. Check save/reopen or downstream effects when relevant and authorized; a toast alone does not prove persistence.

Use supplied interviews, support reports, usability observations, or analytics to refine the task model. State which audience, task, and context each source covers. Analytics can show drop-off but may not explain its cause; support reports do not establish prevalence. Keep conflicting evidence visible rather than averaging away role differences. Do not obtain private research or install tools merely to fill evidence gaps.

## Map the journey

When asked for a journey map, interactive walkthrough, or HTML view, use the [journey map workflow](references/journey-map.md). Start with the job and the product version the evidence covers. Derive entry points, conditions, and roles from this project's UI, source, tests, screenshots, or specification.

When asked to verify an existing map, use the [source audit](references/journey-map.md#audit-the-draft-from-the-sources) as a focused read-only review. Derive the expected routes from the evidence before reading the map. Return concrete discrepancies and citations. Edit and re-render only when the request includes corrections. If the source review supplies an independent outline, [check the draft against it](references/journey-map.md#check-a-separately-derived-source-outline).

Before drafting a map with conditional routes or assignment modes, [trace consequential operations in the original sources](references/journey-map.md#trace-conditional-transitions). Prioritize branches that assign work or create a record. Follow the operation to the saved assignment, then find where the receiver can act. [Prepare a source outline](references/journey-map.md#check-a-separately-derived-source-outline) with the supported routes and separate status and action locations before writing `journey.json`. Use [Multi-Role Workflow](../multi-role-workflow/SKILL.md) when another person receives the work. Use [Journey Analytics](../journey-analytics/SKILL.md) to interpret supplied choice and outcome data or identify missing measurements.

Verify claims about test coverage against the [pinned test](references/journey-map.md#verify-what-a-test-covers). Run the [implicit gap check](references/journey-map.md#find-implicit-evidence-gaps) after tracing the documented paths. Use the [coverage format](references/journey-map.md#record-coverage-and-evidence-gaps) to link scenarios to key steps and put each open question where the answer would change the user's next action or understanding of the result.

When the team asks what to change, use [Purpose-First Redesign](../purpose-first-redesign/SKILL.md) for existing workflows and the [design process](../intuitive-software-design/references/intuitive-software-design-standard.md#39-design-process) for new designs. Add a [change comparison](references/journey-map.md#compare-changes) with sourced baselines, evidenced tradeoffs, and a check that would inform the choice. After drafting it, check that each missing current-state fact the choice depends on appears as an evidence gap on the affected step.

Save the trace as `journey.json`. For a full map, [audit it from the sources](references/journey-map.md#audit-the-draft-from-the-sources). Check the saved [handoffs and alternate destinations](references/journey-map.md#check-the-saved-routes). Use [reviewed rendering](references/journey-map.md#render-and-check) for maps that change records or actors. Return the record and standalone `index.html`. Follow the ordinary walkthrough format for a prose review.

## Return an actionable result

Use focused guidance when the trace reveals a deeper cause: [product mental model](../product-mental-model/SKILL.md) for unclear domain structure, [decision support](../decision-support-design/SKILL.md) for missing choice information, [multi-role workflow](../multi-role-workflow/SKILL.md) for human ownership handoffs, and [connected experience design](../connected-experience-design/SKILL.md) for relevant cross-surface or system-backed continuity. For local cue concerns, read [findability](../intuitive-software-design/references/findability.md), [UI language](../intuitive-software-design/references/ui-language.md), or [experience progression](../intuitive-software-design/references/experience-progression.md) as relevant. Do not expand a small walkthrough into all companion workflows.

Scale the output to the request. A short walkthrough can be a few paragraphs; use a trace table when several transitions need comparison:

| Step and intent | User knowledge and visible clue | Plausible action and expected consequence | Result and evidence | Continuation or gap |
| --- | --- | --- | --- | --- |

Identify **observations**, **inferences**, and **unknowns** throughout. Keep proposed behavior separate from existing behavior. Cite the artifact/state supporting consequential claims; do not invent quotes, success rates, timings, or human test results.

Lead with the earliest consequential task barrier. Connect findings as:

`specific evidence -> user knowledge/decision gap -> Loop break and friction -> smallest complete correction -> validation`

Preserve useful domain density, expert shortcuts, and risk controls. Include relevant pending, failure, recovery, and continuation in the correction. Identify critical failures separately. Use the main skill's audit rubric only when scoring is requested; omit numbers in ordinary walkthroughs.

End with coverage and remaining unknowns, plus a concrete validation task for the important change. Separate functional verification from human validation. Human task prompts should describe the goal without naming the correct control or giving the route; observe recognition, wrong turns, completion, and confidence without inventing targets. If human testing has not occurred, say the user consequence remains a hypothesis.

## Completion check

- The journey starts with a person's goal and realistic knowledge, rather than a component tree.
- The trace does not grant the person hidden implementation knowledge.
- Consequential choices have visible cues, needed information, predicted effects, and evidence boundaries.
- Completion, continuation, and selected recovery paths are covered or explicitly unknown.
- Recommendations follow evidence; agent success is not presented as human usability proof.
