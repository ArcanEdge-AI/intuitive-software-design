# Intuitive Software Design

![ArcanEdge icon](assets/logo.png)

Version 1.5.0

## Overview

Intuitive Software Design helps an agent connect what a person sees to what the product does behind the scenes. It examines the user's goal, mental model, decisions, roles, saved state, connected services, and recovery paths so the experience makes sense from start to finish.

The standard uses three lenses:

| Lens | What it examines |
| --- | --- |
| **UI** | Whether people can find, understand, and operate the controls in front of them. |
| **Flow** | Whether the steps, decisions, state changes, and handoffs support the task. |
| **Feel** | Whether the experience earns confidence through clear feedback, reliable outcomes, and considerate effort. |

## Try it

Ask naturally. For example:

```text
Review this checkout flow from the customer's point of view.
Walk through how a first-time visitor decides whether to request a demo.
Map the user's mental model before we reorganize this dashboard.
Trace this approval from submission through review and completion.
Check how the task continues across devices and connected services.
Suggest the smallest complete change that would make this experience clearer.
```

The main skill routes the request into **Design**, **Review**, **Audit**, or **Improve** guidance and loads supporting references only when they help.

## What's included

| Skill | Use it to |
| --- | --- |
| `intuitive-software-design` | Apply the central standard to design, review, audit, or improve a product experience. |
| `purpose-first-redesign` | Understand a product's purpose and current structure before proposing a redesign. |
| `user-task-walkthrough` | Trace a person's task, decisions, completion, and recovery. Make an interactive journey map when requested. |
| `product-mental-model` | Align product concepts, content, and navigation with how users understand the work. |
| `decision-support-design` | Help people compare options, understand trade-offs, and choose with confidence. |
| `multi-role-workflow` | Clarify ownership, state transitions, handoffs, and recovery across roles. |
| `journey-analytics` | Measure next actions, completion, waiting time, rework, and recovery by cohort using supplied data. |
| `connected-experience-design` | Design task-relevant continuity across devices, platforms, products, and services. |
| `behavioral-evaluation` | Run a structured, separate assessment of agent outputs with controlled scenarios. |

The skills share one authoritative standard rather than maintaining competing definitions. Supporting files include audit and review templates, worked examples, scoring guidance, UI language and findability references, and six Mermaid diagrams.

## Interactive journey maps

Try asking “Map how a staff member completes this task. Include the pending state and how they recover from a failure. Give me an interactive HTML page.”

The walkthrough saves `journey.json` and renders a standalone `index.html` with Python 3.8 or newer and no third-party dependencies. It can trace an existing workflow from evidence or map a product idea with proposed paths and explicit assumptions. The HTML opens on the main route. Use **Alternate paths** to reveal branches and select a step to see its actions, outcomes, and handoffs.

**Coverage** links scenarios to their checkpoints and shows open evidence questions on the affected steps. **Journey outcomes** shows measured results and data coverage by cohort when evidence is available. **What to change** connects consequential friction to options, their supporting evidence and tradeoffs, and what to test before choosing. Use **Preview proposed flow** to click through a proposed change and its recovery paths with sample data. The [journey map workflow](skills/user-task-walkthrough/references/journey-map.md) explains how to refresh the record and regenerate the page.

## The design loop

1. **Start with the person's goal.** Identify what they came to do and what they need to know.
2. **Map the product they encounter.** Connect concepts, navigation, decisions, roles, and system boundaries.
3. **Walk through the task.** Follow meaningful states from entry through completion, including errors and recovery.
4. **Evaluate the experience.** Look for friction, prediction gaps, unnecessary decision density, and critical failures across UI, Flow, and Feel.
5. **Recommend a complete improvement.** Make the smallest change that resolves the supported problem without hiding backend constraints from the user.
6. **Check the evidence.** Separate observed behavior from assumptions and verify predictions with the product and intended users.

The plugin treats synchronization as a product decision, not a default. It asks which information should continue across systems, who may see it, what happens when services disagree, and how a person can recover.

## Behavioral evaluation

The bundled evaluation skill helps teams run separate, controlled comparisons. The earlier evaluation round demonstrated no improvement on the cases it tested. The [full project repository](https://github.com/ArcanEdge-AI/intuitive-software-design/tree/main#behavioral-evaluation) documents the development cases, the frozen validation suite and its limitations.

## About ArcanEdge

Intuitive Software Design is published by [ArcanEdge](https://www.arcanedge.ai/). Its guiding principle is simple: do the hard system work so people can complete their task with clarity, confidence, and as little unnecessary effort as possible.

## License

The plugin instructions, code, and documentation are licensed under the [Apache License 2.0](LICENSE). You may use, modify, and distribute them, including in commercial products, subject to the license terms. The ArcanEdge artwork in logo artwork is excluded and governed by [its separate license](assets/LICENSE).

For a modified fork, remove the reserved logo file, the `composerIcon` and `logo` paths in the Codex manifest, and the README header image unless you have separate permission to use the artwork. The plugin tests accept that unbranded configuration.

If you distribute this project or a derivative based on it, retain the license and the ArcanEdge attribution notice in [NOTICE](NOTICE), as required by the license. Each main skill file also carries a short source notice so attribution travels with individually reused skills. You do not have to publish private changes or contribute improvements back. The license does not grant permission to use ArcanEdge names or marks as your own branding.
