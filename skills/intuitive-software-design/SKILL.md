---
name: intuitive-software-design
description: Design, review, formally audit, score, or improve software screens, workflows, navigation, forms, dashboards, interactions, and product behavior using the Intuitive Software Design Standard. Use when the user asks whether software is intuitive, requests UI/Flow/Feel analysis, or wants the smallest evidence-grounded changes that reduce interaction friction. Do not use as a visual-style or trend critique.
---
<!-- Copyright 2026 ArcanEdge AI. Licensed under Apache-2.0; preserve this notice when redistributing. Source: https://github.com/ArcanEdge-AI/intuitive-software-design -->

# Intuitive Software Design

Apply the standard relative to the intended user. The objective is not to remove useful thought from the user's work; it is to keep the user from having to think about operating the software when they should be thinking about the job.

## Route the request

Classify the primary mode from the user's outcome, not from a keyword alone:

- `DESIGN`: shape something that does not yet exist or prevent intuition problems before implementation.
- `REVIEW`: diagnose an existing design or implementation and explain specific problems without requiring a complete formal scorecard.
- `AUDIT`: conduct a formal screen, workflow, or product evaluation with evidence, 0-4 scores, friction types, severity, and critical failures.
- `IMPROVE`: find the smallest complete changes that remove diagnosed friction while preserving what works.

Use one primary mode. Combine modes only when the user asks for both or when a small secondary step is necessary to complete the main outcome. State the mode briefly in formal work; do not burden a quick request with routing ceremony.

## Establish the evaluation frame

Before judging the experience, establish:

1. intended user and relevant experience or domain knowledge;
2. task and starting point;
3. success condition;
4. evidence available and important evidence missing.

Infer these from the request, repository, product documentation, user stories, interface, and domain context when reasonable. Ask only when a missing fact would materially change the result. Identify meaningful differences when more than one intended-user group is affected.

Never invent user behavior, research results, runtime behavior, hidden states, or scores. Mark a criterion `NE — Not Evaluated: Insufficient Evidence` when evidence cannot support it.

When the outcome depends on how a person discovers, chooses, or completes a task, use [User-Task Walkthrough](../user-task-walkthrough/SKILL.md) before diagnosing or proposing structure. Trace the relevant journey with user-accessible knowledge, visible cues, predicted consequences, and evidence-supported outcomes. Use a short trace for a small task; do not add a full journey report to a styling-only question. For a new design, treat the trace as proposed behavior rather than observed usability.

## Use the standard

The authoritative source is [references/intuitive-software-design-standard.md](references/intuitive-software-design-standard.md). Read its foundation, UI/Flow/Feel model, Intuitive Software Loop, and guardrails for every mode, then use the relevant sections below:

- `DESIGN`: read the design principles and [references/examples.md](references/examples.md). Define the user's loop, states, decisions, feedback, recovery, and measurable acceptance before proposing structure.
- `REVIEW`: inspect the supplied evidence across UI, Flow, and Feel where observable. Use the friction taxonomy, Prediction Gap, Decision Density, Loop break, and critical-failure checks. Use examples only when comparison adds clarity.
- `AUDIT`: also read [references/scoring-reference.md](references/scoring-reference.md) and use [references/audit-template.md](references/audit-template.md). Do not calculate a screen, workflow, or product score from unevaluated criteria.
- `IMPROVE`: trace each recommendation to evidence and an underlying friction source. Prefer a ranked smallest-complete-change plan. Redesign only when smaller changes cannot solve the diagnosed problem.
- For an AI-agent or code-review deliverable, use [references/ai-review-template.md](references/ai-review-template.md).

The standard controls if a companion reference appears to conflict with it.

## Select focused guidance

Load only what changes the requested task; these are supporting capabilities, not a mandatory report set:

