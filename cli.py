#!/usr/bin/env python3
"""Command-line interface for autotoolkit.

Usage:
    python cli.py organize <directory> [--by type|date] [--dry-run]
    python cli.py csv <file.csv> [--out cleaned.csv] [--key col1,col2]
    python cli.py scrape <url>
"""
from __future__ import annotations

import argparse
import sys

from autotoolkit import clean_csv, organize, scrape


def _cmd_organize(args: argparse.Namespace) -> int:
    moves = organize(args.directory, by=args.by, dry_run=args.dry_run)
    verb = "Would move" if args.dry_run else "Moved"
    for source, destination in moves:
        print(f"{verb}: {source.name} -> {destination.parent.name}/{destination.name}")
    print(f"\n{len(moves)} file(s) {'to move' if args.dry_run else 'moved'}.")
    return 0


def _cmd_csv(args: argparse.Namespace) -> int:
    key_columns = args.key.split(",") if args.key else None
    report = clean_csv(args.file, output_path=args.out, key_columns=key_columns)
    print(f"Rows in:            {report['rows_in']}")
    print(f"Rows out:           {report['rows_out']}")
    print(f"Duplicates removed: {report['duplicates_removed']}")
    return 0


def _cmd_scrape(args: argparse.Namespace) -> int:
    result = scrape(args.url)
    print(f"Title: {result['title']}\n")
    for href, text in result["links"]:  # type: ignore[index]
        label = text or "(no text)"
        print(f"- {label} -> {href}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="autotoolkit", description="Small automation helpers.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_org = sub.add_parser("organize", help="Sort files into folders by type or date.")
    p_org.add_argument("directory")
    p_org.add_argument("--by", choices=["type", "date"], default="type")
    p_org.add_argument("--dry-run", action="store_true")
    p_org.set_defaults(func=_cmd_organize)

    p_csv = sub.add_parser("csv", help="Clean and de-duplicate a CSV file.")
    p_csv.add_argument("file")
    p_csv.add_argument("--out", default=None)
    p_csv.add_argument("--key", default=None, help="Comma-separated columns to de-duplicate on.")
    p_csv.set_defaults(func=_cmd_csv)

    p_scrape = sub.add_parser("scrape", help="Fetch a page and list its links.")
    p_scrape.add_argument("url")
    p_scrape.set_defaults(func=_cmd_scrape)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())