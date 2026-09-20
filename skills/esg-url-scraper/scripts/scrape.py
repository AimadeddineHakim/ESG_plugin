#!/usr/bin/env python3
"""Fetch a single URL's main article content using a free, no-API-key fallback chain.

Tier 1: requests -> trafilatura (falls back to BeautifulSoup within the same tier)
Tier 2: r.jina.ai Reader proxy (used only if tier 1 fails or returns too little text)

Prints one JSON object to stdout:
  {"ok": bool, "method": str|null, "title": str|null, "text": str|null, "error": str|null}
Exit code 0 on success, 1 if every tier failed.
"""
import json
import sys

MIN_TEXT_LENGTH = 200
TIMEOUT = 15
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


def tier1_requests_trafilatura(url):
    import requests
    import trafilatura

    resp = requests.get(url, timeout=TIMEOUT, headers={"User-Agent": USER_AGENT})
    resp.raise_for_status()
    html = resp.text

    text = trafilatura.extract(html, include_comments=False, include_tables=False)
    title = None
    metadata = trafilatura.extract_metadata(html)
    if metadata is not None:
        title = metadata.title

    if text and len(text.strip()) >= MIN_TEXT_LENGTH:
        return title, text.strip()

    # Secondary attempt within tier 1: BeautifulSoup extraction.
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    if title is None and soup.title and soup.title.string:
        title = soup.title.string.strip()

    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()

    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    bs_text = "\n\n".join(p for p in paragraphs if p)

    if bs_text and len(bs_text.strip()) >= MIN_TEXT_LENGTH:
        return title, bs_text.strip()

    # Neither extractor found enough text; treat as failure so tier 2 is attempted.
    return None, None


def tier2_jina_reader(url):
    import requests

    reader_url = f"https://r.jina.ai/{url}"
    resp = requests.get(reader_url, timeout=TIMEOUT, headers={"User-Agent": USER_AGENT})
    resp.raise_for_status()
    text = resp.text.strip()

    if not text or len(text) < MIN_TEXT_LENGTH:
        return None, None

    title = None
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        title = line.lstrip("#").strip() if line.startswith("#") else line
        break

    return title, text


def main():
    if len(sys.argv) != 2:
        print(json.dumps({"ok": False, "method": None, "title": None, "text": None,
                           "error": "usage: scrape.py <url>"}))
        sys.exit(1)

    url = sys.argv[1]
    errors = []

    for method_name, fn in (("requests+trafilatura", tier1_requests_trafilatura),
                             ("jina_reader", tier2_jina_reader)):
        try:
            title, text = fn(url)
        except Exception as exc:  # noqa: BLE001 - any tier failure just moves to the next
            errors.append(f"{method_name}: {exc}")
            continue

        if text and len(text.strip()) >= MIN_TEXT_LENGTH:
            print(json.dumps({"ok": True, "method": method_name, "title": title,
                               "text": text, "error": None}))
            sys.exit(0)

        errors.append(f"{method_name}: no usable text extracted")

    print(json.dumps({"ok": False, "method": None, "title": None, "text": None,
                       "error": "; ".join(errors)}))
    sys.exit(1)


if __name__ == "__main__":
    main()
