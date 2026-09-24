# Intuitive Software Scoring Reference

This is the concise operational scorebook for the [Intuitive Software Design Standard](intuitive-software-design-standard.md). The standard is authoritative.

## Scoring rules

1. Establish intended user, task, starting point, success condition, evidence, and exclusions.
2. Score only behavior supported by evidence. Use `NE — Not Evaluated: Insufficient Evidence` otherwise.
3. Attach a one-sentence evidence rationale to each score.
4. Keep screen, workflow, and product assessments separate.
5. Keep severity separate from score.
6. Report Critical Failures outside all averages.
7. Exclude `NE` from arithmetic and report coverage; never convert it to zero.

## Universal scale

| Score | Label | Behavioral anchor |
| ---: | --- | --- |
| 0 | Broken | Intended users cannot reasonably infer or complete the interaction without intervention, or the behavior prevents success. |
| 1 | Difficult | Explanation, experimentation, repeated correction, or substantial avoidable effort is required. |
| 2 | Understandable | Users can figure it out, but noticeable interpretation, thought, or rechecking is required. |
| 3 | Intuitive | Most intended users should understand and predict it without assistance. |
| 4 | Effortless | It closely matches established mental models and requires minimal operating attention through result and continuation. |
| NE | Not Evaluated | Evidence does not support a score. |

---

# Screen scorecard

## Orientation

**Measures:** ability to identify location, object, scope, purpose, and current state.

| Score | Observable behavior |
| ---: | --- |
| 0 | Users cannot tell what screen/object they are in or act on the wrong scope. |
| 1 | Users require path history, explanation, or repeated navigation to reconstruct context. |
| 2 | Context can be inferred from multiple cues but requires checking or interpretation. |
| 3 | Most users can state location, object, purpose, and state from the working view. |
| 4 | Context is immediately clear even after a deep link, interruption, or return. |

**Warning signs:** generic titles; absent project/customer identity; unclear edit scope; missing selected navigation; modal without object context.

**Test:** open the screen directly or resume after interruption; ask where the user is, what object is affected, what state it is in, and what can happen next.

## Visual hierarchy

**Measures:** ability to distinguish purpose, priority, grouping, primary information, and primary action.

| Score | Observable behavior |
| ---: | --- |
| 0 | Users cannot find essential information or the primary task because competing elements provide no usable order. |
| 1 | Users scan broadly, choose wrong elements, or need explanation of structure. |
| 2 | Priority becomes clear after deliberate reading or comparison. |
| 3 | Most users locate purpose, key information, and primary action without assistance. |
| 4 | Structure supports rapid scanning and remains clear across content length and responsive states. |

**Warning signs:** every element has equal emphasis; visual prominence contradicts task importance; dense content lacks grouping; primary action competes with secondary actions.

**Test:** show the screen briefly, then ask what it is for, what matters now, and what action appears primary; test realistic dense and narrow states.

## Action clarity

**Measures:** ability to identify available actions, distinguish priority/risk, and predict consequences.

| Score | Observable behavior |
| ---: | --- |
| 0 | The primary action cannot be identified or a consequential action is fundamentally ambiguous. |
| 1 | Users guess among actions, need explanation, or repeatedly choose the wrong action. |
| 2 | Actions can be interpreted, but labels, placement, or consequences require noticeable thought. |
| 3 | Most users identify primary and secondary actions and predict their outcomes unaided. |
| 4 | Actions are immediately recognizable, consequence-specific, and proportionate to risk without unnecessary ceremony. |

**Warning signs:** vague labels such as Done/Process; icon-only primary actions; dangerous and safe actions look equivalent; multiple competing primaries.

**Test:** before activation, ask users what they would choose for the task and what they expect each major action to do.

## Control recognition

**Measures:** ability to recognize interactive elements, operation method, current value, and affected object.

| Score | Observable behavior |
| ---: | --- |
| 0 | Essential controls are not perceived as interactive or cannot be operated by an intended user. |
| 1 | Users hunt, hover, experiment, or require instructions to operate controls. |
| 2 | Controls are discoverable with inspection but have weak affordance or ambiguous target. |
| 3 | Most users recognize controls, state, and operation from established cues. |
| 4 | Controls are immediately recognizable, accessible, stateful, and colocated with what they affect. |

**Warning signs:** text styled like a button or vice versa; hidden hover actions; unlabeled icons; drag-only operation; tiny targets; ambiguous row click.

**Test:** observe first attempts using pointer and keyboard where applicable; inspect names, semantics, focus, hit areas, state, and alternatives.

## Information clarity

