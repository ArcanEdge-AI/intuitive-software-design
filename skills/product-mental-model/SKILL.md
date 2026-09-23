---
name: product-mental-model
description: Map the objects, relationships, lifecycle states, and language an intended user works with before shaping product navigation or screen structure. Use when a UI exposes implementation modules, the product model is unclear, or a workflow needs information architecture grounded in domain work.
---

# Product Mental Model

Explain the product in the intended person's terms before deciding its screen structure. Read the foundation, mental-model alignment, and guardrails in [the standard](../intuitive-software-design/references/intuitive-software-design-standard.md). Do not replace domain contracts with invented simplifications.

## Build two models

Establish the intended user, job, starting knowledge, success, and evidence limits. Extract task-relevant vocabulary from the brief, domain documents, existing UI, source, and supplied research. User research can support a mental-model claim; UI and code alone show the product's model, not what people actually think. Label inferred user models as hypotheses.

Map only the objects and relationships needed for the task:

| User concept | Relationship / ownership | Lifecycle and meaningful transitions | Where the user recognizes it | Evidence / uncertainty |
| --- | --- | --- | --- | --- |

Distinguish an object's identity from its status, its parent from its owner, and an action from a navigation destination. For example, “Approved” may be a proposal state rather than a separate object. Do not infer cardinality, ownership, or legal meaning from names alone.

Separately inspect the implemented model: routes, entities, modules, permissions, and downstream effects. Where source is available, verify important relationships and transitions against current code/tests; otherwise mark them unknown. Compare the models for:

- concepts split across unrelated modules or multiple labels for the same thing;
- distinct concepts merged under a vague name;
- lifecycle transitions hidden as generic edits;
- dependencies users must understand but cannot see;
- relationships or terminology that differ materially across roles.

Implementation structure can be appropriate. Recommend a change only when a specific mismatch adds interpretation, navigation, memory, or process work.

## Propose a coherent structure

State what the product should help the person understand: which object they are working on, how it relates to the job, its state, available actions, and where work goes next. Propose grouping/navigation in those terms before components. Preserve identity, permissions, domain terminology, and consequential transitions.

Use [the task walkthrough](../user-task-walkthrough/SKILL.md) to check that the proposed structure supports the job from entry through continuation. Use [findability guidance](../intuitive-software-design/references/findability.md) when labels/grouping are the concern. A diagram or object table is optional when it clarifies relationships; it is not proof of usability.

## Example

Fixture: The brief describes “prepare a proposal for a client's project.” The UI has separate menus for Clients, Projects, Documents, and Pricing. Source connects proposal records to projects and recipients, but no research is supplied.

Hypothesis: A project-centered proposal entry point may match this job better than searching a global Documents module. Confirm existing access paths and role needs before recommending regrouping. Keep the global library if it supports cross-project work; do not force every role into one hierarchy.

Validation: Ask intended users where they would look to prepare or retrieve a proposal without naming the destination. Verify that any proposed grouping preserves authorized access and existing relationships. Do not claim a better mental model merely because a diagram is cleaner.

## Return

Give a compact user-concept map, supported implementation mismatches, smallest structural correction, preserved contracts, and concrete validation. Separate observed product structure from inferred user expectations. Avoid unrequested scores, invented research, schema changes, and implementation unless authorized.
