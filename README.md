# Intuitive Software Design

Intuitive Software Design is a self-contained Codex plugin for designing, reviewing, auditing, scoring, and improving software interfaces and workflows. It turns “make it intuitive” into an evidence-grounded system centered on the intended user, UI/Flow/Feel, the Intuitive Software Loop, Prediction Gap, Decision Density, friction types, 0-4 behavioral scoring, severity, and Critical Failures.

**License:** `UNLICENSED`. No reuse license is granted by this public repository.

## What is included

- one routed Codex skill with `DESIGN`, `REVIEW`, `AUDIT`, and `IMPROVE` modes;
- a purpose-first redesign skill that maps an existing page with GitNexus before proposing a fresh product model;
- a user-task walkthrough skill that traces a person's knowledge, decisions, expected consequences, completion, and recovery across applications and websites;
- product mental-model, decision-support, and multi-role workflow skills;
- focused findability, UI-language, and experience-progression references loaded only when relevant;
- a behavioral evaluation skill with eight raw fixture packets, a separate assessor rubric, and a comparison record;
- the authoritative Intuitive Software Design Standard;
- detailed screen, workflow, and product scoring guidance;
- six explanatory Mermaid diagrams and concrete before/after examples;
- reusable audit and AI-review templates;
- structural tests plus ten forward-test scenarios (behavioral prompts, not proof of executed model evaluations).

No MCP server, external app, backend, account, or network service is required.

## Install in Codex

The source is designed for the personal marketplace layout:

```text
<user-profile>/plugins/intuitive-software-design
<user-profile>/.agents/plugins/marketplace.json
```

The marketplace entry must point to:

```json
{
  "name": "intuitive-software-design",
  "source": {
    "source": "local",
    "path": "./plugins/intuitive-software-design"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Design"
}
```

The default personal marketplace is discovered by Codex. In a Codex build that exposes plugin installation in the app, open the plugin from the local marketplace and install/enable it there. Start a new task after installation or source updates so the task receives the refreshed plugin catalog.

Local updates use the plugin-creator marketplace/cachebuster helpers and `codex plugin add intuitive-software-design@personal`. Start a fresh task after reinstalling; existing tasks do not receive a new catalog automatically. Keep local and published package versions distinct during testing.

## Invoke

Select or mention the **Intuitive Software Design** plugin in Codex, then ask naturally:

```text
@Intuitive Software Design audit this application.
@Intuitive Software Design review this workflow.
@Intuitive Software Design help design this feature.
@Intuitive Software Design score this screen.
@Intuitive Software Design improve this interface.
```

When direct skill syntax is available, the bundled skill can also be invoked as:

```text
$intuitive-software-design audit the create-project workflow.
$purpose-first-redesign map the Projects page and propose how it should work before implementation.
$user-task-walkthrough trace how a first-time visitor would evaluate our service and decide whether to enquire.
$product-mental-model map the user's concepts before reorganizing this interface.
$decision-support-design review this plan-selection step.
$multi-role-workflow trace this request through submission, review, and processing.
$behavioral-evaluation prepare a controlled comparison of this plugin's outputs.
```

Installed plugin catalogs may display the fully qualified skill name as:

```text
intuitive-software-design:intuitive-software-design
intuitive-software-design:purpose-first-redesign
intuitive-software-design:user-task-walkthrough
intuitive-software-design:product-mental-model
intuitive-software-design:decision-support-design
intuitive-software-design:multi-role-workflow
intuitive-software-design:behavioral-evaluation
```

The user normally does not need to choose an internal workflow. The main skill classifies the request as Design, Review, Audit, or Improve and uses a task walkthrough when the outcome depends on discovering, choosing, or completing a task. Walkthrough predictions remain hypotheses until checked against intended-user evidence.

## Validate

From the plugin root, run:

```powershell
python tests/test_plugin.py
python C:\Users\<you>\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\intuitive-software-design
python C:\Users\<you>\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py .
```

Use a fresh Codex process for behavioral testing. The scenario prompts and acceptance gates are in `tests/scenarios/`.

## Test agent-output quality

The reusable kit is in `skills/behavioral-evaluation/`. Start a fresh task with the locally installed plugin and one raw packet from its `references/fixtures/` directory. Give the execution task the packet and plugin, without the assessor rubric or a prior answer. Capture the response, then assess it separately against `references/assessor-rubric.md` and record provenance using `references/comparison-record.md`.

The eight cases cover product structure, decisions, findability, wording, handoffs, experience progression, false success, and appropriate density. Fixtures are fictional; passing them does not establish human usability. Preparing the kit does not dispatch paid model calls. Record not-run cases honestly and compare versions under matching inputs/settings where feasible.

## Authoritative-source rule

`skills/intuitive-software-design/references/intuitive-software-design-standard.md` is authoritative. The scoring reference and templates are operational projections of that standard. If a companion file conflicts, the standard controls and the companion should be corrected.