**Measures:** ability to interpret information needed for the current task accurately and efficiently.

| Score | Observable behavior |
| ---: | --- |
| 0 | Essential information is missing, misleading, contradictory, or unusable for the decision. |
| 1 | Users need explanation, cross-reference, or repeated correction to understand it. |
| 2 | Meaning can be derived but requires translation, careful comparison, or avoidable lookup. |
| 3 | Most intended users interpret essential information correctly without assistance. |
| 4 | Information is immediately usable, appropriately precise, contextualized, and resilient to realistic variation. |

**Warning signs:** internal codes; unexplained abbreviations; ambiguous units/dates; detached labels; hidden assumptions; important state only in color.

**Test:** ask users to explain the relevant values and make the task decision; test realistic edge content, localization/format variation, and non-color interpretation.

## Feedback and state visibility

**Measures:** ability to understand current, changed, pending, successful, failed, and partially completed state.

| Score | Observable behavior |
| ---: | --- |
| 0 | Users cannot tell whether an important action occurred or what state the system is in. |
| 1 | State is discovered only by retry, refresh, navigation, or explanation. |
| 2 | State is present but delayed, indirect, transient, or requires checking. |
| 3 | Most users can see acknowledgment, current state, and result without assistance. |
| 4 | Feedback is immediate and honest through pending, result, failure, recovery, and continuation, including semantic announcement where needed. |

**Warning signs:** unchanged button during work; silent autosave; success toast as the only durable evidence; stale values; color-only status; no partial result.

**Test:** exercise default, slow, success, failure, retry, duplicate activation, background, and partial-completion states.

## Cognitive load

**Measures:** avoidable interpretation, recall, comparison, decision, and monitoring effort on the screen.

| Score | Observable behavior |
| ---: | --- |
| 0 | The screen makes a required decision or action infeasible because essential structure, context, or manageable choice is absent. |
| 1 | Users rely on notes, repeated lookup, trial and error, or substantial comparison to proceed. |
| 2 | The task is achievable but requires noticeable avoidable scanning, recall, or decision work. |
| 3 | Necessary complexity is organized so most users can proceed without avoidable mental work. |
| 4 | The screen presents the right context and decisions at the right time, supporting both rapid recognition and accurate work. |

**Warning signs:** many interdependent choices; context on another screen; dense content without task grouping; redundant fields; hidden defaults.

**Test:** inventory facts remembered and decisions made; observe re-reading, comparison, backtracking, notes, and hesitation. Do not treat density alone as failure.

## Consistency

**Measures:** transfer of learned appearance, wording, placement, operation, and behavior across comparable contexts.

| Score | Observable behavior |
| ---: | --- |
| 0 | Identical or indistinguishable controls behave incompatibly in a way that blocks or seriously misleads users. |
| 1 | Users must relearn common actions or repeatedly correct transferred expectations. |
| 2 | Most patterns transfer, but meaningful exceptions are not obvious and require checking. |
| 3 | Comparable elements and tasks follow stable rules; visible exceptions are understandable. |
| 4 | Knowledge transfers immediately across the product while meaningful domain differences remain explicit. |

**Warning signs:** same label/different result; different labels/same action; inconsistent row behavior; variant components missing states; arbitrary placement drift.

**Test:** compare repeated patterns across representative screens and ask users to predict behavior based on a prior encounter.

## Screen calculation

Report each evaluated criterion. A screen percentage may be shown as:

```text
screen percentage = sum(evaluated scores) / (4 × evaluated criterion count) × 100
```

Always show the evaluated count, `NE` items, evidence scope, and separate Critical Failures. Do not use the percentage as the primary diagnosis.

---

# Workflow scorecard

## Entry-point clarity

**Measures:** ability to find and identify the correct place to begin the task.

| Score | Observable behavior |
| ---: | --- |
| 0 | Users cannot reasonably find the starting point or consistently start in a blocking wrong path. |
| 1 | Search, explanation, or repeated menu exploration is required. |
| 2 | The entry point can be found after deliberate scanning or indirect navigation. |
| 3 | Most users find and recognize the correct start without assistance. |
| 4 | The entry point is available in the relevant context and immediately recognizable at the moment of need. |

**Warning signs:** task hidden under administration; multiple synonymous starts; action absent from the object context; misleading menu category.

**Test:** begin from the realistic starting point and observe first-action success, wrong paths, and time to first meaningful action.

## Next-action clarity

**Measures:** ability to identify the next useful action at every significant step.

