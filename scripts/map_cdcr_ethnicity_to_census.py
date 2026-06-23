#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd


DEFAULT_MAPPING_PATH = Path(__file__).resolve().parents[1] / "mappings" / "cdcr_census_ethnicity_mapping.json"
DEFAULT_GROUP_COL = "census race ethnicity group"
DEFAULT_STATUS_COL = "census mapping status"
DEFAULT_NOTE_COL = "census mapping note"


def load_mapping(path: Path) -> dict[str, dict[str, str]]:
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, dict):
        raise ValueError("Mapping file must be a JSON object keyed by CDCR ethnicity label.")
    return raw


def normalize_label(value: Any) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def apply_mapping(
    df: pd.DataFrame,
    mapping: dict[str, dict[str, str]],
    source_col: str,
    group_col: str,
    status_col: str,
    note_col: str,
    include_audit_columns: bool = False,
) -> pd.DataFrame:
    if source_col not in df.columns:
        raise KeyError(f"Source column not found: {source_col}")

    out = df.copy()
    normalized = out[source_col].map(normalize_label)

    def mapped_field(label: str, field: str, default: str) -> str:
        entry = mapping.get(label)
        if not entry:
            return default
        return str(entry.get(field, default))

    out[group_col] = normalized.map(lambda label: mapped_field(label, "census_group", "review_needed"))
    if include_audit_columns:
        out[status_col] = normalized.map(lambda label: mapped_field(label, "status", "review"))
        out[note_col] = normalized.map(
            lambda label: mapped_field(label, "note", "No mapping entry found; needs review.")
        )

    return out


def labels_needing_review(
    df: pd.DataFrame,
    mapping: dict[str, dict[str, str]],
    source_col: str,
) -> pd.Series:
    normalized = df[source_col].map(normalize_label)
    return normalized[~normalized.isin(mapping)].value_counts(dropna=False)


def print_review_summary(
    df: pd.DataFrame,
    mapping: dict[str, dict[str, str]],
    source_col: str,
    group_col: str,
) -> pd.Series:
    print("\nMapped group counts:")
    print(df[group_col].value_counts(dropna=False).to_string())

    review_labels = labels_needing_review(df, mapping, source_col)
    if review_labels.empty:
        print("\nNo review labels found.")
        return review_labels

    print("\nLabels needing review:")
    print(review_labels.to_string())
    return review_labels


def main() -> int:
    parser = argparse.ArgumentParser(description="Map CDCR ethnicity labels to Census-compatible groups.")
    parser.add_argument("--input", required=True, help="Input CSV file.")
    parser.add_argument("--output", help="Output CSV file. Required unless --dry-run is used.")
    parser.add_argument("--source-col", default="ethnicity")
    parser.add_argument("--mapping", default=str(DEFAULT_MAPPING_PATH))
    parser.add_argument("--group-col", default=DEFAULT_GROUP_COL)
    parser.add_argument("--status-col", default=DEFAULT_STATUS_COL)
    parser.add_argument("--note-col", default=DEFAULT_NOTE_COL)
    parser.add_argument(
        "--include-audit-columns",
        action="store_true",
        help="Also write mapping status and note columns. Off by default for publication compatibility.",
    )
    parser.add_argument(
        "--allow-review",
        action="store_true",
        help="Allow output containing review_needed values. Default: stop before writing.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print mapping counts and review labels without writing a file.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    mapping = load_mapping(Path(args.mapping))

    if not args.dry_run and not args.output:
        parser.error("--output is required unless --dry-run is used.")

    if input_path.suffix.lower() != ".csv":
        raise ValueError("Only CSV input is supported.")

    df = pd.read_csv(input_path)

    out = apply_mapping(
        df=df,
        mapping=mapping,
        source_col=args.source_col,
        group_col=args.group_col,
        status_col=args.status_col,
        note_col=args.note_col,
        include_audit_columns=args.include_audit_columns,
    )

    review_labels = print_review_summary(out, mapping, args.source_col, args.group_col)
    if not review_labels.empty and not args.allow_review:
        raise ValueError("Unmapped ethnicity labels found; output was not written.")

    if args.dry_run:
        print("\nDry run complete; no output file was written.")
        return 0

    output_path = Path(args.output)
    if output_path.suffix.lower() != ".csv":
        raise ValueError("Only CSV output is supported.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False)

    print(f"Wrote {len(out):,} rows to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
