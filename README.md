# ESG Tracking

A Claude Code plugin that takes a company name and produces a scored, sourced, human-readable ESG (Environmental, Social, Governance) controversy report — end to end, from a single natural-language request.

Given "do a full ESG assessment of Anthropic," it will: research the web for ESG controversy coverage, independently re-verify every source with a second, free scraping method, cluster multiple articles about the same incident into one controversy instead of scoring the same thing twice, fill genuine information gaps by spinning up its own follow-up research sub-agent, score each controversy's severity, and track what changed since the last time it was run for that company.

Real example outputs are already in this repo — see [Quick look](#quick-look-no-install-needed) below.

## Install

Two commands, no API keys, no config files.

```
/plugin marketplace add AimadeddineHakim/ESG_plugin
/plugin install esg-tracking@esg-tracking
```

(Or, in one step, on Claude Code v2.1.275+: `/plugin install esg-tracking --marketplace AimadeddineHakim/ESG_plugin`.)

This works from anywhere — it doesn't depend on where you put anything locally. If you're working from a local copy of this repo instead, use `/plugin marketplace add ./path/to/ESG_Tracking` with the relative path to your copy.

There's nothing else to install ahead of time: the one Python dependency this plugin has (for its free web scraper) installs itself automatically the first time it's needed — see [Dependencies](#dependencies) below.

## Run it

Open this project folder in Claude Code (working directory matters — see [Working directory](#working-directory)) and just ask, in plain language:

```
do a full ESG assessment of Anthropic
```

```
do a full ESG assessment of OpenAI and Meta in 2026
```

That's the whole interaction. Behind the scenes this routes to the `esg-full-assessment` agent, which runs the full pipeline (see [How it works](#how-it-works)) and writes everything to `assessment/<company-slug>/`.

For multiple companies in one request, it runs them **in parallel**, not one after another — each company gets its own agent invocation launched at the same time.

Other things you can ask for individually, without running the full pipeline:
- `"research ESG controversies for {company}"` — just the web research step, no scoring.
- `"scrape the sources for {company}"` — independently re-verify already-collected sources.
- `"assess this article for an ESG controversy: {company}, {text}"` — score one piece of text you already have, no research.
- `"what changed since the last {company} assessment?"` — read the run history without doing a new run.

## Quick look (no install needed)

Three companies have already been run end to end in this repo — open these directly, no setup required:

- [`assessment/anthropic/report.md`](assessment/anthropic/report.md)
- [`assessment/openai/report.md`](assessment/openai/report.md)
- [`assessment/meta/report.md`](assessment/meta/report.md) (scoped to 2026)

Each company's folder also has the full machine-readable trail behind that report: `assessment.json` (one entry per controversy, with its score/flag/category), `reports/clusters.json` (which source articles were grouped into which controversy, and why), `scored-text/` (the exact text handed to the scorer, for auditing a score after the fact), and `history/CHANGELOG.md` (what changed across reruns).

## How it works

One skill per pipeline stage, orchestrated by the `esg-full-assessment` agent:

| Stage | Skill | Does |
|---|---|---|
| 1 | `esg-research-scope` | Resolves the company + date range from your request, scaffolds `assessment/<company-slug>/{reports,sources}/` |
| 2 | `esg-deep-research` | Searches the web across all 3 ESG pillars, saves each source, labels it with which specific controversy it covers |
| 3 | `esg-url-scraper` | Independently re-fetches every source with a free, no-key scraper fallback chain (`requests`+`trafilatura`, then a Jina Reader proxy) — a second, differently-sourced copy of each article |
| 4 | `esg-controversy-clustering` | Groups sources that describe the *same* incident into one cluster, so a story covered by 3 outlets gets scored once, not 3 times |
| 5 | `esg-controversy-assessment` | Scores each cluster: category/pillar, nature of harm, scale of impact, company role, case status, a 0–9 severity score, and a flag color |
| 6 | `esg-history-tracker` | Snapshots the run and diffs it against the previous one — new controversies, ones no longer surfaced, and anything whose score/status changed |
| 7 | `esg-report-writer` | Turns the scored results into `report.md`, most severe first |

Two things worth calling out:
- **Gap-fill research**: if a cluster's collected text doesn't have enough to determine something the scorer needs (e.g. whether a case is still ongoing), the agent spins up its own foreground sub-agent to go find that one specific answer before scoring — rather than guessing or leaving it blank.
- **Nothing here needs an API key.** The scraper fallback chain and the web research both run on tools already available inside Claude Code.

## Dependencies

The scraper (`esg-url-scraper`) uses `requests`, `trafilatura`, and `beautifulsoup4`. You don't need to install these yourself — the skill checks for them and runs `pip install -r skills/esg-url-scraper/scripts/requirements.txt` automatically the first time it hits a missing import. If you'd rather install it ahead of time (or something about your Python environment makes auto-install unreliable):

```
pip install -r skills/esg-url-scraper/scripts/requirements.txt
```

## Working directory

Run Claude Code with this project folder open (or as your working directory). Every skill writes its output to `assessment/<company-slug>/...` relative to wherever Claude Code is running — that's standard for how a Claude Code plugin operates against "the current project," not an extra setup step, but it does mean output won't land here if you run it from somewhere else.

## Repo layout

```
skills/      one folder per pipeline-stage skill (SKILL.md + any bundled scripts)
agents/      esg-full-assessment (the pipeline orchestrator) and esg-analyst (score-only, for text you already have)
assessment/  output — one folder per company that's been run
examples/    a fully worked example of the scoring taxonomy
```
