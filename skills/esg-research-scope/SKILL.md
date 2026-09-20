---
name: esg-research-scope
description: Use this skill before esg-deep-research, when the user's request needs to be turned into a precise research scope — e.g. "research ESG controversies for Anthropic in 2026", "look at OpenAI and Google since June 2025", "find recent Tesla governance issues". Parses the request to determine, with precision, which company or companies are meant and what date range (start/end) the research should cover, then scaffolds assessment/<company-slug>/{reports,sources}/ and writes context.json for each. Asks the user to confirm if a company name is ambiguous or unclear — never guesses. Does not itself search the web or save sources — that's esg-deep-research's job, run as a separate step afterward.
allowed-tools: Write, Bash(mkdir -p assessment/*)
---

# ESG Research Scope

Turn a user's request into a precise, structured research scope — which company (or companies) and which date range — before `esg-deep-research` runs. This skill does not search the web; it only resolves scope and writes a `context.json` per company for later steps to read.

## Step 1 — Identify the company or companies

Read the user's request and extract every company it names.

- If a name is ambiguous (could refer to more than one real company) or no company is named at all, **ask the user to confirm** before proceeding — do not guess. This matches `esg-deep-research`'s own rule for company identification.
- If the request names several companies (e.g. "compare Anthropic and OpenAI"), treat each as a separate target — Steps 2–4 run once per company.
- Derive `<company-slug>` the same way `esg-deep-research` does: lowercase, spaces/punctuation replaced with hyphens (e.g. "Coca-Cola Europacific Partners" → `coca-cola-europacific-partners`).

## Step 2 — Determine the date range

Look for explicit date scoping language in the request and convert it to ISO 8601 `date_start`/`date_end`:

- A bare year (e.g. "in 2026") → `date_start: 2026-01-01`, `date_end: 2026-12-31`.
- An explicit range (e.g. "from June 2025 to March 2026") → the corresponding start/end dates.
- A relative phrase (e.g. "last 6 months", "recent", "since Q1 2026") → resolve relative to today's date.
- An open-ended phrase (e.g. "since March 2026", "starting last year") → set `date_start` accordingly and leave `date_end: null` (through present).
- No date scoping mentioned anywhere in the request → leave both `date_start: null` and `date_end: null` (unbounded — no date restriction).

If the resolved range is a guess based on a vague phrase (e.g. "recently"), note that assumption in the Step 4 report so the user can correct it — but don't block on it; only company ambiguity blocks (Step 1).

## Step 3 — Scaffold the folders and write the context file

For each identified company:

1. `mkdir -p assessment/<company-slug>/reports assessment/<company-slug>/sources` — creates both folders `esg-deep-research` and `esg-url-scraper` write into. `mkdir -p` is idempotent, so this is safe to re-run even if the company already has an assessment folder.
2. `Write assessment/<company-slug>/context.json`:

   ```json
   {
     "company": "<company display name as named/confirmed by the user>",
     "company_slug": "<company-slug>",
     "date_start": "<ISO date>" | null,
     "date_end": "<ISO date>" | null
   }
   ```

## Step 4 — Report back

For each company, tell the user: the resolved company name/slug, the resolved date range (or "unbounded" if both are null), and any assumption made when interpreting a vague date phrase. Confirm that `assessment/<company-slug>/reports/` and `assessment/<company-slug>/sources/` were created alongside `context.json`. Do not run `esg-deep-research` automatically — that's a separate, explicit next step.