| Score | Observable behavior |
| ---: | --- |
| 0 | A required step becomes a dead end or no next action can be inferred. |
| 1 | Users need guidance, try multiple controls, or repeatedly choose the wrong next action. |
| 2 | The next action can be determined after interpretation or rechecking. |
| 3 | Most users identify the next action without assistance at each evaluated step. |
| 4 | Each state makes the useful next action and viable alternatives immediately clear without constraining expert choice. |

**Warning signs:** generic Continue; primary action changes location unpredictably; completed step has no continuation; competing primary actions.

**Test:** pause at each step and ask what can/should happen next and why.

## Sequence matches user task

**Measures:** alignment between workflow order, domain dependencies, and the user's mental model.

| Score | Observable behavior |
| ---: | --- |
| 0 | The sequence contradicts necessary task logic or prevents successful completion. |
| 1 | Users must translate system structure, perform major detours, or repeatedly reorder work mentally. |
| 2 | The sequence is workable but contains noticeable implementation-driven or poorly timed steps. |
| 3 | The order follows the intended user's job and meaningful dependencies. |
| 4 | The sequence feels natural, removes implementation leakage, and adapts efficiently to common variations. |

**Warning signs:** record setup before meaningful object creation; irrelevant permissions early; duplicated handoffs; configuration before needed information exists.

**Test:** compare users' pre-product task descriptions with the implemented path and label each step by user value, risk control, or system leakage.

## Context preservation

**Measures:** continuity of object identity, choices, state, location, and task-relevant information across steps.

| Score | Observable behavior |
| ---: | --- |
| 0 | Critical context is lost, causing wrong-object action, blocked completion, or unavoidable restart. |
| 1 | Users must repeatedly re-enter, look up, copy, or navigate back for context. |
| 2 | Core context survives, but users must check or reconstruct secondary information. |
| 3 | Relevant identity, choices, and state carry through the workflow. |
| 4 | Context remains immediately available across transitions, interruptions, errors, and return paths without clutter. |

**Warning signs:** selected project absent; values reset; filters/position lost; errors clear fields; return opens a default dashboard.

**Test:** trace needed information between steps, trigger errors and back navigation, and resume after interruption.

## Decision load

**Measures:** number, complexity, timing, consequence, and support of meaningful decisions.

| Score | Observable behavior |
| ---: | --- |
| 0 | Users lack the information or ability to make a required decision, blocking or invalidating the task. |
| 1 | Excessive or opaque decisions cause guessing, abandonment, or repeated correction. |
| 2 | Decisions are possible but require avoidable comparison, premature commitment, or substantial thought. |
| 3 | Necessary decisions appear with sufficient context at appropriate times. |
| 4 | Decision Density is minimized without hiding important choice; safe defaults and remembered preferences support accurate, efficient work. |

**Warning signs:** many interdependent choices at once; advanced settings required early; arbitrary options; no consequence explanation; unsafe default.

**Test:** inventory decisions, required knowledge, timing, consequence, and whether each can be inferred, defaulted, deferred, remembered, or removed.

## Backtracking required

**Measures:** avoidable reversals, detours, repeated navigation, and rework needed to complete the task.

| Score | Observable behavior |
| ---: | --- |
| 0 | Completion requires an impossible return/restart or backtracking destroys essential work. |
| 1 | Repeated backtracking or detours are necessary for normal completion. |
| 2 | One or more avoidable returns are needed to retrieve context, change prerequisites, or verify state. |
| 3 | Normal completion proceeds without avoidable backtracking; deliberate review remains available. |
| 4 | The flow anticipates dependencies, supports safe revision in place, and preserves position and work. |

**Warning signs:** previous data omitted; prerequisites revealed late; global settings detour; no in-context correction; return loses state.

**Test:** map forward and reverse transitions and record every revisit, why it occurred, and whether it advanced the user's job.

## Progress visibility

**Measures:** ability to understand current position, completed work, remaining work, pending operations, and blockers.

| Score | Observable behavior |
| ---: | --- |
| 0 | Users cannot determine whether the workflow is active, stalled, or complete. |
| 1 | Progress requires explanation, repeated refresh, or external tracking. |
| 2 | Progress is partially visible but vague, transient, or disconnected from meaningful steps. |
| 3 | Most users can identify current step, completed work, and relevant remaining work. |
| 4 | Progress remains clear through branching, background work, interruption, failure, and resumption. |

**Warning signs:** spinner without context; numbered steps with meaningless names; hidden background job; completed sections not marked; blocker absent.

**Test:** pause at multiple stages and ask what has happened, what is processing, what remains, and what blocks continuation.

## Completion confidence

**Measures:** ability to know that success occurred, what is now true, and what can happen next.

