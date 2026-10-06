"""Minimal web scraper: fetch a page and extract links and the page title.

Pure standard library — no third-party dependencies.
"""
from __future__ import annotations

import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin

USER_AGENT = "autotoolkit/1.0 (+https://github.com/jjrc163/python-automation-toolkit)"


class _PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.links: list[tuple[str, str]] = []
        self._in_title = False
        self._current_href: str | None = None
        self._current_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "title":
            self._in_title = True
        elif tag == "a":
            href = dict(attrs).get("href")
            if href:
                self._current_href = href
                self._current_text = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        elif tag == "a" and self._current_href is not None:
            text = " ".join("".join(self._current_text).split())
            self.links.append((self._current_href, text))
            self._current_href = None
            self._current_text = []

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data
        if self._current_href is not None:
            self._current_text.append(data)


def fetch(url: str, timeout: int = 15) -> str:
    """Fetch *url* and return the decoded HTML."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def scrape(url: str, timeout: int = 15) -> dict[str, object]:
    """Fetch *url* and return {'title': str, 'links': [(absolute_url, text), ...]}."""
    html = fetch(url, timeout=timeout)
    parser = _PageParser()
    parser.feed(html)
    links = [(urljoin(url, href), text) for href, text in parser.links]
    return {"title": parser.title.strip(), "links": links}