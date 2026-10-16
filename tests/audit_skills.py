#!/usr/bin/env python3
"""Static regression checks for the ANTiqiu Skills bundle."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "antiqiu-skills"
SKILLS = PLUGIN / "skills"
ORIGINAL = {
    "diagnose-work",
    "execute-work",
    "human-writing",
    "herdr-orchestrator",
    "keep-task-in-scope",
    "native-hybrid-agents",
    "plan-work",
    "refine-text",
    "trim-agent-instructions",
    "write-action-first",
}
SYNCED = {
    "academic-humanizer", "apple-design-skill", "apply-design-typography-standards",
    "audit-research-release", "build-project-wiki", "designing-studies",
    "discovering-literature", "game-the-llm-reviewer", "refine-text",
    "reverse-engineer-anything", "rolling-goal-prompt", "run-research-program",
    "team", "vivid-figures-skill", "write-research-paper", "zhihu", "zhihu-public-reader",
}
CLAUDE_DESIGN = {"claude-design", "frontend-design", "frontend-app-builder"}
EXPECTED = ORIGINAL | SYNCED | CLAUDE_DESIGN
LEGACY = {
    "brainstorming",
    "executing-plans",
    "receiving-code-review",
    "systematic-debugging",
    "verification-before-completion",
    "writing-plans",
}
BASELINE_METADATA_BYTES = 3784
BASELINE_OVERLAP_LINES = 186
BASELINE_DIAGNOSTIC_SUPPORT_LINES = 636


def fail(message: str) -> None:
    raise AssertionError(message)


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"missing YAML frontmatter: {path}")
    try:
        block = text.split("---\n", 2)[1]
    except IndexError as exc:
        raise AssertionError(f"unclosed frontmatter: {path}") from exc
    values: dict[str, str] = {}
    lines = block.splitlines()
    for index, line in enumerate(lines):
        if not line.strip() or line.startswith((" ", "\t")):
            continue
        key, sep, value = line.partition(":")
        if sep:
            value = value.strip()
            if value in {"|", "|-", "|+", ">", ">-", ">+"}:
                continuation = []
                for following in lines[index + 1:]:
                    if following.strip() and not following.startswith((" ", "\t")):
                        break
                    continuation.append(following.strip())
                value = ("\n" if value.startswith("|") else " ").join(continuation).strip()
            values[key.strip()] = value.strip("'\"")
    return values


def check_relative_links(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    # Example Markdown and regex literals are content, not navigable links.
    text = re.sub(r"(?ms)^```[^\n]*\n.*?^```[^\n]*$", "", text)
    text = re.sub(r"`[^`\n]+`", "", text)
    for raw in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        target = raw.split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        if not (path.parent / target).exists():
            errors.append(f"broken link: {path.relative_to(ROOT)} -> {raw}")
    return errors


def main() -> int:
    errors: list[str] = []
    source_snapshot_link_warnings: list[str] = []
    skill_dirs = sorted(path.parent for path in SKILLS.glob("*/SKILL.md"))
    names = {path.name for path in skill_dirs}
    if names != EXPECTED:
        errors.append(f"skill set mismatch: expected={sorted(EXPECTED)} actual={sorted(names)}")
    bundled_apple_fonts = list((SKILLS / "apple-design-skill").rglob("PingFang*.[ot]tf")) + list(
        (SKILLS / "apple-design-skill").rglob("PingFang*.woff*")
    )
    if bundled_apple_fonts:
        errors.append(f"proprietary Apple font files bundled: {bundled_apple_fonts}")
    if names & LEGACY:
        errors.append(f"legacy skills still enabled: {sorted(names & LEGACY)}")

    metadata_bytes = 0
    original_metadata_bytes = 0
    body_lines = 0
    details: list[dict[str, object]] = []
    for directory in skill_dirs:
        skill_file = directory / "SKILL.md"
        text = skill_file.read_text(encoding="utf-8")
        meta = frontmatter(skill_file)
        name = meta.get("name", "")
        description = meta.get("description", "")
        if name != directory.name:
            errors.append(f"name does not match directory: {directory.name} -> {name}")
        if not description:
            errors.append(f"empty description: {directory.name}")
        if directory.name in ORIGINAL and len(description.encode("utf-8")) > 600:
            errors.append(f"description exceeds 600 bytes: {directory.name}")
        if "TODO" in text or "[TODO" in text:
            errors.append(f"placeholder remains: {directory.name}")
        if directory.name in ORIGINAL and not (directory / "agents" / "openai.yaml").is_file():
            errors.append(f"missing agents/openai.yaml: {directory.name}")
        metadata = f"{name}\n{description}".encode("utf-8")
        metadata_bytes += len(metadata)
        if directory.name in ORIGINAL:
            original_metadata_bytes += len(metadata)
        lines = len(text.splitlines())
        body_lines += lines
        details.append({"name": name, "metadata_bytes": len(metadata), "skill_lines": lines})

    overlap_lines = sum(
        len((SKILLS / name / "SKILL.md").read_text(encoding="utf-8").splitlines())
        for name in ("plan-work", "execute-work", "diagnose-work")
    )
    if original_metadata_bytes >= BASELINE_METADATA_BYTES:
        errors.append("metadata was not reduced")
    if original_metadata_bytes > 3500:
        errors.append(f"original workflow metadata budget exceeded: {original_metadata_bytes} > 3500")
    if overlap_lines >= BASELINE_OVERLAP_LINES:
        errors.append("merged workflow bodies were not reduced")
    if overlap_lines > 120:
        errors.append(f"merged workflow line budget exceeded: {overlap_lines} > 120")

    diagnostic_support = {
        "condition-based-waiting.md",
        "root-cause-tracing.md",
    }
    actual_support = {
        path.name
        for path in (SKILLS / "diagnose-work").iterdir()
        if path.is_file() and path.name != "SKILL.md"
    }
    if actual_support != diagnostic_support:
        errors.append(
            f"diagnostic support mismatch: expected={sorted(diagnostic_support)} "
            f"actual={sorted(actual_support)}"
        )
    diagnostic_support_lines = sum(
        len((SKILLS / "diagnose-work" / name).read_text(encoding="utf-8").splitlines())
        for name in diagnostic_support
    )
    if diagnostic_support_lines > 80:
        errors.append(f"diagnostic support line budget exceeded: {diagnostic_support_lines} > 80")

    write_yaml = (SKILLS / "write-action-first" / "agents" / "openai.yaml").read_text(
        encoding="utf-8"
    )
    if "allow_implicit_invocation: false" not in write_yaml:
        errors.append("write-action-first must remain explicit-only")

    required_files = [
        ROOT / "LICENSE",
        ROOT / "NOTICE.md",
        ROOT / "licenses" / "superpowers-MIT.txt",
        ROOT / "licenses" / "hero-MIT.txt",
        SKILLS / "human-writing" / "LICENSE",
        SKILLS / "write-action-first" / "LICENSE",
        SKILLS / "academic-humanizer" / "LICENSE",
        SKILLS / "apple-design-skill" / "LICENSE",
        SKILLS / "frontend-design" / "LICENSE.txt",
        SKILLS / "frontend-app-builder" / "LICENSE",
        SKILLS / "vivid-figures-skill" / "LICENSE",
    ]
    for path in required_files:
        if not path.is_file():
            errors.append(f"missing license or notice: {path.relative_to(ROOT)}")

    plugin = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    if plugin.get("name") != "antiqiu-skills" or plugin.get("skills") != "./skills/":
        errors.append("plugin manifest does not point to the skill bundle")
    marketplace = json.loads(
        (ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8")
    )
    if marketplace.get("name") != "antiqiu-skills":
        errors.append("marketplace name mismatch")

    for path in ROOT.rglob("*.md"):
        if ".git" not in path.parts:
            links = check_relative_links(path)
            if path.is_relative_to(SKILLS / "vivid-figures-skill" / "catalog" / "sources"):
                # Imported provenance snapshots retain their original paths and bytes.
                # Their historical links do not describe the live template layout.
                source_snapshot_link_warnings.extend(links)
            else:
                errors.extend(links)
    # Parse shipped Python without generating caches or calling external models.
    import ast
    for path in ROOT.rglob("*.py"):
        if ".git" not in path.parts:
            try:
                ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
            except SyntaxError as exc:
                errors.append(f"invalid Python: {path.relative_to(ROOT)}: {exc}")
    forbidden = list(ROOT.rglob("__pycache__")) + list(ROOT.rglob("*.pyc"))
    if forbidden:
        errors.append(f"generated Python artifacts committed: {forbidden}")

    report = {
        "ok": not errors,
        "skill_count": len(skill_dirs),
        "metadata_bytes": metadata_bytes,
        "synced_skill_count": len(SYNCED),
        "original_workflow_metadata_bytes": original_metadata_bytes,
        "original_workflow_metadata_reduction_percent": round(
            (BASELINE_METADATA_BYTES - original_metadata_bytes) / BASELINE_METADATA_BYTES * 100, 1
        ),
        "merged_workflow_lines": overlap_lines,
        "merged_workflow_reduction_percent": round(
            (BASELINE_OVERLAP_LINES - overlap_lines) / BASELINE_OVERLAP_LINES * 100, 1
        ),
        "diagnostic_support_files": len(diagnostic_support),
        "diagnostic_support_lines": diagnostic_support_lines,
        "diagnostic_support_reduction_percent": round(
            (BASELINE_DIAGNOSTIC_SUPPORT_LINES - diagnostic_support_lines)
            / BASELINE_DIAGNOSTIC_SUPPORT_LINES
            * 100,
            1,
        ),
        "all_skill_lines": body_lines,
        "skills": details,
        "source_snapshot_link_warnings": source_snapshot_link_warnings,
        "errors": errors,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, json.JSONDecodeError) as exc:
        print(f"audit failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