| Score | Observable behavior |
| ---: | --- |
| 0 | Users cannot distinguish success from pending, failure, or abandonment. |
| 1 | Users confirm by retrying, refreshing, checking elsewhere, or asking for help. |
| 2 | Completion is indicated but lacks durable evidence, consequence, or clear continuation. |
| 3 | Most users understand that the task succeeded and the resulting state. |
| 4 | Success is explicit, durable, consequence-specific, and linked to the next useful action or resulting object. |

**Warning signs:** silent return to list; generic Success toast; button remains actionable; no created object/status; partial completion presented as full success.

**Test:** after completion, ask what happened, what is now true, where the result is, and what the user would do next.

## Error recovery

**Measures:** ability to understand, correct, retry, undo, or resume from realistic mistakes and system failures without avoidable loss.

| Score | Observable behavior |
| ---: | --- |
| 0 | A realistic error creates an unrecoverable dead end, critical loss, or unsafe repeated action. |
| 1 | Recovery needs external help, restart, repeated experimentation, or major rework. |
| 2 | A recovery path exists but is vague, lossy, indirect, or requires notable diagnosis. |
| 3 | Most users can identify the cause, preserve valid work, correct it, and resume. |
| 4 | Prevention, specific diagnosis, preserved context, safe recovery, and confirmed resolution work across realistic failure modes. |

**Warning signs:** generic error; cleared form; destructive retry; no undo; partial result hidden; permission failure with no next step.

**Test:** trigger validation, permission, network, timeout, conflict, destructive, and partial-completion cases relevant to the task.

## Prediction consistency

**Measures:** repeated alignment between reasonable expectation and actual actions, transitions, defaults, and consequences.

| Score | Observable behavior |
| ---: | --- |
| 0 | A major repeated mismatch blocks completion or creates serious consequence. |
| 1 | Users repeatedly guess wrong, correct actions, or avoid controls because outcomes are unreliable. |
| 2 | Most behavior can be learned, but important exceptions or hidden consequences require vigilance. |
| 3 | Actions and transitions reliably match reasonable expectations across the evaluated flow. |
| 4 | The flow builds confidence: learned patterns transfer, exceptions are explicit, and high-consequence behavior is especially predictable. |

**Warning signs:** row behavior changes; same label/different consequence; hidden default; unexpected destination; intermittent or stale state.

**Test:** collect expectations before actions across the workflow and compare with actual behavior; repeat similar actions in different contexts.

## Workflow calculation

```text
workflow percentage = sum(evaluated scores) / (4 × evaluated criterion count) × 100
```

Show criterion scores, evidence rationales, evaluated count, `NE` criteria, and separate Critical Failures. Lead with the primary weakness and major friction, not the number.

---

# Behavior Confidence interaction scorecard

Score each criterion for representative observed interactions using the universal 0–4 scale. Record `NE` when the required action or state has not been observed. These scores describe interaction behavior, not the screen or workflow scores above.

## Outcome predictability

**Measures:** whether the intended user can foresee the action's result and affected object before acting, and whether observed behavior matches that expectation.

| Score | Observable behavior |
| ---: | --- |
| 0 | The visible promise points to a materially wrong object or result, preventing safe task completion. |
| 1 | Users must guess, experiment, or seek explanation to predict a consequential action. |
| 2 | The result and scope can be inferred only after deliberate checking or backtracking. |
| 3 | Most intended users can state the result and affected object before acting, and the observed result matches. |
| 4 | The prediction remains clear across realistic scopes, interruptions, and consequential variations. |

**Warning signs:** generic action labels; missing object identity; hidden side effects; a preview that disagrees with the result.

**Test:** before activation, ask the intended user what will change and for which object; then compare with the observed result.

## State feedback

**Measures:** whether the user can distinguish pending, success, failure, partial completion, and durable state for the interaction.

| Score | Observable behavior |
| ---: | --- |
| 0 | The interaction presents a false success or gives no usable indication of consequential state. |
| 1 | Users must retry, refresh, or ask someone else to discover the actual result. |
| 2 | State is visible only indirectly or briefly and requires rechecking. |
| 3 | Observed pending and result states are clear, honest, and tied to the affected object. |
| 4 | State remains clear through delay, partial completion, interruption, and later return where those conditions apply. |

**Warning signs:** unchanged control during work; success toast before durable completion; missing partial-result detail; status visible only by color.

**Test:** observe the interaction in applicable slow, success, failure, and partial states; compare acknowledgment with the durable result.

## Cross-context consistency

**Measures:** whether the interaction follows a learnable rule across comparable objects, roles, devices, or repeated uses.

