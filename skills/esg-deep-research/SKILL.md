---
name: esg-deep-research
description: Use this skill when asked to research, find, or gather ESG controversy sources for a company from the internet — e.g. "research ESG controversies for {company}", "find sources on {company}'s ESG issues online", "pull articles about {company} controversies". Searches the web for Environmental/Social/Governance controversy coverage, fetches the pages, and saves each source as a Markdown file under assessment/<company>/reports/. Does not classify or score the sources — that is esg-controversy-assessment's job, run separately afterward.
allowed-tools: Read, WebSearch, WebFetch, Write, Bash(mkdir -p assessment/*/reports)
---

# Deep Research: ESG Controversy Source Collection

Find and save web sources discussing ESG controversies for a target company. This skill only collects sources — it does not detect, classify, or score controversies (see the `esg-controversy-assessment` skill for that, run as a separate step on the saved files).

## Step 1 — Identify the target company and check for a scope

Take the company name from what the user explicitly named in their request. If no company is named, or the request could refer to more than one company (e.g. a common name, or several companies mentioned), ask the user to confirm before searching — do not guess.

Derive a `<company-slug>` from the company name: lowercase, spaces and punctuation replaced with hyphens (e.g. "Coca-Cola Europacific Partners" → `coca-cola-europacific-partners`).

Check whether `assessment/<company-slug>/context.json` already exists (e.g. written by a prior `esg-research-scope` run). If it does, `Read` it and use its `company`, `company_slug`, `date_start`, and `date_end` values instead of re-deriving them — this is the resolved scope for Step 2's date-aware queries. If it doesn't exist, proceed as above with no date scoping (unbounded); this skill still works standalone without a scope having been run first.

Also check whether `assessment/<company-slug>/reports/clusters.json` already exists (written by a prior `esg-controversy-clustering` run, on an earlier pass over this company). If it does, `Read` it — its `controversy`/`description` pairs are the canonical registry of incidents already being tracked for this company, used in Step 4 to keep labels stable across reruns. If it doesn't exist (first run for this company, or clustering hasn't run yet), proceed with no registry — labels will just be assigned fresh.

## Step 2 — Run targeted searches

Generic "{company} news" searches surface PR and unrelated coverage. Instead, run several `WebSearch` queries that each target one ESG angle, so all three pillars get covered rather than whatever the first query happens to return:

- `"{company}" controversy`
- `"{company}" lawsuit OR fined OR investigation`
- `"{company}" pollution OR emissions OR environmental`
- `"{company}" labor OR "human rights" OR discrimination`
- `"{company}" fraud OR corruption OR governance scandal`

Adjust/add queries based on what's already known about the company; the goal is coverage of Environmental, Social, and Governance angles, not running every query verbatim.

If Step 1 resolved a date range, append a date-scoping phrase to every query above:
- Both `date_start`/`date_end` set, same year → append that year (e.g. `"{company}" controversy 2026`).
- Both set, different years → append `"{start_year}-{end_year}"`.
- Only `date_start` set → append `"since {start_year}"`.
- Only `date_end` set → append `"through {end_year}"`.
- Neither set (unbounded) → no change.

## Step 3 — Select sources worth fetching

From the search results, prioritize:
- Independent news outlets and business press.
- Regulatory, NGO, or watchdog reports.

Deprioritize the company's own press releases/marketing pages — they're a secondary, self-interested source. Only fetch one if no independent coverage exists for a given allegation, and note in the saved file that it's a company statement, not independent reporting.

Skip obvious duplicates (same story syndicated word-for-word across multiple outlets) — save the original/most detailed version. Distinct articles that independently cover the same underlying incident are *not* duplicates in this sense — keep them (they'll be linked via a shared `controversies` label in Step 4), since multiple independent accounts of one incident are useful corroborating evidence, not redundant. If a date range was resolved in Step 1, also discard sources clearly published outside that range, even if a search surfaces them.

## Step 4 — Fetch and save each source

For each selected URL:

1. Fetch it with `WebFetch` and extract the substantive article text (drop navigation, ads, related-article boilerplate).
2. Ensure the destination folder exists: `mkdir -p assessment/<company-slug>/reports` (already created by `esg-research-scope` if that was run first; this is a defensive no-op otherwise).
3. Determine the `controversies` label(s) for this source: one or more short slugs (same style as `<company-slug>`: lowercase, hyphenated) identifying the specific incident(s) the article covers — e.g. `["coxon-resignation"]`, or `["wikipedia-messaging-incident", "benchmaxxing", "navier-stokes-dispute"]` for a roundup article covering several incidents. Before minting a new label, check for a match against, in order:
   - The registry from `clusters.json` read in Step 1 (if it existed) — this is the canonical source of truth for incidents already tracked across prior runs. Compare against each entry's `description`, not just its label name, since a genuinely matching incident won't always share obvious wording.
   - Labels already assigned to sources saved earlier in *this* run.

   If the source covers an incident that matches an existing entry from either check, reuse that exact label instead of minting a near-duplicate (e.g. don't create both `coxon-resignation` and `coxon-departure` for the same event). Only create a new label when the incident genuinely isn't covered by anything in the registry or this run so far.
4. Write the source to `assessment/<company-slug>/reports/<source-slug>.md` (slug derived from the article title) via `Write`, formatted as:

   ```markdown
   ---
   title: <page title>
   url: <source url>
   fetched: <ISO date>
   query: <the search query that surfaced it>
   controversies: [<slug>, ...]
   ---

   <extracted article text>
   ```

## Step 5 — Write the index and manifest

After saving all sources:

1. Write `assessment/<company-slug>/reports/index.md` listing every saved file: title, URL, and a one-line summary of what controversy/topic it covers. This lets a later step skim what's available without opening every file.
2. Write `assessment/<company-slug>/reports/manifest.json`: a JSON array of `{title, url}` objects, one per saved source file, using the same `title`/`url` values from each file's frontmatter (Step 4), in the order the sources were saved. This is a machine-readable worklist other tools can consume without parsing frontmatter out of every file, e.g.:

   ```json
   [
     {"title": "Article A headline", "url": "https://example.com/article-a"},
     {"title": "Article B headline", "url": "https://example.com/article-b"}
   ]
   ```

## Step 6 — Report back

Tell the user how many sources were saved and where (`assessment/<company-slug>/reports/`, plus the `index.md` and `manifest.json` written alongside them), and note any query that returned nothing useful. Do not assess, classify, or score the sources in this response — stop at collection.
