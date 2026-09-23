---
name: connected-experience-design
description: Design or review how a user's task, identity, saved state, and service outcomes continue across relevant devices, platforms, products, or external systems. Use when system behavior changes user effort, trust, recovery, or a product promise; do not presume universal synchronization.
---

# Connected Experience Design

Use this skill when a task crosses surfaces or when backend, data, identity, or integration behavior materially changes what a person can do, understand, trust, or recover. Read the [authoritative standard](../intuitive-software-design/references/intuitive-software-design-standard.md), especially the system-backed experience contract. This skill applies that contract through UI, Flow, and Feel; it adds no fourth layer or score.

Do not load it for screen-only styling. Do not treat “connected” as a requirement to sync everything, make platform interfaces identical, or automate away a meaningful user decision.

## Establish the user's job and promise

Identify the intended person, task, realistic starting point, success condition, and evidence. Include the device, platform, account, collaborators, or external service only when they affect this job.

Record any relevant promise made by the product or website, such as work being saved, a task being resumable, or an action being completed elsewhere. Treat a marketing statement as a promise to investigate, not evidence that the capability works. Separate what is visible, documented, implemented, exercised, and still unknown.

## Choose the continuity the task actually needs

These capabilities are related but distinct. Assess only those relevant to the task:

- **Shared identity:** the person can establish which account, organization, or role is active.
- **Shared data:** the relevant domain object and its saved state are available on another surface.
- **Task handoff:** enough task-specific context is preserved for the person to resume useful work.
- **Platform capability:** each supported platform lets the person perform the needed action, using appropriate controls and conventions.
- **Connected action:** a service or another actor receives, processes, or completes a requested operation.

Do not infer shared data from shared sign-in, task handoff from data sync, edit capability from read access, or external completion from request delivery. If no cross-surface continuity is needed or authorized, say so and preserve the justified boundary.

## Trace the experience contract

Map the task through the relevant frontstage and system boundaries:

```text
User intent and product promise
  -> entry surface and active identity/authority
  -> task or domain-object identity
  -> user action and service/integration boundary
  -> actual current and durable state
  -> visible acknowledgment and next step
  -> continuation, correction, or recovery
```

Use a compact trace when more than one boundary matters:

| Task stage | User's question or intent | Visible cue or promise | System behavior and evidence | Actual state and acknowledgment | Continue or recover |
| --- | --- | --- | --- | --- | --- |

Check that object identity, ownership, state meaning, and authority remain coherent. An account can have multiple workspaces; a “Saved” label can refer to a local draft; a submitted request can still await processing. Expose technical boundaries only when they change a meaningful choice, risk, status, or outcome. Do not make people coordinate internal services or databases.

For website-to-product journeys, trace the consequential claim into the first product task that should fulfill it. Include sign-in, onboarding, setup, and the first saved or completed outcome only when they are on that path. Preserve a user's reasonable choice to evaluate, decline, or defer rather than treating conversion as the only success.

## Preserve useful context safely

Recommend the smallest amount of continuation that makes the task easier and more reliable. Identify which object, selection, progress, decision, or status must carry forward, and which interface details can appropriately change by platform.

Consider privacy and authority at each boundary: what information moves, who can access it, whether permissions change by device or role, and whether an action needs fresh consent or confirmation. Prefer task-relevant state over copying all local context. Do not expose sensitive information in notifications, handoff previews, or shared devices without evidence and authorization.

Select failure cases by consequence and evidence. When relevant, inspect offline work, slow or failed delivery, stale data, concurrent edits, duplicate activation, partial external completion, expired identity, and retry/reconciliation. For each selected case, establish what the person can see, whether their work is preserved, who owns the next action, and how they can safely continue. Do not impose an exhaustive matrix on a small task.

## Keep claims within evidence

Distinguish an attempted request, queued or pending work, durable saved state, confirmed external completion, and a usable continuation path. A toast, optimistic update, HTTP request, source path, or unit test alone may not prove the user-visible outcome. Use a suitable read-back, reload, authorized downstream view, state trace, or runtime observation when the claim requires it.

Source can show what code is intended to do; tests can show what a tested case did; runtime evidence can show what happened in that environment. None alone establishes that intended users can discover, understand, or trust the behavior. Label predictions and untested boundaries. Do not invent synchronization guarantees, latency targets, error rates, user research, or production incidence.

## Recommend and validate

Connect each recommendation as:

`observed promise or task barrier -> specific continuity gap -> user effort or risk -> smallest complete correction -> observable validation`

Include the visible status and a useful continuation or recovery path in the proposed interaction. Preserve effective platform differences, purposeful decisions, offline or local-only requirements, and existing privacy controls. Do not propose a new backend, shared account, sync layer, or integration unless the task evidence justifies that change.

Validate relevant behavior at each boundary: the same intended task/object, current identity and authorization, saved or external state, honest acknowledgment, and expected next action. Exercise failure/recovery paths only where scope and risk warrant. Separately validate user comprehension or discoverability with an uncoached task; implementation success is not usability proof.

## Return

State the task and evidence scope. Show the compact boundary trace when useful, then lead with the earliest consequential gap. Separate observations, inferences, and unknowns. Explain whether the need is shared identity, data, task handoff, platform capability, connected action, or none. Give the smallest supported correction and a concrete functional and, when relevant, human validation task. Do not assign numeric scores unless the main audit workflow requests them.

## Completion check

- The cross-surface capability follows a demonstrated user job or an explicit product promise.
- Identity, object/task state, action ownership, and actual completion are distinguished.
- Platform differences, authorization, privacy, and recovery are considered where relevant.
- No universal sync or architecture change is recommended without task-grounded evidence.
- Implementation claims and human usability claims remain within their evidence.