| Score | Observable behavior |
| ---: | --- |
| 0 | The same apparent action produces incompatible consequential results across comparable contexts. |
| 1 | Users repeatedly relearn or correct transferred expectations. |
| 2 | The general rule transfers, but exceptions require avoidable checking. |
| 3 | Comparable interactions follow a stable rule and visible exceptions are understandable. |
| 4 | Expectations transfer immediately across relevant contexts while real domain differences remain explicit. |

**Warning signs:** same label with different scope; inconsistent pending/result behavior; a device or role silently changing consequences.

**Test:** compare the same action in at least two relevant contexts and ask users to predict the second from the first. Mark `NE` if only one context was observed.

## Failure recovery

**Measures:** whether a failed or interrupted interaction leaves the user with understandable state, preserved work, and a safe continuation.

| Score | Observable behavior |
| ---: | --- |
| 0 | A failure leaves important work or outcome irrecoverable or unknown. |
| 1 | Recovery requires support, full re-entry, or risky blind repetition. |
| 2 | A retry or alternative exists, but state or duplication risk needs checking. |
| 3 | Users see what happened, keep relevant work, and can retry or choose a safe next step. |
| 4 | Recovery remains clear through partial results, duplicate attempts, and interruption where relevant. |

**Warning signs:** lost input; generic error; retry after uncertain success; no path past a partial failure.

**Test:** cause a realistic failure or interruption, then verify what is preserved, what the user can infer, and whether retry changes the result safely. Mark `NE` without failure evidence.

---

# Product assessment

Use product scoring only with representative coverage.

| Dimension | Inputs | Normalization |
| --- | --- | --- |
| UI Clarity | Evaluated screen criteria across representative screens | mean score / 4 × 100 |
| Flow Intuition | Evaluated workflow criteria across priority workflows | mean score / 4 × 100 |
| Behavior Confidence | Four separately scored interaction criteria across representative observed interactions | mean evaluated interaction-criterion score / 4 × 100 |

For each representative interaction, record the user's reasonable expectation, observed action and result, and these four independent 0–4 scores with evidence rationales:

| Interaction criterion | What to assess |
| --- | --- |
| Outcome predictability | Before acting, can the intended user predict the result and affected object from the available cues? |
| State feedback | During and after the action, can the user tell whether it is pending, succeeded, failed, or partially completed, and see the durable result? |
| Cross-context consistency | Does the same action follow a learnable rule in comparable contexts, with meaningful exceptions made clear? |
| Failure recovery | When the action fails or is interrupted, can the user understand the state, preserve work, and retry or choose a safe next step? |

Apply the universal scale to observed behavior for each criterion. Mark an interaction criterion `NE` when its behavior was not observed; a screenshot alone cannot establish pending results or recovery. Calculate the mean over evaluated interaction-criterion scores only, and report both evaluated/possible criteria and which interaction states were exercised. Do not copy screen or workflow scores into Behavior Confidence. Keep Critical Failures separate.

Use an unweighted mean only when all three dimensions are evaluated. Define any risk-based weights before scoring. Report roles, tasks, screens, states, devices, accessibility methods, and exclusions.

Required product summary:

```text
UI Clarity:            __ / 100  (coverage: __)
Flow Intuition:        __ / 100  (coverage: __)
Behavior Confidence:   __ / 100  (coverage: __)
Overall:               __ / 100  or NE

Primary Weakness:
Major Friction:
Critical Failures:
Evidence Gaps:
```

## Severity

| Level | Consequence |
| --- | --- |
| Critical | Critical task prevention, dangerous misunderstanding, unrecoverable consequence, or fundamental high-consequence expectation failure. |
| High | Repeated errors, substantial friction, significant confusion, or major effort. |
| Medium | Noticeable hesitation, extra navigation, avoidable decisions, rechecking, or recurring minor mistakes. |
| Low | Small but real friction without material threat to completion. |

Severity is assigned per finding and is not derived mechanically from the score.

## Critical Failures

Check and report separately:

- ambiguous primary consequential action;
- important action without visible confirmation;
- unexpected consequential navigation;
- dangerous action not distinguishable or reasonably recoverable;
- required-task dead end;
- silent important data modification;
- hidden critical state;
- identical controls with materially incompatible behavior;
- critical information forced into human memory despite system possession;
- important unrecoverable error;
- unclear completion for a critical task;
- strong expectation contradiction with serious consequence;
- accessibility barrier blocking a critical task for an intended user.

For each confirmed failure include evidence, affected user/task, consequence, current recovery, severity, and smallest complete correction.
