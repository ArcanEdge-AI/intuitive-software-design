---
name: decision-support-design
description: Design or review the information, comparisons, defaults, and consequences needed for meaningful user choices. Use for selection, comparison, approval, configuration, or purchase decisions when the UI may ask people to choose before they have enough information.
---
<!-- Copyright 2026 ArcanEdge AI. Licensed under Apache-2.0; preserve this notice when redistributing. Source: https://github.com/ArcanEdge-AI/intuitive-software-design -->

# Decision-Support Design

Make the decision understandable at the moment it is required. Read intended-user framing, Decision Density, progressive disclosure, error prevention, and guardrails in [the standard](../intuitive-software-design/references/intuitive-software-design-standard.md).

## Define the decision

Identify who chooses, their goal, relevant expertise, available options, consequence, reversibility, and information already known. Separate the person's decision from the business's desired conversion or preferred option. Include choosing later or declining only when legitimate for the task.

For each consequential decision, record:

| Choice | Information needed now | Material differences / tradeoffs | Default and justification | Consequence / correction | Evidence gaps |
| --- | --- | --- | --- | --- | --- |

Use task evidence to select comparison criteria. Do not invent preferences, eligibility, prices, guarantees, or a universally best option. A choice supported by domain judgment is not automatically UI friction.

## Evaluate support and timing

Check whether the interface:

- provides comparable units, scope, limitations, and relevant costs before commitment;
- shows enough context to choose without remembering another page;
- distinguishes factual differences from recommendation or marketing claims;
- explains why an option is unavailable and what can be done next;
- permits revisiting a reversible choice while preserving useful work;
- presents consequential defaults visibly with a task-grounded justification;
- defers information or choices only when they can safely wait.

Do not remove useful options to lower a decision count. Prefer grouping and meaningful comparison when complexity belongs to the job. Do not preselect spending, disclosure, notifications, or irreversible effects merely to shorten the flow. Preserve needed confirmations and disclose the scope of commitment.

Use [the walkthrough](../user-task-walkthrough/SKILL.md) to test the sequence and [UI language guidance](../intuitive-software-design/references/ui-language.md) when labels conceal differences or consequences.

## Example

Fixture: A plan selector lists Basic, Pro, and Premium with feature counts. The brief says the buyer needs team access and occasional exports. No current feature eligibility or pricing evidence is supplied.

Correction hypothesis: Compare the verified team-access/export limits and relevant commitments in the same place as the choice. Do not recommend Pro until those facts establish fit. A “Most popular” badge is not evidence that it serves this buyer.

Validation: Give likely buyers a realistic need and ask them to select an option and explain its consequences without revealing the intended plan. Separately verify that prices, restrictions, and selected configuration match the system behavior. Do not invent a completion or conversion target.

## Return

Lead with the decision that lacks necessary support. Connect evidence to the missing information, prediction/decision friction, smallest complete correction, and observable validation. Label proposed defaults and comparisons as hypotheses until supported. No numeric scoring unless requested through the main audit workflow; no purchase or configuration change without authorization.
