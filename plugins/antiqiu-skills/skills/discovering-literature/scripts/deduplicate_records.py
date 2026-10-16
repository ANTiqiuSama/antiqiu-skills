#!/usr/bin/env python3
"""Cluster JSONL literature records conservatively while preserving provenance."""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any


DOI_PREFIX = re.compile(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", re.I)


def normalize_doi(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    return DOI_PREFIX.sub("", value.strip()).strip().casefold() or None


def normalize_title(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    normalized = unicodedata.normalize("NFKC", value).casefold()
    normalized = "".join(character for character in normalized if character.isalnum())
    return normalized or None


def normalize_year(value: Any) -> int | None:
    if isinstance(value, int) and 1000 <= value <= 9999:
        return value
    if isinstance(value, str) and re.fullmatch(r"\d{4}", value.strip()):
        return int(value)
    return None


def load_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"line {line_number} must be a JSON object")
        value = dict(value)
        value.setdefault("_input_line", line_number)
        records.append(value)
    return records


def cluster_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    clusters: list[dict[str, Any]] = []
    doi_index: dict[str, int] = {}
    title_year_index: dict[tuple[str, int], set[int]] = {}

    for record in records:
        doi = normalize_doi(record.get("doi"))
        title = normalize_title(record.get("title"))
        year = normalize_year(record.get("year"))
        title_year = (title, year) if title and year else None

        cluster_index = doi_index.get(doi) if doi else None
        basis: list[str] = []
        if cluster_index is not None:
            basis.append("doi")
        elif title_year and title_year in title_year_index:
            compatible: list[int] = []
            for candidate_index in sorted(title_year_index[title_year]):
                existing_dois = {
                    normalize_doi(member.get("doi"))
                    for member in clusters[candidate_index]["members"]
                    if normalize_doi(member.get("doi"))
                }
                if not doi or not existing_dois or doi in existing_dois:
                    compatible.append(candidate_index)
            if len(compatible) == 1:
                cluster_index = compatible[0]
                basis.append("title-year")

        if cluster_index is None:
            cluster_index = len(clusters)
            clusters.append({"canonical": record, "members": [record], "match_basis": []})
        else:
            cluster = clusters[cluster_index]
            cluster["members"].append(record)
            cluster["match_basis"] = sorted(set(cluster["match_basis"] + basis))
            if sum(bool(value) for value in record.values()) > sum(
                bool(value) for value in cluster["canonical"].values()
            ):
                cluster["canonical"] = record

        if doi:
            doi_index[doi] = cluster_index
        if title_year:
            title_year_index.setdefault(title_year, set()).add(cluster_index)

    for cluster in clusters:
        cluster["cluster_size"] = len(cluster["members"])
        cluster["sources"] = sorted(
            {
                source
                for member in cluster["members"]
                for source in (
                    member.get("sources", [])
                    if isinstance(member.get("sources"), list)
                    else [member.get("source")]
                )
                if isinstance(source, str) and source.strip()
            },
            key=str.casefold,
        )
    return clusters


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Input JSONL records")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output clustered JSONL")
    parser.add_argument("--report", type=Path, help="Optional summary JSON path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        records = load_records(args.input)
        clusters = cluster_records(records)
        output = "".join(
            json.dumps(cluster, ensure_ascii=False, sort_keys=True) + "\n"
            for cluster in clusters
        )
        args.output.write_text(output, encoding="utf-8")
        if args.report:
            report = {
                "input_records": len(records),
                "output_clusters": len(clusters),
                "duplicate_records": len(records) - len(clusters),
                "clusters_with_duplicates": sum(cluster["cluster_size"] > 1 for cluster in clusters),
            }
            args.report.write_text(
                json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
