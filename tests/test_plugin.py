#!/usr/bin/env python3
"""Deterministic structural and contract tests for the plugin source."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "intuitive-software-design"
REDESIGN_SKILL = ROOT / "skills" / "purpose-first-redesign"
CONNECTED_SKILL = ROOT / "skills" / "connected-experience-design"
REFERENCES = SKILL / "references"
SCENARIOS = ROOT / "tests" / "scenarios"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def text(path: Path) -> str:
    require(path.is_file(), f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def grader_input_match(body: str) -> re.Pattern[str]:
    match = re.search(r"(?m)^input_match: '(.*)'$", body)
    require(match is not None, "Routing grader lacks input_match")
    return re.compile(match.group(1))


# Grader keys documented for `claude plugin eval`; an unknown key is ignored at run time, so a typo would
# silently change what a paid run measures.
GRADER_KEYS = {
    "regex": {"pattern", "flags", "match", "target"},
    "tool_used": {"tool", "input_match", "min", "max"},
    "tool_order": {"before", "after"},
    "file_exists": {"path", "exists"},
    "llm": {"criteria", "focus"},
    "baseline": {"baseline_file", "criteria"},
}


def grader_frontmatter(body: str) -> dict[str, str]:
    match = re.match(r"---\n(.*?)\n---\n", body, re.DOTALL)
    require(match is not None, "Eval grader lacks frontmatter")
    return dict(re.findall(r"(?m)^([a-z_]+):\s*(.*)$", match.group(1)))


def grader_is_scored(fields: dict[str, str]) -> bool:
    """Scored in a two-arm run: not an unscored plugin-fired indicator (see the plugin-evals docs)."""
    skill_indicator = fields.get("type") == "tool_used" and fields.get("tool") == "Skill"
    return fields.get("arm") != "with-only" and (not skill_indicator or fields.get("arm") == "both")


def test_manifest() -> None:
    manifest_path = ROOT / ".codex-plugin" / "plugin.json"
    manifest = json.loads(text(manifest_path))
    claude = json.loads(text(ROOT / ".claude-plugin" / "plugin.json"))
    require(manifest["name"] == claude["name"] == "intuitive-software-design", "Plugin names disagree")
    require(re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", manifest["version"]) is not None, "Version is not semver")
    require(manifest["version"] == claude["version"], "Codex and Claude versions disagree")
    require(f"version-{manifest['version']}-" in text(ROOT / "README.md"), "README version badge disagrees")
    require(manifest.get("skills") == "./skills/", "Manifest must expose ./skills/")
    require("mcpServers" not in manifest and "apps" not in manifest and "hooks" not in manifest, "Plugin must remain self-contained")
    interface = manifest["interface"]
    require(interface["displayName"] == "Intuitive Software Design", "Display name is not discoverable")
    prompts = interface.get("defaultPrompt", [])
    require(isinstance(prompts, list) and 1 <= len(prompts) <= 3, "defaultPrompt must contain one to three prompts")
    require(all(isinstance(prompt, str) and len(prompt) <= 128 for prompt in prompts), "A default prompt exceeds 128 characters")
    artwork_keys = ("composerIcon", "logo")
    has_artwork = any(key in interface for key in artwork_keys)
    require(all(key in interface for key in artwork_keys) or not has_artwork,
            "Codex artwork paths must be both present or both absent")
    if has_artwork:
        for key in artwork_keys:
            require((ROOT / interface[key]).is_file(), f"Codex {key} image is missing")
        require("excluded" in text(ROOT / "assets" / "LICENSE").lower(),
                "Artwork license must state the Apache exclusion")
    else:
        require(not (ROOT / "assets" / "logo.png").exists(),
                "Unbranded forks must remove the reserved artwork")
        require('<img src="assets/logo.png"' not in text(ROOT / "README.md"),
                "Unbranded forks must remove the README logo reference")
    marketplace = json.loads(text(ROOT / ".claude-plugin" / "marketplace.json"))
    require(any(entry.get("name") == manifest["name"] and entry.get("source") in {".", "./"}
                for entry in marketplace.get("plugins", [])), "Claude marketplace must expose the root plugin")


def test_skill_frontmatter() -> None:
    for path in (ROOT / "skills").glob("*/SKILL.md"):
        body = text(path)
        match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", body, re.DOTALL)
        require(match is not None, f"Missing YAML frontmatter: {path.parent.name}")
        fields = dict(re.findall(r"^([a-z][a-z-]*):\s*(.+)$", match.group(1), re.MULTILINE))
        require(fields.get("name") == path.parent.name, f"Wrong skill name: {path.parent.name}")
        require(bool(fields.get("description", "").strip()), f"Missing description: {path.parent.name}")


def test_skill_contract() -> None:
    skill = text(SKILL / "SKILL.md")
    for token in ("DESIGN", "REVIEW", "AUDIT", "IMPROVE", "Not Evaluated", "Critical Failure"):
        require(token in skill, f"Skill routing/guardrail missing: {token}")
    require("Do not produce a screen redesign by default" in skill, "Improve guardrail is missing")
    require("assign numeric scores unless the user asks" in skill, "Review scoring guardrail is missing")
    require("They do not prove responsiveness" in skill, "Screenshot evidence guardrail is missing")
    require("../purpose-first-redesign/SKILL.md" in skill and "broad creative freedom" in skill,
            "Broad redesign route is missing")
    require("Loop Break:" in skill and "Validation:" in skill, "Finding shape lacks loop or validation")
    # Eval transcripts showed routed runs acting on SKILL.md alone, so the contract summary must live here
    # and point back to the standard, which controls.
    require("## Recovery and validation contract" in skill
            and "references/intuitive-software-design-standard.md#recovery-and-validation-contract" in skill,
            "Main skill must summarize and link the standard's recovery and validation contract")
    require("Behavior Confidence from one observed success path is `NE`" in skill,
            "AUDIT guidance must keep Behavior Confidence NE without representative coverage")
    openai = text(SKILL / "agents" / "openai.yaml")
    require("$intuitive-software-design" in openai, "Skill default prompt must name the skill")


def test_purpose_first_redesign_contract() -> None:
    skill = text(REDESIGN_SKILL / "SKILL.md")
    required = (
        "GitNexus",
        "Route and entry points",
        "Must preserve",
        "Free to rethink",
        "Orient -> Recognize -> Predict -> Act -> Confirm -> Continue",
        "Treat the current layout as evidence",
        "Do not edit source",
        "discussion-ready brief",
        "intuitive-software-design-standard.md#recovery-and-validation-contract",
        "check with intended users that states their goal without naming the control",
    )
    for token in required:
        require(token in skill, f"Purpose-first redesign contract missing: {token}")
    openai = text(REDESIGN_SKILL / "agents" / "openai.yaml")
    require("$purpose-first-redesign" in openai, "Redesign default prompt must name the skill")


def test_connected_experience_contract() -> None:
    skill = text(CONNECTED_SKILL / "SKILL.md")
    required = (
        "Shared identity",
        "Shared data",
        "Task handoff",
        "Platform capability",
        "Connected action",
        "actual current and durable state",
        "universal synchronization",
        "marketing statement as a promise to investigate",
        "privacy and authority",
        "Source can show what code is intended to do",
    )
    for token in required:
        require(token.lower() in skill.lower(), f"Connected-experience contract missing: {token}")
    openai = text(CONNECTED_SKILL / "agents" / "openai.yaml")
    require("$connected-experience-design" in openai, "Connected-experience default prompt must name the skill")


def test_authoritative_standard() -> None:
    standard = text(REFERENCES / "intuitive-software-design-standard.md")
    required = (
        "the intended user can correctly infer what to do next",
        "UI, Flow, and Feel",
        "ORIENT",
        "RECOGNIZE",
        "PREDICT",
        "CONFIRM",
        "CONTINUE",
        "Technical Architecture ≠ User Workflow",
        "System-backed experience",
        "actual saved, shared, or external state",
        "universal synchronization",
        "Prediction Gap",
        "Decision Density",
        "Navigation Friction",
        "Interpretation Friction",
        "Decision Friction",
        "Interaction Friction",
        "Memory Friction",
        "Feedback Friction",
        "Recovery Friction",
        "Process Friction",
        "Intuition Critical Failures",
        "Minimal UI does not automatically mean intuitive UI",
        "The goal is not to eliminate thinking",
        "### Recovery and validation contract",
        "One observed success path is never representative",
    )
    for token in required:
        require(token in standard, f"Authoritative concept missing: {token}")
    finding_format = standard.split("## 37. Finding format", 1)[1].split("## 38. Audit process", 1)[0]
    require("Loop Break:" in finding_format and "Validation:" in finding_format,
            "Standard finding format lacks loop or validation")
    require(standard.count("```mermaid") >= 6, "Standard must include at least six Mermaid diagrams")


def test_scoring_contract() -> None:
    scoring = text(REFERENCES / "scoring-reference.md")
    standard = text(REFERENCES / "intuitive-software-design-standard.md")
    for score in ("0 | Broken", "1 | Difficult", "2 | Understandable", "3 | Intuitive", "4 | Effortless"):
        require(score in scoring, f"Universal score missing: {score}")
    require("NE | Not Evaluated" in scoring, "Insufficient-evidence state is missing")
    screen = (
        "Orientation", "Visual hierarchy", "Action clarity", "Control recognition",
        "Information clarity", "Feedback and state visibility", "Cognitive load", "Consistency",
    )
    workflow = (
        "Entry-point clarity", "Next-action clarity", "Sequence matches user task",
        "Context preservation", "Decision load", "Backtracking required", "Progress visibility",
        "Completion confidence", "Error recovery", "Prediction consistency",
    )
    for criterion in screen + workflow:
        require(f"## {criterion}" in scoring, f"Detailed scoring rubric missing: {criterion}")
    require(scoring.count("**Warning signs:**") == 22, "Every scored criterion needs warning signs")
    require(scoring.count("**Test:**") == 22, "Every scored criterion needs a test method")
    for criterion in ("Outcome predictability", "State feedback", "Cross-context consistency", "Failure recovery"):
        require(criterion in scoring, f"Behavior Confidence input missing: {criterion}")
    require("Do not copy screen or workflow scores" in scoring, "Behavior Confidence must not reuse other scores")
    require("Do not reuse UI or Flow criterion scores" in standard, "Standard does not define distinct Behavior Confidence inputs")
    audit = text(REFERENCES / "audit-template.md")
    require("| Expected outcome and affected object | Observed action, result, and state |" in audit
            and "Behavior Confidence coverage:" in audit,
            "Audit template lacks interaction-level scoring evidence")
    require("One observed success path is never representative" in scoring
            and "Behavior Confidence:   __ / 100  or NE" in scoring
            and "Representative: yes / no (if no, Behavior Confidence is NE)" in audit,
            "Behavior Confidence must be NE without representative interaction coverage")


def test_references_and_links() -> None:
    required = (
        "intuitive-software-design-standard.md",
        "scoring-reference.md",
        "examples.md",
        "audit-template.md",
        "ai-review-template.md",
    )
    for name in required:
        text(REFERENCES / name)

    for markdown in (ROOT / "skills").rglob("*.md"):
        body = text(markdown)
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", body):
            if target.startswith(("http://", "https://")):
                continue
            relative, _, fragment = target.partition("#")
            linked = (markdown.parent / relative).resolve() if relative else markdown
            require(linked.is_file(), f"Broken link in {markdown.name}: {target}")
            if fragment:
                require(fragment in heading_slugs(text(linked)), f"Broken anchor in {markdown.name}: {target}")


def heading_slugs(markdown: str) -> set[str]:
    """GitHub-style heading anchors, ignoring headings inside fenced code blocks."""
    prose = re.sub(r"(?ms)^```.*?^```", "", markdown)
    return {re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
            for heading in re.findall(r"(?m)^#{1,6}\s+(.+?)\s*$", prose)}


def test_scenarios() -> None:
    expected = {
        "01-screen-review.md": ("UI", "Flow", "Feel"),
        "02-workflow-audit.md": ("AUDIT", "Decision Density", "Intuitive Software Loop"),
        "03-new-design.md": ("DESIGN", "mental model", "hypothesis"),
        "04-critical-failure.md": ("Critical Failure", "independently"),
        "05-expert-software.md": ("expert", "density"),
        "06-minimal-unclear.md": ("minimal", "cognitive"),
        "07-purpose-first-redesign.md": ("GitNexus", "current layout", "stops for discussion"),
        "08-website-task-walkthrough.md": ("knowledge", "conversion"),
        "09-draft-task-walkthrough.md": ("persistence", "human"),
        "10-incomplete-walkthrough-evidence.md": ("unknown", "proposed"),
    }
    found = {path.name for path in SCENARIOS.glob("*.md")}
    require(found == set(expected), f"Scenario set mismatch: {sorted(found)}")
    for name, tokens in expected.items():
        body = text(SCENARIOS / name)
        require("## Prompt" in body and "## Acceptance gates" in body, f"Malformed scenario: {name}")
        gates = body.split("## Acceptance gates", 1)[1]
        require(len(re.findall(r"(?m)^- .+", gates)) >= 4, f"Scenario {name} needs substantive acceptance gates")
        for token in tokens:
            flags = 0 if token in {"DESIGN", "REVIEW", "AUDIT", "IMPROVE"} else re.IGNORECASE
            require(re.search(rf"(?<!\w){re.escape(token)}(?!\w)", gates, flags) is not None,
                    f"Scenario {name} lacks acceptance gate: {token}")


def test_no_placeholders() -> None:
    marker = "[" + "TODO:"
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".json", ".yaml", ".py", ".ps1"}:
            body = path.read_text(encoding="utf-8")
            require(marker not in body, f"Unfinished placeholder: {path.relative_to(ROOT)}")


def test_bundled_skill_discovery() -> None:
    expected = {
        "intuitive-software-design", "purpose-first-redesign", "user-task-walkthrough",
        "product-mental-model", "decision-support-design", "multi-role-workflow",
        "behavioral-evaluation", "connected-experience-design",
    }
    found = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
    require(found == expected, f"Bundled skill catalog mismatch: {sorted(found)}")
    for name in expected:
        folder = ROOT / "skills" / name
        metadata = text(folder / "agents" / "openai.yaml")
        require(f"${name}" in metadata, f"Default invocation targets wrong skill: {name}")
    for name in ("findability.md", "ui-language.md", "experience-progression.md"):
        text(REFERENCES / name)


def test_evaluation_kit_integrity() -> None:
    kit = ROOT / "skills" / "behavioral-evaluation" / "references"
    index = text(kit / "case-index.md")
    packets = set((kit / "fixtures").glob("*.md"))
    linked = {
        (kit / target).resolve()
        for target in re.findall(r"\[[^\]]+\]\((fixtures/[^)]+)\)", index)
    }
    require(len(packets) == 11 and {p.resolve() for p in packets} == linked,
            "Every evaluation packet must be indexed exactly once within the eleven-case set")
    text(kit / "assessor-rubric.md")
    text(kit / "comparison-record.md")
    for packet in packets:
        links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text(packet))
        require(not any("assessor-rubric" in target for target in links),
                f"Raw execution packet leaks assessor instructions: {packet.name}")
    require("Cases 01–06 closely follow worked examples" in index, "Example-aligned regression cases must be labeled")
    cases = sorted((ROOT / "evals").glob("*/prompt.md"))
    require(len(cases) >= 3, "Held-out eval suite needs diverse cases")
    for prompt in cases:
        body = text(prompt)
        require(body.startswith("---\n") and "allowed_tools:" in body, f"Malformed eval prompt: {prompt}")
        graders = sorted((prompt.parent / "graders").glob("*.md"))
        require(all(text(grader).startswith("---\n") for grader in graders),
                f"Eval grader lacks frontmatter: {prompt.parent.name}")
        scored = 0
        for grader in graders:
            body = text(grader)
            fields = grader_frontmatter(body)
            kind = fields.get("type", "")
            require(kind in GRADER_KEYS, f"Unknown grader type in {prompt.parent.name}/{grader.name}")
            unknown = set(fields) - {"type", "weight", "arm"} - GRADER_KEYS[kind]
            require(not unknown, f"Undocumented grader keys {sorted(unknown)} in {prompt.parent.name}/{grader.name}")
            require(fields.get("arm", "with-only") in {"with-only", "both"},
                    f"Unknown grader arm in {prompt.parent.name}/{grader.name}")
            if kind == "regex":
                pattern = re.match(r"'(.*)'$", fields.get("pattern", ""))
                require(pattern is not None, f"Regex grader needs a single-quoted pattern: {grader.name}")
                re.compile(pattern.group(1), re.IGNORECASE if "i" in fields.get("flags", "") else 0)
            if grader_is_scored(fields):
                scored += 1
                if kind == "llm":
                    require("PASS if" in body and "FAIL if" in body,
                            f"Scored rubric needs explicit PASS and FAIL conditions: {prompt.parent.name}/{grader.name}")
        # One conjunctive rubric can only score a run 0 or 1, which hides partial improvements; a case still
        # passes only when every scored criterion passes.
        require(scored >= 3, f"Eval case needs at least three independently scored criteria: {prompt.parent.name}")
        invoked = text(prompt.parent / "graders" / "skill-invoked.md")
        read = text(prompt.parent / "graders" / "skill-read.md")
        invoke_pattern = grader_input_match(invoked)
        target_match = re.search(r'([a-z][a-z0-9-]+)"$', invoke_pattern.pattern)
        require(target_match is not None, f"Skill indicator has no target: {prompt.parent.name}")
        skill_name = target_match.group(1)
        require((ROOT / "skills" / skill_name / "SKILL.md").is_file(),
                f"Skill indicator targets an unbundled skill: {prompt.parent.name}")
        require("type: tool_used" in invoked and "tool: Skill" in invoked and "arm: with-only" in invoked
                and skill_name in invoked and '"skill"' in invoked,
                f"Skill routing indicator must match an exact invocation: {prompt.parent.name}")
        require("type: tool_used" in read and "tool: Read" in read and "arm: with-only" in read
                and skill_name in read and r"SKILL\.md" in read,
                f"Read routing indicator must match the skill file: {prompt.parent.name}")
        other_skill = next(path.parent.name for path in sorted((ROOT / "skills").glob("*/SKILL.md"))
                           if path.parent.name != skill_name)
        read_pattern = grader_input_match(read)
        require(invoke_pattern.search(json.dumps({"skill": f"intuitive-software-design:{skill_name}"})) is not None
                and invoke_pattern.search(json.dumps({"skill": f"intuitive-software-design:{other_skill}"})) is None,
                f"Skill indicator matches the wrong skill: {prompt.parent.name}")
        for separator in ("/", "\\"):
            skill_root = f"intuitive-software-design{separator}skills{separator}"
            correct_paths = (
                f"{skill_root}{skill_name}{separator}SKILL.md",
                f"{skill_root}{other_skill}{separator}..{separator}{skill_name}{separator}SKILL.md",
            )
            wrong_paths = (
                f"{skill_root}{other_skill}{separator}SKILL.md",
                f"{skill_root}{skill_name}{separator}..{separator}{other_skill}{separator}SKILL.md",
            )
            require(all(read_pattern.search(json.dumps({"file_path": path})) is not None for path in correct_paths)
                    and all(read_pattern.search(json.dumps({"file_path": path})) is None for path in wrong_paths),
                    f"Read indicator matches the wrong skill file: {prompt.parent.name}")
    confidence = ROOT / "evals" / "behavior-confidence-heldout" / "graders"
    require("arm: with-only" in text(confidence / "vocabulary.md"),
            "Plugin-specific vocabulary must not inflate the baseline comparison")
    require("--ablation with-without" in text(ROOT / "README.md"),
            "Eval instructions must use the supported two-arm comparison")


def main() -> None:
    tests = (
        test_manifest,
        test_skill_frontmatter,
        test_skill_contract,
        test_purpose_first_redesign_contract,
        test_connected_experience_contract,
        test_authoritative_standard,
        test_scoring_contract,
        test_references_and_links,
        test_scenarios,
        test_no_placeholders,
        test_bundled_skill_discovery,
        test_evaluation_kit_integrity,
    )
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS all {len(tests)} plugin contract tests")


if __name__ == "__main__":
    main()
