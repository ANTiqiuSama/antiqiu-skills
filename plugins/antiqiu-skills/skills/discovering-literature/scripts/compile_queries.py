#!/usr/bin/env python3
"""Compile a concept-matrix JSON file into a reproducible Boolean query draft."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


TARGETS = ("generic", "pubmed", "wos", "scopus")
LANGUAGES = ("en", "zh", "mixed")


def unique_strings(values: list[Any]) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        if not isinstance(value, str):
            raise ValueError("all terms must be strings")
        term = value.strip()
        if not term:
            continue
        key = term.casefold()
        if key not in seen:
            seen.add(key)
            output.append(term)
    return output


def selected_terms(container: Any, language: str) -> list[str]:
    if not isinstance(container, dict):
        raise ValueError("terms and exclude values must be objects keyed by language")
    keys = ("en", "zh") if language == "mixed" else (language,)
    values: list[Any] = []
    for key in keys:
        candidate = container.get(key, [])
        if not isinstance(candidate, list):
            raise ValueError(f"terms.{key} must be an array")
        values.extend(candidate)
    return unique_strings(values)


def quote_term(term: str) -> str:
    escaped = term.replace('"', '\\"')
    needs_quotes = bool(re.search(r"\s", escaped))
    return f'"{escaped}"' if needs_quotes else escaped


def render_term(term: str, target: str) -> str:
    rendered = quote_term(term)
    if target == "pubmed":
        return f"{rendered}[Title/Abstract]"
    return rendered


def render_block(terms: list[str], target: str) -> str:
    if not terms:
        raise ValueError("each concept group must contain at least one selected term")
    return "(" + " OR ".join(render_term(term, target) for term in terms) + ")"


def compile_query(payload: dict[str, Any], target: str, language: str) -> dict[str, Any]:
    groups = payload.get("groups")
    if not isinstance(groups, list) or not groups:
        raise ValueError("groups must be a non-empty array")

    rendered_groups: list[dict[str, Any]] = []
    blocks: list[str] = []
    names: set[str] = set()
    for index, group in enumerate(groups):
        if not isinstance(group, dict):
            raise ValueError(f"groups[{index}] must be an object")
        name = group.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"groups[{index}].name must be a non-empty string")
        if name in names:
            raise ValueError(f"duplicate group name: {name}")
        names.add(name)
        terms = selected_terms(group.get("terms", {}), language)
        blocks.append(render_block(terms, target))
        rendered_groups.append({"name": name, "terms": terms})

    query = " AND ".join(blocks)
    exclusions = selected_terms(payload.get("exclude", {}), language)
    if exclusions:
        query += " NOT " + render_block(exclusions, target)

    if target == "wos":
        query = f"TS=({query})"
    elif target == "scopus":
        query = f"TITLE-ABS-KEY({query})"

    return {
        "target": target,
        "language": language,
        "query": query,
        "groups": rendered_groups,
        "exclude": exclusions,
        "warnings": [
            "Verify current official database syntax and field availability before execution.",
            "Treat generated terms and queries as reproducible drafts, not evidence.",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Concept-matrix JSON file")
    parser.add_argument("--target", choices=TARGETS, default="generic")
    parser.add_argument("--language", choices=LANGUAGES, default="mixed")
    parser.add_argument("-o", "--output", type=Path, help="Write JSON output to this path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        result = compile_query(payload, args.target, args.language)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
