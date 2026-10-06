# python-automation-toolkit

A small, dependency-free Python toolkit for everyday automation: organize files, clean CSV data, and scrape web pages.

Built with the **standard library only** — clone it and run it, no `pip install` required.

## Features

| Command | What it does |
|---|---|
| `organize` | Sorts files in a folder into subfolders by **type** or **date** |
| `csv` | Cleans a CSV: trims whitespace, drops empty rows, removes duplicates |
| `scrape` | Fetches a web page and lists its title and links |

## Quick start

```bash
git clone https://github.com/jjrc163/python-automation-toolkit.git
cd python-automation-toolkit

# Sort a messy Downloads folder by file type (preview first)
python cli.py organize ~/Downloads --by type --dry-run
python cli.py organize ~/Downloads --by type

# Clean a CSV and de-duplicate on the email column
python cli.py csv contacts.csv --out contacts_clean.csv --key email

# List the links on a page
python cli.py scrape https://example.com
```

## Project layout

```
python-automation-toolkit/
├── autotoolkit/
│   ├── __init__.py
│   ├── organize.py     # file organization
│   ├── csvclean.py     # CSV cleaning + de-duplication
│   └── scrape.py       # minimal HTML scraper
├── cli.py              # command-line entry point
└── tests/              # pytest suite
```

## Tests

```bash
pip install -r requirements.txt
pytest -q
```

## Design notes

- **No third-party runtime dependencies.** Everything uses the Python standard library, so the tools run anywhere Python 3.10+ is available.
- **Safe by default.** `organize` supports `--dry-run` and never overwrites an existing file (it appends `_1`, `_2`, …).
- **Tested.** The core logic is covered by unit tests using `tmp_path` fixtures.

## License

MIT — see [LICENSE](LICENSE).