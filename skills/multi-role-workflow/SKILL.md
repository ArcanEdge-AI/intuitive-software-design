---
name: multi-role-workflow
description: Map product work across people, permissions, ownership, queues, and external handoffs. Use when a task requires submission, review, approval, processing, or collaboration and one person's completion depends on another actor or system.
---
<!-- Copyright 2026 ArcanEdge AI. Licensed under Apache-2.0; preserve this notice when redistributing. Source: https://github.com/ArcanEdge-AI/intuitive-software-design -->

# Multi-Role Workflow

Follow the whole job across actors, not only the current person's last screen. Read evidence discipline, context preservation, feedback, recovery, Critical Failures, and guardrails in [the standard](../intuitive-software-design/references/intuitive-software-design-standard.md).

## Define the actors and shared work

Establish the overall outcome and each actor's legitimate subtask. Identify the object being handed off, current owner, state, authority to act, needed information, and completion signals. Include relevant external systems or offline work from supplied evidence; do not invent email, spreadsheet, or operational dependencies.

Build the role inventory before tracing the steps. For each assignment or decision, record the product's role label, the work it owns, and its scope. Inspect both the shared record and any parts assigned independently. When the interface supports different assignment modes, check the controls and saved assignments for each in-scope mode. Use a walkthrough or test fixture to establish the route it exercises, then check the other modes in the current implementation or specification.

Keep separately assigned roles distinct even when they share a workspace, permissions, or a person. A record owner and a specialist responsible for an assigned part have different scopes. Use the role's label from the evidence and state when its assignment applies. Group labels only when the evidence shows their responsibilities are interchangeable throughout the scoped workflow. Keep a supported role in the inventory when its entry point or actions are unknown, and state the gap.

When a broad role in a summary or permission check differs from the role named by the assignment controls, saved assignment, or relevant test, trace those sources together before naming the actor. Use the assigned role's label for the route shown. Keep broader eligibility in the authority description and conflicting or older labels in the evidence note. Combine labels only if the sources establish them as aliases for the same assignment mode and responsibility. Record both whole-record and part-level assignments when the evidence supports both. The test account's job title or permission alone cannot establish who owns the work.

Before mapping the actions that follow an assignment, reconcile the assignment controls and saved work with the role inventory. Give each evidenced assignee a `people` entry and link it from the assigning step's [`assignments` field](../user-task-walkthrough/references/journey-map.md#write-the-record). Keep a role with a known assignment in that list even when the sources leave its next action open.

| Stage / shared object | Actor and authority | Input and prerequisite | Action / transition | Next owner and visible acknowledgment | Failure / recovery | Evidence |
| --- | --- | --- | --- | --- | --- | --- |

Separate **permission**, **responsibility**, and **visibility**. A manager who can view a request may not own its next action. A successful submission does not prove delivery, review, approval, processing, or payment. Treat a service or integration as a system boundary with a real state transition, not automatically as another human role. When the same work must continue across devices or products, use [Connected Experience Design](../connected-experience-design/SKILL.md) for the relevant task and state continuity.

## Inspect consequential handoffs

At every change of owner, identify the work being transferred, the condition that sends it, the role that can act on it, the place where that role picks it up, and the confirmation available to each side. For a new or copied record, check the assignment actually saved for that outcome and trace the receiving action on that record. A sender's access to the original record or a confirmation link establishes neither who owns the resulting work nor where they can act. Include stalled delivery, reassignment, or return for correction when those outcomes change who has the next action.

When work changes hands, give the sender and each materially different receiving role their own actionable step. A step describes the named actor's work and where that actor does it. An alternate route that changes who acts needs its own destination step, even when it reaches the same saved result as another route. Distinguish a person acting on their own behalf from someone authorized to act or record a result on their behalf. Use the handoff to show the relationship between those steps. Leave an unsupported action location unknown.

For the task, check:

- whether the initiating actor can tell what was handed off, to whom, and what happens next;
- whether the receiver can discover and understand pending work with sufficient context;
- whether shared states distinguish submitted, received, in review, approved, rejected, processed, and failed when those meanings apply;
- whether amendments, returns, cancellation, and failed delivery preserve ownership and history;
- whether simultaneous edits, stale approvals, duplicate processing, or reassignment affect correctness;
- whether external completion is acknowledged and reconciliation/retry is clear when evidence supports such a boundary;
- whether a downstream service actually accepted or completed its stage, rather than merely receiving a request;
- whether each role sees appropriate information without exposing another role's private data.

Select checks by actual risk and scope. Do not add an enterprise queue or audit system to a simple workflow without a demonstrated need. An email notification alone does not prove the recipient can access or act on the object.

Use [user-task walkthrough](../user-task-walkthrough/SKILL.md) for each materially different actor journey and [product mental model](../product-mental-model/SKILL.md) if shared objects/states are unclear. Preserve role differences rather than averaging them into one usability judgment.

## Evidence and actions

Source and tests may support role rules but do not prove runtime authorization. A screenshot from one role cannot establish another role's experience. Exercise role transitions only in an authorized environment with appropriate accounts/fixtures. Do not send real notifications, approve requests, change permissions, impersonate roles, or process payments merely to complete a map. Mark untested handoffs and access behavior unknown.

## Example

Fixture: An employee's request shows “Complete” after submission. A manager queue screenshot lists that request as Pending. Finance behavior is not supplied.

Observed product states conflict in their apparent completion scope; actual confusion is an inference. A smaller correction may be “Submitted — awaiting manager review” for the employee while preserving the manager's actionable Pending state. Finance processing and access remain unknown. Do not claim end-to-end completion or invent a payment step.

Validation: In an authorized fixture, verify the handoff, receiver entry point, state agreement, relevant return path, and role-appropriate access. Separately ask each actor to explain what has happened and who acts next, without coaching them with the intended states.

## Return

Provide the actor/state map, consequential gaps, evidence-supported smallest corrections, selected failure/return paths, and validation per boundary. Identify critical misrouting, unauthorized disclosure, or irreversible effects separately. No unrequested scores or live workflow changes.

For an interactive map, use the [journey record format](../user-task-walkthrough/references/journey-map.md#write-the-record). Give each role in the inventory its own `people` entry with its responsibility and scope, including roles without a separate screen. Name the acting role on the step and add `authority` where the owner and permitted actors differ. Attach a handoff to the specific continuation that transfers the work. A successful send and a receiving queue entry each deserve their own evidence when available. If the receiver or acknowledgment is unknown, retain the known transition and record the gap in the step. Before rendering, follow every in-scope handoff and alternate receiver route. Verify that it leads to a reachable step with the right actor, action, and action location. If a checkpoint's action describes work by several actors, split those actions into linked steps.
