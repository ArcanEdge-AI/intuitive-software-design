<p align="center">
  <img src="assets/logo.png" alt="ArcanEdge gold geometric mark" width="180" />
</p>

<h1 align="center">Intuitive Software Design</h1>

<p align="center"><strong>Engineer the backend so well that users get a smooth, likeable experience with minimal effort.</strong></p>

<p align="center">An evidence-grounded plugin for designing, reviewing, and improving software around the real tasks people need to complete.</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.3.1-9F7AEA?style=for-the-badge" alt="Version 1.3.1" />
  <img src="https://img.shields.io/badge/skills-8-2563EB?style=for-the-badge" alt="Eight focused skills" />
  <img src="https://img.shields.io/badge/harness-Claude%20Code%20%7C%20Codex-111827?style=for-the-badge" alt="Claude Code and Codex plugin formats" />
  <img src="https://img.shields.io/badge/license-Apache--2.0%20%2B%20reserved%20artwork-9F7AEA?style=for-the-badge" alt="Apache-licensed skills and reserved artwork" />
</p>

<p align="center">
  <a href="#overview">Overview</a> ·
  <a href="#install">Install</a> ·
  <a href="#try-it">Try it</a> ·
  <a href="#whats-included">What's included</a> ·
  <a href="#the-design-loop">Design loop</a> ·
  <a href="#behavioral-evaluation">Evaluation</a> ·
  <a href="#license">License</a>
</p>

## Overview

Intuitive Software Design helps an agent connect what a person sees to what the product does behind the scenes. It examines the user's goal, mental model, decisions, roles, saved state, connected services, and recovery paths so the experience makes sense from start to finish.

The standard uses three lenses:

| Lens | What it examines |
| --- | --- |
| **UI** | Whether people can find, understand, and operate the controls in front of them. |
| **Flow** | Whether the steps, decisions, state changes, and handoffs support the task. |
| **Feel** | Whether the experience earns confidence through clear feedback, reliable outcomes, and considerate effort. |

It is designed for product and coding agents working on websites, applications, and cross-platform workflows. The package includes native plugin manifests for Claude Code and Codex, with reusable guidance organized as focused skills.

## Install

### Claude Code

For a local trial from the repository root:

```bash
claude --plugin-dir .
```

Once this version is on the repository's default branch, Claude Code users can add the [ArcanEdge marketplace](.claude-plugin/marketplace.json) and install the plugin:

```text
/plugin marketplace add ArcanEdge-AI/intuitive-software-design
/plugin install intuitive-software-design@arcanedge-plugins
```

When the plugin is available in Claude's directory, find **Intuitive Software Design** in the plugin browser and install it there.

### Codex

Install **Intuitive Software Design** from the Codex plugin marketplace. In a task, mention the plugin by name or describe the work you want help with.

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
| `user-task-walkthrough` | Trace a person's goal, knowledge, decisions, expected consequences, completion, and recovery. |
| `product-mental-model` | Align product concepts, content, and navigation with how users understand the work. |
| `decision-support-design` | Help people compare options, understand trade-offs, and choose with confidence. |
| `multi-role-workflow` | Clarify ownership, state transitions, handoffs, and recovery across roles. |
| `connected-experience-design` | Design task-relevant continuity across devices, platforms, products, and services. |
| `behavioral-evaluation` | Run a structured, separate assessment of agent outputs with controlled scenarios. |

The skills share one authoritative standard rather than maintaining competing definitions. Supporting files include audit and review templates, worked examples, scoring guidance, UI language and findability references, and six Mermaid diagrams.

## The design loop

1. **Start with the person's goal.** Identify what they came to do and what they need to know.
2. **Map the product they encounter.** Connect concepts, navigation, decisions, roles, and system boundaries.
3. **Walk through the task.** Follow meaningful states from entry through completion, including errors and recovery.
4. **Evaluate the experience.** Look for friction, prediction gaps, unnecessary decision density, and critical failures across UI, Flow, and Feel.
5. **Recommend a complete improvement.** Make the smallest change that resolves the supported problem without hiding backend constraints from the user.
6. **Check the evidence.** Separate observed behavior from assumptions and verify predictions with the product and intended users.

The plugin treats synchronization as a product decision, not a default. It asks which information should continue across systems, who may see it, what happens when services disagree, and how a person can recover.

## Behavioral evaluation

The evaluation kit contains eleven fictional scenario packets, a separate assessor rubric, and a comparison record. Cases 01–06 are example-aligned regression cases; they must not be presented as independent evidence of generalization. Cases 07–11 broaden coverage.

