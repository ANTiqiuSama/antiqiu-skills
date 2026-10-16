"""Read-only table facts for figure planning; deliberately no chart recommendations."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from pandas.api.types import is_bool_dtype, is_datetime64_any_dtype, is_numeric_dtype


def clean(value):
    """Strict JSON, including pandas/numpy values and overflowed statistics."""
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(v) for v in value]
    if isinstance(value, np.generic):
        return clean(value.item())
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if value is pd.NA or value is pd.NaT:
        return None
    if isinstance(value, (pd.Timestamp, pd.Timedelta)):
        return str(value)
    return value


def profile_dataframe(frame, columns=None, group=None, max_columns=40):
    if not frame.columns.is_unique:
        raise ValueError("Column labels must be unique; select or rename ambiguous fields first.")
    requested = list(frame.columns) if columns is None else list(dict.fromkeys(columns))
    missing = [c for c in requested + ([group] if group is not None else []) if c not in frame.columns]
    if missing:
        raise ValueError(f"Unknown columns: {missing}")
    if max_columns < 1:
        raise ValueError("max_columns must be positive")
    selected = requested[:max_columns]
    result = {
        "rows": len(frame), "columns_total": len(frame.columns),
        "columns_profiled": len(selected), "requested_columns_omitted": len(requested) - len(selected),
        "duplicate_rows": int(frame.duplicated().sum()), "fields": [],
        "notes": ["Facts only: roles, pairing, causal meaning and uncertainty need contextual interpretation.",
                  "Numeric statistics exclude null and nonfinite values; IQR flags are descriptive, not deletion advice.",
                  "Examples and category counts are bounded; no values in the input are modified."],
    }
    for name in selected:
        series = frame[name]
        valid = series.dropna()
        unique = int(series.nunique(dropna=True))
        field = {"name": str(name), "dtype": str(series.dtype), "missing": int(series.isna().sum()),
                 "non_null": len(valid), "unique_non_null": unique, "hints": []}
        if str(name).lower() in {"id", "index", "sample_id", "subject_id", "patient_id", "编号", "序号"} or str(name).lower().endswith("_id"):
            field["hints"].append("Name suggests an identifier; confirm its role from context.")
        if len(valid) and unique == len(valid):
            field["all_non_null_values_unique"] = True
        if is_numeric_dtype(series) and not is_bool_dtype(series):
            array = valid.to_numpy(dtype=float)
            finite = array[np.isfinite(array)]
            field.update(finite_count=len(finite), nonfinite_count=int((~np.isfinite(array)).sum()))
            if len(finite):
                numbers = pd.Series(finite)
                q1, median, q3 = numbers.quantile([.25, .5, .75])
                iqr = q3 - q1
                field["numeric"] = dict(min=finite.min(), q1=q1, median=median, q3=q3, max=finite.max(),
                                        mean=numbers.mean(), sample_std=numbers.std(),
                                        skew=numbers.skew() if len(finite) >= 3 else None,
                                        iqr_outside_count=int(((finite < q1 - 1.5 * iqr) | (finite > q3 + 1.5 * iqr)).sum()))
                if unique <= 12 and np.equal(finite, np.floor(finite)).all():
                    field["hints"].append("Few integer levels; may be a numeric measure, ordinal scale or category code.")
            if unique <= 12:
                field["value_counts"] = [{"value": k, "count": int(v)} for k, v in valid.value_counts().head(8).items()]
                field["value_counts_omitted"] = max(0, unique - 8)
        else:
            field["top_values"] = [{"value": str(k)[:100], "count": int(v)} for k, v in valid.value_counts().head(8).items()]
            field["other_unique_values"] = max(0, unique - 8)
            if is_datetime64_any_dtype(series):
                field["datetime_range"] = {"min": str(valid.min()), "max": str(valid.max())} if len(valid) else None
            elif len(valid):
                examples = valid.astype(str).head(50)
                date_like = examples.str.match(r"^\d{4}[-/]\d{1,2}[-/]\d{1,2}(?:$|[ T])")
                if date_like.any():
                    field["hints"].append(f"{int(date_like.sum())}/{len(examples)} sampled non-null strings look like dates; values were not parsed.")
        result["fields"].append(field)
    if group is not None:
        grouped = frame.groupby(group, dropna=False, sort=False, observed=True)
        groups = []
        for index, (key, part) in enumerate(grouped):
            if index >= 20:
                break
            counts = {}
            for name in selected:
                values = part[name]
                item = {"non_null": int(values.notna().sum())}
                if is_numeric_dtype(values) and not is_bool_dtype(values):
                    item["finite"] = int(np.isfinite(values.dropna().to_numpy(dtype=float)).sum())
                counts[str(name)] = item
            groups.append({"value": None if pd.isna(key) else str(key)[:100], "rows": len(part), "valid_by_field": counts})
        total = int(frame[group].nunique(dropna=False))
        result["groups"] = {"column": str(group), "total": total, "omitted": max(0, total - 20), "items": groups}
    return clean(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--sheet", help="Excel sheet name (default: first sheet)")
    parser.add_argument("--columns", nargs="+", help="Relevant columns only")
    parser.add_argument("--group", help="Explicit grouping column; does not infer paired observations")
    parser.add_argument("--max-columns", type=int, default=40)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output and args.output.resolve() == args.path.resolve():
        parser.error("Output must differ from the input data path.")
    suffix = args.path.suffix.lower()
    try:
        if suffix in {".csv", ".tsv"}:
            frame = pd.read_csv(args.path, sep="\t" if suffix == ".tsv" else ",")
        elif suffix == ".xlsx":
            frame = pd.read_excel(args.path, sheet_name=args.sheet if args.sheet is not None else 0)
        else:
            parser.error("Supported files: .csv, .tsv, .xlsx; use profile_dataframe for an existing DataFrame.")
        result = profile_dataframe(frame, args.columns, args.group, args.max_columns)
    except (ValueError, OSError, ImportError) as error:
        parser.error(str(error))
    result["source"] = str(args.path.resolve())
    result["notes"].append("Dtypes reflect the table reader's inference, not confirmed semantic roles; inspect raw fields when formatting matters.")
    encoded = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)
    if args.output:
        args.output.write_text(encoded + "\n", encoding="utf-8")
    else:
        print(encoded)


if __name__ == "__main__":
    main()