- If domain objects, relationships, lifecycle, or navigation structure are unclear, use [Product Mental Model](../product-mental-model/SKILL.md) before arranging screens.
- If selection, comparison, approval, or configuration lacks necessary context, use [Decision-Support Design](../decision-support-design/SKILL.md).
- If completion depends on another actor or external system, use [Multi-Role Workflow](../multi-role-workflow/SKILL.md).
- If the task crosses devices, platforms, products, or service boundaries—or a backend behavior materially changes effort, state, trust, or recovery—use [Connected Experience Design](../connected-experience-design/SKILL.md). Do not apply it to screen-only styling or presume that data should sync.
- For locating information/actions, read [findability](references/findability.md).
- For action labels, status, instructions, and errors, read [UI language](references/ui-language.md).
- For first-product-use, occasional return, or repeated expert work, read [experience progression](references/experience-progression.md).
- When the user asks to test this plugin's agent-output quality, use [Behavioral Evaluation](../behavioral-evaluation/SKILL.md); it is separate from a product usability audit.

For proposed UI elements, explain the task question, decision, action, or confirmation they serve. Do not add controls or structure whose benefit cannot be tied to the user's job and supporting evidence.

## Operating rules

1. Separate observation from inference. Say what is visible or demonstrated, then explain the likely user consequence.
2. Evaluate `UI`, `Flow`, and `Feel` independently. A clear screen can belong to a poor workflow; attractive software can behave unpredictably.
3. Treat screenshots as evidence of visible UI, state cues, and predictive affordances only. They do not prove responsiveness, action results, transitions, error handling, recovery, keyboard operation, or broad Feel quality; mark those `NE`.
4. Locate the broken Intuitive Software Loop stage: Orient, Recognize, Predict, Act, Confirm, or Continue.
5. Name the friction precisely: Navigation, Interpretation, Decision, Interaction, Memory, Feedback, Recovery, or Process.
6. Keep severity separate from the 0-4 intuition score.
7. Report every Critical Failure separately; never average one away.
8. Treat accessibility as part of intuitive operation, while distinguishing confirmed defects from evidence that was not available.
9. Do not penalize appropriate professional density, domain terminology, or expert shortcuts. Judge whether the intended user can recognize structure, predict behavior, and work efficiently.
10. Do not equate minimal, modern, or aesthetically preferred interfaces with intuitive ones.
11. Recommend the smallest complete correction that resolves the underlying problem, includes necessary states and recovery, and preserves effective behavior.
12. When a promised result depends on a service, data store, or integration, distinguish the requested action, actual state, user-facing acknowledgment, and continuation or recovery. A dispatched request or optimistic update alone is not completion evidence.

## Output calibration

For quick design help, answer directly with the intended user, key decision, proposed flow, essential states, and important tradeoffs.

For reviews, lead with the most consequential diagnosis and cite specific evidence. Use concise findings unless the user requests a formal report. Do not use the audit template or assign numeric scores unless the user asks to score or the requested review is explicitly formal; omit the Score field and use qualitative evidence boundaries instead.

For audits, include scope and evidence confidence, separate critical failures, criterion scores with rationales, friction and Loop-break summaries, prioritized findings, and a smallest-complete-change plan. Use this finding shape when appropriate:

```text
Finding: [specific problem]
Area: UI | Flow | Feel | Cross-Cutting
Principle: [standard principle]
Friction Type: [taxonomy term]
Evidence: [observable evidence]
User Impact: [effect on intended user and task]
Severity: Critical | High | Medium | Low
Score: [criterion and 0-4, or NE]
Recommendation: [smallest complete corrective change]
Expected Outcome: [observable improvement]
```

The full block, including `Score`, is for `AUDIT`, explicitly requested scoring, or an explicitly formal review. In an ordinary `REVIEW`, omit `Score` rather than manufacturing formality.

For improvements, connect each change as `evidence -> friction source -> correction -> expected behavior`. Do not produce a screen redesign by default.

## Completion check

Before returning:

- the intended user, task, and success condition are explicit or reasonably inferred;
- claims stay within available evidence;
- UI, Flow, and Feel are distinguished where the evidence permits;
- scores use only the 0-4 behavioral rubrics and show `NE` where needed;
- critical failures are separate from averages;
- recommendations preserve what works and solve the entire diagnosed state or workflow gap;
- the answer is specific enough that a designer, developer, PM, QA reviewer, or AI agent can act on it.
