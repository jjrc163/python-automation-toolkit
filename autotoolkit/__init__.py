"""autotoolkit — small, dependency-free automation helpers.

Modules:
    organize  — sort files into folders by type or date
    csvclean  — clean and de-duplicate CSV files
    scrape    — fetch a page and extract its title and links
"""

from .csvclean import clean_csv, clean_rows
from .organize import category_for, organize
from .scrape import fetch, scrape

__all__ = ["organize", "category_for", "clean_csv", "clean_rows", "fetch", "scrape"]
__version__ = "1.0.0"