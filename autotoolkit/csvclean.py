"""Clean and de-duplicate CSV files.

Pure standard library — no third-party dependencies.
"""
from __future__ import annotations

import csv
from pathlib import Path


def _normalize(value: str, strip: bool) -> str:
    return value.strip() if strip else value


def clean_rows(
    rows: list[dict[str, str]],
    key_columns: list[str] | None = None,
    drop_empty: bool = True,
    strip: bool = True,
) -> tuple[list[dict[str, str]], int]:
    """Return (cleaned_rows, duplicates_removed).

    - ``strip`` trims whitespace from every cell.
    - ``drop_empty`` removes rows where every cell is blank.
    - ``key_columns`` de-duplicates on those columns (all columns if omitted).
    """
    cleaned: list[dict[str, str]] = []
    seen: set[tuple[str, ...]] = set()
    duplicates = 0

    for row in rows:
        normalized = {k: _normalize(v, strip) for k, v in row.items()}

        if drop_empty and all(not v for v in normalized.values()):
            continue

        if key_columns:
            key = tuple(normalized.get(col, "") for col in key_columns)
        else:
            key = tuple(normalized.values())

        if key in seen:
            duplicates += 1
            continue
        seen.add(key)
        cleaned.append(normalized)

    return cleaned, duplicates


def clean_csv(
    input_path: str | Path,
    output_path: str | Path | None = None,
    key_columns: list[str] | None = None,
    drop_empty: bool = True,
    strip: bool = True,
) -> dict[str, int]:
    """Clean a CSV file and write the result.

    Returns a small report: rows_in, rows_out, duplicates_removed.
    """
    source = Path(input_path)
    destination = Path(output_path) if output_path else source.with_name(f"{source.stem}_clean{source.suffix}")

    with source.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    cleaned, duplicates = clean_rows(rows, key_columns, drop_empty, strip)

    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned)

    return {
        "rows_in": len(rows),
        "rows_out": len(cleaned),
        "duplicates_removed": duplicates,
    }