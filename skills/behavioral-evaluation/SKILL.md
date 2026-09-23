---
name: behavioral-evaluation
description: Prepare or assess controlled evaluations of Intuitive Software Design agent outputs using realistic UI task fixtures and separate acceptance criteria. Use when testing plugin quality or comparing plugin versions; not for scoring a live product's usability or treating agent results as human research.
---
<!-- Copyright 2026 ArcanEdge AI. Licensed under Apache-2.0; preserve this notice when redistributing. Source: https://github.com/ArcanEdge-AI/intuitive-software-design -->

# Behavioral Evaluation

Evaluate whether this plugin changes an agent's decisions in useful, evidence-grounded ways. Package validation, agent-output quality, and human usability are different results. Keep the authoritative [standard](../intuitive-software-design/references/intuitive-software-design-standard.md) as the interpretation boundary.

## Prepare a bounded comparison

Establish the question, candidate version, baseline if any, case selection, permitted resources/actions, and evaluation budget. Preparing prompts is not authority to dispatch models, spawn helpers, spend credits, access a live system, or publish results. Use the user's authorized route/settings for actual execution; record model, effort, tools, and environment rather than assuming defaults.

Use [the case index](references/case-index.md) to choose relevant fixture packets. Every packet contains a task and raw artifacts; [the assessor rubric](references/assessor-rubric.md) contains acceptance criteria. For a quality evaluation, provide the execution task only the selected packet and plugin, not the rubric, expected diagnosis, or prior answer. Read the rubric when assessing outputs, not as additional task context. Do not load all cases by default.

Cases are fictional and static. They measure reasoning from the supplied artifacts, not operation of a real UI. For runtime evaluations, separately record authorized fixture setup, actual interactions, and state evidence.

## Execute without contaminating the result

Use a fresh task for each condition where feasible. Keep raw task, artifacts, model/effort, tool availability, and output requirements comparable. State any difference that could explain a result. Do not give the candidate extra research or the baseline the candidate's instructions. Record the exact package version and skill availability; a source-path test is not installed-catalog activation.

Preserve the raw answer and relevant tool evidence before assessing it. Do not rewrite a response into a passing one. If execution cannot proceed, record Not run and the blocker instead of a result. A single uncontrolled example is exploratory evidence, not measured improvement.

## Assess supported behavior

Read the rubric after output capture. For each selected case, mark its gates Pass, Partial, Fail, or Not evaluated with an output excerpt or precise evidence pointer. Partial means some required behavior is present but incomplete; Not evaluated means evidence is insufficient, not success. Explain disagreements with the gate using the standard and fixture rather than silently changing expected results.

Look for meaningful diagnosis, appropriate evidence boundaries, preserved expertise/contracts, complete corrections, and concrete validation. Also check false positives: unnecessary simplification, invented research, unsupported runtime claims, and unauthorized actions. Keyword or heading presence alone is not a behavioral pass.

Use [the comparison record](references/comparison-record.md) to preserve outputs, provenance, gate results, regressions, and limits. Do not compute an aggregate that hides a critical failure or silently excludes failed/not-run cases. Keep this evaluation rubric separate from the product audit's 0–4 scores.

## Improve only what evidence supports

Identify a repeatable error or a specific instruction gap before revising the plugin. Rerun affected cases and relevant counterexamples after the change; retain unaffected accepted results with version provenance. Do not add a universal rule for every one-off response.

Report what ran, what was assessed, and whether improvements are supported under comparable conditions. Human discoverability, task success, and confidence remain unvalidated unless actual intended-user research supports them. Never claim a plugin-quality percentage or broader reliability from an unexecuted kit.
