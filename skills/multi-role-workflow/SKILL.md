---
name: multi-role-workflow
description: Map product work across people, permissions, ownership, queues, and external handoffs. Use when a task requires submission, review, approval, processing, or collaboration and one person's completion depends on another actor or system.
---
<!-- Copyright 2026 ArcanEdge AI. Licensed under Apache-2.0; preserve this notice when redistributing. Source: https://github.com/ArcanEdge-AI/intuitive-software-design -->

# Multi-Role Workflow

Follow the whole job across actors, not only the current person's last screen. Read evidence discipline, context preservation, feedback, recovery, Critical Failures, and guardrails in [the standard](../intuitive-software-design/references/intuitive-software-design-standard.md).

## Define the actors and shared work

Establish the overall outcome and each actor's legitimate subtask. Identify the object being handed off, current owner, state, authority to act, needed information, and completion signals. Include relevant external systems or offline work from supplied evidence; do not invent email, spreadsheet, or operational dependencies.

| Stage / shared object | Actor and authority | Input and prerequisite | Action / transition | Next owner and visible acknowledgment | Failure / recovery | Evidence |
| --- | --- | --- | --- | --- | --- | --- |

Separate **permission**, **responsibility**, and **visibility**. A manager who can view a request may not own its next action. A successful submission does not prove delivery, review, approval, processing, or payment. Treat a service or integration as a system boundary with a real state transition, not automatically as another human role. When the same work must continue across devices or products, use [Connected Experience Design](../connected-experience-design/SKILL.md) for the relevant task and state continuity.

## Inspect consequential handoffs

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
