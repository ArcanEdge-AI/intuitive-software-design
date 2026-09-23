#!/usr/bin/env python3
"""Deterministic structural and contract tests for the plugin source."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "intuitive-software-design"
REDESIGN_SKILL = ROOT / "skills" / "purpose-first-redesign"
REFERENCES = SKILL / "references"
SCENARIOS = ROOT / "tests" / "scenarios"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def text(path: Path) -> str:
    require(path.is_file(), f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def test_manifest() -> None:
    manifest_path = ROOT / ".codex-plugin" / "plugin.json"
    manifest = json.loads(text(manifest_path))
    require(manifest["name"] == ROOT.name == "intuitive-software-design", "Plugin name/folder mismatch")
    require(re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", manifest["version"]) is not None, "Version is not semver")
    require(manifest.get("skills") == "./skills/", "Manifest must expose ./skills/")
    require("mcpServers" not in manifest and "apps" not in manifest and "hooks" not in manifest, "Plugin must remain self-contained")
    interface = manifest["interface"]
    require(interface["displayName"] == "Intuitive Software Design", "Display name is not discoverable")
    prompts = interface.get("defaultPrompt", [])
    require(isinstance(prompts, list) and 1 <= len(prompts) <= 3, "defaultPrompt must contain one to three prompts")
    require(all(isinstance(prompt, str) and len(prompt) <= 128 for prompt in prompts), "A default prompt exceeds 128 characters")


def test_skill_contract() -> None:
    skill = text(SKILL / "SKILL.md")
    for token in ("DESIGN", "REVIEW", "AUDIT", "IMPROVE", "Not Evaluated", "Critical Failure"):
        require(token in skill, f"Skill routing/guardrail missing: {token}")
    require("Do not produce a screen redesign by default" in skill, "Improve guardrail is missing")
    require("assign numeric scores unless the user asks" in skill, "Review scoring guardrail is missing")
    require("They do not prove responsiveness" in skill, "Screenshot evidence guardrail is missing")
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
    )
    for token in required:
        require(token in skill, f"Purpose-first redesign contract missing: {token}")
    openai = text(REDESIGN_SKILL / "agents" / "openai.yaml")
    require("$purpose-first-redesign" in openai, "Redesign default prompt must name the skill")


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
    )
    for token in required:
        require(token in standard, f"Authoritative concept missing: {token}")
    require(standard.count("```mermaid") >= 6, "Standard must include at least six Mermaid diagrams")


def test_scoring_contract() -> None:
    scoring = text(REFERENCES / "scoring-reference.md")
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
    require(scoring.count("**Warning signs:**") == 18, "Every screen/workflow criterion needs warning signs")
    require(scoring.count("**Test:**") == 18, "Every screen/workflow criterion needs a test method")


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
            if target.startswith(("http://", "https://", "#")):
                continue
            relative = target.split("#", 1)[0]
            if not relative:
                continue
            require((markdown.parent / relative).resolve().is_file(), f"Broken link in {markdown.name}: {target}")


def test_scenarios() -> None:
    expected = {
        "01-screen-review.md": ("UI", "Flow", "Feel"),
        "02-workflow-audit.md": ("Prediction Gap", "Decision Density", "Intuitive Software Loop"),
        "03-new-design.md": ("DESIGN", "does not yet exist"),
        "04-critical-failure.md": ("Critical Failure", "independently"),
        "05-expert-software.md": ("domain", "density"),
        "06-minimal-unclear.md": ("minimal", "cognitive"),
        "07-purpose-first-redesign.md": ("GitNexus", "current layout", "Do not implement"),
        "08-website-task-walkthrough.md": ("knowledge", "conversion"),
        "09-draft-task-walkthrough.md": ("persistence", "human"),
        "10-incomplete-walkthrough-evidence.md": ("unknown", "proposed"),
    }
    found = {path.name for path in SCENARIOS.glob("*.md")}
    require(found == set(expected), f"Scenario set mismatch: {sorted(found)}")
    for name, tokens in expected.items():
        body = text(SCENARIOS / name)
        require("## Prompt" in body and "## Acceptance gates" in body, f"Malformed scenario: {name}")
        for token in tokens:
            require(token.lower() in body.lower(), f"Scenario {name} lacks acceptance token: {token}")


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
        "behavioral-evaluation",
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
    require(len(packets) == 8 and {p.resolve() for p in packets} == linked,
            "Every evaluation packet must be indexed exactly once within the eight-case set")
    text(kit / "assessor-rubric.md")
    text(kit / "comparison-record.md")
    for packet in packets:
        links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text(packet))
        require(not any("assessor-rubric" in target for target in links),
                f"Raw execution packet leaks assessor instructions: {packet.name}")


def main() -> None:
    tests = (
        test_manifest,
        test_skill_contract,
        test_purpose_first_redesign_contract,
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
