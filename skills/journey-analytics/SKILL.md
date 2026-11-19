---
name: journey-analytics
description: Analyze supplied behavioral events or aggregates for next actions, completion, waiting time, rework, and recovery in a software journey. Measure by cohort and make eligibility, follow-up windows, and evidence gaps explicit.
---
<!-- Copyright 2026 ArcanEdge AI. Licensed under Apache-2.0; preserve this notice when redistributing. Source: https://github.com/ArcanEdge-AI/intuitive-software-design -->

# Journey Analytics

Use the project's authorized event exports, aggregate reports, or supplied research. Link measurements to the task or decision they describe. For a whole journey, use [User-Task Walkthrough](../user-task-walkthrough/SKILL.md) to map the goal and [Multi-Role Workflow](../multi-role-workflow/SKILL.md) when one person's action hands work to another.

Use the `fixture` basis for supplied synthetic event records or measured aggregates. Test setup, scripted choices, expected assertions, and timeouts describe what a test exercises. Cite them in the route evidence. If the inputs contain only those definitions or product rules, leave decision counts and outcome metrics absent and state what data could support them.

## Define the decision population

1. Identify the product version or environment, step, available choices, and cohort. Use role, starting state, or experience where those differences affect eligibility or interpretation.
2. Define an eligible opportunity. For a visible choice, use people or cases shown the choice while it was available. Account for people who could perform only one option, test traffic, duplicated events, and missing exposure coverage.
3. Choose a capture period, counting unit, and follow-up window appropriate to the task. A repeated click can be one decision opportunity. For work that passes across people, join only on the authorized work item or run and check what each role actually received.

## Measure next actions

- For an event export, map the eligibility and action events to the project step and choices. Count the first recorded mapped action per eligible opportunity within the follow-up window. Inspect timestamps, duplicates, and which late or incomplete opportunities have a full window. Use a local query or script for aggregation so the counts are reproducible.
- For aggregates, confirm that the numerator and denominator describe the same unit, cohort, period, and window. Require mutually exclusive counts for ranking first choices. Preserve known zeros and show unmapped opportunities without assigning them a cause. Missing telemetry, waiting on another role, and confirmed abandonment have different evidence.
- Report counts with the eligible denominator, period, source, and any meaningful capture or sampling limitations. Rank recorded choices within their cohort. Treat low counts, ties, selection bias, and product changes as limits on predictions. Event sequences show what was recorded. Use research with an appropriate task and population to explain possible reasons or suggest hypotheses worth testing.
- Preserve rare high-consequence paths and supported routes with sparse data. A frequently taken route may still signal friction, a requirement, or a default.

## Measure journey outcomes

Define the task's successful outcome from the workflow evidence. For an event export, use a local query or script to group events by the authorized work item or task opportunity, sort them by time, and deduplicate repeated records. Follow each eligible item from a known entry through its own window. For aggregates, verify the source describes the same eligibility, event definitions, and follow-up before reusing a result. Keep independent samples separate even when their cohort labels match.

- **Completion.** Count distinct eligible items with evidence of the specified outcome within the window. Classify other cases from a known terminal result or verified follow-up coverage. Use the result the person came for as the completion event.
- **Waiting time.** Define the start and end of a wait at a queue, handoff, or processing step. Pair valid timestamps for the same item and occurrence. Report median elapsed time for those pairs, or a source-supported mean. State the sample size. Record how many eligible cases lacked a pair when the total is known. Incomplete waits, invalid order, and unknown capture limit what the matched sample can establish.
- **Rework.** Count distinct items with a documented correction or repeat of previously performed work. Specify what qualifies and which items could encounter it. Multiple corrections on the same item contribute one item to a rework rate.
- **Recovery.** Start with distinct items that encountered the documented failure, interruption, or return. Count those reaching a verified resumed state or completed outcome, as defined for the measure. A retry attempt supplies evidence of an attempt. Use its result to determine recovery.

For each count, use the number of eligible items with a known result as the rate denominator. Show that measured count alongside the eligible population. Preserve an explicit measured zero. Keep an unavailable value or an item with incomplete follow-up outside the measured denominator. Anchor missing data as an evidence gap when it limits the decision. Separate verified results from explanations of why people take a path.

## Return results

State the measured behavior, cohort, source, and evidence limits. For a map, use the separate formats for [decision counts](../user-task-walkthrough/references/journey-map.md#record-measured-decisions) and [journey outcomes](../user-task-walkthrough/references/journey-map.md#record-journey-outcomes). Attach only aggregate results and provenance. Keep raw event identifiers and personal information out of the map. Mark synthetic measures as fixtures. When the supplied data cannot support a measurement, document the evidence needed to make it.
