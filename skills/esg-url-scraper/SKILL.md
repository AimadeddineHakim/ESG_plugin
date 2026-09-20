---
name: esg-url-scraper
description: Use this skill when asked to scrape, re-fetch, or independently verify ESG research sources for a company that esg-deep-research already ran — e.g. "scrape the sources for {company}", "re-scrape anthropic's sources", "independently fetch {company}'s research URLs". Reads assessment/<company-slug>/reports/manifest.json for the full list of URLs esg-deep-research found, re-fetches every one of them using free no-key scrapers (requests+trafilatura, then Jina Reader as fallback), saves successes into assessment/<company-slug>/sources/, and writes a results manifest linking each URL back to its original esg-deep-research report file. Does not search for new URLs — that's esg-deep-research's job.
allowed-tools: Read, Glob, Write, Bash(${CLAUDE_SKILL_DIR}/scripts/scrape.py *), Bash(python3 -m pip install -r ${CLAUDE_SKILL_DIR}/scripts/requirements.txt), Bash(mkdir -p assessment/*/sources)
---

# ESG URL Scraper

Independently re-fetch every source `esg-deep-research` found for a company, using free scrapers with no API key required, and record a results manifest that links each URL back to the original report file. This skill does not search for new URLs — it only re-fetches URLs already recorded in `assessment/<company-slug>/reports/manifest.json`, and it re-fetches all of them unconditionally, regardless of whether the original `esg-deep-research` report already looks complete.

## Step 1 — Identify the target company

Take the company name from the user's request. Derive `<company-slug>` the same way `esg-deep-research` does: lowercase, spaces/punctuation replaced with hyphens.

## Step 2 — Load the manifest and match report files

`Read assessment/<company-slug>/reports/manifest.json` — this is the authoritative worklist: a `{title, url}` array of every source `esg-deep-research` saved. Every entry in it gets scraped in Step 4.

To later link each entry back to the report file it came from: `Glob assessment/<company-slug>/reports/*.md` (excluding `index.md`), `Read` each match, and build a `url → filename` lookup from each file's `url:` frontmatter value. If a manifest entry's URL has no matching file (shouldn't normally happen), its `report_file` will be `null`.

## Step 3 — Dependency check

The scraper script needs `requests`, `trafilatura`, and `beautifulsoup4`. If running the script in Step 4 fails with `ModuleNotFoundError`, run:

```
python3 -m pip install -r ${CLAUDE_SKILL_DIR}/scripts/requirements.txt
```

then retry. (Use `python3 -m pip`, not a bare `pip` command — `pip` isn't guaranteed to be on `PATH` on every machine, but the `python3` this skill's own script requires already is.)

## Step 4 — Scrape every URL in the manifest

For every entry in `manifest.json` (unconditionally — no content-quality check gates this), run:

```
${CLAUDE_SKILL_DIR}/scripts/scrape.py "<url>"
```

This tries two free, no-key tiers in order, falling through only when the previous one fails or returns too little text:

1. `requests` HTTP fetch → `trafilatura` extraction (with a `BeautifulSoup` fallback parse in the same tier).
2. `r.jina.ai` Reader proxy — a free, no-key service that returns clean Markdown for pages the first tier can't reach.

It prints one JSON object to stdout:

```json
{"ok": true, "method": "requests+trafilatura", "title": "...", "text": "...", "error": null}
```

or, if both tiers failed:

```json
{"ok": false, "method": null, "title": null, "text": null, "error": "..."}
```

Keep track of the outcome for each entry — it feeds both the saved file (Step 5) and the results manifest (Step 6).

## Step 5 — Save the scraped source

On success (`ok: true`):

1. Ensure the destination folder exists: `mkdir -p assessment/<company-slug>/sources` (already created by `esg-research-scope` if that was run first; this is a defensive no-op otherwise).
2. `Write` a new file at `assessment/<company-slug>/sources/<source-slug>.md` (same slug convention as `esg-deep-research`, derived from the title), in the same frontmatter format `esg-deep-research` uses, plus a `scraper` field:

   ```markdown
   ---
   title: <existing title, or the script's title if the manifest entry had none>
   url: <unchanged>
   fetched: <today's ISO date>
   scraper: <method from the script output>
   ---

   <text from the script output>
   ```

Leave the original report file in `assessment/<company-slug>/reports/` untouched — `sources/` holds the independently re-fetched copy.

On failure (`ok: false`), write nothing.

## Step 6 — Write the results manifest and report back

After processing every manifest entry, `Write assessment/<company-slug>/sources/manifest.json`: one object per URL, linking it to both the scrape outcome and the original report file found in Step 2:

```json
[
  {
    "url": "https://example.com/article-a",
    "title": "Article A headline",
    "status": "success",
    "scraper": "requests+trafilatura",
    "error": null,
    "report_file": "reports/article-a-slug.md",
    "source_file": "sources/article-a-slug.md"
  },
  {
    "url": "https://example.com/article-b",
    "title": "Article B headline",
    "status": "failed",
    "scraper": null,
    "error": "requests+trafilatura: 403 ...; jina_reader: 403 ...",
    "report_file": "reports/article-b-slug.md",
    "source_file": null
  }
]
```

- `report_file`: path (relative to `assessment/<company-slug>/`) of the original `esg-deep-research` report this URL came from (from Step 2's lookup), or `null` if none matched.
- `source_file`: path (relative to `assessment/<company-slug>/`) of the newly scraped file, or `null` on failure.

Then tell the user:
- How many sources were successfully scraped and saved to `assessment/<company-slug>/sources/`, and via which tier (`requests+trafilatura` vs `jina_reader`).
- How many failed, listing their URLs and errors, so the user can fetch those manually if needed.
