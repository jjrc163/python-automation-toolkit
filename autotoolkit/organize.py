"""Organize files in a directory by type or modification date.

Pure standard library — no third-party dependencies.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

CATEGORIES: dict[str, set[str]] = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff"},
    "documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".odt", ".rtf", ".tex"},
    "spreadsheets": {".xls", ".xlsx", ".csv", ".ods", ".tsv"},
    "presentations": {".ppt", ".pptx", ".odp", ".key"},
    "audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "video": {".mp4", ".mkv", ".mov", ".avi", ".webm", ".wmv"},
    "archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"},
    "code": {
        ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".cpp", ".c", ".h",
        ".cs", ".go", ".rs", ".rb", ".php", ".html", ".css", ".scss",
        ".json", ".xml", ".yml", ".yaml", ".sh", ".sql",
    },
}


def category_for(path: Path) -> str:
    """Return the category name for a file based on its extension."""
    ext = path.suffix.lower()
    for name, extensions in CATEGORIES.items():
        if ext in extensions:
            return name
    return "other"


def _target_dir(path: Path, by: str) -> str:
    if by == "type":
        return category_for(path)
    if by == "date":
        return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m")
    raise ValueError(f"Unknown grouping: {by!r} (expected 'type' or 'date')")


def organize(directory: str | Path, by: str = "type", dry_run: bool = False) -> list[tuple[Path, Path]]:
    """Move files in *directory* into subfolders grouped by *by*.

    Returns a list of (source, destination) pairs that were (or would be) moved.
    """
    root = Path(directory)
    if not root.is_dir():
        raise NotADirectoryError(f"{root} is not a directory")

    moves: list[tuple[Path, Path]] = []
    for item in sorted(root.iterdir()):
        if item.is_dir() or item.name.startswith("."):
            continue
        target_dir = root / _target_dir(item, by)
        destination = target_dir / item.name
        if destination.exists():
            stem, suffix = item.stem, item.suffix
            counter = 1
            while destination.exists():
                destination = target_dir / f"{stem}_{counter}{suffix}"
                counter += 1
        moves.append((item, destination))

    if not dry_run:
        for source, destination in moves:
            destination.parent.mkdir(parents=True, exist_ok=True)
            source.rename(destination)

    return moves