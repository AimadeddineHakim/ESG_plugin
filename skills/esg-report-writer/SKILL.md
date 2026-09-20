---
name: esg-report-writer
description: Use this skill after esg-full-assessment (or after esg-controversy-assessment has been run per-controversy and assessment.json exists), when a human-readable ESG report is needed for a company — e.g. "write the ESG report for Anthropic", "summarize the assessment for OpenAI". Reads assessment/<company-slug>/assessment.json and writes assessment/<company-slug>/report.md: one section per controversy (category, severity, score, flag, sources) plus a summary of flag/category counts. Does not score or re-assess anything itself — purely formats existing assessment.json output.
allowed-tools: Read, Write
---

# ESG Report Writer

Turn a company's `assessment.json` (one entry per controversy) into a human-readable report. This skill formats existing results — it never scores, classifies, or re-assesses anything itself.

## Step 1 — Identify the company

Take `<company-slug>` from the request, same convention as the other skills.

## Step 2 — Read the inputs

`Read assessment/<company-slug>/assessment.json` — required; if it doesn't exist, stop and tell the user to run the assessment step first (`esg-full-assessment` or `esg-controversy-assessment` per-controversy) rather than guessing at content.

`Read assessment/<company-slug>/context.json` if it exists, for the resolved date range (`date_start`/`date_end`) to note the report's scope. If it doesn't exist, treat the scope as unbounded.

## Step 3 — Compute the summary

From `assessment.json`, compute:
- Total number of controversies assessed.
- Counts by flag color (Red / Orange / Yellow / Green).
- Counts by category (Environmental / Social / Governance).

## Step 4 — Write the report

Write `assessment/<company-slug>/report.md`:

1. **Header**: company name, date range covered (from Step 2, or "unbounded"), today's date as the generation date, and the summary counts from Step 3.
2. **One section per controversy**, ordered **most severe first** (ascending `Score` — lower is more severe on the existing 0–9 scale). For each:
   - Heading: controversy label/title and its Flag + Score + Severity (e.g. "## 1. Reddit Data-Scraping & Privacy Lawsuit — Orange Flag (Score: 1, Severity: Severe)").
   - Category/Pillar (and Sub-Pillar too, for Social controversies).
   - Nature of Harm, Scale of Impact, Company Role, Case Status — pulled from the entry's `assessment` object.
   - A short narrative (2-4 sentences) summarizing what happened, grounded in the assessed text.
   - The source URLs backing this controversy (from the entry's `urls` list).

## Step 5 — Report back

Confirm `assessment/<company-slug>/report.md` was written, and give the top-line summary counts from Step 3.
