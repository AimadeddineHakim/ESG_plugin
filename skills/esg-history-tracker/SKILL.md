---
name: esg-history-tracker
description: Use this skill after assessment.json has been (re)written for a company, to snapshot the run and record what changed since the previous run — e.g. "track history for Anthropic", "what changed since the last Anthropic assessment". Archives the current assessment.json into assessment/<company-slug>/history/, diffs it against the most recent prior snapshot (new/removed/changed controversies), and appends a dated entry to assessment/<company-slug>/history/CHANGELOG.md. On a first-ever run for a company, just archives the baseline with no diff.
allowed-tools: Read, Write, Glob, Bash(mkdir -p assessment/*/history)
---

# ESG History Tracker

Snapshot a company's just-written `assessment.json` and record what changed since the previous run. This skill never scores or re-assesses anything — it only archives and diffs existing results.

## Step 1 — Identify the company

Take `<company-slug>` from the request, same convention as the other skills.

## Step 2 — Read the current run's output

`Read assessment/<company-slug>/assessment.json` — required; it must already exist (this skill runs *after* scoring, not instead of it). If it doesn't exist, stop and tell the user to run the assessment step first.

## Step 3 — Find the previous snapshot

`mkdir -p assessment/<company-slug>/history`, then `Glob assessment/<company-slug>/history/*.json`.

If no prior snapshot files exist, this is the first run for this company — skip straight to Step 5 with an empty diff (nothing to compare against).

## Step 4 — Diff against the most recent prior snapshot

Take the prior snapshot with the latest timestamp in its filename (all snapshot filenames sort chronologically, see Step 5). `Read` it and compare against the current run's `assessment.json`, matching entries by their `controversy` label:

- **New**: a `controversy` label present in the current run but not in the prior snapshot.
- **No longer found**: a label present in the prior snapshot but not in the current run. Phrase this carefully — "not present in this run's collected sources," not "resolved." Absence isn't proof the underlying issue was resolved; it may just mean this run's searches didn't resurface it.
- **Changed**: a label present in both, but `assessment.Score`, `assessment.Flag`, or the Case Status (`assessment.status`) differs between the two — record the old value and the new value.
- **Unchanged**: a label present in both with no differences in those fields — report only a count, don't itemize.

## Step 5 — Write the snapshot

Copy the current run's `assessment.json` verbatim to `assessment/<company-slug>/history/<ISO-timestamp>.json`, using a filesystem-safe ISO 8601 timestamp for the filename (colons replaced with hyphens), e.g. `2026-09-20T20-14-00Z.json`. This is what Step 4 compares against on the *next* run.

## Step 6 — Append to the changelog

Append (never overwrite) a dated section to `assessment/<company-slug>/history/CHANGELOG.md`:

```markdown
## 2026-09-20T20:14:00Z

**New (2):** reddit-scraping-lawsuit, ai-slowdown-antitrust-lawsuit
**No longer found (1):** some-old-label
**Changed (1):** coxon-resignation: Score 6→5, Flag Green→Yellow
**Unchanged:** 8
```

On a first run (no prior snapshot to diff against), write instead:

```markdown
## 2026-09-20T20:14:00Z

First run — 11 controversies baselined.
```

## Step 7 — Report back

Tell the user the diff summary (counts of new/no-longer-found/changed/unchanged, and a one-line list of which controversies are new or changed), and confirm where the snapshot and changelog were written.
