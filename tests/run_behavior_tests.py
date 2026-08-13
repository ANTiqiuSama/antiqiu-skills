#!/usr/bin/env python3
"""Run isolated fresh-session behavior checks for every bundled Skill."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins" / "antiqiu-skills" / "skills"
CASES = ROOT / "tests" / "behavior_cases.json"


def run_case(
    case: dict[str, object],
    model: str,
    timeout: int,
    temp_root: Path,
    codex_home: Path,
) -> dict[str, object]:
    case_id = str(case["id"])
    case_dir = temp_root / case_id
    skill_dir = case_dir / ".agents" / "skills"
    skill_dir.mkdir(parents=True)
    selected = str(case["skill"])
    names = sorted(path.name for path in SKILLS.iterdir() if (path / "SKILL.md").is_file())
    for name in names if selected == "*" else [selected]:
        os.symlink(SKILLS / name, skill_dir / name, target_is_directory=True)

    output_path = case_dir / "last-message.txt"
    command = [
        "codex",
        "exec",
        "--ephemeral",
        "--ignore-user-config",
        "--skip-git-repo-check",
        "-s",
        "read-only",
        "-C",
        str(case_dir),
        "-m",
        model,
        "-c",
        'model_reasoning_effort="low"',
        "-o",
        str(output_path),
        str(case["prompt"]),
    ]
    started = time.monotonic()
    environment = os.environ.copy()
    environment["CODEX_HOME"] = str(codex_home)
    completed = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
        env=environment,
    )
    elapsed = round(time.monotonic() - started, 2)
    response = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
    folded = response.casefold()
    missing = [term for term in case.get("must_contain", []) if str(term).casefold() not in folded]
    missing_any = [
        alternatives
        for alternatives in case.get("must_contain_any", [])
        if not any(str(term).casefold() in folded for term in alternatives)
    ]
    forbidden = [term for term in case.get("must_not_contain", []) if str(term).casefold() in folded]
    ok = (
        completed.returncode == 0
        and bool(response.strip())
        and not missing
        and not missing_any
        and not forbidden
    )
    return {
        "id": case_id,
        "skill": selected,
        "ok": ok,
        "exit_code": completed.returncode,
        "elapsed_seconds": elapsed,
        "missing": missing,
        "missing_any": missing_any,
        "forbidden": forbidden,
        "response": response.strip(),
        "transport_tail": "\n".join(completed.stdout.splitlines()[-8:]),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-5.6-terra")
    parser.add_argument("--jobs", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument(
        "--output", type=Path, default=ROOT / "tests" / "results" / "behavior-results.json"
    )
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    cases = json.loads(CASES.read_text(encoding="utf-8"))
    ids = [case["id"] for case in cases]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate behavior case id")
    for case in cases:
        selected = case["skill"]
        if selected != "*" and not (SKILLS / selected / "SKILL.md").is_file():
            raise SystemExit(f"missing skill for case {case['id']}: {selected}")
    print(f"validated {len(cases)} behavior cases")
    if args.validate_only:
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="antiqiu-skills-eval-") as temp:
        temp_root = Path(temp)
        codex_home = temp_root / "codex-home"
        codex_home.mkdir()
        auth_file = Path.home() / ".codex" / "auth.json"
        if not auth_file.is_file():
            raise SystemExit(f"missing Codex authentication file: {auth_file}")
        os.symlink(auth_file, codex_home / "auth.json")
        with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
            futures = [
                pool.submit(run_case, case, args.model, args.timeout, temp_root, codex_home)
                for case in cases
            ]
            results = [future.result() for future in futures]

    report = {
        "ok": all(result["ok"] for result in results),
        "model": args.model,
        "case_count": len(results),
        "passed": sum(bool(result["ok"]) for result in results),
        "results": sorted(results, key=lambda item: str(item["id"])),
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("ok", "model", "case_count", "passed")}, indent=2))
    for result in report["results"]:
        print(
            f"{result['id']}: {'PASS' if result['ok'] else 'FAIL'} "
            f"({result['elapsed_seconds']}s) missing={result['missing']} "
            f"missing_any={result['missing_any']} forbidden={result['forbidden']}"
        )
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
