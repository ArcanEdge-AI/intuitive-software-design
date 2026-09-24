---
name: purpose-first-redesign
description: Redesign an existing software page or workflow when the user grants broad creative freedom and wants to discuss how it should work. Map the page's real purpose, users, data, actions, and downstream flows first; use GitNexus when available. Treat the current layout as evidence, not a constraint, and do not implement until the user asks.
---
<!-- Copyright 2026 ArcanEdge AI. Licensed under Apache-2.0; preserve this notice when redistributing. Source: https://github.com/ArcanEdge-AI/intuitive-software-design -->

# Purpose-First Redesign

Use this skill when an existing page may need more than incremental cleanup and the user wants to rethink how it should work before implementation.

The objective is to design around the user's job, not around the current component tree, database model, or visual layout.

## Required foundation

Read the foundation, UI/Flow/Feel model, Intuitive Software Loop, design principles, design process, and guardrails in [the Intuitive Software Design Standard](../intuitive-software-design/references/intuitive-software-design-standard.md). Read [the examples](../intuitive-software-design/references/examples.md) when they help distinguish task structure from visual treatment. Apply the standard's [recovery and validation contract](../intuitive-software-design/references/intuitive-software-design-standard.md#recovery-and-validation-contract) to the proposed experience; the brief's states and validation items below summarize it, and the standard controls.

This is a `DESIGN` workflow informed by evidence from an existing product. Existing behavior is observable evidence; the proposed redesign remains a design hypothesis until validated with intended users.

## 1. Establish the redesign frame

Identify or reasonably infer:

- intended user and relevant domain experience;
- job the page should help them complete;
- starting point and successful end state;
- frequency, consequence, permissions, device, and time-pressure constraints;
- evidence available and important evidence still missing.

Ask only when a missing fact would materially change the product model. Do not start with components, cards, tables, or visual trends.

## 2. Map the page's real purpose

When GitNexus is available and the codebase is indexed, use it before proposing the redesign:

1. Read the repository context and check index freshness.
2. Query for the page, route, and the user job it supports.
3. Inspect the primary screen symbol and important callers/callees.
4. Read relevant process traces.
5. Verify implementation-relevant findings in current source and tests.

Trace this minimum product map:

```text
Route and entry points
  -> screen composition
  -> data sources and derived state
  -> visible and hidden actions
  -> downstream destinations and workflows
  -> role and permission gates
  -> loading, empty, failure, partial, and recovery states
```

Also inspect the rendered page when available. Exercise only safe, reversible interactions needed to understand behavior. A screenshot alone does not prove flow, responsiveness, keyboard operation, or recovery.

If GitNexus is unavailable, stale, or missing the repository, say so and use repository search, source inspection, tests, documentation, and runtime evidence instead. Never invent a process trace.

## 3. Separate purpose from inheritance

When domain objects, relationships, or lifecycle meaning are unclear, use [Product Mental Model](../product-mental-model/SKILL.md) to compare the user's inferred concepts with the implementation map. When work crosses actors or external systems, use [Multi-Role Workflow](../multi-role-workflow/SKILL.md) to identify ownership, shared states, and handoff boundaries before proposing structure.

Create two explicit inventories:

- **Must preserve:** domain contracts, consequential actions, permissions, data requirements, safe recovery, and proven useful behavior.
- **Free to rethink:** layout, grouping, navigation model, information hierarchy, interaction pattern, progressive disclosure, and visual composition.

Treat the current layout as evidence of what exists, not a requirement for what comes next. Do not preserve a table, card grid, dashboard, wizard, or side panel merely because it is already implemented.

## 4. Define the user's operating loop

Describe the intended sequence through:

```text
Orient -> Recognize -> Predict -> Act -> Confirm -> Continue
```

For the page, identify:

- the question the user is trying to answer on arrival;
- the first meaningful action;
- the information required before acting;
- the result and feedback after acting;
- the next useful destination or action;
- how context, filters, selection, and work survive return or interruption.

Inventory meaningful decisions and reduce Decision Density by deferring only choices that can safely wait.

Use [User-Task Walkthrough](../user-task-walkthrough/SKILL.md) to ground this loop in the intended person's knowledge and visible decision cues before proposing the product model. Trace the important existing journey and relevant continuation/recovery, then distinguish it from the proposed journey. Implementation knowledge from the purpose map must not silently become user knowledge.

When the page depends on saved work, identity, or a task continuing across devices, platforms, products, or services, use [Connected Experience Design](../connected-experience-design/SKILL.md) for those boundaries. Keep the redesign centered on the user's outcome; do not turn a product map into a request for universal sync or an architecture rewrite.

## 5. Propose the strongest product model

Recommend one coherent direction, not a pile of interchangeable mockups. Include alternatives only when they represent materially different workflows or tradeoffs.

Define:

- information architecture and primary hierarchy;
- direct actions and navigation behavior;
- beginner recognition and expert efficiency;
- default, loading, empty, pending, success, failure, partial, permission, and recovery states that actually apply;
- responsive and keyboard interaction contracts;
- what should remain visible versus progressively disclosed;
- measurable acceptance criteria.

Creative freedom does not waive evidence discipline. Novelty must reduce operating effort or improve task confidence.

For consequential choices, use [Decision-Support Design](../decision-support-design/SKILL.md). Load [findability](../intuitive-software-design/references/findability.md), [UI language](../intuitive-software-design/references/ui-language.md), or [experience progression](../intuitive-software-design/references/experience-progression.md) only when those concerns affect this redesign.

## 6. Hold a design discussion before implementation

Return a discussion-ready brief containing:

1. **Purpose map** — what the page owns and where it leads.
2. **Primary diagnosis** — the earliest broken Intuitive Software Loop stage and main friction source.
3. **Recommended experience** — how the page should work from arrival through continuation.
4. **Screen structure** — a concise text wireframe or flow only when it clarifies relationships.
5. **Key decisions and tradeoffs** — choices that materially affect the product.
6. **States and recovery** — for each consequential action: the pending, success, failure, and partial states that apply; failure that keeps entered work and choices with a clear way to continue or try again; the branches the evidence names, such as eligibility windows; and a confirmation of the actual resulting state that states only what the evidence establishes.
7. **Validation** — a functional check of the resulting state and a check with intended users that states their goal without naming the control, plus the observable result that would show the redesign works. Do not invent targets or findings; lagging signals such as support volume only supplement these checks.
8. **Discussion prompt** — the smallest set of decisions the user should confirm.

Do not edit source, generate implementation files, or launch a build during this discovery/design pass unless the user explicitly asks for implementation in the same request.

## Quality gate

Before returning, verify that:

- the recommendation follows the user's job rather than technical architecture;
- GitNexus or the stated fallback evidence supports the purpose map;
- UI, Flow, and Feel are separated where evidence allows;
- observations, inferences, and design hypotheses are distinguishable;
- the current layout has not silently constrained the proposal;
- necessary risk controls and recovery remain intact;
- states, recovery, and validation meet the recovery and validation contract;
- the result is specific enough to discuss and later implement.