The [`evals/`](evals/) directory holds development and regression cases for `claude plugin eval`. They shaped the plugin's development, so their results are not independent evidence of improvement. Their directory names still contain `heldout` from when they were first written. Each case supplies raw product evidence rather than stating the constraints it is graded on, keeps its graders out of the agent prompt, and scores several independent criteria, so the baseline comparison can show partial differences. A case passes only when every scored criterion passes. Changing a case's prompt or a scored grader creates a new case version (a `-vN` directory) whose scores are not compared with earlier versions.

[`evals-holdout/`](evals-holdout/) is the frozen validation suite (v1) for the candidate at commit `43f042d`. A separate author agent wrote its five cases without seeing any plugin instructions, earlier answers, or graders. Its prompts, criteria, and [analysis plan](evals-holdout/ANALYSIS-PLAN.md) were frozen with SHA-256 hashes before the run.

The suite ran on 2026-09-25 with `claude-sonnet-5`, a Sonnet judge, and three runs per arm, and **no improvement was demonstrated on these cases**. With and without the plugin, every completed answer met all 24 criteria under both the automated judge and a blind review, a pooled difference of +0.00; one no-plugin run timed out and was excluded. Three limitations apply: the cases did not discriminate, the judge and the blind reviewers were all Sonnet models, and no human audit was done.

The v1 round is closed. Do not cite either suite as evidence that the plugin improves outcomes. After any later plugin change, these cases no longer count as held out for that change.

These fixtures support repeatable review; they do not prove that a model evaluation or human usability study has been run. Walkthrough predictions remain hypotheses until checked against the real product and intended-user evidence. Record not-run cases honestly and compare versions with matching inputs and settings where practical.

Claude Code v2.1.269 or later can run the `evals/` suite with `claude plugin eval . --ablation with-without --no-publish --model <approved-model> --judge-model <approved-judge-model> --runs <approved-runs> --max-cost-usd <approved-budget>`. This suite is designed for two-arm comparison. Do not use `--ablation none` with its default 1.0 threshold: a correct run may invoke a skill or read its file without doing both, yet single-arm scoring counts both routing indicators. The run uses model calls, so choose the models, runs, and budget deliberately. If it is noninteractive and the plugin is trusted, add `--trust-plugin`. In two-arm comparisons, the routing, standard-read, and vocabulary graders are unscored indicators. A matching tool call shows the relevant skill was invoked or read; it does not prove the answer followed it. Interpret both indicators with the scored result and trace. The automated CI checks package structure and manifests only; it does not spend on behavioral evals.

## Validate the package

From the repository root:

```bash
python tests/test_plugin.py
claude plugin validate --strict .
```

The structural tests check the package and its routing expectations. Use a fresh agent session for behavior checks so it loads the current plugin version.

## Repository map

```text
.
├── .claude-plugin/       # Claude Code plugin and marketplace manifests
├── .codex-plugin/        # Codex plugin manifest
├── assets/               # Reserved ArcanEdge plugin artwork and its license
├── evals/                # Development and regression eval cases
├── evals-holdout/        # Frozen validation suite v1 for candidate 43f042d
├── LICENSE               # Apache License 2.0
├── NOTICE                # Attribution to ArcanEdge AI and source repository
├── skills/               # Eight self-contained skill workflows
└── tests/                # Structural checks and forward-test scenarios
```

## About ArcanEdge

Intuitive Software Design is published by [ArcanEdge](https://www.arcanedge.ai/). Its guiding principle is simple: do the hard system work so people can complete their task with clarity, confidence, and as little unnecessary effort as possible.

## License

The plugin instructions, code, and documentation are licensed under the [Apache License 2.0](LICENSE). You may use, modify, and distribute them, including in commercial products, subject to the license terms. The ArcanEdge artwork in `assets/logo.png` is excluded and governed by [its separate license](assets/LICENSE).

For a modified fork, remove the reserved logo file, the `composerIcon` and `logo` paths in the Codex manifest, and the README header image unless you have separate permission to use the artwork. The plugin tests accept that unbranded configuration.

If you distribute this project or a derivative based on it, retain the license and the ArcanEdge attribution notice in [NOTICE](NOTICE), as required by the license. Each main skill file also carries a short source notice so attribution travels with individually reused skills. You do not have to publish private changes or contribute improvements back. The license does not grant permission to use ArcanEdge names or marks as your own branding.
