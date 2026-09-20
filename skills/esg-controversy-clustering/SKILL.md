---
name: esg-controversy-clustering
description: Use this skill after esg-deep-research (and optionally esg-url-scraper), when saved report files for a company need to be grouped by which specific controversy they describe — e.g. "cluster the sources for Anthropic", "group these reports by controversy before assessing". Reads assessment/<company-slug>/reports/*.md frontmatter (including each file's `controversies` labels), groups files that share a label into one cluster, and writes assessment/<company-slug>/reports/clusters.json — which also doubles as the canonical label registry esg-deep-research checks on later reruns to avoid minting near-duplicate labels for an already-tracked incident. A single file can belong to multiple clusters (e.g. a roundup article covering several incidents). Does not score or assess anything — that's esg-controversy-assessment's job, run per cluster afterward.
allowed-tools: Read, Glob, Write
---

# ESG Controversy Clustering

Group a company's saved report files by which specific controversy each one describes, so a later assessment step can score once per controversy instead of once per file.

## Step 1 — Identify the company

Take `<company-slug>` from the request, same convention as the other skills: lowercase, spaces/punctuation replaced with hyphens.

## Step 2 — Read every report's frontmatter

`Glob assessment/<company-slug>/reports/*.md`, excluding `index.md`. `Read` each match and extract its `title`, `url`, and `controversies` field (a list of labels, per `esg-deep-research`'s Step 4).

## Step 3 — Group by label

Every file listing a given label becomes a member of that label's cluster. A file with multiple labels is a member of multiple clusters — this is the expected case for roundup/aggregator articles that cover several incidents at once.

If a file has no `controversies` field at all (e.g. it predates this labeling convention), treat it as its own single-member cluster, keyed by its own filename (without the `.md` extension) as the controversy label — graceful degradation, not a hard requirement that every file be labeled.

## Step 4 — Write the cluster manifest

Write `assessment/<company-slug>/reports/clusters.json`: a JSON array, one object per distinct controversy:

```json
[
  {
    "controversy": "coxon-resignation",
    "description": "Former Anthropic researcher Jacob Coxon publicly resigned in September 2026, warning that unchecked AI development risks causing human extinction.",
    "report_files": ["reports/coxon-resignation-nbc.md", "reports/researcher-resignation-governance-esgdive.md"],
    "urls": ["https://...", "https://..."]
  }
]
```

`description` is one sentence, written from the member files' content, summarizing what the incident actually is — specific enough that a future run can tell, from this alone, whether a newly found source is about the same incident or a different one. This is what makes `clusters.json` double as a label registry (see `esg-deep-research`'s Step 1), not just a grouping.

`report_files` and `urls` are parallel lists (same order); for a single-source cluster both are one-element lists — no special-casing.

## Step 5 — Report back

Tell the user how many report files were read and how many distinct controversy clusters they were grouped into (e.g. "12 report files grouped into 9 distinct controversies"), and note any file that had no `controversies` field and fell back to a single-member cluster.
